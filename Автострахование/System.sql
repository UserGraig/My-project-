CREATE TABLE Clients (
    client_id INT PRIMARY KEY,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    email VARCHAR(100),
    phone VARCHAR(20),
	password VARCHAR(20)
);

CREATE TABLE Cars (
    car_id INT PRIMARY KEY,
    make VARCHAR(50),
    model VARCHAR(50),
    year INT,
    vin VARCHAR(17),
    client_id INT,
    FOREIGN KEY (client_id) REFERENCES Clients(client_id)
);

CREATE TABLE Policies (
    policy_id INT PRIMARY KEY,
    policy_number VARCHAR(50),
    start_date DATE,
    end_date DATE,
    premium DECIMAL(10, 2),
    deductible DECIMAL(10, 2),
    car_id INT,
    FOREIGN KEY (car_id) REFERENCES Cars(car_id)
);

CREATE TABLE Requests (
    request_id INT PRIMARY KEY,
    client_id INT,
    type VARCHAR(70),
    description TEXT,
    status VARCHAR(50),
    FOREIGN KEY (client_id) REFERENCES Clients(client_id)
);

INSERT INTO Clients (client_id, first_name, last_name, email, phone, password)
VALUES 
    (1, 'Sergei', 'Petrov', 'sergei.petrov@email.ru', '+7 999 234 56 78', 1111),
    (2, 'Olga', 'Kuznetsova', 'olga.kuznetsova@email.ru', '+7 999 345 67 89', 2222),
    (3, 'Vladimir', 'Volkov', 'vladimir.volkov@email.ru', '+7 999 456 78 90', 3333),
    (4, 'Natalia', 'Sokolova', 'natalia.sokolova@email.ru', '+7 999 567 89 01', 4444),
    (5, 'Irina', 'Kovaleva', 'irina.kovaleva@email.ru', '+7 999 678 90 12', 5555)
	
    (7, 'Dmitri', 'Mikhailov', 'dmitri.mikhailov@email.ru', '+7 999 789 01 23',),
	(8, 'Alexei', 'Fedorov', 'alexei.fedorov@email.ru', '+7 999 890 12 34'),
    (9, 'Maria', 'Novikova', 'maria.novikova@email.ru', '+7 999 901 23 45'),
    (10, 'Andrei', 'Morozov', 'andrei.morozov@email.ru', '+7 999 012 34 56')
	
	
INSERT INTO Cars (car_id, make, model, year, vin, client_id)
VALUES 
    (1, 'Nissan', 'Sentra', 2021, '3N1AB8CV5MY298769', 1),
    (2, 'Hyundai', 'Elantra', 2020, '5NPD84LF6LH514229', 2),
    (3, 'Honda', 'Civic', 2022, '19XFC2F5XNE210643', 3),
    (4, 'Ford', 'Focus', 2019, '1FADP3K29JL278320', 4),
    (5, 'Volkswagen', 'Jetta', 2021, '3VWC57BU3MM024532', 5)
	
	
    (7, 'Chevrolet', 'Malibu', 2020, '1G1ZD5ST1LF034613', 7),
    (8, 'Kia', 'Optima', 2022, 'KNAGM4AD9N5071902', 8),
    (9, 'Mazda', 'Mazda3', 2021, '3MZBN1U73MM101476', 9),
    (10, 'Subaru', 'Impreza', 2020, '4S3GTAA68L3710717', 10),
    (11, 'Toyota', 'Camry', 2022, '4T1E31AK6NU017870', 2),
    (12, 'Nissan', 'Altima', 2021, '1N4BL4BV6MN312195', 3),
    (13, 'Honda', 'Accord', 2020, '1HGCV2F35LA005893', 4),
    (14, 'Ford', 'Fusion', 2019, '3FA6P0HD7KR192292', 5),
    (15, 'Volkswagen', 'Passat', 2021, '1VWAA7A37MC006805', 6)
    
	
INSERT INTO Policies (policy_id, policy_number, start_date, end_date, premium, deductible, car_id)
VALUES
	(1, 'POL20230523RU002', '2023-05-23', '2024-05-22', 1100.00, 500.00, 1),
	(2, 'POL20230523RU003', '2023-05-23', '2024-05-22', 1250.00, 500.00, 2),
	(3, 'POL20230523RU004', '2023-05-23', '2024-05-22', 1300.00, 500.00, 3),
	(4, 'POL20230523RU005', '2023-05-23', '2024-05-22', 1400.00, 500.00, 4),
	(5, 'POL20230523RU006', '2023-05-23', '2024-05-22', 1200.00, 500.00, 5)
	
	(7, 'POL20230523RU007', '2023-05-23', '2024-05-22', 1350.00, 500.00, 7),
	(8, 'POL20230523RU008', '2023-05-23', '2024-05-22', 1400.00, 500.00, 8),
	(9, 'POL20230523RU009', '2023-05-23', '2024-05-22', 1150.00, 500.00, 9),
	(10, 'POL20230523RU010', '2023-05-23', '2024-05-22', 1300.00, 500.00, 10),
	(12, 'POL20230523RU011', '2023-05-23', '2024-05-22', 1200.00, 500.00, 11),
	(13, 'POL20230523RU012', '2023-05-23', '2024-05-22', 1250.00, 500.00, 12),
	(14, 'POL20230523RU013', '2023-05-23', '2024-05-22', 1300.00, 500.00, 13),
	(15, 'POL20230523RU014', '2023-05-23', '2024-05-22', 1400.00, 500.00, 14)
	
	
