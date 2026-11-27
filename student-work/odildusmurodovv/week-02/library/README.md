# Week 02 – Library API with SQLAlchemy

## Setup & Commands

1. Set `DATABASE_URL` for an empty PostgreSQL database:

       export DATABASE_URL="postgresql+psycopg://USER:PASSWORD@HOST:5432/library_homework"

2. Install dependencies:

       python -m pip install -r requirements.txt

3. Create tables and seed initial records (run once):

       python setup_db.py

4. Start the server:

       python -m uvicorn main:app --reload

Open API documentation: http://127.0.0.1:8000/docs

---

## Rollback Verification Check

Executed a transaction modifying loan `102`, calling `session.flush()`, and raising an exception before exiting `with session.begin():`:

    Caught expected error: Simulated failure before commit
    Loan 102 returned_on after rollback: None

---

## API Verification Results (`/docs`)

| Check | Endpoint | Observed Result |
| :--- | :--- | :--- |
| Notes for Books 1, 2, 3 | `GET /books/{1,2,3}/notes` | `200` — 4, 3, and 3 notes with generated integer IDs |
| Missing book notes | `GET /books/999/notes` | `404` — `{"detail": "Book not found"}` |
| Open loans before return | `GET /loans?open=true` | `200` — Loan `102` (`The Hobbit`, `Ali`, `returned_on: null`) |
| Returned loans before return | `GET /loans?open=false` | `200` — Loans `101` (`Mina`) and `103` (`Sara`) |
| Books left join | `GET /books/loans` | `200` — 4 rows; Book `1` appears twice (`101`, `102`), Book `3` appears with `loan_id: null` |
| Return loan 102 | `PATCH /loans/102/return` | `200` — `returned_on` updated to `"2026-01-15"` |
| Open loans after return | `GET /loans?open=true` | `200` — `[]` |
| Restart persistence check | `GET /loans` | `200` — Loan `102` retained `"returned_on": "2026-01-15"` |
| Unknown loan return | `PATCH /loans/999/return` | `404` — `{"detail": "Loan not found"}` |

---

## Explanations

- **How `create_all()` creates tables:** `Base.metadata.create_all(engine)` inspects all ORM subclasses of `Base` (`Book`, `Member`, `Loan`, `BookNote`), reads their table names, column types, primary keys, nullability, and `ForeignKey` constraints, and executes `CREATE TABLE` statements in PostgreSQL for tables that do not yet exist[span_14](start_span)[span_14](end_span).
- **How `session.add_all()` prepares rows:** `session.add_all()` registers ORM instances as pending in the session's unit-of-work identity map; `session.flush()` or committing the transaction emits the corresponding `INSERT` statements to PostgreSQL[span_15](start_span)[span_15](end_span).
- **Why the left join keeps Book 3:** `outerjoin(Loan, Book.id == Loan.book_id)` performs a `LEFT OUTER JOIN` from `books` to `loans`, keeping every row from `books` even when no matching row exists in `loans`, returning `null` for `loan_id` on *The Little Prince*[span_16](start_span)[span_16](end_span).
- **Why the failed transaction left `returned_on` empty:** Although `session.flush()` sent the `UPDATE` within the open transaction, raising an exception before `with session.begin():` exited caused SQLAlchemy to issue a `ROLLBACK`, discarding the uncommitted change[span_17](start_span)[span_17](end_span).
