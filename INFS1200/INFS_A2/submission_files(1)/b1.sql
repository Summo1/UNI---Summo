DELETE FROM RoleGranting
WHERE 
EmployeeID IN (Select EmployeeID From Employee WHERE FirstName = 'John' and LastName ='Stevens')

and AdministrationID IN (Select EmployeeID From Employee WHERE FirstName = 'Mei' and LastName ='Chen')

and Timestamp LIKE '%2024-07-22%'