SELECT * FROM clients;
SELECT * FROM cars;
SELECT * FROM policies;	
SELECT * FROM requests;


INSERT INTO [policies] (policy_id, first_name, last_name, email, phone)
VALUES 
    (8, NULL, NULL, NULL, NULL),
    (9, NULL, NULL, NULL, NULL),
    (10, NULL, NULL, NULL, NULL);
INSERT INTO Clients (client_id, first_name, last_name, email, phone)
VALUES 
    (11, NULL, NULL, NULL, NULL),
    (12, NULL, NULL, NULL, NULL),
    (13, NULL, NULL, NULL, NULL),
    (14, NULL, NULL, NULL, NULL)

	
	
	
INSERT INTO requests (request_id, client_id, type, description, status)
VALUES 
    (1, 1, NULL, NULL, NULL),
    (2, 2, NULL, NULL, NULL),
    (3, 3, NULL, NULL, NULL),
    (4, 4, NULL, NULL, NULL),
	(5, 5, NULL, NULL, NULL)


INSERT INTO Cars (car_id, make, model, year, vin, client_id)
VALUES 
    (1, NULL, NULL, NULL, NULL, NULL),
    (2, NULL, NULL, NULL, NULL, NULL),
    (3, NULL, NULL, NULL, NULL, NULL),
    (4, NULL, NULL, NULL, NULL, NULL),
    (5, NULL, NULL, NULL, NULL, NULL)

INSERT INTO Cars (car_id, make, model, year, vin, client_id)
VALUES 
    (12, NULL, NULL, NULL, NULL, NULL),
    (13, NULL, NULL, NULL, NULL, NULL),
    (14, NULL, NULL, NULL, NULL, NULL),
    (15, NULL, NULL, NULL, NULL, NULL)


DELETE FROM Cars
WHERE car_id BETWEEN 7 AND 11;

DELETE FROM clients
WHERE client_id BETWEEN 8 AND 29;

DELETE FROM requests
WHERE request_id BETWEEN 8 AND 29;


UPDATE Clients SET first_name='sergio' WHERE client_id=2;
DELETE FROM Clients WHERE last_name = 'petrov';

UPDATE Clients
SET email = 'newemail@gmail.com'
WHERE client_id = 1;

	
DROP TABLE Requests; 
DROP TABLE Clients;
DROP TABLE Policies;
DROP TABLE Cars;


-- Créer le rôle client_role
CREATE ROLE clients;

-- Accorder les privilèges SELECT sur la table Cars
GRANT SELECT ON Cars TO clients;

-- Accorder les privilèges SELECT sur la table Policies
GRANT SELECT ON Policies TO clients;

-- Accorder les privilèges INSERT, UPDATE et DELETE sur les tables Clients et Cars
GRANT INSERT, UPDATE, DELETE ON Policies TO clients;
GRANT INSERT, UPDATE, DELETE ON Cars TO clients;


-- Créer le rôle employee_role
CREATE ROLE staff;

-- Accorder les privilèges SELECT sur toutes les tables (Clients, Cars et Policies)
GRANT SELECT ON Clients, Cars, Policies TO staff;

-- Accorder les privilèges INSERT, UPDATE et DELETE sur toutes les tables (Clients, Cars et Policies)
GRANT INSERT, UPDATE, DELETE ON Clients, Cars, Policies TO staff;










--2  Подсчитать количество операций бронирования,
--в которых общая сумма превышает среднюю величину
--операций бронирования по всем пассажирам.

--2Compter le nombre d'opérations de réservation,
--dans lesquels le total est supérieur à la moyenne
--opérations de réservation pour tous les passagers.


2
SELECT COUNT(*) as num_bookings
FROM bookings
WHERE total_amount > (SELECT AVG(total_amount) FROM bookings);


--3  Выведите дату и счастливый час для бронирования билетов.
--Счастливый час – это такой час в которой было 
--забронировано более 300 билетов.

--3 Affichez la date et l'Happy hour pour la réservation de billets.
--Happy hour - c'est l'heure dans laquelle il y avait 
--plus de 300 billets ont été réservés.


3
SELECT DATE(booking_datetime) as booking_date, HOUR(booking_datetime) as booking_hour, COUNT(*) as num_bookings
FROM bookings
GROUP BY booking_date, booking_hour
HAVING num_bookings > 300;

 















