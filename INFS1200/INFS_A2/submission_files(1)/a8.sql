CREATE VIEW NumPermissionsGivenByRoles AS
SELECT RoleID, COUNT(*) as NumberOfPermissions
FROM Permission
GROUP BY RoleID;

CREATE VIEW RolesGivenByAdmin as
SELECT AdministrationID, RoleID, NumberOfPermissions
From RoleGranting
JOIN NumPermissionsGivenByRoles
USING (RoleID);


CREATE VIEW TOTALS AS
SELECT AdministrationID, SUM(NumberOfPermissions) as ROLESGRANTED
FROM RolesGivenByAdmin
GROUP BY AdministrationID;

SELECT AdministrationID FROM TOTALS
WHERE ROLESGRANTED IN (SELECT MAX(ROLESGRANTED) FROM TOTALS)