
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional


class NotificationError(Exception):
	pass


@dataclass
class DeliveryRecord:
	channel: str  # "email" or "sms"
	to: str
	subject: Optional[str]
	body: str
	attempt: int
	success: bool
	error: Optional[str] = None


class BaseNotifier:
	def __init__(self, sender_alias: Optional[str] = None, fail_first_n: int = 0):
		self.sender_alias = sender_alias or "system"
		self.fail_first_n = max(0, int(fail_first_n))
		self._attempt_counter = 0
		self.sent_log: List[DeliveryRecord] = []

	def _maybe_fail(self):
		self._attempt_counter += 1
		if self._attempt_counter <= self.fail_first_n:
			raise NotificationError("Simulated transient failure")

	def _log(self, rec: DeliveryRecord):
		self.sent_log.append(rec)


class EmailNotifier(BaseNotifier):
	def send(self, to: str, subject: str, body: str, attempt: int = 1) -> None:
		self._maybe_fail()
		print(f"[EMAIL] to={to} from={self.sender_alias} subj={subject!r}\n{body}\n---")
		self._log(
			DeliveryRecord(
				channel="email", to=to, subject=subject, body=body, attempt=attempt, success=True
			)
		)


class SMSNotifier(BaseNotifier):
	def __init__(self, sender_alias: Optional[str] = None, fail_first_n: int = 0, segment_size: int = 160):
		super().__init__(sender_alias=sender_alias, fail_first_n=fail_first_n)
		self.segment_size = max(60, int(segment_size))

	def _segments(self, body: str) -> List[str]:
		if len(body) <= self.segment_size:
			return [body]
		parts = [body[i : i + self.segment_size] for i in range(0, len(body), self.segment_size)]
		# Add simple (n/N) suffix to indicate segmentation
		total = len(parts)
		annotated = [f"({i+1}/{total}) {p}" for i, p in enumerate(parts)]
		return annotated

	def send(self, to: str, body: str, attempt: int = 1) -> None:
		self._maybe_fail()
		segments = self._segments(body)
		for seg in segments:
			print(f"[SMS] to={to} from={self.sender_alias}\n{seg}\n---")
			self._log(
				DeliveryRecord(
					channel="sms", to=to, subject=None, body=seg, attempt=attempt, success=True
				)
			)


class NotificationManager:
	def __init__(self, email_notifier: Optional[EmailNotifier] = None, sms_notifier: Optional[SMSNotifier] = None, retries: int = 2):
		self.email = email_notifier or EmailNotifier()
		self.sms = sms_notifier or SMSNotifier()
		self.retries = max(0, int(retries))

	# Email
	def send_email(self, to: str, subject: str, body: str) -> None:
		last_err: Optional[Exception] = None
		for attempt in range(1, self.retries + 2):  # initial try + retries
			try:
				self.email.send(to=to, subject=subject, body=body, attempt=attempt)
				return
			except Exception as e:  # noqa: BLE001 keep broad for simulation
				last_err = e
		# Log failure
		self.email._log(
			DeliveryRecord(
				channel="email", to=to, subject=subject, body=body, attempt=self.retries + 1, success=False, error=str(last_err)
			)
		)
		raise NotificationError(f"Email delivery failed after {self.retries+1} attempts: {last_err}")

	def send_email_template(self, to: str, subject_tmpl: str, body_tmpl: str, context: Dict[str, Any]) -> None:
		subject = subject_tmpl.format(**context)
		body = body_tmpl.format(**context)
		self.send_email(to=to, subject=subject, body=body)

	# SMS
	def send_sms(self, to: str, body: str) -> None:
		last_err: Optional[Exception] = None
		for attempt in range(1, self.retries + 2):
			try:
				self.sms.send(to=to, body=body, attempt=attempt)
				return
			except Exception as e:  # noqa: BLE001
				last_err = e
		self.sms._log(
			DeliveryRecord(
				channel="sms", to=to, subject=None, body=body, attempt=self.retries + 1, success=False, error=str(last_err)
			)
		)
		raise NotificationError(f"SMS delivery failed after {self.retries+1} attempts: {last_err}")

	def send_sms_template(self, to: str, body_tmpl: str, context: Dict[str, Any]) -> None:
		body = body_tmpl.format(**context)
		self.send_sms(to=to, body=body)

	# Convenience: fallback path if email fails use SMS
	def notify_with_fallback(self, to_email: str, to_phone: str, subject: str, body: str) -> str:
		try:
			self.send_email(to=to_email, subject=subject, body=body)
			return "email"
		except NotificationError:
			self.send_sms(to=to_phone, body=f"Subject: {subject}\n{body}")
			return "sms"


__all__ = [
	"NotificationError",
	"DeliveryRecord",
	"EmailNotifier",
	"SMSNotifier",
	"NotificationManager",
]

