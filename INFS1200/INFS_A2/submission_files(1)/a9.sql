SELECT EmployeeID, FirstName, LastName From Employee
WHERE EmployeeID IN (SELECT EmployeeID FROM AdministrativeEmployee WHERE Type = 'LegacyEngineer'

UNION

SELECT EmployeeID FROM RoleGranting WHERE RoleID = '1'

UNION

SELECT EmployeeID FROM RoleGranting WHERE RoleID IN (SELECT RoleID FROM Permission WHERE WebsiteURI = 'https://besttechltd/financialperformance.tech'))
