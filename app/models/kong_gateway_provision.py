from app.extensions import db
from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column
from typing import Optional

class KongGatewayProvision(db.Model):
    consumer_id: Mapped[str] = mapped_column(String(100), primary_key=True)
    workflow_job: Mapped[Optional[int]] = mapped_column(Integer, unique=True, nullable=True)
    status: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)