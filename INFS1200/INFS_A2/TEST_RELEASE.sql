-- INFS1200 RELEASE SET

DROP DATABASE IF EXISTS INFS1200;
CREATE DATABASE INFS1200;
USE INFS1200;

-- Employee
CREATE TABLE Employee (
    EmployeeID VARCHAR(8) PRIMARY KEY,
    FirstName VARCHAR(120),
    LastName VARCHAR(120),
    DOB DATE NOT NULL,
    PasswordHash VARCHAR(128) NOT NULL,
    PasswordSalt VARCHAR(64) NOT NULL
);

-- AdministrativeEmployee
CREATE TABLE AdministrativeEmployee (
    EmployeeID VARCHAR(8) PRIMARY KEY,
    Level INT NOT NULL,
    Type ENUM(
    'ProductEngineer', 
    'DatabaseAdministrator', 
    'LegacyEngineer'
    ) NOT NULL,
    FOREIGN KEY (EmployeeID) 
        REFERENCES Employee(EmployeeID)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

-- Role
CREATE TABLE Role (
    RoleID INT PRIMARY KEY,
    Name VARCHAR(50) NOT NULL UNIQUE,
    Description TEXT
);

-- RoleGranting
CREATE TABLE RoleGranting (
    EmployeeID VARCHAR(8),
    RoleID INT,
    AdministrationID VARCHAR(8),
    Timestamp DATETIME,
    PRIMARY KEY (EmployeeID, RoleID),
    FOREIGN KEY (EmployeeID) REFERENCES Employee(EmployeeID)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    FOREIGN KEY (RoleID) REFERENCES Role(RoleID)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    FOREIGN KEY (AdministrationID) REFERENCES AdministrativeEmployee(EmployeeID)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

-- Permission
CREATE TABLE Permission (
    WebsiteURI VARCHAR(512),
    RoleID INT,
    GrantType ENUM('View', 'Edit'),
    Description TEXT,
    PRIMARY KEY (WebsiteURI, RoleID),
    FOREIGN KEY (RoleID) REFERENCES Role(RoleID)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);


INSERT INTO Employee (EmployeeID, FirstName, LastName, DOB, PasswordHash, PasswordSalt) VALUES
('E0001', 'Mehdi', 'Rahman', '1985-06-15', '3d6f0a5b31287f5b2b31d764a3e6b09a9c2bfa6e5d1e3455b7b1c8e10f9d7f1b', 'xYz89&@p'),
('E0002', 'Mei', 'Chen', '1990-08-20', 'a8b9c0d4e5f61718293ab2cd4ef5b61718293ab2cd4ef5b61718293ab2cd4ef5b', 'kLm34^7pQz'),
('E0003', 'Jeremy', 'Chen', '1988-03-10', 'b2cd4ef5b61718293ab2cd4ef5b61718293ab2cd4ef5b61718293ab2cd4ef5b9c', 'mNop8!@hG'),
('E0004', 'Fatima', NULL, '1995-11-25', 'c4e5f61718293ab2cd4ef5b61718293ab2cd4ef5b61718293ab2cd4ef5b617182', 'qRsT56%$w'),
('E0005', 'Sofia', 'Gonzalez', '1987-09-12', 'ed8cd892c82ebeb261f662663dcae5c22f1fca2c60c78f0dc9e0991795a6f9f9', '!%pgH51b!1'),
('E0006', 'John', 'Stevens', '1992-04-03', '41854b9416e7d992fcfa5f489ad5a5334eb4eda636cf0c4314835ee43c6cb574', 'LW8cUj33Qxw'),
('E0007', 'Elena', 'Popov', '1989-12-30', 'bc9256e23093d8f31e418931e3e68da5031bb3aac1c1ae8201d746f4aabb8513', '3b3SZgmAlp'),
('E0008', 'Omar', NULL, '1996-07-21', '2d03d5085f6b9c78a1625302a452cbfdc5a11f7b3cd7e267082b357fff50cc03', 'ibOWLl*u');


INSERT INTO AdministrativeEmployee (EmployeeID, Level, Type) VALUES
('E0001', 9, 'DatabaseAdministrator'),
('E0002', 7, 'ProductEngineer'),
('E0006', 10, 'LegacyEngineer');

INSERT INTO Role (RoleID, name, Description) VALUES
(1, 'DBA', 'Manages database structures and access control'),
(2, 'Developer', 'Responsible for writing, testing, and maintaining code for applications'),
(3, 'HR', 'Manages employee relations, recruitment, and organizational policies'),
(4, 'Finance', 'Handles financial planning, budgeting, and company expenditures'),
(5, 'FinancialPerformanceOverview', 'Handles High-level financial performance of BestTechLtd');

INSERT INTO RoleGranting (EmployeeID, RoleID, AdministrationID, Timestamp) VALUES
('E0001', 1, 'E0001', '2023-01-01 08:00:00'),
('E0002', 2, 'E0002', '2023-05-20 14:15:00'),
('E0002', 3, 'E0002', '2023-05-20 14:15:00'),
('E0002', 4, 'E0002', '2023-05-20 14:15:00'),
('E0003', 3, 'E0001', '2023-11-05 12:10:00'),
('E0004', 4, 'E0001', '2023-11-05 12:10:00'),
('E0005', 2, 'E0001', '2023-11-05 12:10:00'),
('E0006', 2, 'E0002', '2024-04-05 11:25:00'),
('E0006', 3, 'E0002', '2024-06-18 15:50:00'),
('E0006', 4, 'E0002', '2024-07-22 08:35:00'),
('E0007', 4, 'E0001', '2024-09-05 14:10:00'),
('E0008', 5, 'E0001', '2024-10-12 17:30:00');

INSERT INTO Permission (WebsiteURI, RoleID, GrantType, Description) VALUES
('https://workday.besttechltd.com', 3, 'Edit', 'Manage employee records and payroll processing'),
('https://hubspot.besttechltd.com', 3, 'Edit', 'Access recruitment and onboarding data'),
('https://bamboohr.besttechltd.com', 3, 'Edit', 'View HR analytics and reporting'),
('https://aurion.besttechltd.com', 4, 'Edit', 'Manage BestTechLtd finances, budgets, and reporting'),
('https://quickbooks.besttechltd.com', 4, 'Edit', 'View financial statements and invoices'),
('https://xero.besttechltd.com', 4, 'Edit', 'Process payroll and manage financial transactions'),
('https://datadog.besttechltd.com', 2, 'Edit', 'Monitor application performance and logs'),
('https://grafana.besttechltd.com', 2, 'Edit', 'Visualize metrics and system performance'),
('https://jenkins.besttechltd.com', 2, 'Edit', 'Manage CI/CD pipelines and automation'),
('https://github.besttechltd.com', 2, 'Edit', 'Access and modify source code repositories'),
('https://sonarqube.besttechltd.com', 2, 'Edit', 'Analyze code quality and security vulnerabilities'),
('https://workday.besttechltd.com', 1, 'Edit', 'Manage employee records and payroll processing'),
('https://hubspot.besttechltd.com', 1, 'Edit', 'Access recruitment and onboarding data'),
('https://bamboohr.besttechltd.com', 1, 'Edit', 'View HR analytics and reporting'),
('https://aurion.besttechltd.com', 1, 'Edit', 'Manage BestTechLtd finances, budgets, and reporting'),
('https://quickbooks.besttechltd.com', 1, 'Edit', 'View financial statements and invoices'),
('https://xero.besttechltd.com', 1, 'Edit', 'Process payroll and manage financial transactions'),
('https://datadog.besttechltd.com', 1, 'Edit', 'Monitor application performance and logs'),
('https://grafana.besttechltd.com', 1, 'Edit', 'Visualize metrics and system performance'),
('https://jenkins.besttechltd.com', 1, 'Edit', 'Manage CI/CD pipelines and automation'),
('https://github.besttechltd.com', 1, 'Edit', 'Access and modify source code repositories'),
('https://sonarqube.besttechltd.com', 1, 'Edit', 'Analyze code quality and security vulnerabilities'),
('https://besttechltd/financialperformance.tech', 5, 'Edit', 'Financial Performance of Best Tech Ltd');