"""
FakeMailer: implementação in-memory de mailer para testes.
Captura todos os emails em memória — sem SMTP real, sem efeitos externos.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Optional


@dataclass
class EmailMessage:
    to: str | list[str]
    subject: str
    body: Optional[str] = None
    html: Optional[str] = None
    from_address: Optional[str] = None
    cc: list[str] = field(default_factory=list)
    sent_at: datetime = field(default_factory=lambda: datetime.now(tz=timezone.utc))


class FakeMailer:
    def __init__(self) -> None:
        self._sent: list[EmailMessage] = []

    async def send(
        self,
        to: str | list[str],
        subject: str,
        body: Optional[str] = None,
        html: Optional[str] = None,
        from_address: Optional[str] = None,
        cc: Optional[list[str]] = None,
    ) -> None:
        self._sent.append(
            EmailMessage(
                to=to,
                subject=subject,
                body=body,
                html=html,
                from_address=from_address,
                cc=cc or [],
            )
        )

    def get_sent(self) -> list[EmailMessage]:
        return list(self._sent)

    def get_last_sent(self) -> Optional[EmailMessage]:
        return self._sent[-1] if self._sent else None

    def get_sent_to(self, email: str) -> list[EmailMessage]:
        def matches(msg: EmailMessage) -> bool:
            recipients = msg.to if isinstance(msg.to, list) else [msg.to]
            return email in recipients

        return [m for m in self._sent if matches(m)]

    def assert_sent_to(self, email: str) -> None:
        messages = self.get_sent_to(email)
        if not messages:
            sent_to = [m.to for m in self._sent]
            raise AssertionError(
                f"Expected email to be sent to '{email}', but got: {sent_to}"
            )

    def assert_not_sent_to(self, email: str) -> None:
        messages = self.get_sent_to(email)
        if messages:
            raise AssertionError(
                f"Expected no email to be sent to '{email}', but {len(messages)} were sent."
            )

    def assert_sent_count(self, count: int) -> None:
        if len(self._sent) != count:
            raise AssertionError(
                f"Expected {count} email(s) to be sent, but got {len(self._sent)}."
            )

    def assert_nothing_sent(self) -> None:
        self.assert_sent_count(0)

    def clear(self) -> None:
        self._sent.clear()
