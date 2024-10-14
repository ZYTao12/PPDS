from fastapi import APIRouter, HTTPException, Body, Request, Response, HTTPException, status
from fastapi.encoders import jsonable_encoder
from typing import List
from backend.models import User, UserLogin, UserUpdate, Event

router = APIRouter()

@router.post("/", response_description="Add new user", status_code=status.HTTP_201_CREATED, response_model=User)
def create_user(request: Request, user: User = Body(...)):
    user = jsonable_encoder(user)
    if "_id" in user:
        del user["_id"]  # Remove _id if it's in the request body
    new_user = request.app.database["user"].insert_one(user)
    created_user = request.app.database["user"].find_one({"_id": new_user.inserted_id})
    return created_user

@router.get("/", response_description="List all users", response_model=List[User])
def list_users(request: Request):
    users = list(request.app.database["user"].find({}))
    return users
