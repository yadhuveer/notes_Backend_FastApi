from datetime import datetime
import uuid

def get_user_doc(user_name, user_email, hashed_pw):
    return {
        "_id": str(uuid.uuid4()),
        "user_name": user_name,
        "user_email": user_email,
        "password": hashed_pw,
        "created_on": datetime.utcnow(),
        "last_update": datetime.utcnow()
    }

def get_note_doc(note_title, note_content, user_id):
    return {
        "_id": str(uuid.uuid4()),
        "note_title": note_title,
        "note_content": note_content,
        "created_on": datetime.utcnow(),
        "last_update": datetime.utcnow(),
        "user_id": user_id
    }
