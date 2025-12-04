-- University Management System Database Schema
-- PostgreSQL Database Schema

-- Drop tables if they exist (for clean setup)
DROP TABLE IF EXISTS attendance CASCADE;
DROP TABLE IF EXISTS timetable CASCADE;
DROP TABLE IF EXISTS notifications CASCADE;
DROP TABLE IF EXISTS grades CASCADE;
DROP TABLE IF EXISTS student_courses CASCADE;
DROP TABLE IF EXISTS faculty_courses CASCADE;
DROP TABLE IF EXISTS courses CASCADE;
DROP TABLE IF EXISTS students CASCADE;
DROP TABLE IF EXISTS faculty CASCADE;
DROP TABLE IF EXISTS admin CASCADE;

-- Admin table
CREATE TABLE admin (
    user_id VARCHAR(50) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Faculty table
CREATE TABLE faculty (
    user_id VARCHAR(50) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Students table
CREATE TABLE students (
    user_id VARCHAR(50) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Courses table
CREATE TABLE courses (
    course_id VARCHAR(50) PRIMARY KEY,
    course_name VARCHAR(255) NOT NULL,
    credits INTEGER NOT NULL,
    prerequisites VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Course-Faculty relationship (many-to-many)
-- This stores which faculty are eligible/assigned to which courses
CREATE TABLE faculty_courses (
    faculty_id VARCHAR(50) REFERENCES faculty(user_id) ON DELETE CASCADE,
    course_id VARCHAR(50) REFERENCES courses(course_id) ON DELETE CASCADE,
    PRIMARY KEY (faculty_id, course_id)
);

-- Student-Course enrollment (many-to-many)
CREATE TABLE student_courses (
    student_id VARCHAR(50) REFERENCES students(user_id) ON DELETE CASCADE,
    course_id VARCHAR(50) REFERENCES courses(course_id) ON DELETE CASCADE,
    enrolled_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (student_id, course_id)
);

-- Grades table
CREATE TABLE grades (
    id SERIAL PRIMARY KEY,
    student_id VARCHAR(50) REFERENCES students(user_id) ON DELETE CASCADE,
    course_id VARCHAR(50) REFERENCES courses(course_id) ON DELETE CASCADE,
    grade VARCHAR(10) NOT NULL,
    semester VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(student_id, course_id)
);

-- Notifications table
CREATE TABLE notifications (
    id SERIAL PRIMARY KEY,
    sender VARCHAR(50),
    receiver VARCHAR(50) NOT NULL,  -- 'all' for broadcast or specific user_id
    message TEXT NOT NULL,
    date DATE DEFAULT CURRENT_DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Timetable table
CREATE TABLE timetable (
    id SERIAL PRIMARY KEY,
    course_id VARCHAR(50) REFERENCES courses(course_id) ON DELETE CASCADE,
    course_name VARCHAR(255),
    faculty_id VARCHAR(50) REFERENCES faculty(user_id) ON DELETE SET NULL,
    faculty_name VARCHAR(255),
    day VARCHAR(20) NOT NULL,
    slot VARCHAR(20) NOT NULL,
    room VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Attendance table
CREATE TABLE attendance (
    id SERIAL PRIMARY KEY,
    student_id VARCHAR(50) REFERENCES students(user_id) ON DELETE CASCADE,
    course_id VARCHAR(50) REFERENCES courses(course_id) ON DELETE CASCADE,
    faculty_id VARCHAR(50) REFERENCES faculty(user_id) ON DELETE SET NULL,
    date DATE NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'Present',  -- Present, Absent, Late, Excused
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(student_id, course_id, date)
);

-- Create indexes for better query performance
CREATE INDEX idx_student_courses_student ON student_courses(student_id);
CREATE INDEX idx_student_courses_course ON student_courses(course_id);
CREATE INDEX idx_faculty_courses_faculty ON faculty_courses(faculty_id);
CREATE INDEX idx_faculty_courses_course ON faculty_courses(course_id);
CREATE INDEX idx_grades_student ON grades(student_id);
CREATE INDEX idx_grades_course ON grades(course_id);
CREATE INDEX idx_notifications_receiver ON notifications(receiver);
CREATE INDEX idx_timetable_course ON timetable(course_id);
CREATE INDEX idx_timetable_faculty ON timetable(faculty_id);
CREATE INDEX idx_attendance_student ON attendance(student_id);
CREATE INDEX idx_attendance_course ON attendance(course_id);
CREATE INDEX idx_attendance_faculty ON attendance(faculty_id);
CREATE INDEX idx_attendance_date ON attendance(date);

