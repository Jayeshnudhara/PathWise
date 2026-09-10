CREATE DATABASE pathwise;

USE pathwise;

CREATE TABLE students (
    student_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(150) UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE assessment_results (
    result_id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT,
    career VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (student_id)
        REFERENCES students(student_id)
        ON DELETE CASCADE
);

CREATE TABLE careers (
    career_id INT AUTO_INCREMENT PRIMARY KEY,
    career_name VARCHAR(100) NOT NULL,
    description TEXT
);

INSERT INTO careers (career_name, description)
VALUES
('AI/ML Engineer', 'Build artificial intelligence and machine learning systems.'),
('Full Stack Developer', 'Build complete web applications using frontend and backend technologies.'),
('Data Analyst', 'Analyze data and create insights to support decision making.'),
('Cloud Engineer', 'Design and manage cloud infrastructure and services.'),
('UI/UX Designer', 'Design user interfaces and user experiences for digital products.');
CREATE TABLE opportunities (
    opportunity_id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(150) NOT NULL,
    company VARCHAR(150) NOT NULL,
    opportunity_type VARCHAR(50),
    description TEXT,
    required_skills TEXT,
    location VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
INSERT INTO opportunities
(title, company, opportunity_type, description, required_skills, location)
VALUES
(
    'AI Intern',
    'TechNova',
    'Internship',
    'Work on beginner-level AI and machine learning projects.',
    'Python, Machine Learning, SQL',
    'Bangalore'
),
(
    'Frontend Developer Intern',
    'WebWorks',
    'Internship',
    'Build responsive web interfaces.',
    'HTML, CSS, JavaScript, React',
    'Bangalore'
),
(
    'Data Analyst Intern',
    'DataSphere',
    'Internship',
    'Analyze datasets and create useful business insights.',
    'Python, SQL, Excel',
    'Remote'
);