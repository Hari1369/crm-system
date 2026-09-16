from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from sqlalchemy import text

from app.database import SessionLocal

app = FastAPI()


@app.get("/", response_class=HTMLResponse)
def home():

    db = SessionLocal()

    try:
        db.execute(text("SELECT 1"))

        return """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Support CRM</title>
        </head>
        <body>
            <h1>Support CRM</h1>
            <h2>Database Configured Successfully ✅</h2>
            <p>FastAPI is connected to PostgreSQL.</p>
        </body>
        </html>
        """

    except Exception as e:

        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Support CRM</title>
        </head>
        <body>
            <h1>Support CRM</h1>
            <h2>Database Connection Failed ❌</h2>
            <p>{e}</p>
        </body>
        </html>
        """

    finally:
        db.close()