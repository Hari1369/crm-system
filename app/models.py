from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from app.database import Base


class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True)
    ticket_id = Column(String(20), unique=True, nullable=False)
    customer_name = Column(String(100), nullable=False)
    customer_email = Column(String(255), nullable=False)
    subject = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    status = Column(String(20), nullable=False, default="Open")
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)


class Note(Base):
    __tablename__ = "notes"

    id = Column(Integer, primary_key=True)
    ticket_id = Column(
        String(20),
        ForeignKey("tickets.ticket_id"),
        nullable=False
    )
    note_text = Column(Text, nullable=False)
    created_at = Column(DateTime, nullable=False)