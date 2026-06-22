from pydantic import BaseModel, ConfigDict, EmailStr
from typing import Literal


# Validation class, only these values will be used as post
class UserCreate(BaseModel):
    email: str
    name: str
    username: str
    password: str

class UserResponse(BaseModel):
    id: int
    email: str
    name: str
    username: str

    model_config = ConfigDict(from_attributes=True)  # this is used because the returned response from the Db is a sqlalchemy object and we need it to be a dict.       

class UserUpdate(BaseModel):
    name: str | None = None
    email: str | None = None
    username: str | None = None
    password: str | None = None

# validation class for issues
class CreateIssue(BaseModel):
    title: str
    description: str
    priority: Literal["Low", "Medium", "High", "Critical"]
    status: Literal["Done", "In Progress","Resolved", "Closed"]
    assigned_to: str

class IssueResponse(BaseModel):
    id: int
    title: str
    description: str
    priority: Literal["Low", "Medium", "High", "Critical"]
    status: Literal["Done", "In Progress","Resolved", "Closed"]
    assigned_to: int 
    created_by: int

    model_config = ConfigDict(from_attributes=True)  # this is used because the returned response from the Db is a sqlalchemy object and we need it to be a dict.       

class LoginRequest(BaseModel):
    email: EmailStr
    password: str
