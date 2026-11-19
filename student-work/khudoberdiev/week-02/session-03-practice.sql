
/*
Ran all exercises on postgres.new (browser), database: campus_practice.
Local PostgreSQL 17 is also installed and working (psql connects);
I used the browser to match the in-class setup.
*/


-- Exercise 1A: create tables
-- Ran on postgres.new (browser)
/*
CREATE TABLE table_name (
    column_name  type  rules,
    column_name  type  rules,
    column_name  type  rules
);
*/
CREATE TABLE events(
    id integer PRIMARY KEY,
    title text NOT NULL,
    event_on date NOT NULL
);

 CREATE TABLE students(
    id integer PRIMARY KEY,
    name text NOT NULL
 );

 CREATE TABLE registrations(
    id integer PRIMARY KEY,
    event_id integer NOT NULL REFERENCES events (id),
    student_id integer NOT NULL REFERENCES students (id),
    registered_on date NOT NULL,
    cancelled_on date
 );

 -- Exercise 1B: insert the starter rows
/*
INSERT INTO table_name (col1, col2, col3)
VALUES (value1, value2, value3);
*/

INSERT INTO events (id, title, event_on)
VALUES 
(1, 'Robotics Demo', DATE '2026-11-26'), 
(2, 'AI Study Jam', DATE '2026-11-27');

INSERT INTO students (id, name)
VALUES (11, 'Jin');

INSERT INTO registrations (id, event_id, student_id, registered_on, cancelled_on)
VALUES (101, 1, 11, DATE '2026-11-19', NULL);

-- Exercise 2: find records
/*

SELECT col1, col2          -- which columns (* = all)
FROM table_name            -- which table
WHERE condition            -- which rows (optional)
ORDER BY col ASC | DESC;   -- sort order (optional, ASC is default)

Conditions:
  col = value          -- equal
  col <> value         -- not equal
  col > / < / >= / <=  -- comparisons
  col IS NULL          -- value is missing (never use = NULL)
  col IS NOT NULL      -- value exists
  cond1 AND cond2      -- both true
  cond1 OR cond2       -- either true

Order of clauses is fixed: SELECT -> FROM -> WHERE -> ORDER BY
*/
--1
SELECT id, title, event_on FROM events
ORDER BY title ASC;

--2
SELECT id, event_id, student_id, registered_on FROM registrations
WHERE cancelled_on IS NULL;


--3 inner selecting

SELECT id, name
FROM students
WHERE id = 11;


--better one (personallly liked)
SELECT id, name
FROM students
WHERE id IN (
    SELECT student_id
    FROM registrations
    WHERE cancelled_on IS NULL

);

--Exercise 3A: cancel registration 101.
/*
Syntax reference: changing data

UPDATE table_name
SET col1 = value1, col2 = value2   -- new values (comma between columns)
WHERE condition;                   -- which rows to change

*/

SELECT * FROM registrations
WHERE id = 101;

UPDATE registrations
SET cancelled_on = DATE '2026-11-20'
WHERE id = 101;
-- recheck active registrations: 0 rows
SELECT id, event_id, student_id, registered_on FROM registrations
WHERE cancelled_on IS NULL;


--3B
/*
INSERT INTO registrations (id, event_id, student_id, registered_on, cancelled_on)
VALUES (199, 99, 11, DATE '2026-11-22', NULL)
*/

/*
Error: insert or update on table "registrations" 
violates foreign key constraint "registrations_event_id_fkey"
*/

SELECT * FROM events
WHERE id = 99;


SELECT * FROM students
WHERE id = 11;

/*
Our INSERT ... call didn't work, we looked at the error, and worked on that error
, meaning check that event_id FK itself in orignal events table. And 
It turns out it doesn't exist in original table firstplace, which was the cause of the error

And we also checked for student_id FK in the same but it 
returned one row, meaning it really exists
*/

SELECT * FROM registrations
WHERE id = 199;


-- 3B: DELETE
/*
DELETE FROM table_name
WHERE condition;                   -- which rows to remove

 the parent rows must exist 
 before the registration that points to them in inserting to the joing table
*/

INSERT INTO registrations (id, event_id, student_id, registered_on, cancelled_on)
VALUES (102, 2, 11, DATE '2026-11-22', NULL);

SELECT * FROM registrations
WHERE id = 102;

DELETE FROM registrations
WHERE id = 102;

SELECT * FROM registrations
WHERE id = 102;
-- 0 rows after delete

SELECT * FROM registrations;