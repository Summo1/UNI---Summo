CREATE TABLE Credential(
    CredentialID varchar(255),
    EmployeeID varchar(255),
    PasswordSalt varchar(255),
    PasswordHash varchar(255),
    Timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (CredentialID),
    FOREIGN KEY (EmployeeID) REFERENCES Employee(EmployeeID)
);

INSERT INTO Credential (CredentialID, EmployeeID, PasswordSalt, PasswordHash)
SELECT CONCAT('C',EmployeeID), EmployeeID, PasswordSalt, PasswordHash FROM Employee;

ALTER TABLE Employee 
DROP COLUMN PasswordHash, 
DROP Column PasswordSalt;