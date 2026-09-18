"""
High School Management System API

A super simple FastAPI application that allows students to view and sign up
for extracurricular activities at Mergington High School.
"""

from typing import Optional

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from pydantic import BaseModel, Field
import os
from pathlib import Path

app = FastAPI(title="Mergington High School API",
              description="API for viewing and signing up for extracurricular activities")

# Mount the static files directory
current_dir = Path(__file__).parent
app.mount("/static", StaticFiles(directory=os.path.join(Path(__file__).parent,
          "static")), name="static")

# In-memory activity database
activities = {
    "Chess Club": {
        "description": "Learn strategies and compete in chess tournaments",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 12,
        "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
    },
    "Programming Class": {
        "description": "Learn programming fundamentals and build software projects",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
        "max_participants": 20,
        "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
    },
    "Gym Class": {
        "description": "Physical education and sports activities",
        "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
        "max_participants": 30,
        "participants": ["john@mergington.edu", "olivia@mergington.edu"]
    },
    "Soccer Team": {
        "description": "Join the school soccer team and compete in matches",
        "schedule": "Tuesdays and Thursdays, 4:00 PM - 5:30 PM",
        "max_participants": 22,
        "participants": ["liam@mergington.edu", "noah@mergington.edu"]
    },
    "Basketball Team": {
        "description": "Practice and play basketball with the school team",
        "schedule": "Wednesdays and Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 15,
        "participants": ["ava@mergington.edu", "mia@mergington.edu"]
    },
    "Art Club": {
        "description": "Explore your creativity through painting and drawing",
        "schedule": "Thursdays, 3:30 PM - 5:00 PM",
        "max_participants": 15,
        "participants": ["amelia@mergington.edu", "harper@mergington.edu"]
    },
    "Drama Club": {
        "description": "Act, direct, and produce plays and performances",
        "schedule": "Mondays and Wednesdays, 4:00 PM - 5:30 PM",
        "max_participants": 20,
        "participants": ["ella@mergington.edu", "scarlett@mergington.edu"]
    },
    "Math Club": {
        "description": "Solve challenging problems and participate in math competitions",
        "schedule": "Tuesdays, 3:30 PM - 4:30 PM",
        "max_participants": 10,
        "participants": ["james@mergington.edu", "benjamin@mergington.edu"]
    },
    "Debate Team": {
        "description": "Develop public speaking and argumentation skills",
        "schedule": "Fridays, 4:00 PM - 5:30 PM",
        "max_participants": 12,
        "participants": ["charlotte@mergington.edu", "henry@mergington.edu"]
    }
}


class SessionCreate(BaseModel):
    name: str = Field(min_length=1)
    start_year: int
    end_year: int


class SessionUpdate(BaseModel):
    name: Optional[str] = Field(default=None, min_length=1)
    start_year: Optional[int] = None
    end_year: Optional[int] = None


class SemesterCreate(BaseModel):
    name: str = Field(min_length=1)
    session_id: str
    start_date: str
    end_date: str


class SemesterUpdate(BaseModel):
    name: Optional[str] = Field(default=None, min_length=1)
    session_id: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None


class ClassCreate(BaseModel):
    name: str = Field(min_length=1)
    grade_level: str = Field(min_length=1)


class ClassUpdate(BaseModel):
    name: Optional[str] = Field(default=None, min_length=1)
    grade_level: Optional[str] = Field(default=None, min_length=1)


class SectionCreate(BaseModel):
    name: str = Field(min_length=1)
    class_id: str


class SectionUpdate(BaseModel):
    name: Optional[str] = Field(default=None, min_length=1)
    class_id: Optional[str] = None


class CourseCreate(BaseModel):
    name: str = Field(min_length=1)
    code: str = Field(min_length=1)
    class_ids: list[str] = Field(default_factory=list)
    semester_ids: list[str] = Field(default_factory=list)


class CourseUpdate(BaseModel):
    name: Optional[str] = Field(default=None, min_length=1)
    code: Optional[str] = Field(default=None, min_length=1)
    class_ids: Optional[list[str]] = None
    semester_ids: Optional[list[str]] = None


academic_structure = {
    "sessions": {},
    "semesters": {},
    "classes": {},
    "sections": {},
    "courses": {},
}


def _next_id(entity: str) -> str:
    singular_names = {
        "sessions": "session",
        "semesters": "semester",
        "classes": "class",
        "sections": "section",
        "courses": "course",
    }
    return f"{singular_names[entity]}-{len(academic_structure[entity]) + 1}"


def _require_entity(entity: str, entity_id: str) -> dict:
    record = academic_structure[entity].get(entity_id)
    if record is None:
        raise HTTPException(status_code=404, detail=f"{entity[:-1].capitalize()} not found")
    return record


def _require_relationships(entity: str, entity_ids: list[str]) -> None:
    for entity_id in entity_ids:
        _require_entity(entity, entity_id)


