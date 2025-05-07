SELECT RoleID, COUNT(*) as NumberOfPermissions
FROM Permission
GROUP BY RoleID
