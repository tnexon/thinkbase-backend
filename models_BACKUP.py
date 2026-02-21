# models.py
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class TaskBase(BaseModel):
    text: str
    completed: bool = False

class TaskCreate(TaskBase):
    id: int

class Task(TaskBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class IdeaBase(BaseModel):
    text: str
    domain: Optional[str] = None

class IdeaCreate(IdeaBase):
    id: int

class IdeaUpdate(BaseModel):
    text: Optional[str] = None
    domain: Optional[str] = None
    recommendations: Optional[str] = None
    feature_list: Optional[str] = None

class Idea(IdeaBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    recommendations: Optional[str] = None
    feature_list: Optional[str] = None
    feature_list_generated_at: Optional[datetime] = None

    class Config:
        from_attributes = True