DROP SCHEMA IF EXISTS rental;
CREATE schema rental;
USE rental;

CREATE TABLE IF NOT EXISTS users
(
UserName VARCHAR(50) NOT NULL,
Password VARCHAR(20) NOT NULL,
Email VARCHAR(80) NOT NULL,
Role INT,
PRIMARY KEY (UserName)
);

CREATE TABLE IF NOT EXISTS accountprofile
(
UserID INT auto_increment NOT NULL,
UserName VARCHAR(50) NOT NULL,
ProfileName VARCHAR(80),
Address VARCHAR(80),
Email VARCHAR(80) NOT NULL,
PhoneNumber VARCHAR(20),
PRIMARY KEY (UserID),
FOREIGN KEY (UserName) REFERENCES users(UserName)
ON UPDATE CASCADE
ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS car
(
CarID INT auto_increment NOT NULL,
CarModel VARCHAR(50) NOT NULL,
Year INT NOT NULL,
RegNumber VARCHAR(10) NOT NULL, 
SeatCap INT NOT NULL,
RentalPerDay float NOT NULL,
UserID INT,
PRIMARY KEY (CarID),
FOREIGN KEY (UserID) REFERENCES accountprofile(UserID)
);


INSERT INTO users VALUES 
("customer1","customer1","customer1@gamil.com",NULL),
("customer2","customer2","customer2@gmail.com",NULL),
("customer3","customer3","customer3@gmail.com",NULL),
("customer4","customer4","customer4@gmail.com",NULL),
("customer5","customer5","customer5@gmail.com",NULL),
("admin","admin","admin@gmail.com",1),
("staff1","staff1","staff1@gmail.com",2),
("staff2","staff2","staff2@gmail.com",2),
("staff3","staff3","staff3@gmail.com",2);

INSERT INTO accountprofile VALUES 
(000001,"customer1","customername1","auckland 1000","customer1@gmail.com","02100001"),
(00002,"customer2","customername2","auckland bilingol street","customer2@gmail.com","02200002"),
(00003,"customer3","customername3","auckland woolsworth street","customer3@gmail.com","02800003"),
(00004,"customer4","customername4","auckland kate street", "customer4@gmail.com","02100004"),
(00005,"customer5","customername5","auckland lake street", "customer5@gmail.com","02100005"),
(006,"staff1","staffname1","auckland bike street","staff1@gmail.com","02100221"),
(007,"staff2","staffname2","auckland desk street","staff2@gmail.com","02100222"),
(008,"staff3","staffname3","auckland window street","staff3@gmail.com","02100223");

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
