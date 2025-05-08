ALTER TABLE AdministrativeEmployee
ADD CONSTRAINT AdministrationMax CHECK (Level <= 10)