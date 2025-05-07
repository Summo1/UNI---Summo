SELECT RoleID, COUNT(*) as NumberOfPermissions
FROM Permissions
GROUP BY RoleID
