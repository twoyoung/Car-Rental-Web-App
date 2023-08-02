DROP SCHEMA IF EXISTS rental;
CREATE schema rental;
USE rental;

CREATE TABLE IF NOT EXISTS user
(
UserName VARCHAR(50) NOT NULL,
Password VARCHAR(100) NOT NULL,
Role INT ,
PRIMARY KEY (UserName)
);

CREATE TABLE IF NOT EXISTS staff
(
StaffID INT auto_increment NOT NULL,
UserName VARCHAR(50) NOT NULL,
Email VARCHAR(80) NOT NULL,
DisplayName VARCHAR(80),
Address VARCHAR(80),
PhoneNumber VARCHAR(20),
PRIMARY KEY (StaffID),
FOREIGN KEY (UserName) REFERENCES user(UserName)
ON DELETE CASCADE
ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS customer
(
CustomerID INT auto_increment NOT NULL,
UserName VARCHAR(50) NOT NULL,
Email VARCHAR(80) NOT NULL,
DisplayName VARCHAR(80),
Address VARCHAR(80),
PhoneNumber VARCHAR(20),
PRIMARY KEY (CustomerID),
FOREIGN KEY (UserName) REFERENCES user(UserName)
ON DELETE CASCADE
ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS car
(
CarID INT auto_increment NOT NULL,
CarModel VARCHAR(50) NOT NULL,
Year INT NOT NULL,
RegNumber VARCHAR(10) NOT NULL, 
SeatCap INT NOT NULL,
RentalPerDay float NOT NULL,
CustomerID INT,
PRIMARY KEY (CarID),
FOREIGN KEY (CustomerID) REFERENCES customer(CustomerID)
ON UPDATE CASCADE
ON DELETE SET NULL
);


INSERT INTO user VALUES 
("admin","$2b$12$5IdI3BmxSLJu23bemyxhCe7CzIebQ2JR6FQQ89t0eG9bxibsfM0S6",1),
("customer1","customer1",3),
("staff1","staff1",2);

INSERT INTO staff VALUES
(1,"staff1","staff1@gmail.com","staffname1","auckland bike street","02100221");

INSERT INTO customer VALUES
(1,"customer1","customer1@gamil.com","customername1","auckland 1000","02100001");

INSERT INTO car VALUES
(1,"Toyota Estima",2003,"WSJ788",8,300.5,NULL),
(2,"Toyota IST",2004,"JWS416",5,30.7,NULL),
(3,"Honda Fit",2008,"YANG",5,31.4,1),
(4,"Toyota Estima",2003,"WSJ788",8,300.5,NULL);

SELECT LPAD(StaffID, 6, '0') AS StaffID FROM staff;
SELECT LPAD(CustomerID, 6, '0') AS CustomerID FROM customer;
SELECT LPAD(CarID, 6, '0') AS CarID FROM car;
