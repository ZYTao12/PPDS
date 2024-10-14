from fastapi import APIRouter, HTTPException, Body, Request, Response, HTTPException, status
from fastapi.encoders import jsonable_encoder
from typing import List
from models import User, UserLogin, UserUpdate, Event, EventUpdate
from bson import ObjectId
import requests

router = APIRouter()

@router.post("/users/", response_description="Add new user", status_code=status.HTTP_201_CREATED, response_model=User)
def create_user(request: Request, user: User = Body(...)):
    user = jsonable_encoder(user)
    if "_id" in user:
        del user["_id"]  # Remove _id if it's in the request body
    new_user = request.app.database["user"].insert_one(user)
    created_user = request.app.database["user"].find_one({"_id": new_user.inserted_id})
    return created_user

@router.get("/users/", response_description="List all users", response_model=List[User])
def list_users(request: Request):
    users = list(request.app.database["user"].find({}))
    return users

@router.get("/users/{id}", response_description="Get a single user by id", response_model=User)
def find_user(id: str, request: Request):
    if (user := request.app.database["user"].find_one({"_id": ObjectId(id)})) is not None:
        return user
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with ID {id} not found")

@router.post("/login", response_description="User login with OAuth 2.0", response_model=UserLogin)
async def login(request: Request, user_login: UserLogin = Body(...)):
    oauth_token = user_login.oauthToken

    if not oauth_token or "access_token" not in oauth_token:
        raise HTTPException(status_code=400, detail="Invalid OAuth token")

    # Verify the token with Google
    google_user_info_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    headers = {"Authorization": f"Bearer {oauth_token['access_token']}"}
    
    response = requests.get(google_user_info_url, headers=headers)
    
    if response.status_code != 200:
        raise HTTPException(status_code=401, detail="Invalid Google token")

    google_user_info = response.json()

    # Check if the user exists in your database
    user = request.app.database["user"].find_one({"email": google_user_info["email"]})

    if not user:
        # Create a new user if they don't exist
        new_user = {
            "email": google_user_info["email"],
            "name": google_user_info.get("name"),
        }
        result = request.app.database["user"].insert_one(new_user)
        user = request.app.database["user"].find_one({"_id": result.inserted_id})

    # Update the user's OAuth token
    request.app.database["user"].update_one(
        {"_id": user["_id"]},
        {"$set": {"oauthToken": oauth_token}}
    )

    return UserLogin(oauthToken=oauth_token)

@router.put("/users/{id}", response_description="Update a user", response_model=UserUpdate)
def update_user(id: str, request: Request, user: UserUpdate = Body(...)):
    user = {k: v for k, v in user.model_dump().items() if v is not None}
    if len(user) >= 1:
        update_result = request.app.database["user"].update_one({"_id": ObjectId(id)}, {"$set": user})

        if update_result.modified_count == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with ID {id} not found")   
    if (
        existing_user := request.app.database["user"].find_one({"_id": ObjectId(id)})
    ) is not None:
        return existing_user
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with ID {id} not found")

@router.delete("/users/{id}", response_description="Delete a user")
def delete_user(id: str, request: Request):
    delete_result = request.app.database["user"].delete_one({"_id": ObjectId(id)})
    if delete_result.deleted_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with ID {id} not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.post("/events/", response_description="Add a new event", status_code=status.HTTP_201_CREATED, response_model=Event)
def create_event(request: Request, event: Event = Body(...)):
    event = jsonable_encoder(event)
    if "_id" in event:
        del event["_id"]  # Remove _id if it's in the request body
    new_event = request.app.database["event"].insert_one(event)
    created_event = request.app.database["event"].find_one({"_id": new_event.inserted_id})
    return created_event

@router.get("/events/", response_description="List all events", response_model=List[Event])
def list_events(request: Request):
    events = list(request.app.database["event"].find({}))
    return events

@router.get("/events/{id}", response_description="Get a single event by id", response_model=Event)
def find_event(id: str, request: Request):
    if (event := request.app.database["event"].find_one({"_id": ObjectId(id)})) is not None:
        return event
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Event with ID {id} not found")

@router.put("/events/{id}", response_description="Update an event", response_model=EventUpdate)
def update_event(id: str, request: Request, event: EventUpdate = Body(...)):
    event = {k: v for k, v in event.model_dump().items() if v is not None}
    if len(event) >= 1:
        update_result = request.app.database["event"].update_one({"_id": ObjectId(id)}, {"$set": event})

        if update_result.modified_count == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Event with ID {id} not found")   
    if (
        existing_event := request.app.database["event"].find_one({"_id": ObjectId(id)})
    ) is not None:
        return existing_event
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Event with ID {id} not found")

@router.delete("/events/{id}", response_description="Delete an event")
def delete_event(id: str, request: Request):
    delete_result = request.app.database["event"].delete_one({"_id": ObjectId(id)})
    if delete_result.deleted_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Event with ID {id} not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)