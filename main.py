from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr
from typing import List, Optional
from uuid import uuid4

app = FastAPI()
db = {}

class User(BaseModel):
    user_name: str
    user_id: str
    user_email: EmailStr
    age: Optional[int] = None
    recommendations: List[str]
    ZIP: Optional[str] = None

@app.post("/users/")
async def create_user(user: User):
    if user.user_email in [u['user_email'] for u in db.values()]:
        raise HTTPException(status_code=400, detail="Email already exists")
    
    user_id = str(uuid4()) 
    user.user_id = user_id
    db[user_id] = user.dict()
    return {"message": "User created successfully", "user_id": user_id}

@app.put("/users/{user_id}")
async def update_user(user_id: str, updated_user: User):
    if user_id not in db:
        raise HTTPException(status_code=404, detail="User not found")
    
    db[user_id].update(updated_user.dict())
    return {"message": "User updated successfully"}
@app.get("/users/{user_id}")
async def get_user(user_id: str):
    if user_id not in db:
        raise HTTPException(status_code=404, detail="User not found")
    
    return db[user_id]
@app.delete("/users/{user_id}")
async def delete_user(user_id: str):
    if user_id not in db:
        raise HTTPException(status_code=404, detail="User not found")
    
    del db[user_id]
    return {"message": "User deleted successfully"}
