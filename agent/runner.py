"""Two-run agent with a policy gate before every tool call.

Run A may inspect untrusted ticket text. Run B receives ticket numbers parsed
from filenames only; it never receives ticket body text or attacker-supplied
customer IDs. Private customer records are not passed to the summarizer.
"""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
import hashlib
import json
from pathlib import Path
import re
from uuid import uuid4

from agent import ledger, pii, policy, tools


REPORTS_DIR = Path(__file__).resolve().parent.parent / "reports"
DEFAULT_LEDGER_PATH = REPORTS_DIR / "ledger.jsonl"
_TICKET_NAME = re.compile(r"ticket-(\d+)\.md")


class RunnerScaffoldPending(NotImplementedError):
    """Kept for compatibility with the lab's baseline dispatcher."""


def _ticket_numbers(docs: list[dict]) -> tuple[int, ...]:
    numbers = set()
    for doc in docs:
        filename = doc.get("id", "")
        match = _TICKET_NAME.fullmatch(filename)
        if match:
            numbers.add(int(match.group(1)))
    return tuple(sorted(numbers))


def _related_customers(ticket_numbers: tuple[int, ...]) -> list[str]:
    """Use the trusted customer index after its private read is authorized."""
    wanted = set(ticket_numbers)
    records = json.loads(tools.CUSTOMERS_FILE.read_text(encoding="utf-8"))
    return sorted(record["customer_id"] for record in records
                  if wanted.intersection(record.get("related_tickets", [])))


def handle(message: str, llm, log_dir: Path | None = None,
           principal_id: str = "support_l1") -> str:
    ledger_path = (Path(log_dir) if log_dir is not None else REPORTS_DIR) / "ledger.jsonl"
    invocation = uuid4().hex
    expires_at = (datetime.now(timezone.utc) + timedelta(minutes=5)).isoformat()

    def authorize(tool: str, arguments: object, classification: str,
                  purpose: str, run_name: str, scopes: tuple[str, ...],
                  egress: bool = False) -> bool:
        context = policy.PolicyContext(
            data_classification=classification,
            request_purpose=purpose,
            agent_owner=f"lab24-agent/{run_name}",
            delegation_depth=0,
            egress_enabled=egress,
            principal_id=principal_id,
            requested_tool=tool,
            agent_scopes=scopes,
            parent_scopes=(),
            expires_at=expires_at,
        )
        allowed, reason = policy.check(context)
        argument_bytes = json.dumps(arguments, sort_keys=True, ensure_ascii=False).encode("utf-8")
        ledger.append({
            "ts": datetime.now(timezone.utc).isoformat(),
            "agent_id": context.agent_owner,
            "run_id": f"{invocation}/{run_name}",
            "tool": tool,
            "args_hash": hashlib.sha256(argument_bytes).hexdigest(),
            "classification": classification,
            "decision": "allow" if allowed else "deny",
            "reason": reason,
            "on_behalf_of": principal_id,
            "expires_at": expires_at,
        }, ledger_path)
        return allowed

    # Run A: untrusted content is confined to search and local analysis.
    if not authorize("search_docs", message, "internal", "summarize-tickets",
                     "run-a", ("search_docs",)):
        return llm.summarize([])
    docs = tools.search_docs(message)
    ticket_numbers = _ticket_numbers(docs)
    instruction = llm.find_injection("\n\n".join(doc["text"] for doc in docs))
    summary_docs = [{"id": doc["id"], "text": pii.redact(doc["text"])}
                    for doc in docs]

    # Run B: only typed ticket numbers cross the boundary.
    if ticket_numbers and authorize("read_customer", ticket_numbers, "restricted",
                                    "support-reply", "run-b", ("read_customer",)):
        for customer_id in _related_customers(ticket_numbers):
            if authorize("read_customer", customer_id, "restricted", "support-reply",
                         "run-b", ("read_customer",)):
                tools.read_customer(customer_id)

    if instruction is not None:
        # The attempted egress is logged even when policy refuses it.
        if authorize("http_post", instruction.target_url, "restricted", "support-reply",
                     "run-egress", ("http_post",), egress=True):
            tools.http_post(instruction.target_url, {})
    return llm.summarize(summary_docs)
