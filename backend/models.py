from pydantic import BaseModel, EmailStr

# User input for signup or login
class UserIn(BaseModel):
    email: EmailStr
    password: str

# What we return to the frontend (safe, no password)
class UserOut(BaseModel):
    id: str
    email: EmailStr

# Internal model for database (stores hashed password)
class UserInDB(UserIn):
    id: str
    hashed_password: str
