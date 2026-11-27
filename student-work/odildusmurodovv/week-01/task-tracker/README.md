# Week 01 – Task Tracker API

## Setup & Commands

Install dependencies:

    python -m pip install -r requirements.txt

Start the server:

    python -m uvicorn main:app --reload

Open API documentation:

http://127.0.0.1:8000/docs

Run automated tests:

    python -m pytest -v

---

## Example Requests & Responses

### Create a task (`POST /tasks`)

Request:

    {
      "title": "Study FastAPI"
    }

Response (`201 Created`):

    {
      "id": 1,
      "title": "Study FastAPI",
      "description": "",
      "completed": false
    }

### Filter tasks (`GET /tasks?completed=false`)

Response (`200 OK`):

    [
      {
        "id": 1,
        "title": "Study FastAPI",
        "description": "",
        "completed": false
      }
    ]

### Replace a task (`PUT /tasks/1`)

Request:

    {
      "title": "Study FastAPI and Pytest",
      "description": "Complete Homework 03",
      "completed": true
    }

Response (`200 OK`):

    {
      "id": 1,
      "title": "Study FastAPI and Pytest",
      "description": "Complete Homework 03",
      "completed": true
    }

### Delete a task (`DELETE /tasks/1`)

Response: `204 No Content` (empty body).

---

## Automated Test Results

Running `python -m pytest -v` passes all 7 tests:

- `test_create_and_retrieve_task_defaults` — PASSED
- `test_filter_completed_and_incomplete_tasks` — PASSED
- `test_reject_invalid_titles_without_mutating_store` — PASSED
- `test_missing_and_invalid_path_ids` — PASSED
- `test_replace_task_and_reject_incomplete_put` — PASSED
- `test_delete_task_returns_204_and_subsequent_calls_return_404` — PASSED
- `test_delete_does_not_reuse_ids_or_overwrite_existing` — PASSED

---

## Notes & Reflections

- **In-memory storage limitation:** Tasks are stored in a Python dictionary (`tasks`) in RAM. Whenever the server restarts or reloads, all created tasks are lost and `next_task_id` resets to `1`.
- **Bug investigated:** Initially, using `if completed:` in `GET /tasks` skipped filtering when `completed=false` was passed because `False` is falsy in Python. Changing the check to `if completed is not None:` ensured `completed=false` properly filters incomplete tasks while omitting the parameter returns all tasks.
- **Checkpoint explanations:**
  - *Path ID vs. missing ID:* `/tasks/abc` fails FastAPI/Pydantic integer validation (`422`), whereas `/tasks/999` is a valid positive integer that passes validation and triggers our `404` lookup check.
  - *ID counter behavior:* Using an ever-increasing `next_task_id` instead of `len(tasks) + 1` prevents ID reuse and record overwrites after deletions.
- **AI assistance & verification:** Used an AI assistant to structure the Pydantic models (`TaskCreate`, `TaskReplace`, `TaskRead`) and `pytest` cases. Verified every endpoint manually in `/docs`, confirmed state reset after server restart, and ran `pytest` to verify all edge cases.
