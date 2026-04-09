-- Create departments table
CREATE TABLE IF NOT EXISTS departments (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL
);

-- Create classes table
CREATE TABLE IF NOT EXISTS classes (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    department_id INTEGER REFERENCES departments(id)
);

-- Create students table
CREATE TABLE IF NOT EXISTS students (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    reg_no VARCHAR(50) UNIQUE NOT NULL,
    class_id INTEGER REFERENCES classes(id)
);

-- Create units table
CREATE TABLE IF NOT EXISTS units (
    id SERIAL PRIMARY KEY,
    code VARCHAR(20) UNIQUE NOT NULL,
    title VARCHAR(200) NOT NULL
);

-- Create trainers table
CREATE TABLE IF NOT EXISTS trainers (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL, -- In production, use hashed passwords
    department_id INTEGER REFERENCES departments(id)
);

-- Create class_units table (Mapping units to classes with trainers)
CREATE TABLE IF NOT EXISTS class_units (
    id SERIAL PRIMARY KEY,
    class_id INTEGER REFERENCES classes(id),
    unit_id INTEGER REFERENCES units(id),
    trainer_id INTEGER REFERENCES trainers(id)
);

-- Create attendance table
CREATE TABLE IF NOT EXISTS attendance (
    id SERIAL PRIMARY KEY,
    student_id INTEGER REFERENCES students(id),
    unit_id INTEGER REFERENCES units(id),
    trainer_id INTEGER REFERENCES trainers(id),
    lesson VARCHAR(10) NOT NULL, -- L1, L2, L3, L4
    week INTEGER NOT NULL, -- 1-52
    date DATE NOT NULL,
    status VARCHAR(20) NOT NULL -- Present, Absent
);

-- Create admins table
CREATE TABLE IF NOT EXISTS admins (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL -- In production, use hashed passwords
);

-- Seed data
INSERT INTO departments (name) VALUES ('Electrical'), ('Mechanical'), ('Civil');

INSERT INTO classes (name, department_id) VALUES 
('ELECT-1', 1), 
('ELECT-2', 1), 
('MECH-1', 2);

INSERT INTO students (name, reg_no, class_id) VALUES 
('Alice Mwangi', 'E001', 1), 
('Brian Otieno', 'E002', 1), 
('Catherine Njoroge', 'E003', 2), 
('Daniel Kimani', 'M001', 3);

INSERT INTO units (code, title) VALUES 
('EE101', 'Circuit Theory'), 
('EE102', 'Digital Systems'), 
('ME101', 'Engineering Drawing');

INSERT INTO trainers (name, username, password, department_id) VALUES 
('John Trainer', 'john', 'john123', 1), 
('Mary Trainer', 'mary', 'mary123', 2);

INSERT INTO class_units (class_id, unit_id, trainer_id) VALUES 
(1, 1, 1), -- ELECT-1, EE101, John
(1, 2, 1), -- ELECT-1, EE102, John
(3, 3, 2); -- MECH-1, ME101, Mary

INSERT INTO admins (username, password) VALUES ('admin', 'admin123');
