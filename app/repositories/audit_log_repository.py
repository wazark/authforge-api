#app/repositories/audit_log_repository.py
"""
Audit log repository.

Handles persistence of audit events.
"""

from sqlalchemy.orm import Session
from typing import Optional, Dict, Any

from app.models.audit_log import AuditLog


class AuditLogRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(
        self,
        action: str,
        user_id: Optional[int] = None,
        details: Optional[Dict[str, Any]] = None,
    ) -> AuditLog:
        log = AuditLog(
            action=action,
            user_id=user_id,
            details=details or {},
        )

        self.db.add(log)
        self.db.commit()
        self.db.refresh(log)

        return log