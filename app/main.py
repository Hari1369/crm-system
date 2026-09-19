from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from sqlalchemy import text

from app.database import engine, SessionLocal
from app.models import Ticket, Note
from fastapi.templating import Jinja2Templates
from app.schemas.ticket import Ticket_User
from datetime import datetime

app = FastAPI()
db = SessionLocal()
templates = Jinja2Templates(directory="app/templates")



current_time = datetime.now()



@app.get("/", response_class=HTMLResponse)
def home():
    if db:
        print("Database is configured")
    else:
        print("Database is NOT configured")
    return "OK"

@app.get("/register_ticket", response_class=HTMLResponse)
def register_page(request: Request):
    return templates.TemplateResponse(request, "register.html", {"request": request})

@app.post("/register")
def register_ticket(request: Request, customer_name: str = Form(), customer_email: str = Form(), subject: str = Form(), description: str = Form()):
    ticket = Ticket_User(customer_name=customer_name, customer_email=customer_email, subject=subject, description=description)
    # print("Customer Name    :", ticket.customer_name)
    # print("Customer Email   :", ticket.customer_email)
    # print("Subject          :", ticket.subject)
    # print("Description      :", ticket.description)
    last_ticket = db.query(Ticket).order_by(Ticket.id.desc()).first()
    if last_ticket:
        next_number = last_ticket.id + 1
    else:
        next_number = 1
    ticket_id = f"TKT-{next_number:03d}"
    new_ticket = Ticket(
        ticket_id=ticket_id,
        customer_name=ticket.customer_name,
        customer_email=str(ticket.customer_email),
        subject=ticket.subject,
        description=ticket.description,
        status="Open",
        created_at=current_time
    )

    db.add(new_ticket)
    db.commit()
    db.refresh(new_ticket)

    # print("Ticket inserted successfully!")
    # print("Ticket ID:", new_ticket.ticket_id)

    return templates.TemplateResponse(
        request,
        "register.html",
        {
            "request": request,
            "message": "Ticket created successfully!",
            "ticket_id": new_ticket.ticket_id
        }
    )

@app.get("/tickets", response_class=HTMLResponse)
def tickets_page(request: Request):
    tickets_data, notes_data = tables_data()
    return templates.TemplateResponse(request,"tickets.html",{"request": request, "tickets": tickets_data, "notes": notes_data})

def tables_data():
    tickets = db.query(Ticket).all()
    notes = db.query(Note).all()

    tickets_data = []
    notes_data = []

    if tickets and notes:
        for i in tickets:
            id_1 = i.id
            ticket_id = i.ticket_id
            customer_name = i.customer_name
            customer_email = i.customer_email
            subject = i.subject
            description = i.description
            status = i.status
            created_at = i.created_at.strftime("%d-%m-%Y %H:%M:%S")
            # updated_at = i.updated_at.strftime("%d-%m-%Y %H:%M:%S")
            if i.updated_at:
                updated_at = i.updated_at.strftime("%d-%m-%Y %H:%M:%S")
            else:
                updated_at = "Action Required"

            if id_1 and ticket_id and customer_name and customer_email and subject and description and status:
                tickets_data.append({
                    "id": id_1,
                    "ticket_id": ticket_id,
                    "customer_name": customer_name,
                    "customer_email": customer_email,
                    "subject": subject,
                    "description": description,
                    "status": status,
                    "created_at": created_at,
                    "updated_at": updated_at
                })
            else:
                print("1 NO DATA FOUND!")

        for i in notes:
            id_2 = i.id
            ticket_id = i.ticket_id
            note_text = i.note_text
            created_at = i.created_at.strftime("%d-%m-%Y %H:%M:%S")


            if id_2 and ticket_id and note_text:
                notes_data.append({
                    "id": id_2,
                    "ticket_id": ticket_id,
                    "note_text": note_text,
                    "created_at": created_at
                })
            else:
                print("2 NO DATA FOUND!")
    else:
        print("3 NO DATA FOUND!")
    return tickets_data, notes_data




db.close()



# @app.post("/register")
# def register_ticket(customer_name: str = Form(), customer_email: str = Form(), subject: str = Form(), description: str = Form()):
#     print("Customer Name:", customer_name)
#     print("Customer Email:", customer_email)
#     print("Subject:", subject)
#     print("Description:", description)
#     return "Data Received"
