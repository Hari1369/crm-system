from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy import text

from app.database import engine, SessionLocal, Base
from app.models import Ticket, Note
from fastapi.templating import Jinja2Templates
from app.schemas.ticket import Ticket_User
from datetime import datetime
from sqlalchemy import or_
from fastapi import Body
from zoneinfo import ZoneInfo


app = FastAPI()
db = SessionLocal()
templates = Jinja2Templates(directory="app/templates")




@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    if db:
        print("Database is configured")
    else:
        print("Database is NOT configured")
    return templates.TemplateResponse(request, "dashboard.html", {"request": request})


@app.get("/api/api/register_ticket", response_class=HTMLResponse)
def register_page(request: Request):
    return templates.TemplateResponse(request, "register.html", {"request": request})


ALLOWED_STATUSES = ["Open", "In Progress", "Closed"]

@app.get("/api/tickets", response_class=HTMLResponse)
def tickets_page(request: Request, query: str = "", status: str = ""):
    q = db.query(Ticket)

    if query:
        q = q.filter(or_(
            Ticket.ticket_id.ilike(f"%{query}%"),
            Ticket.customer_name.ilike(f"%{query}%"),
            Ticket.customer_email.ilike(f"%{query}%"),
            Ticket.subject.ilike(f"%{query}%"),
            Ticket.description.ilike(f"%{query}%"),
        ))

    if status in ALLOWED_STATUSES:
        q = q.filter(Ticket.status == status)

    tickets = q.order_by(Ticket.created_at.desc()).all()
    return templates.TemplateResponse(request, "tickets.html", {
        "request": request, "tickets": tickets, "query": query,
        "status": status, "statuses": ALLOWED_STATUSES,
    })

# @app.get("/api/tickets", response_class=HTMLResponse)
# def tickets_page(request: Request, query: str = ""):
#     if query:
#         tickets = db.query(Ticket).filter(
#             or_(
#                 Ticket.ticket_id.ilike(f"%{query}%"),
#                 Ticket.customer_name.ilike(f"%{query}%"),
#                 Ticket.customer_email.ilike(f"%{query}%"),
#                 Ticket.subject.ilike(f"%{query}%"),
#                 Ticket.description.ilike(f"%{query}%"),
#                 Ticket.status.ilike(f"%{query}%")
#             )
#         ).all()
#     else:
#         tickets = db.query(Ticket).all()

#     print("DATABASE TICKETS:", tickets)
#     print("NUMBER OF TICKETS:", len(tickets))

#     return templates.TemplateResponse(
#         request,
#         "tickets.html",
#         {
#             "request": request,
#             "tickets": tickets,
#             "query": query
#         }
#     )


# def tables_data():
def tables_data(tickets, notes):
    # tickets = db.query(Ticket).all()
    # notes = db.query(Note).all()

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

            print("1 CREATED AT : ", created_at)

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

            print("2 CREATED AT : ", created_at)

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



@app.get("/api/notes_report", response_class=HTMLResponse)
def notes_report(request: Request, query: str = ""):

    tickets = db.query(Ticket).all()

    if query:
        notes = db.query(Note).filter(
            or_(
                Note.ticket_id.ilike(f"%{query}%"),
                Note.note_text.ilike(f"%{query}%")
            )
        ).all()
    else:
        notes = db.query(Note).all()

    tickets_data, notes_data = tables_data(tickets, notes)

    return templates.TemplateResponse(
        request,
        "notes.html",
        {
            "request": request,
            "tickets": tickets_data,
            "notes": notes_data,
            "query": query
        }
    )

    
@app.post("/api/register")
def register_ticket(request: Request, customer_name: str = Form(), customer_email: str = Form(), subject: str = Form(), description: str = Form()):

    current_time = datetime.now(ZoneInfo("Asia/Kolkata")).replace(tzinfo=None)

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


@app.post("/api/reply")
def reply_ticket(ticket_id: str = Form(), note_text: str = Form(), status: str = Form("In Progress")):

    # current_time = datetime.now(ZoneInfo("Asia/Kolkata"))
    current_time = datetime.now(ZoneInfo("Asia/Kolkata")).replace(tzinfo=None)

    ticket = db.query(Ticket).filter(Ticket.ticket_id == ticket_id).first()
    if not ticket:
        return {"message": "Ticket not found"}
    new_note = Note(ticket_id=ticket_id, note_text=note_text, created_at=current_time)
    db.add(new_note)
    ticket.updated_at = current_time
    if status in ALLOWED_STATUSES:
        ticket.status = status
    db.commit()
    db.refresh(new_note)

    return RedirectResponse(url="/api/tickets", status_code=303)


@app.get("/api/ticket_report", response_class=HTMLResponse)
def ticket_report(request: Request, id: int, ticket_id: str):
    ticket = db.query(Ticket).filter(Ticket.id == id, Ticket.ticket_id == ticket_id).first()
    if not ticket:
        return {"message": "Ticket not found"}

    notes = db.query(Note).filter(Note.ticket_id == ticket_id).all()
    created_at = ticket.created_at.strftime("%d-%m-%Y %H:%M:%S")

    if ticket.updated_at:
        updated_at = ticket.updated_at.strftime("%d-%m-%Y %H:%M:%S")
    else:
        updated_at = "Action Required"

    notes_data = []
    for note in notes:
        note_created_at = note.created_at.strftime("%d-%m-%Y %H:%M:%S")
        notes_data.append({
            "request": request,
            "ticket": ticket,
            "note_text": note.note_text,
            "created_at": note_created_at,
            "notes": notes_data
        })

    return templates.TemplateResponse(
        request,
        "ticket_report.html",
        {
            "request": request,
            "ticket": ticket,
            "notes": notes_data,
            "created_at": created_at,
            "updated_at": updated_at
        }
    )

@app.put("/api/tickets/{ticket_id}")
def resolve_ticket(ticket_id: str, data: dict = Body(...)):
    ticket = db.query(Ticket).filter(Ticket.ticket_id == ticket_id).first()
    if not ticket:
        return {
            "success": False,
            "message": "Ticket not found"
        }

    status = data.get("status")
    note_text = data.get("notes")

    if not note_text:
        return {
            "success": False,
            "message": "Reply message is required"
        }

    # current_time = datetime.now(ZoneInfo("Asia/Kolkata"))
    current_time = datetime.now(ZoneInfo("Asia/Kolkata")).replace(tzinfo=None)

    ticket.status = status
    ticket.updated_at = current_time

    new_note = Note(
        ticket_id=ticket_id,
        note_text=note_text,
        created_at=current_time
    )

    db.add(new_note)
    db.commit()

    return {
        "success": True,
        "updated_at": current_time.strftime("%d-%m-%Y %H:%M:%S")
    }





db.close()



# @app.post("/api/register")
# def register_ticket(customer_name: str = Form(), customer_email: str = Form(), subject: str = Form(), description: str = Form()):
#     print("Customer Name:", customer_name)
#     print("Customer Email:", customer_email)
#     print("Subject:", subject)
#     print("Description:", description)
#     return "Data Received"
