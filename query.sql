CREATE TABLE login (
    username TEXT,
    email TEXT,
    password TEXT
);
SELECT * From login
UPDATE login SET password = '123' WHERE username = 'Rohan';


CREATE TABLE passwords(
username TEXT,
email TEXT,
Website_name TEXT,
email2 TEXT,
password TEXT
)
SELECT * From passwords

DELETE FROM login WHERE email='hmanral265@gmail.com';