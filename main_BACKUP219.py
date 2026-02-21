# main.py
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import os
from dotenv import load_dotenv
from datetime import datetime
from anthropic import Anthropic

from models import Task, TaskCreate, Idea, IdeaCreate, IdeaUpdate
from database import get_db, init_db

load_dotenv()

# Initialize Anthropic client
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
anthropic_client = Anthropic(api_key=ANTHROPIC_API_KEY) if ANTHROPIC_API_KEY else None

app = FastAPI(
    title="To-Do & Ideas API",
    description="Backend API for managing tasks and ideas with AI integration",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database on startup
@app.on_event("startup")
def startup_event():
    init_db()

# ==================== HEALTH CHECK ====================

@app.get("/")
def read_root():
    return {
        "message": "To-Do & Ideas API",
        "version": "1.0.0",
        "status": "running"
    }

@app.get("/health")
def health_check():
    return {"status": "healthy"}

# ==================== TASKS ENDPOINTS ====================

@app.get("/api/tasks", response_model=List[Task])
def get_tasks():
    """Get all tasks"""
    try:
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM tasks ORDER BY created_at DESC")
            tasks = cursor.fetchall()
            return tasks
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {str(e)}"
        )

@app.get("/api/tasks/{task_id}", response_model=Task)
def get_task(task_id: int):
    """Get a specific task by ID"""
    try:
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM tasks WHERE id = %s", (task_id,))
            task = cursor.fetchone()
            if not task:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Task not found"
                )
            return task
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {str(e)}"
        )

@app.post("/api/tasks", response_model=Task, status_code=status.HTTP_201_CREATED)
def create_task(task: TaskCreate):
    """Create a new task"""
    try:
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO tasks (id, text, completed, task_owner, due_date, created_at)
                VALUES (%s, %s, %s, %s, %s, NOW())
                RETURNING *
                """,
                (task.id, task.text, task.completed, task.task_owner, task.due_date)
            )
            new_task = cursor.fetchone()
            return new_task
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {str(e)}"
        )

@app.put("/api/tasks/{task_id}", response_model=Task)
def update_task(task_id: int, task: TaskCreate):
    """Update an existing task"""
    try:
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                UPDATE tasks
                SET text = %s, completed = %s, task_owner = %s, due_date = %s
                WHERE id = %s
                RETURNING *
                """,
                (task.text, task.completed, task.task_owner, task.due_date, task_id)
            )
            updated_task = cursor.fetchone()
            if not updated_task:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Task not found"
                )
            return updated_task
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {str(e)}"
        )

@app.delete("/api/tasks/{task_id}")
def delete_task(task_id: int):
    """Delete a specific task"""
    try:
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM tasks WHERE id = %s RETURNING id", (task_id,))
            deleted = cursor.fetchone()
            if not deleted:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Task not found"
                )
            return {"message": "Task deleted successfully", "id": task_id}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {str(e)}"
        )

@app.delete("/api/tasks/completed/all")
def delete_completed_tasks():
    """Delete all completed tasks"""
    try:
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM tasks WHERE completed = TRUE RETURNING id")
            deleted_tasks = cursor.fetchall()
            count = len(deleted_tasks)
            return {
                "message": f"{count} completed task(s) deleted successfully",
                "count": count
            }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {str(e)}"
        )

# ==================== IDEAS ENDPOINTS ====================

@app.get("/api/ideas", response_model=List[Idea])
def get_ideas():
    """Get all ideas"""
    try:
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM ideas ORDER BY created_at DESC")
            ideas = cursor.fetchall()
            return ideas
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {str(e)}"
        )

@app.get("/api/ideas/{idea_id}", response_model=Idea)
def get_idea(idea_id: int):
    """Get a specific idea by ID"""
    try:
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM ideas WHERE id = %s", (idea_id,))
            idea = cursor.fetchone()
            if not idea:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Idea not found"
                )
            return idea
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {str(e)}"
        )

