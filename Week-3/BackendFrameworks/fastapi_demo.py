"""
FastAPI Framework Demonstration.

This is a self-contained, runnable FastAPI application demonstrating modern, 
asynchronous API features. It implements a complete CRUD resource endpoint for 
items, query/path parameters, Pydantic schemas, and dependency injection.

To run this application:
  1. Install dependencies: pip install fastapi uvicorn
  2. Execute the server: uvicorn fastapi_demo:app --reload
  3. Open your browser and navigate to:
     - API Docs (Swagger): http://127.0.0.1:8000/docs
     - ReDoc: http://127.0.0.1:8000/redoc
"""

from typing import Dict, List, Optional
from fastapi import FastAPI, Path, Query, HTTPException, Depends, status
from pydantic import BaseModel, Field

# ==============================================================================
# 1. APPLICATION INITIALIZATION
# ==============================================================================

# FastAPI automatically generates Swagger UI and ReDoc pages from variables here.
app = FastAPI(
    title="FastAPI Course Demo API",
    description="An educational CRUD API demonstrating FastAPI path, query, async, and dependencies.",
    version="1.0.0"
)


# ==============================================================================
# 2. PYDANTIC SCHEMAS (Data Validation)
# ==============================================================================

class CourseItem(BaseModel):
    """
    Pydantic schema representing a Course Item.
    Pydantic handles serialization, validation, and auto-documentation schemas.
    """
    name: str = Field(..., min_length=2, max_length=50, example="Python Web Frameworks")
    description: Optional[str] = Field(None, max_length=250, example="Deep dive into Django and FastAPI")
    difficulty: str = Field("Intermediate", example="Intermediate")
    weeks: int = Field(..., gt=0, le=12, description="Duration in weeks", example=3)


# Mock Database representation (In-memory dictionary)
db: Dict[int, dict] = {
    1: {"name": "HTML and CSS Basics", "description": "Front-end essentials", "difficulty": "Beginner", "weeks": 1},
    2: {"name": "SQL Databases", "description": "PostgreSQL and querying", "difficulty": "Intermediate", "weeks": 2}
}


# ==============================================================================
# 3. DEPENDENCY INJECTION (DI)
# ==============================================================================

async def get_token_header(token: str = Query(..., description="A mock API Token for security")):
    """
    A dependency function that validates a token parameter.
    If validation fails, raising HTTPExceptions automatically stops request processing.
    """
    if token != "secret-learning-token":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing Authorization Token."
        )
    return token


# ==============================================================================
# 4. CRUD ENDPOINTS (GET, POST, PUT, DELETE)
# ==============================================================================

@app.get("/", tags=["General"])
async def root():
    """
    Asynchronous root endpoint.
    'async def' is used because FastAPI runs on ASGI and supports non-blocking I/O out-of-the-box.
    """
    return {
        "message": "Welcome to the FastAPI Demo API",
        "docs_url": "/docs",
        "instructions": "Append query '?token=secret-learning-token' to secure routes."
    }


# GET: Retrieve list of items (Demonstrates Query Parameters & Async)
@app.get("/courses", response_model=Dict[int, dict], tags=["Courses"])
async def read_courses(
    limit: int = Query(10, ge=1, le=100, description="Limit the number of returned results"),
    difficulty: Optional[str] = Query(None, description="Filter items by difficulty level")
):
    """
    Retrieves all course items in the mock DB.
    Demonstrates query parameter validation and default values (limit, difficulty).
    """
    filtered_db = db
    if difficulty:
        filtered_db = {k: v for k, v in db.items() if v["difficulty"].lower() == difficulty.lower()}
        
    # Apply limit
    return dict(list(filtered_db.items())[:limit])


# GET: Retrieve a single item (Demonstrates Path Parameters)
@app.get("/courses/{course_id}", tags=["Courses"])
async def read_course(
    course_id: int = Path(..., description="The ID of the course to retrieve", gt=0)
):
    """
    Retrieve a specific course by its integer ID.
    Raises 404 error if course is not found.
    """
    if course_id not in db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course item not found.")
    return db[course_id]


# POST: Create a new resource (Demonstrates Pydantic Payload Request & DI)
@app.post("/courses", status_code=status.HTTP_201_CREATED, tags=["Courses"])
async def create_course(
    item: CourseItem,
    # Injecting the get_token_header dependency: route cannot run unless token matches
    token: str = Depends(get_token_header)
):
    """
    Adds a new course.
    - Demonstrates reading and validating JSON request bodies via Pydantic model `item`.
    - Demonstrates dependency injection for route authorization verification.
    """
    new_id = max(db.keys()) + 1 if db else 1
    db[new_id] = item.model_dump()  # Pydantic v2 model serialization method
    return {"id": new_id, "data": db[new_id]}


# PUT: Update an existing resource
@app.put("/courses/{course_id}", tags=["Courses"])
async def update_course(
    course_id: int = Path(..., gt=0),
    item: CourseItem = None,
    token: str = Depends(get_token_header)
):
    """
    Updates an existing course resource.
    Fails if the resource ID does not exist.
    """
    if course_id not in db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course item not found to update.")
        
    db[course_id] = item.model_dump()
    return {"id": course_id, "updated_data": db[course_id]}


# DELETE: Remove a resource
@app.delete("/courses/{course_id}", tags=["Courses"])
async def delete_course(
    course_id: int = Path(..., gt=0),
    token: str = Depends(get_token_header)
):
    """
    Deletes a course resource by its ID.
    Fails if the ID is missing.
    """
    if course_id not in db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course item not found to delete.")
        
    deleted_item = db.pop(course_id)
    return {"status": "success", "deleted_item": deleted_item}
