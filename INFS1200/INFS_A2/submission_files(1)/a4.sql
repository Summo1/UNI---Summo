SELECT * FROM Role
WHERE RoleID IN(
SELECT RoleID FROM Permission WHERE WebsiteURI LIKE '%.com');

