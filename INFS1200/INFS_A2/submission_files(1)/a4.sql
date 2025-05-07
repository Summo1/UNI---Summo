SELECT * FROM Role
WHERE RoleID in(
SELECT RoleID FROM Permission WHERE WebsiteURI LIKE ‘%.com’);

