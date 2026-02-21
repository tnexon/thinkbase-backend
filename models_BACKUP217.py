# models.py
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime

# ==================== TASK MODELS ====================

class TaskBase(BaseModel):
    text: str
    completed: bool = False
    task_owner: Optional[str] = None  # NEW: Store who owns/created the task

class TaskCreate(TaskBase):
    id: int

class Task(TaskBase):
    id: int
    created_at: datetime
    task_owner: Optional[str] = None

    class Config:
        from_attributes = True

# ==================== IDEA MODELS ====================

class IdeaBase(BaseModel):
    text: str
    domain: Optional[str] = None
    created_by: Optional[str] = None  # NEW: Store who created the idea

class IdeaCreate(IdeaBase):
    id: int

class IdeaUpdate(BaseModel):
    """Model for updating an idea - all fields optional"""
    text: Optional[str] = None
    domain: Optional[str] = None
    recommendations: Optional[str] = None  # AI feedback text (legacy field)
    ai_feedback: Optional[str] = None  # NEW: Dedicated AI feedback storage
    feature_list: Optional[str] = None
    chat_history: Optional[List[Dict[str, str]]] = None  # Array of chat messages
    created_by: Optional[str] = None  # Who created the idea

class Idea(IdeaBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    recommendations: Optional[str] = None  # Legacy AI feedback field
    ai_feedback: Optional[str] = None  # NEW: Dedicated AI feedback column
    feature_list: Optional[str] = None
    feature_list_generated_at: Optional[datetime] = None
    chat_history: Optional[List[Dict[str, str]]] = None  # Chat history array
    created_by: Optional[str] = None  # NEW: Creator of the idea

    class Config:
        from_attributes = True

# ==================== AI REQUEST MODELS ====================

class AIFeedbackRequest(BaseModel):
    prompt: str

class AIChatRequest(BaseModel):
    messages: List[Dict[str, str]]
    max_tokens: int = 2000
