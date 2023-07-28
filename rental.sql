DROP SCHEMA IF EXISTS rental;
CREATE schema rental;
USE rental;

CREATE TABLE IF NOT EXISTS users
(
UserName VARCHAR(50) NOT NULL,
Password VARCHAR(20) NOT NULL,
Role INT NOT NULL,
PRIMARY KEY (UserName)
);

CREATE TABLE IF NOT EXISTS customer
(
CustomerID INT auto_increment NOT NULL,
CustomerName VARCHAR(80) NOT NULL,
Address VARCHAR(80) NOT NULL,
Email VARCHAR(80) NOT NULL,
PhoneNumber VARCHAR(20),
UserName VARCHAR(50) NOT NULL,
PRIMARY KEY (CustomerID),
FOREIGN KEY (UserName) REFERENCES users(UserName)
);

CREATE TABLE IF NOT EXISTS staff
(
StaffID INT auto_increment NOT NULL,
StaffName VARCHAR(80) NOT NULL,
Address VARCHAR(80) NOT NULL,
Email VARCHAR(80) NOT NULL,
PhoneNumber VARCHAR(20),
UserName VARCHAR(50) NOT NULL,
PRIMARY KEY (StaffID),
FOREIGN KEY (UserName) REFERENCES users(UserName)
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
);


INSERT INTO users VALUES 
("customer1","customer1",1),
("customer2","customer2",1),
("customer3","customer3",1),
("customer4","customer4",1),
("customer5","customer5",1),
("admin","admin",2),
("staff1","staff1",3),
("staff2","staff2",3),
("staff3","staff3",3);

INSERT INTO customer VALUES 
(000001,"customername1","auckland 1000","customer1@gmail.com","02100001","customer1"),
(00002,"customername2","auckland bilingol street","customer2@gmail.com","02200002","customer2"),
(00003,"customername3","auckland woolsworth street","customer3@gmail.com","02800003","customer3"),
(00004,"customername4","auckland kate street", "customer4@gmail.com","02100004","customer4"),
(00005,"customername5","auckland lake street", "customer5@gmail.com","02100005","customer5");

INSERT INTO staff VALUES 
(001,"staffname1","auckland bike street","staff1@gmail.com","02100221","staff1"),
(002,"staffname2","auckland desk street","staff2@gmail.com","02100222","staff2"),
(003,"staffname3","auckland window street","staff3@gmail.com","02100223","staff3");

INSERT INTO car VALUES
(00001,"Toyota Estima",2003,"WSJ788",8,300.5,NULL),
(00002,"Toyota IST",2004,"JWS416",5,30.7,NULL),
(00003,"Honda Fit",2008,"YANG",5,31.4,000001),
(00004,"Toyota Estima",2003,"WSJ788",8,300.5,NULL),
(00005,"Toyota IST",2004,"JWS416",5,30.7,NULL),
(00006,"Honda Fit",2008,"YANG",5,31.4,000001),
(00007,"Toyota Estima",2003,"WSJ788",8,300.5,NULL),
(00008,"Toyota IST",2004,"JWS416",5,30.7,NULL),
(00009,"Honda Fit",2008,"YANG",5,31.4,000001),
(00010,"Toyota Estima",2003,"WSJ788",8,300.5,NULL),
(00011,"Toyota IST",2004,"JWS416",5,30.7,000004),
(00012,"Honda Fit",2008,"YANG",5,31.4,000001),
(00013,"Toyota Estima",2003,"WSJ788",8,300.5,NULL),
(00014,"Toyota IST",2004,"JWS416",5,30.7,NULL),
(00015,"Honda Fit",2008,"YANG",5,31.4,000001),
(00016,"Toyota Estima",2003,"WSJ788",8,300.5,NULL),
(00017,"Toyota IST",2004,"JWS416",5,30.7,NULL),
(00018,"Honda Fit",2008,"YANG",5,31.4,000001),
(00019,"Toyota Estima",2003,"WSJ788",8,300.5,NULL),
(00020,"Toyota IST",2004,"JWS416",5,30.7,000005);
