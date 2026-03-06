import sqlite3

conn = sqlite3.connect("college_attendance.db")
cur = conn.cursor()

# turn on foreign keys in SQLite
cur.execute("PRAGMA foreign_keys = ON;")

# ----------------------------
# DROP old tables if needed
# ----------------------------
cur.execute("DROP TABLE IF EXISTS attendance")
cur.execute("DROP TABLE IF EXISTS attendance_sessions")
cur.execute("DROP TABLE IF EXISTS class_subjects")
cur.execute("DROP TABLE IF EXISTS students")
cur.execute("DROP TABLE IF EXISTS subjects")
cur.execute("DROP TABLE IF EXISTS teachers")
cur.execute("DROP TABLE IF EXISTS classes")

# ----------------------------
# CREATE TABLES
# ----------------------------
cur.execute("""
CREATE TABLE classes (
    class_id INTEGER PRIMARY KEY AUTOINCREMENT,
    year_name TEXT NOT NULL,
    division TEXT NOT NULL,
    academic_year TEXT NOT NULL,
    UNIQUE(year_name, division, academic_year)
)
""")

cur.execute("""
CREATE TABLE students (
    student_id INTEGER PRIMARY KEY AUTOINCREMENT,
    roll_no TEXT NOT NULL UNIQUE,
    full_name TEXT NOT NULL,
    email TEXT,
    class_id INTEGER NOT NULL,
    FOREIGN KEY (class_id) REFERENCES classes(class_id)
)
""")

cur.execute("""
CREATE TABLE teachers (
    teacher_id INTEGER PRIMARY KEY AUTOINCREMENT,
    teacher_name TEXT NOT NULL,
    email TEXT
)
""")

cur.execute("""
CREATE TABLE subjects (
    subject_id INTEGER PRIMARY KEY AUTOINCREMENT,
    subject_code TEXT NOT NULL UNIQUE,
    subject_name TEXT NOT NULL
)
""")

cur.execute("""
CREATE TABLE class_subjects (
    class_subject_id INTEGER PRIMARY KEY AUTOINCREMENT,
    class_id INTEGER NOT NULL,
    subject_id INTEGER NOT NULL,
    teacher_id INTEGER NOT NULL,
    UNIQUE(class_id, subject_id),
    FOREIGN KEY (class_id) REFERENCES classes(class_id),
    FOREIGN KEY (subject_id) REFERENCES subjects(subject_id),
    FOREIGN KEY (teacher_id) REFERENCES teachers(teacher_id)
)
""")

cur.execute("""
CREATE TABLE attendance_sessions (
    session_id INTEGER PRIMARY KEY AUTOINCREMENT,
    class_subject_id INTEGER NOT NULL,
    session_date TEXT NOT NULL,
    start_time TEXT,
    FOREIGN KEY (class_subject_id) REFERENCES class_subjects(class_subject_id)
)
""")

cur.execute("""
CREATE TABLE attendance (
    session_id INTEGER NOT NULL,
    student_id INTEGER NOT NULL,
    status TEXT NOT NULL CHECK(status IN ('P','A')),
    PRIMARY KEY (session_id, student_id),
    FOREIGN KEY (session_id) REFERENCES attendance_sessions(session_id),
    FOREIGN KEY (student_id) REFERENCES students(student_id)
)
""")

# ----------------------------
# SEED DATA
# ----------------------------
cur.execute("""
INSERT INTO classes (year_name, division, academic_year)
VALUES ('SY', 'A', '2025-26')
""")

cur.executemany("""
INSERT INTO teachers (teacher_name, email)
VALUES (?, ?)
""", [
    ('Pooja Jadhav', 'pooja@college.com'),
    ('Prof. Meenakshi mam', 'ashwini@college.com'),
    ('Prof. Gavade Sir', 'c@college.com'),
    ('Prof. Ashwini Patil', 'd@college.com'),
    ('Prof.', 'e@college.com'),
    ('Prof.', 'f@college.com')
])

cur.executemany("""
INSERT INTO subjects (subject_code, subject_name)
VALUES (?, ?)
""", [
    ('101', 'DATABASE MANAGEMENT SYSTEM'),
    ('102', 'DATA SCIENCE'),
    ('103', 'PROBABILITY AND STATISTICS'),
    ('104', 'EMBEDDED SYSTEM'),
    ('105', 'PROJECT MANAGEMENT'),
    ('106', 'EVS')
])

cur.executemany("""
INSERT INTO class_subjects (class_id, subject_id, teacher_id)
VALUES (?, ?, ?)
""", [
    (1, 1, 1),
    (1, 2, 2),
    (1, 3, 3),
    (1, 4, 4),
    (1, 5, 5),
    (1, 6, 6)
])

cur.executemany("""
INSERT INTO students (roll_no, full_name, email, class_id)
VALUES (?, ?, ?, ?)
""", [
    ('2153', 'Student 01', 's2153@gmail.com', 1),
    ('2154', 'Student 02', 's2154@gmail.com', 1),
    ('2155', 'Student 03', 's2155@gmail.com', 1),
    ('2156', 'Student 04', 's2156@gmail.com', 1),
    ('2157', 'Student 05', 's2157@gmail.com', 1),
    ('2158', 'Student 06', 's2158@gmail.com', 1),
    ('2159', 'Student 07', 's2159@gmail.com', 1),
    ('2160', 'Student 08', 's2160@gmail.com', 1),
    ('2161', 'Student 09', 's2161@gmail.com', 1),
    ('2162', 'Student 10', 's2162@gmail.com', 1)
])

conn.commit()
conn.close()

print("SQLite database created successfully!")