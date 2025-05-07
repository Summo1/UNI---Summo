Select * FROM Employee
WHERE EmployeeID IN(
SELECT EmployeeID FROM RoleGranting WHERE AdministrationID != “E0002”);
