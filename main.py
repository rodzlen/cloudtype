from typing import Dict
from sqlalchemy.orm import Session
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from database import Tickets, get_db

app =FastAPI()

class TicketModel(BaseModel):
    age : int

@app.get('/')
def home():
    return "Hi"

@app.post('/tickets/')
def post(ticket: TicketModel, db: Session = Depends(get_db)):
    if not ticket:
        raise HTTPException(status_code=400, detail="Value Error")
    new_ticket = {"age": ticket.age}
    db.add(new_ticket)
    db.commit()
    return new_ticket

@app.get('/tickets/')
def get_tickets(db : Session = Depends(get_db)):
    tickets = db.query(Tickets).all()
    return tickets

@app.get('/tickets/{ticket_id}')
def get_ticket(ticket_id:int, db :Session = Depends(get_db)):
    ticket = db.query(Tickets).filter(Tickets.id==ticket_id).first()
    return ticket
