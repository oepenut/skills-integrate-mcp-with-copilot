# Mergington High School Activities API

A super simple FastAPI application that allows students to view and sign up for extracurricular activities.

## Features

- View all available extracurricular activities
- Sign up for activities
- Manage academic sessions, semesters, classes, sections, and courses

## Getting Started

1. Install the dependencies:

   ```
   pip install fastapi uvicorn
   ```

2. Run the application:

   ```
   python app.py
   ```

3. Open your browser and go to:
   - API documentation: http://localhost:8000/docs
   - Alternative documentation: http://localhost:8000/redoc

## API Endpoints

| Method | Endpoint                                                          | Description                                                         |
| ------ | ----------------------------------------------------------------- | ------------------------------------------------------------------- |
| GET    | `/activities`                                                     | Get all activities with their details and current participant count |
| POST   | `/activities/{activity_name}/signup?email=student@mergington.edu` | Sign up for an activity                                             |
| GET    | `/academic-structure`                                              | Get the complete academic structure and its relationships           |
| POST   | `/academic/sessions`                                               | Create a school session                                             |
| PUT    | `/academic/sessions/{session_id}`                                  | Update a school session                                             |
| POST   | `/academic/semesters`                                              | Create a semester linked to a session                               |
| PUT    | `/academic/semesters/{semester_id}`                                | Update a semester                                                   |
| POST   | `/academic/classes`                                                | Create a class or grade level                                       |
| PUT    | `/academic/classes/{class_id}`                                     | Update a class                                                      |
| POST   | `/academic/sections`                                               | Create a section linked to a class                                  |
| PUT    | `/academic/sections/{section_id}`                                  | Update a section                                                    |
| POST   | `/academic/courses`                                                | Create a course linked to classes and semesters                     |
| PUT    | `/academic/courses/{course_id}`                                    | Update a course and its relationships                               |

## Data Model

The application uses a simple data model with meaningful identifiers:

1. **Activities** - Uses activity name as identifier:

   - Description
   - Schedule
   - Maximum number of participants allowed
   - List of student emails who are signed up

2. **Students** - Uses email as identifier:
   - Name
   - Grade level

3. **Academic structure** - Uses generated IDs and explicit relationships:
   - Sessions contain semesters
   - Classes contain sections
   - Courses link to classes and semesters

All data is stored in memory, which means data will be reset when the server restarts. The academic endpoints are currently unprotected; authentication and role-based access belong to the separate authentication issue.
