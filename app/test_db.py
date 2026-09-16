from app.database import SessionLocal
from app.models import Ticket

db = SessionLocal()

tickets = db.query(Ticket).all()

print(tickets)

db.close()