import os
from collections.abc import Iterator
from datetime import date
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Query
from pydantic import BaseModel, ConfigDict
from sqlalchemy import Text, create_engine, select, Date, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column


class Base(DeclarativeBase):
    pass


class Book(Base):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(Text)


class Loan(Base):
    
    __tablename__ = "loans"

    id: Mapped[int] = mapped_column(primary_key=True)
    book_id: Mapped[int] = mapped_column(ForeignKey("books.id"))
    member_id: Mapped[int] = mapped_column(ForeignKey("members.id"))
    borrowed_on: Mapped[date] = mapped_column(Date)
    returned_on: Mapped[date | None] = mapped_column(Date)


class BookRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str


class LoanRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    book_id: int
    member_id: int
    borrowed_on: date
    returned_on: date | None


engine = create_engine(os.environ["DATABASE_URL"])
app = FastAPI(title="Library SQL Homework")


def get_session() -> Iterator[Session]:
    with Session(engine) as session:
        yield session


@app.get("/books", response_model=list[BookRead])
def list_books(session: Annotated[Session, Depends(get_session)]):
    statement = select(Book).order_by(Book.id)
    return session.scalars(statement).all()


@app.get("/loans", response_model=list[LoanRead])
def list_loans(
    session: Annotated[Session, Depends(get_session)],
    is_open: Annotated[bool | None, Query(alias="open")] = None,
):
    statement = select(Loan).order_by(Loan.id)
    if is_open is True:
        statement = statement.where(Loan.returned_on.is_(None))
    elif is_open is False:
        statement = statement.where(Loan.returned_on.is_not(None))
    return session.scalars(statement).all()

   
    