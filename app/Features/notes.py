from fastapi import APIRouter, Depends, HTTPException, status, Header
from sqlalchemy.orm import Session
from typing import List
from app import Tables, dataTypes
from app.SQL_Connection import get_db
from app.Authentication.authentication import verify_access_token


router = APIRouter(
    prefix="/notes",
    tags=["Notes"]
)



@router.post("/", response_model=dataTypes.NoteResponse)
def create_note(request: dataTypes.NoteCreate, Authorization: str = Header(...),db: Session = Depends(get_db)):

    print("Hi")
    token = Authorization.split(" ")[1]
    print("token is "+token)
    user_id = verify_access_token(token)
    note = Tables.Note(
        note_title=request.note_title,
        note_content=request.note_content,
        user_id=user_id
    )
    db.add(note)
    db.commit()
    db.refresh(note)
    return note



@router.get("/", response_model=List[dataTypes.NoteResponse])
def get_notes(Authorization: str = Header(...), db: Session = Depends(get_db)):
    token = Authorization.split(" ")[1]

    user_id = verify_access_token(token)
    
    notes = db.query(Tables.Note).filter(Tables.Note.user_id == user_id).all()
    return notes


@router.put("/{note_id}", response_model=dataTypes.NoteResponse)
def update_note(note_id: str, request: dataTypes.NoteCreate, db: Session = Depends(get_db), Authorization: str = Header(...)):
    token = Authorization.split(" ")[1]
    user_id = verify_access_token(token)
    note = db.query(Tables.Note).filter(Tables.Note.note_id == note_id, Tables.Note.user_id == user_id).first()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")

    note.note_title = request.note_title
    note.note_content = request.note_content
    db.commit()
    db.refresh(note)
    return note



@router.delete("/{note_id}")
def delete_note(note_id: str, db: Session = Depends(get_db),Authorization: str = Header(...)):
    token = Authorization.split(" ")[1]
    user_id = verify_access_token(token)
    note = db.query(Tables.Note).filter(Tables.Note.note_id == note_id, Tables.Note.user_id == user_id).first()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    db.delete(note)
    db.commit()
    return {"detail": "Note deleted successfully"}
