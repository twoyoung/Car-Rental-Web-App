DROP SCHEMA IF EXISTS rental;
CREATE schema rental;
USE rental;

CREATE TABLE IF NOT EXISTS user
(
UserID INT auto_increment NOT NULL,
UserName VARCHAR(50) NOT NULL UNIQUE,
Password VARCHAR(100) NOT NULL,
Role INT,
PRIMARY KEY (UserID)
);

CREATE TABLE IF NOT EXISTS staff
(
UserID INT NOT NULL,
StaffID INT auto_increment NOT NULL,
Email VARCHAR(80) NOT NULL,
DisplayName VARCHAR(80),
Address VARCHAR(80),
PhoneNumber VARCHAR(20),
PRIMARY KEY (StaffID),
FOREIGN KEY (UserID) REFERENCES user(UserID)
ON DELETE CASCADE
ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS customer
(
UserID INT NOT NULL,
CustomerID INT auto_increment NOT NULL,
Email VARCHAR(80) NOT NULL,
DisplayName VARCHAR(80),
Address VARCHAR(80),
PhoneNumber VARCHAR(20),
PRIMARY KEY (CustomerID),
FOREIGN KEY (UserID) REFERENCES user(UserID)
ON DELETE CASCADE
ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS car
(
CarID INT auto_increment NOT NULL,
CarImage LONGBLOB,
CarModel VARCHAR(50) NOT NULL,
Year YEAR NOT NULL,
RegNumber VARCHAR(10) NOT NULL, 
SeatCap INT NOT NULL,
RentalPerDay DECIMAL(8,2) NOT NULL,
CustomerID INT,
PRIMARY KEY (CarID),
FOREIGN KEY (CustomerID) REFERENCES customer(CustomerID)
ON UPDATE CASCADE
ON DELETE SET NULL
);


INSERT INTO user VALUES 
(1,"admin","$2b$12$5IdI3BmxSLJu23bemyxhCe7CzIebQ2JR6FQQ89t0eG9bxibsfM0S6",1),
(2,"customer1","customer1",3),
(3,"staff1","staff1",2);

INSERT INTO staff VALUES
(3,1,"staff1@gmail.com","staffname1","auckland bike street","02100221");

INSERT INTO customer VALUES
(2,1,"customer1@gamil.com","customername1","auckland 1000","02100001");

INSERT INTO car VALUES
(1,LOAD_FILE('https://www.transfercar.co.nz/relocation/Christchurch_Airport/Auckland_Airport/509510.html
https://www.transfercar.co.nz/uploads/thumbs/vehicle_mobile_vertical_new/uploads/vehicles/5e289036e2665762f6d35e29dbcadbdf7483c849.jpg'),"Toyota Estima",2003,"WSJ788",8,300.5,NULL),
(2,LOAD_FILE('https://www.transfercar.co.nz/relocation/Christchurch_Airport/Auckland_Airport/509510.html
https://www.transfercar.co.nz/uploads/thumbs/vehicle_mobile_vertical_new/uploads/vehicles/5e289036e2665762f6d35e29dbcadbdf7483c849.jpg'),"Toyota IST",2004,"JWS416",5,30.7,NULL),
(3,LOAD_FILE('https://www.transfercar.co.nz/relocation/Christchurch_Airport/Auckland_Airport/509510.html
https://www.transfercar.co.nz/uploads/thumbs/vehicle_mobile_vertical_new/uploads/vehicles/5e289036e2665762f6d35e29dbcadbdf7483c849.jpg'),"Honda Fit",2008,"YANG",5,31.4,1),
(4,LOAD_FILE('https://www.transfercar.co.nz/relocation/Christchurch_Airport/Auckland_Airport/509510.html
https://www.transfercar.co.nz/uploads/thumbs/vehicle_mobile_vertical_new/uploads/vehicles/5e289036e2665762f6d35e29dbcadbdf7483c849.jpg'),"Toyota Estima",2003,"WSJ788",8,300.5,NULL);
