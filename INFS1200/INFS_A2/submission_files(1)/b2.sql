INSERT INTO Employee (EmployeeID, FirstName, LastName, DOB, PasswordHash, PasswordSalt)
VALUES ('E0024', 'James', 'Moran', '2001-11-21', 'e7cf3ef8d8aac2c1c93963e7a58b7b62ade24d0d0ba2c8ae0f7fb6c8b0aa0332', 'D;%yL9TS:5PalS/d');


INSERT INTO RoleGranting (EmployeeID, RoleID, AdministrationID, Timestamp)
SELECT 'E0024', RoleID , 'E0001', '2025-05-08 09:00:00'
From RoleGranting WHERE EmployeeID = 'E0005';
