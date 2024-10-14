from typing import Any, Optional
from pydantic import BaseModel, Field, GetJsonSchemaHandler
from pydantic_core import core_schema
from bson import ObjectId
from datetime import datetime

class PyObjectId(ObjectId):
    @classmethod
    def __get_pydantic_core_schema__(
        cls, _source_type: Any, _handler: Any
    ) -> core_schema.CoreSchema:
        return core_schema.json_or_python_schema(
            json_schema=core_schema.str_schema(),
            python_schema=core_schema.is_instance_schema(ObjectId),
            serialization=core_schema.plain_serializer_function_ser_schema(str),
        )

class User(BaseModel):
    id: Optional[PyObjectId] = Field(default=None, alias="_id")
    name: str = Field(...)
    netid: str = Field(...)
    email: str = Field(...)

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        json_schema_extra = {
            "example": {
                "name": "John Doe",
                "netid": "jd1234",
                "email": "jd1234@nyu.edu"
            }
        }

# model for user login, used for oauth, token
class UserLogin(BaseModel):
    oauthToken: Optional[dict] = Field(
        None,
        description="OAuth token information",
        example={
            "access_token": "ya29.a0AfH6SMBx...",
            "refresh_token": "1//0eXy...",
            "scope": "https://www.googleapis.com/auth/calendar.readonly",
            "token_type": "Bearer",
            "expiry_date": 1617211232170
        }
    )

    class Config:
        populate_by_name = True

# model for updating user information, including preferences, expressed availability, and calendarID
class UserUpdate(BaseModel):
    name: Optional[str] = None
    netid: Optional[str] = None
    email: Optional[str] = None
    preferences: Optional[dict] = Field(
        None,
        description="User preferences",
        example={
            "eventTypes": ["meeting", "workshop"],
            "availability": [
                {"day": "Monday", "start": "09:00", "end": "17:00"},
                {"day": "Tuesday", "start": "10:00", "end": "18:00"}
            ]
        }
    )
    calendarID: Optional[str] = Field(None, description="User's Google Calendar ID")

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str
        }
        json_schema_extra = {
            "example": {
                "name": "John Doe",
                "netid": "jd1234",
                "email": "jd1234@nyu.edu",
                "preferences": {
                    "eventTypes": ["meeting", "workshop"],
                    "availability": [
                        {"day": "Monday", "start": "09:00", "end": "17:00"},
                        {"day": "Tuesday", "start": "10:00", "end": "18:00"}
                    ]
                },
                "calendarID": "calendar12345@group.calendar.google.com"
            }
        }

# model for serializing events, used for retrieving events from Google Calendar and NYU Engage and suggesting events to users
# which corresponds to Events: imports in Google Calendar API
class Event(BaseModel):
    id: str = Field(..., alias="_id")
    name: str = Field(...)
    description: str = Field(...)
    category: str = Field(...)
    venue: str = Field(...)
    startTime: datetime = Field(...)
    endTime: datetime = Field(...)
    createdAt: datetime = Field(...)
    source: str = Field(...)    # NYU Engage, Personal, etc.
    responseStatus: Optional[str] = Field(None, description="Response status of the event")
    # "needsAction", "declined", "tentative", "accepted"

    class Config:
        populate_by_name = True
        json_encoders = {
            ObjectId: str,
            datetime: lambda v: v.isoformat()
        }
        json_schema_extra = {
            "example": {
                "_id": "5f8d0d55b54764421b7156bc",
                "name": "STEM Conference 2024",
                "description": "A STEM conference",
                "category": "STEM",
                "venue": "NYU Auditorium",
                "startTime": "2024-11-01T09:00:00Z",
                "endTime": "2024-11-01T17:00:00Z",
                "createdAt": "2024-10-01T10:00:00Z",
                "source": "NYU Engage"
            }
        }
