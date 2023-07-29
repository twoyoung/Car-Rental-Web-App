DROP SCHEMA IF EXISTS rental;
CREATE schema rental;
USE rental;

CREATE TABLE IF NOT EXISTS user
(
UserID INT auto_increment NOT NULL,
UserName VARCHAR(50) NOT NULL,
Password VARCHAR(100) NOT NULL,
Email VARCHAR(80) NOT NULL,
ProfileName VARCHAR(80),
Address VARCHAR(80),
PhoneNumber VARCHAR(20),
Role INT,
PRIMARY KEY (UserID)
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
FOREIGN KEY (UserID) REFERENCES user(UserID)
);

INSERT INTO user VALUES 
(1,"admin","admin","admin@gmail.com",NULL,NULL,NULL,1),
(2,"customer1","customer1","customer1@gamil.com","customername1","auckland 1000","02100001",NULL),
(3,"customer2","customer2","customer2@gmail.com","customername2","auckland bilingol street","02200002",NULL),
(4,"customer3","customer3","customer3@gmail.com","customername3","auckland woolsworth street","02800003",NULL),
(5,"customer4","customer4","customer4@gmail.com","customername4","auckland kate street","02100004",NULL),
(6,"customer5","customer5","customer5@gmail.com","customername5","auckland lake street","02100005",NULL),
(7,"staff1","staff1","staff1@gmail.com","staffname1","auckland bike street","02100221",2),
(8,"staff2","staff2","staff2@gmail.com","staffname2","auckland desk street","02100222",2),
(9,"staff3","staff2","staff3@gmail.com","staffname3","auckland window street","02100223",2);

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
