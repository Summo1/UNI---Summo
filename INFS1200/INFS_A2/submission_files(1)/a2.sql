SELECT WebsiteURI, COUNT(*) as NumberOfRoles
FROM Permission
GROUP By WebsiteURI;
