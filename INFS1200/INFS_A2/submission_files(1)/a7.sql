SELECT FirstName, LastName FROM Employee
Where EmployeeID IN(
    SELECT EmployeeID FROM RoleGranting WHERE RoleID IN(
        SELECT RoleID FROM RoleGranting WHERE EmployeeID = 'E0007')) and EmployeeID != 'E0007';