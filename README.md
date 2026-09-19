# Support CRM — Customer Support Ticketing System

A web application for managing customer support tickets. Support agents can create tickets, search and filter them, read the full details of a ticket, and update its status with notes.

Built for the Datastraw assessment: **Database + API + Frontend**, all in one project.

> **Live demo:** `https://YOUR-APP-URL` *(replace with your deployed link)*
> **Demo video:** `https://YOUR-VIDEO-URL` *(replace with your video link)*

---

## Features

- **Create tickets** — customer name, email, issue title and description. A ticket ID (`TKT-001`, `TKT-002`, ...) and a timestamp are generated automatically.
- **Ticket list** — ID, customer name, email, subject, status and dates in one table.
- **Search** — across ticket ID, customer name, email, subject and description.
- **Filter by status** — Open, In Progress or Closed. Works together with search.
- **Ticket detail page** — full ticket information and the history of notes.
- **Update tickets** — change the status and add a note (as many times as needed).
- **Notes page** — every note on every ticket, with search.

---

## Tech stack

| Layer     | Technology                                          |
|-----------|-----------------------------------------------------|
| Backend   | Python, [FastAPI](https://fastapi.tiangolo.com/), Uvicorn |
| Database  | PostgreSQL, SQLAlchemy 2 (ORM), psycopg2            |
| Frontend  | Jinja2 server-rendered templates, plain HTML / CSS / JavaScript |
| Config    | `.env` file loaded with python-dotenv               |

---

## Project structure

crm-system/
├── app/
│   ├── main.py            # FastAPI app: all routes and business logic
│   ├── database.py        # Database connection (reads DATABASE_URL from .env)
│   ├── models.py          # SQLAlchemy models: Ticket, Note
│   ├── schemas/
│   │   └── ticket.py      # Validation of the "create ticket" form
│   └── templates/         # HTML pages
│       ├── dashboard.html
│       ├── register.html      # create-ticket form
│       ├── tickets.html       # list + search + filter
│       ├── ticket_report.html # ticket details + update
│       └── notes.html
├── .env.example           # template for your local settings
├── .gitignore
├── requirements.txt
└── README.md

---

## Installation and setup

### 1. Prerequisites

Install these first:

- **Python 3.12 or newer** — check with `python --version` (developed on 3.14)
- **PostgreSQL 14 or newer** — check with `psql --version` (tested with 16)
- **Git**

### 2. Get the code

git clone https://github.com/Hari1369/crm-system.git
cd crm-system

### 3. Create and activate a virtual environment

A virtual environment keeps this project's packages separate from the rest of your computer.

**macOS / Linux**

python3 -m venv venv
source venv/bin/activate

**Windows (Command Prompt)**

python -m venv venv
venv\Scripts\activate

**Windows (PowerShell)**

powershell
python -m venv venv
venv\Scripts\Activate.ps1

> If PowerShell says *"running scripts is disabled on this system"*, run this once in the same window and try again:
> `Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned`

When it works, your terminal prompt starts with `(venv)`. To leave the environment later, type `deactivate`.

### 4. Install the dependencies

With `(venv)` active:

bash
pip install --upgrade pip
pip install -r requirements.txt


### 5. Create the PostgreSQL database

Open a PostgreSQL shell:

- **Linux:** `sudo -u postgres psql`
- **macOS:** `psql postgres`
- **Windows:** open **SQL Shell (psql)** from the Start menu, or run `psql -U postgres`

Then run these two commands:

sql
CREATE USER admin WITH PASSWORD 'admin';
CREATE DATABASE support_crm OWNER admin;


Type `\q` to exit. (`admin` / `admin` is fine for a local machine. Use a strong password for anything public.)

You do **not** need to create any tables — the app creates the `tickets` and `notes` tables by itself the first time it starts.

### 6. Configure the environment variables

Copy the example file to `.env`:

bash
# macOS / Linux
cp .env.example .env

# Windows (Command Prompt)
copy .env.example .env

Open `.env` and set your database connection string:

env
DATABASE_URL=postgresql://admin:admin@localhost:5432/support_crm

The format is `postgresql://USER:PASSWORD@HOST:PORT/DATABASE_NAME`. If your password contains special characters such as `@` or `#`, URL-encode them (`@` becomes `%40`, `#` becomes `%23`).

| Variable       | Description                          | Example                                                |
|----------------|--------------------------------------|--------------------------------------------------------|
| `DATABASE_URL` | PostgreSQL connection string         | `postgresql://admin:admin@localhost:5432/support_crm`  |

> `.env` holds your private settings and is already listed in `.gitignore`. **Never commit it.** Only `.env.example` goes to GitHub.

### 7. Run the application

From the project root folder (the one containing `app/` and `requirements.txt`), with `(venv)` active:

uvicorn app.main:app --reload

Open **http://127.0.0.1:8000** in your browser. `--reload` restarts the server automatically when you edit code; leave it off in production.

> Always start the server from the project root. Running it from another folder fails because the templates are found by a relative path.

---

## Using the app

1. **Dashboard** (`/`) — links to create tickets, view tickets and view notes.
2. **Create a ticket** (`/api/register_ticket`) — fill in the form. The new ticket starts as **Open**.
3. **View tickets** (`/api/tickets`) — type in the search box and press **Search**, or pick a status from the dropdown to filter. Press **Clear** to reset.
4. **Open a ticket** — press **Report** on any row to see its details and notes. Press **Update Ticket** to choose a new status and write a note.
5. **Notes** (`/api/notes_report`) — every note across all tickets.

Rules for the create-ticket form:

- The customer email must be a `@gmail.com` address.
- The customer name can be up to 50 characters and is stored in capital letters.

---

## Routes

| Method | Path                               | Purpose                                             |
|--------|------------------------------------|-----------------------------------------------------|
| GET    | `/`                                | Dashboard                                           |
| GET    | `/api/register_ticket`                 | Create-ticket form                                  |
| POST   | `/api/register`                        | Save a new ticket                                   |
| GET    | `/api/tickets?query=&status=`          | Ticket list; optional search text and status filter |
| GET    | `/api/ticket_report?id=&ticket_id=`    | Ticket details and notes                            |
| PUT    | `/api/tickets/{ticket_id}`             | Update status and add a note                        |
| GET    | `/api/notes_report?query=`             | All notes; optional search text                     |

`PUT /api/tickets/{ticket_id}` example:

{ "status": "In Progress", "notes": "Looking into the issue." }

Response: `{ "success": true, "updated_at": "19-09-2026 14:30:00" }`. Valid statuses are `Open`, `In Progress` and `Closed`.

The interactive API documentation is available at **http://127.0.0.1:8000/docs**.

---

## Database

Two tables, created automatically on startup:

**`tickets`**

| Column           | Type          | Notes                          |
|------------------|---------------|--------------------------------|
| `id`             | integer, PK   | auto-increment                 |
| `ticket_id`      | varchar(20)   | unique, e.g. `TKT-001`         |
| `customer_name`  | varchar(100)  |                                |
| `customer_email` | varchar(255)  |                                |
| `subject`        | varchar(255)  |                                |
| `description`    | text          |                                |
| `status`         | varchar(20)   | Open / In Progress / Closed    |
| `created_at`     | timestamp     |                                |
| `updated_at`     | timestamp     | set when a ticket is updated   |

**`notes`**

| Column       | Type        | Notes                        |
|--------------|-------------|------------------------------|
| `id`         | integer, PK | auto-increment               |
| `ticket_id`  | varchar(20) | foreign key to `tickets.ticket_id` |
| `note_text`  | text        |                              |
| `created_at` | timestamp   |                              |

---

## Troubleshooting

| Problem | Fix |
|---|---|
| `RuntimeError: DATABASE_URL is not set` | You have no `.env` file, or it is not in the project root. Run the copy command from step 6. |
| `password authentication failed for user "admin"` | The user or password in `.env` does not match what you created in step 5. |
| `database "support_crm" does not exist` | Create the database (step 5). |
| `Connection refused` (or `could not connect to server`) | PostgreSQL is not running, or is on a different port. Start the PostgreSQL service and check the port in `DATABASE_URL`. |
| `TemplateNotFound` | You started the server from the wrong folder. `cd` into the project root and run the command again. |
| `error while attempting to bind on address ... address already in use` | Port 8000 is taken. Use `uvicorn app.main:app --reload --port 8001`. |
| `uvicorn: command not found` | The virtual environment is not active. Activate it (step 3). |

---

## Deployment (Render / Railway)

1. Create a **PostgreSQL** database on the host and copy its connection URL.
2. Create a **Web Service** from this GitHub repository.
3. Set the environment variable `DATABASE_URL` to the connection URL from step 1. (URLs that begin with `postgres://` are handled automatically.)
4. Build command: `pip install -r requirements.txt`
5. Start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

The tables are created automatically on the first start.


Name:
crm-database

Database:
support_crm

User:
support_admin

Region:
choose a region

Plan:
Free