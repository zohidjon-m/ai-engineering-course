# Homework 04: Run a SQL query through FastAPI

This project adds a `GET /loans` endpoint to the library API. It uses SQLAlchemy to read loans from PostgreSQL and supports filtering by whether a loan is still open.

## SQL


SELECT id, book_id, member_id, borrowed_on, returned_on
FROM loans
WHERE returned_on IS NULL
ORDER BY id;
```

On the seed data this returns only loan `102`.

## API response

Request: `GET /loans?open=true`


[
  {
    "id": 102,
    "book_id": 1,
    "member_id": 12,
    "borrowed_on": "2026-01-12",
    "returned_on": null
  }
]
```

Other requests behave as expected:

| Request | Result |
| --- | --- |
| `GET /loans?open=true` | Loan `102` only |
| `GET /loans?open=false` | Loans `101` and `103`, in that order |
| `GET /loans` | All three loans, in ID order |

## Setup


pip install -r requirements.txt
psql "<your connection string>" -f library.sql
$env:DATABASE_URL = "<your connection string>"
uvicorn main:app --reload
```

Then open `http://127.0.0.1:8000/docs` and try the requests above. The connection string is read from the `DATABASE_URL` environment variable and is not stored in this repository.

## How it works

When a request such as `GET /loans?open=true` arrives, FastAPI matches it to the `list_loans` route, parses `open` into a boolean, and passes in a database session. The route builds a SQLAlchemy `select(Loan)` ordered by `id`, adding `WHERE returned_on IS NULL` for open loans or `IS NOT NULL` for returned ones. SQLAlchemy sends the generated SQL to PostgreSQL over the connection, and the returned rows are converted into the `LoanRead` model and sent back as JSON.