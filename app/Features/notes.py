from fastapi import APIRouter, Depends, HTTPException, status, Header
from typing import List
from app import dataTypes
from app.Authentication.authentication import verify_access_token
from app.Mongo_Connection import  get_database
from app.requiredData import get_note_doc

router = APIRouter(
    prefix="/notes",
    tags=["Notes"]
)


@router.post("/", response_model=dataTypes.NoteResponse)
async def create_note(request: dataTypes.NoteCreate, Authorization: str = Header(...)):
    

    db=get_database()
    token = Authorization.split(" ")[1]
    user_id = verify_access_token(token)

    new_note = get_note_doc(
        note_title=request.note_title,
        note_content=request.note_content,
        user_id=user_id
    )
    await db["notes"].insert_one(new_note)

    return {
        "note_id": new_note["_id"],
        "note_title": new_note["note_title"],
        "note_content": new_note["note_content"],
        "user_id": new_note["user_id"],
        "created_on": new_note["created_on"],
    }


@router.get("/", response_model=List[dataTypes.NoteResponse])
async def get_notes(Authorization: str = Header(...)):
    db=get_database()
    token = Authorization.split(" ")[1]
    user_id = verify_access_token(token)

    notes_cursor = db["notes"].find({"user_id": user_id})
    notes = await notes_cursor.to_list(length=100)

    return [
        {
            "note_id": note["_id"],
            "note_title": note["note_title"],
            "note_content": note["note_content"],
            "user_id": note["user_id"],
            "created_on": note["created_on"],
        }
        for note in notes
    ]


@router.put("/{note_id}", response_model=dataTypes.NoteResponse)
async def update_note(note_id: str, request: dataTypes.NoteCreate, Authorization: str = Header(...)):
    db=get_database()
    token = Authorization.split(" ")[1]
    user_id = verify_access_token(token)

    note = await db["notes"].find_one({"_id": note_id, "user_id": user_id})
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")

    update_data = {
        "$set": {
            "note_title": request.note_title,
            "note_content": request.note_content,
        }
    }

    await db["notes"].update_one({"_id": note_id}, update_data)
    updated_note = await db["notes"].find_one({"_id": note_id})

    return {
        "note_id": updated_note["_id"],
        "note_title": updated_note["note_title"],
        "note_content": updated_note["note_content"],
        "user_id": updated_note["user_id"],
        "created_on": updated_note["created_on"],
    }


@router.delete("/{note_id}")
async def delete_note(note_id: str, Authorization: str = Header(...)):
    db=get_database()
    token = Authorization.split(" ")[1]
    user_id = verify_access_token(token)

    note = await db["notes"].find_one({"_id": note_id, "user_id": user_id})
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")

    await db["notes"].delete_one({"_id": note_id})
    return {"detail": "Note deleted successfully"}
