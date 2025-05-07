SELECT WebsiteURI, COUNT(*) as NumberOfRoles
FROM Permissions
GROUP By WebsiteURI;
