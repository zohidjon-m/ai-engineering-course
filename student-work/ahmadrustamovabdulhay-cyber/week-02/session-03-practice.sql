CREATE TABLE events (
    id integer PRIMARY KEY,
    title text NOT NULL,
    event_on date NOT NULL
);

INSERT INTO events (id, title, event_on)
VALUES
    (1, 'Robotics Demo', '2026-11-26'),
    (2, 'AI Study Jam', '2026-11-27');

CREATE TABLE students (
    id integer PRIMARY KEY,
    name text NOT NULL
);

INSERT INTO students (id, name)
VALUES (11, 'Jin');

CREATE TABLE registrations (
    id integer PRIMARY KEY,
    registered_on date NOT NULL,
    cancelled_on date,
    student_id integer REFERENCES students(id),
    event_id integer REFERENCES events(id)
);

INSERT INTO registrations (id, registered_on, cancelled_on, student_id, event_id)
VALUES (101, '2026-11-19', NULL, 11, 1);

INSERT INTO registrations (id, registered_on, cancelled_on, student_id, event_id)
VALUES (102, '2026-11-22', NULL, 11, 2);

SELECT *
FROM registrations
WHERE cancelled_on IS NULL;

SELECT *
FROM students
WHERE id = 11;

SELECT *
FROM registrations
WHERE id = 101;

SELECT *
FROM events
ORDER BY title;

SELECT *
FROM events
ORDER BY event_on DESC;

UPDATE registrations
SET cancelled_on = '2026-11-20'
WHERE id = 101;

SELECT *
FROM registrations
WHERE id = 199;

DELETE FROM registrations
WHERE id = 102;

SELECT *
FROM registrations
WHERE id = 101;

-- Rejected foreign-key test:
-- INSERT INTO registrations (id, registered_on, cancelled_on, event_id, student_id)
-- VALUES (199, '2026-11-22', NULL, 99, 11);
-- Error: Key (event_id)=(99) is not present in table "events".
-- Explanation: student 11 exists, but event 99 does not. The event_id foreign key rejected the insert.