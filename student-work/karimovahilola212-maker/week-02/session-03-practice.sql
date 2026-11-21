
-- Session 03 Practice: Campus Event Registration
-- Student: Hilola Karimova

-- 1. Create database
-- Run this separately if the database does not exist:
-- CREATE DATABASE campus_practice;

-- Connect to the database:
-- \connect campus_practice

-- 2. Create tables

CREATE TABLE events (
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    event_on DATE NOT NULL
);

CREATE TABLE students (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL
);

CREATE TABLE registrations (
    id INTEGER PRIMARY KEY,
    event_id INTEGER NOT NULL REFERENCES events(id),
    student_id INTEGER NOT NULL REFERENCES students(id),
    registered_on DATE NOT NULL,
    cancelled_on DATE
);

-- 3. Insert sample data

INSERT INTO events (id, title, event_on)
VALUES
(1, 'Robotics Demo', DATE '2026-11-26'),
(2, 'AI Study Jam', DATE '2026-11-27');

INSERT INTO students (id, name)
VALUES (11, 'Jin');

INSERT INTO registrations (
    id, event_id, student_id, registered_on, cancelled_on
)
VALUES (
    101, 1, 11, DATE '2026-11-19', NULL
);

-- 4. Exercise 2: SELECT queries

-- List events ordered by title
SELECT id, title, event_on
FROM events
ORDER BY title ASC;

-- Find active registrations
SELECT id, event_id, student_id, registered_on
FROM registrations
WHERE cancelled_on IS NULL;

-- Find student by ID
SELECT id, name
FROM students
WHERE id = 11;

-- 5. Exercise 3A: Cancel registration 101

UPDATE registrations
SET cancelled_on = DATE '2026-11-20'
WHERE id = 101;

-- Verify cancellation
SELECT *
FROM registrations
WHERE id = 101;

-- Check active registrations again
SELECT id, event_id, student_id, registered_on
FROM registrations
WHERE cancelled_on IS NULL;

-- 6. Exercise 3B: Test foreign key constraint

-- This INSERT should fail because event_id 99 does not exist.
-- Expected: foreign key constraint violation.
-- INSERT INTO registrations (
--     id, event_id, student_id, registered_on, cancelled_on
-- )
-- VALUES (
--     199, 99, 11, DATE '2026-11-22', NULL
-- );

-- Verify event 99 does not exist
SELECT *
FROM events
WHERE id = 99;

-- Verify student 11 exists
SELECT *
FROM students
WHERE id = 11;

-- Verify rejected registration was not inserted
SELECT *
FROM registrations
WHERE id = 199;

-- 7. Exercise 3C: Insert and delete practice registration

INSERT INTO registrations (
    id, event_id, student_id, registered_on, cancelled_on
)
VALUES (
    102, 2, 11, DATE '2026-11-22', NULL
);

-- Check registration 102
SELECT *
FROM registrations
WHERE id = 102;

-- Delete registration 102
DELETE FROM registrations
WHERE id = 102;

-- Verify deletion
SELECT *
FROM registrations
WHERE id = 102;

-- Final table
SELECT *
FROM registrations;