@app.post("/api/ideas", response_model=Idea, status_code=status.HTTP_201_CREATED)
def create_idea(idea: IdeaCreate):
    """Create a new idea"""
    try:
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO ideas (id, text, domain, chat_history, created_by, created_at)
                VALUES (%s, %s, %s, '[]'::jsonb, %s, NOW())
                RETURNING *
                """,
                (idea.id, idea.text, idea.domain, idea.created_by)
            )
            new_idea = cursor.fetchone()
            return new_idea
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {str(e)}"
        )

@app.put("/api/ideas/{idea_id}", response_model=Idea)
def update_idea(idea_id: int, idea: IdeaUpdate):
    """Update an existing idea"""
    try:
        with get_db() as conn:
            cursor = conn.cursor()
            
            # Build dynamic update query based on provided fields
            update_fields = []
            values = []
            
            if idea.text is not None:
                update_fields.append("text = %s")
                values.append(idea.text)
            if idea.domain is not None:
                update_fields.append("domain = %s")
                values.append(idea.domain)
            if idea.recommendations is not None:
                update_fields.append("recommendations = %s")
                values.append(idea.recommendations)
            if idea.ai_feedback is not None:
                update_fields.append("ai_feedback = %s")
                values.append(idea.ai_feedback)
            if idea.feature_list is not None:
                update_fields.append("feature_list = %s")
                values.append(idea.feature_list)
                update_fields.append("feature_list_generated_at = NOW()")
            if idea.chat_history is not None:
                # Convert chat_history list to JSON string for PostgreSQL JSONB
                import json
                update_fields.append("chat_history = %s::jsonb")
                values.append(json.dumps(idea.chat_history))
            if idea.created_by is not None:
                update_fields.append("created_by = %s")
                values.append(idea.created_by)
            
            if update_fields:
                update_fields.append("updated_at = NOW()")
                values.append(idea_id)
                
                query = f"""
                    UPDATE ideas
                    SET {', '.join(update_fields)}
                    WHERE id = %s
                    RETURNING *
                """
                cursor.execute(query, values)
                updated_idea = cursor.fetchone()
                
                if not updated_idea:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail="Idea not found"
                    )
                return updated_idea
            else:
                # No fields to update, just return the existing idea
                return get_idea(idea_id)
                
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {str(e)}"
        )

@app.delete("/api/ideas/{idea_id}")
def delete_idea(idea_id: int):
    """Delete a specific idea"""
    try:
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM ideas WHERE id = %s RETURNING id", (idea_id,))
            deleted = cursor.fetchone()
            if not deleted:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Idea not found"
                )
            return {"message": "Idea deleted successfully", "id": idea_id}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {str(e)}"
        )

@app.delete("/api/ideas/all")
def delete_all_ideas():
    """Delete all ideas"""
    try:
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM ideas RETURNING id")
            deleted_ideas = cursor.fetchall()
            count = len(deleted_ideas)
            return {
                "message": f"{count} idea(s) deleted successfully",
                "count": count
            }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {str(e)}"
        )

# ==================== STATISTICS ENDPOINTS ====================

@app.get("/api/stats")
def get_statistics():
    """Get overall statistics"""
    try:
        with get_db() as conn:
            cursor = conn.cursor()
            
            # Task statistics
            cursor.execute("SELECT COUNT(*) as total FROM tasks")
            total_tasks = cursor.fetchone()['total']
            
            cursor.execute("SELECT COUNT(*) as completed FROM tasks WHERE completed = TRUE")
            completed_tasks = cursor.fetchone()['completed']
            
            # Idea statistics
            cursor.execute("SELECT COUNT(*) as total FROM ideas")
            total_ideas = cursor.fetchone()['total']
            
            cursor.execute("SELECT COUNT(*) as with_recommendations FROM ideas WHERE recommendations IS NOT NULL")
            ideas_with_recommendations = cursor.fetchone()['with_recommendations']
            
            cursor.execute("SELECT COUNT(*) as with_features FROM ideas WHERE feature_list IS NOT NULL")
            ideas_with_features = cursor.fetchone()['with_features']
            
            # Ideas by domain
            cursor.execute("""
                SELECT domain, COUNT(*) as count 
                FROM ideas 
                WHERE domain IS NOT NULL 
                GROUP BY domain
            """)
            ideas_by_domain = cursor.fetchall()
            
            return {
                "tasks": {
                    "total": total_tasks,
                    "completed": completed_tasks,
                    "active": total_tasks - completed_tasks
                },
                "ideas": {
                    "total": total_ideas,
                    "with_recommendations": ideas_with_recommendations,
                    "with_features": ideas_with_features,
                    "by_domain": ideas_by_domain
                }
            }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {str(e)}"
        )

# ==================== AI ENDPOINTS ====================

@app.post("/api/ai/feedback")
async def get_ai_feedback(request: dict):
    """
    AI Feedback endpoint - Used for generating next steps
    Frontend calls this for: "Make Task" with AI next steps
    
    Request body: {"prompt": "your prompt text"}
    """
    if not anthropic_client:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="AI service not configured. Please add ANTHROPIC_API_KEY to .env file"
        )
    
    try:
        prompt = request.get("prompt", "")
        
        if not prompt:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Prompt is required"
            )
        
        message = anthropic_client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=2000,
            messages=[{"role": "user", "content": prompt}]
        )
        
        return {
            "content": [
                {"type": "text", "text": block.text}
                for block in message.content
                if hasattr(block, 'text')
            ]
        }
    except HTTPException:
        raise
    except Exception as e:
        print(f"AI feedback error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"AI service error: {str(e)}"
        )

@app.post("/api/ai/chat")
async def ai_chat(request: dict):
    """
    AI Chat endpoint - Used for conversational AI features
    Frontend calls this for:
    - Initial AI feedback on ideas
    - Chat follow-ups
    - Idea refinement
    - Feature list generation
    
    Request body: {
        "messages": [{"role": "user", "content": "message"}],
        "max_tokens": 2000
    }
    """
    if not anthropic_client:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="AI service not configured. Please add ANTHROPIC_API_KEY to .env file"
        )
    
    try:
        messages = request.get("messages", [])
        max_tokens = request.get("max_tokens", 2000)
        
        if not messages:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Messages array is required"
            )
        
        message = anthropic_client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=max_tokens,
            messages=messages
        )
        
        return {
            "content": [
                {"type": "text", "text": block.text}
                for block in message.content
                if hasattr(block, 'text')
            ]
        }
    except HTTPException:
        raise
    except Exception as e:
        print(f"AI chat error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"AI service error: {str(e)}"
        )