@app.get("/")
def root():
    return RedirectResponse(url="/static/index.html")


@app.get("/activities")
def get_activities():
    return activities


@app.get("/academic-structure")
def get_academic_structure():
    return academic_structure


@app.post("/academic/sessions", status_code=201)
def create_session(session: SessionCreate):
    if session.start_year > session.end_year:
        raise HTTPException(status_code=400, detail="Start year must not be after end year")

    session_id = _next_id("sessions")
    academic_structure["sessions"][session_id] = {
        "id": session_id,
        **session.model_dump(),
    }
    return academic_structure["sessions"][session_id]


@app.put("/academic/sessions/{session_id}")
def update_session(session_id: str, session: SessionUpdate):
    current = _require_entity("sessions", session_id)
    updated = {**current, **session.model_dump(exclude_unset=True)}
    if updated["start_year"] > updated["end_year"]:
        raise HTTPException(status_code=400, detail="Start year must not be after end year")

    academic_structure["sessions"][session_id] = updated
    return updated


@app.post("/academic/semesters", status_code=201)
def create_semester(semester: SemesterCreate):
    _require_entity("sessions", semester.session_id)
    semester_id = _next_id("semesters")
    academic_structure["semesters"][semester_id] = {
        "id": semester_id,
        **semester.model_dump(),
    }
    return academic_structure["semesters"][semester_id]


@app.put("/academic/semesters/{semester_id}")
def update_semester(semester_id: str, semester: SemesterUpdate):
    current = _require_entity("semesters", semester_id)
    changes = semester.model_dump(exclude_unset=True)
    if "session_id" in changes:
        _require_entity("sessions", changes["session_id"])

    updated = {**current, **changes}
    academic_structure["semesters"][semester_id] = updated
    return updated


@app.post("/academic/classes", status_code=201)
def create_class(school_class: ClassCreate):
    class_id = _next_id("classes")
    academic_structure["classes"][class_id] = {
        "id": class_id,
        **school_class.model_dump(),
    }
    return academic_structure["classes"][class_id]


@app.put("/academic/classes/{class_id}")
def update_class(class_id: str, school_class: ClassUpdate):
    current = _require_entity("classes", class_id)
    updated = {**current, **school_class.model_dump(exclude_unset=True)}
    academic_structure["classes"][class_id] = updated
    return updated


@app.post("/academic/sections", status_code=201)
def create_section(section: SectionCreate):
    _require_entity("classes", section.class_id)
    section_id = _next_id("sections")
    academic_structure["sections"][section_id] = {
        "id": section_id,
        **section.model_dump(),
    }
    return academic_structure["sections"][section_id]


@app.put("/academic/sections/{section_id}")
def update_section(section_id: str, section: SectionUpdate):
    current = _require_entity("sections", section_id)
    changes = section.model_dump(exclude_unset=True)
    if "class_id" in changes:
        _require_entity("classes", changes["class_id"])

    updated = {**current, **changes}
    academic_structure["sections"][section_id] = updated
    return updated


@app.post("/academic/courses", status_code=201)
def create_course(course: CourseCreate):
    _require_relationships("classes", course.class_ids)
    _require_relationships("semesters", course.semester_ids)
    course_id = _next_id("courses")
    academic_structure["courses"][course_id] = {
        "id": course_id,
        **course.model_dump(),
    }
    return academic_structure["courses"][course_id]


@app.put("/academic/courses/{course_id}")
def update_course(course_id: str, course: CourseUpdate):
    current = _require_entity("courses", course_id)
    changes = course.model_dump(exclude_unset=True)
    if "class_ids" in changes:
        _require_relationships("classes", changes["class_ids"])
    if "semester_ids" in changes:
        _require_relationships("semesters", changes["semester_ids"])

    updated = {**current, **changes}
    academic_structure["courses"][course_id] = updated
    return updated


@app.post("/activities/{activity_name}/signup")
def signup_for_activity(activity_name: str, email: str):
    """Sign up a student for an activity"""
    # Validate activity exists
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    # Get the specific activity
    activity = activities[activity_name]

    # Validate student is not already signed up
    if email in activity["participants"]:
        raise HTTPException(
            status_code=400,
            detail="Student is already signed up"
        )

    # Add student
    activity["participants"].append(email)
    return {"message": f"Signed up {email} for {activity_name}"}


@app.delete("/activities/{activity_name}/unregister")
def unregister_from_activity(activity_name: str, email: str):
    """Unregister a student from an activity"""
    # Validate activity exists
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    # Get the specific activity
    activity = activities[activity_name]

    # Validate student is signed up
    if email not in activity["participants"]:
        raise HTTPException(
            status_code=400,
            detail="Student is not signed up for this activity"
        )

    # Remove student
    activity["participants"].remove(email)
    return {"message": f"Unregistered {email} from {activity_name}"}
