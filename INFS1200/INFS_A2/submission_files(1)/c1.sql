CREATE TABLE LegacyEmployee (
    LegacyEmployeeID varchar(255),
    GrantAccessToken Binary(32),
    RoleID int NOT NULL,
    PRIMARY KEY (LegacyEmployeeID),
    FOREIGN KEY (LegacyEmployeeID) REFERENCES Employee(EmployeeID)
)
