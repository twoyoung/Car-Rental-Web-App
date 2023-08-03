DROP SCHEMA IF EXISTS rental;
CREATE schema rental;
USE rental;

CREATE TABLE IF NOT EXISTS user
(
UserID INT auto_increment NOT NULL,
UserName VARCHAR(50) NOT NULL UNIQUE,
Password VARCHAR(255) NOT NULL,
Role INT,
PRIMARY KEY (UserID)
);

CREATE TABLE IF NOT EXISTS staff
(
UserID INT NOT NULL,
StaffID INT auto_increment NOT NULL,
Email VARCHAR(80) NOT NULL,
FirstName VARCHAR(50) NULL DEFAULT NULL,
LastName VARCHAR(50) NULL DEFAULT NULL,
PhoneNumber VARCHAR(25) NULL DEFAULT NULL,
Address LONGTEXT NULL DEFAULT NULL,
Suburb VARCHAR(50) NULL DEFAULT NULL,
City VARCHAR(50) NULL DEFAULT NULL,
State VARCHAR(50) NULL DEFAULT NULL,
Postcode VARCHAR(15) NULL DEFAULT NULL,
Country VARCHAR(50) NULL DEFAULT NULL,
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
FirstName VARCHAR(50) NULL DEFAULT NULL,
LastName VARCHAR(50) NULL DEFAULT NULL,
PhoneNumber VARCHAR(25) NULL DEFAULT NULL,
Address LONGTEXT NULL DEFAULT NULL,
Suburb VARCHAR(50) NULL DEFAULT NULL,
City VARCHAR(50) NULL DEFAULT NULL,
State VARCHAR(50) NULL DEFAULT NULL,
Postcode VARCHAR(15) NULL DEFAULT NULL,
Country VARCHAR(50) NULL DEFAULT NULL,
PRIMARY KEY (CustomerID),
FOREIGN KEY (UserID) REFERENCES user(UserID)
ON DELETE CASCADE
ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS car
(
CarID INT auto_increment NOT NULL,
CarImage VARCHAR(255) NULL DEFAULT NULL,
CarModel VARCHAR(50) NOT NULL,
Year YEAR NOT NULL,
RegNumber VARCHAR(10) NOT NULL, 
SeatCap INT NOT NULL,
RentalPerDay DECIMAL(8,2) NOT NULL,
CustomerID INT NULL DEFAULT NULL,
PRIMARY KEY (CarID),
FOREIGN KEY (CustomerID) REFERENCES customer(CustomerID)
ON UPDATE CASCADE
ON DELETE SET NULL
);


INSERT INTO user VALUES 
(1,'admin','$2b$12$5IdI3BmxSLJu23bemyxhCe7CzIebQ2JR6FQQ89t0eG9bxibsfM0S6',1),
(2,'staff1','$2b$12$IjfIZvwypg1iDIpVp7YSFO5ylzh6pehl2qP1oeHwix6QGkbHEd8OW',2),
(3,'staff2','$2b$12$5ZVlqF/05GGNFOvlHGcK9eJSHR/v0FLA0UtbkI.648.AyLcem1DWu',2),
(4,'staff3','$2b$12$nvfNV0nAR.0UXt6EMQH/gOegI2qTcaInyrY/b5zutvG3f6IURE5VS',2),
(5,'customer1','$2b$12$7AIp8bifi3F849jnPiIG4eoH2lbStfvRfUM0.I9Sy5j4mYDWuZZ4i',3),
(6,'customer2','$2b$12$NRURQ3DAFvfQeH7qTmov9ub1dHSm4dop1htnGFkOmVWS4.nD5Ab5O',3),
(7,'customer3','$2b$12$5BUG6ybtdMBb7F.PrIHVCe8Njx5LaCB3blH.xT99Rqb1YFsiBw/OK',3),
(8,'customer4','$2b$12$ytqvRJ/Cq2xu21xYw6OhUu0N7T5me8626CrGuOcvjFvFhyqLbU2ZG',3),
(9,'customer5','$2b$12$hZdqPGFb.TmrE7WWY/AUZuKuJvT9HUUWaOQ78.K4mFRngxrQ3A63a',3);


INSERT INTO staff VALUES
(2,1,'staff1@gmail.com','Bedecs','Anna','(123)555-0100','123 1st Street','Avondale','Auckland',NULL,'1023','New Zealand'),
(3,2,'staff2@gmail.com','Axen','Thomas','(123)555-0100','123 11th Street','Papanui','Christchurch',NULL,'2024','New Zealand'),
(4,3,'staff3@gmail.com','Xie','Ming-Yang','(123)555-0100)','456 13th Street','Greenlane','Auckland',NULL,'1010','New Zealand');

INSERT INTO customer VALUES
(5,1,'customer1@gmail.com','O’Donnell','Martin','(123)555-0100','789 20th Street',NULL,'Las Vegas','NV','99999','USA'),
(6,2,'customer2@gmail.com','Bagel','Jean Philippe','(123)555-0100','456 16th Street',NULL,'Chicago', 'IL', '99999', 'USA'),
(7,3,'customer3@gmail.com','Andersen', 'Elizabeth','(123)555-0100','456 16th Street',NULL,'Memphis', 'TN', '99999', 'USA'),
(8,4,'customer4@gmail.com','Wacker', 'Roland','(123)555-0100','456 16th Street',NULL,'New York', 'NY', '99999', 'USA'),
(9,5,'customer5@gmail.com','Grilo', 'Carlos','(123)555-0100','456 16th Street',NULL,'Salt Lake City', 'UT', '99999', 'USA');

INSERT INTO car VALUES
(1,'img1.jpg','Toyota Estima',2003,'WSJ788',8,60.5,1),
(2,'img2.jpg','Subaru Legacy',2004,'JWS416',5,30.7,NULL),
(3,'img3.jpg','Honda Fit',2008,'NAJ399',5,31.4,NULL),
(4,'img4.jpg','Toyota Estima',2003,'WSJ788',8,80.5,NULL),
(5,'img5.jpg','Ford Ranger',2009,'GDD842',5,50.5,NULL),
(6,'img6.jpg','Toyota Aqua',2013,'PTJ520',7,70.8,NULL),
(7,'img7.jpg','Suzuki Swift',2010,'ADF911',5,50.3,NULL),
(8,'img8.jpg','Nissan Note',2014,'GHI135',5,40,NULL),
(9,'img9.jpg','Nissan Serena',2013,'DEF246',8,28.9,2),
(10,'img10.jpg','Nissan NV350',2019,'PQR789',10,58.3,NULL),
(11,'img11.jpg','Toyota Hiace',2008,'UVW456',14,45.6,NULL),
(12,'img12.jpg','Mazda Demio',2012,'MNO321',5,27.4,NULL),
(13,'img13.jpg','Toyota Camry',2006,'JKL654',5,63.3,5),
(14,'img14.jpg','Nissan NV350',2017,'QWE987',7,25.6,NULL),
(15,'img15.jpg','Toyota Yaris',2019,'FCT456',5,75.7,NULL),
(16,'img16.jpg','Toyota Aqua',2015,'RST802',5,78.6,NULL),
(17,'img17.jpg','Toyota Prius',2014,'LMN618',5,84.5,NULL),
(18,'img18.jpg','Nissan Note',2016,'YZX333',5,37.7,NULL),
(19,'img19.jpg','Toyota Wish',2012,'NOP999',7,74.5,NULL),
(20,'img20.jpg','Toyota RAV4',2011,'HIJ777',6,57.4,NULL);
