SELECT EmployeeID, FirstName, LastName From Employee
WHERE EmployeeID IN (SELECT EmployeeID FROM AdministrativeEmployee WHERE Type = 'LegacyEngineer')

OR EmployeeID IN

(SELECT EmployeeID FROM RoleGranting WHERE RoleID = '1')

OR EmployeeID IN

(SELECT EmployeeID FROM RoleGranting WHERE RoleID IN (SELECT RoleID FROM Permission WHERE WebsiteURI = 'https://besttechltd/financialperformance.tech'))
