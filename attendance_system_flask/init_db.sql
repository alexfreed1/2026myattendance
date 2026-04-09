-- ============================================================
-- Run this entire script in the Supabase SQL Editor
-- ============================================================

-- Create admins table (not created by default)
CREATE TABLE IF NOT EXISTS admins (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Ensure trainers table has all needed columns
-- (already exists, just making sure password column is there)
ALTER TABLE trainers ADD COLUMN IF NOT EXISTS password VARCHAR(255) NOT NULL DEFAULT '';

-- ============================================================
-- Seed admins (password = admin123)
-- ============================================================
INSERT INTO admins (username, password)
VALUES ('admin', '$2b$12$Ft.yDpoALpZN00vh.SE9ZOSVSwMQxEhXrlQv5FLu7Uro9lvt6HClq')
ON CONFLICT (username) DO NOTHING;

-- ============================================================
-- Seed trainers (john / john123, mary / mary123)
-- ============================================================
INSERT INTO trainers (name, username, password, department_id)
SELECT 'John Trainer', 'john', '$2b$12$s92rG93.Vf/2h/Ma9T2HK.3ZV08r4phurE10QfKjVr1VQkQ1WPjFK',
       id FROM departments WHERE name = 'Electrical' LIMIT 1
ON CONFLICT (username) DO NOTHING;

INSERT INTO trainers (name, username, password, department_id)
SELECT 'Mary Trainer', 'mary', '$2b$12$Ga5HsQDJ8EqRAV34LZK2w.hP5VwS05JWZqTWBHYujh2nE5Tiijgg.',
       id FROM departments WHERE name = 'Mechanical' LIMIT 1
ON CONFLICT (username) DO NOTHING;

-- ============================================================
-- Seed students
-- ============================================================
INSERT INTO students (name, reg_no, class_id)
SELECT 'Alice Mwangi', 'E001', id FROM classes WHERE name = 'ELECT-1' LIMIT 1
ON CONFLICT (reg_no) DO NOTHING;

INSERT INTO students (name, reg_no, class_id)
SELECT 'Brian Otieno', 'E002', id FROM classes WHERE name = 'ELECT-1' LIMIT 1
ON CONFLICT (reg_no) DO NOTHING;

INSERT INTO students (name, reg_no, class_id)
SELECT 'Catherine Njoroge', 'E003', id FROM classes WHERE name = 'ELECT-2' LIMIT 1
ON CONFLICT (reg_no) DO NOTHING;

INSERT INTO students (name, reg_no, class_id)
SELECT 'Daniel Kimani', 'M001', id FROM classes WHERE name = 'MECH-1' LIMIT 1
ON CONFLICT (reg_no) DO NOTHING;

-- ============================================================
-- Seed class_units (assign units to classes with trainers)
-- ============================================================
INSERT INTO class_units (class_id, unit_id, trainer_id)
SELECT c.id, u.id, t.id
FROM classes c, units u, trainers t
WHERE c.name = 'ELECT-1' AND u.code = 'EE101' AND t.username = 'john'
AND NOT EXISTS (
    SELECT 1 FROM class_units WHERE class_id = c.id AND unit_id = u.id
);

INSERT INTO class_units (class_id, unit_id, trainer_id)
SELECT c.id, u.id, t.id
FROM classes c, units u, trainers t
WHERE c.name = 'ELECT-1' AND u.code = 'EE102' AND t.username = 'john'
AND NOT EXISTS (
    SELECT 1 FROM class_units WHERE class_id = c.id AND unit_id = u.id
);

INSERT INTO class_units (class_id, unit_id, trainer_id)
SELECT c.id, u.id, t.id
FROM classes c, units u, trainers t
WHERE c.name = 'MECH-1' AND u.code = 'ME101' AND t.username = 'mary'
AND NOT EXISTS (
    SELECT 1 FROM class_units WHERE class_id = c.id AND unit_id = u.id
);
