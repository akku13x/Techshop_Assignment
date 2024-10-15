CREATE DATABASE TechShopDB;

USE TechShopDB;

CREATE TABLE Customers (
    CustomerID INT PRIMARY KEY IDENTITY(1,1),
    FirstName NVARCHAR(50) NOT NULL,
    LastName NVARCHAR(50) NOT NULL,
    Email NVARCHAR(100) NOT NULL UNIQUE,
    Phone NVARCHAR(15),
    Address NVARCHAR(255)
);

CREATE TABLE Products (
    ProductID INT PRIMARY KEY IDENTITY(1,1),
    ProductName NVARCHAR(100) NOT NULL,
    Description NVARCHAR(255),
    Price DECIMAL(10, 2) NOT NULL CHECK (Price >= 0)
);

CREATE TABLE Orders (
    OrderID INT PRIMARY KEY IDENTITY(1,1),
    CustomerID INT NOT NULL,
    OrderDate DATETIME DEFAULT GETDATE(),
    TotalAmount DECIMAL(10, 2) NOT NULL CHECK (TotalAmount >= 0),
    FOREIGN KEY (CustomerID) REFERENCES Customers(CustomerID)
);

CREATE TABLE OrderDetails (
    OrderDetailID INT PRIMARY KEY IDENTITY(1,1),
    OrderID INT NOT NULL,
    ProductID INT NOT NULL,
    Quantity INT NOT NULL CHECK (Quantity > 0),
    FOREIGN KEY (OrderID) REFERENCES Orders(OrderID),
    FOREIGN KEY (ProductID) REFERENCES Products(ProductID)
);

CREATE TABLE Inventory (
    InventoryID INT PRIMARY KEY IDENTITY(1,1),
    ProductID INT NOT NULL,
    QuantityInStock INT NOT NULL CHECK (QuantityInStock >= 0),
    LastStockUpdate DATETIME DEFAULT GETDATE(),
    FOREIGN KEY (ProductID) REFERENCES Products(ProductID)
);

CREATE TABLE Payments (
    PaymentID INT PRIMARY KEY IDENTITY(1,1),
    OrderID INT NOT NULL,
    PaymentMethod NVARCHAR(50) NOT NULL,
    Amount DECIMAL(10, 2) NOT NULL CHECK (Amount >= 0),
    PaymentDate DATETIME DEFAULT GETDATE(),
    FOREIGN KEY (OrderID) REFERENCES Orders(OrderID) ON DELETE CASCADE
);

select * from Customers;
select * from Products;
select * from Orders;
select * from OrderDetails;
select * from Inventory;
select * from Payments;

ALTER TABLE Orders
ADD Status VARCHAR(20) DEFAULT 'Pending';  -- Assuming a default status


SELECT COLUMN_NAME 
FROM INFORMATION_SCHEMA.COLUMNS 
WHERE TABLE_NAME = 'Products';


ALTER TABLE Products
ADD StockQuantity INT NOT NULL DEFAULT 0; 

-- This script will allow nulls in OrderDate and TotalAmount columns
-- It will NOT allow nulls in OrderID since it is a primary key

-- Modify the Orders table
ALTER TABLE Orders
ALTER COLUMN OrderDate DATETIME NULL;  -- Allow nulls in OrderDate
ALTER TABLE Orders
ALTER COLUMN TotalAmount DECIMAL(10, 2) NULL;  -- Allow nulls in TotalAmount

ALTER TABLE Orders
DROP CONSTRAINT <ConstraintName>;  -- Replace <ConstraintName> with the actual name of your check constraint

ALTER TABLE Orders
ADD CONSTRAINT CHK_TotalAmount CHECK (TotalAmount >= 0 OR TotalAmount IS NULL);

INSERT INTO products (ProductName, Description, Price, StockQuantity) 
VALUES 
('Apple iPhone 15', '256 GB, Midnight Black', 129999.00, 75),
('Sony Bravia TV', '65-inch, 4K UHD, Smart TV', 149999.00, 50),
('Dell XPS 13', '13-inch, 8 GB RAM, 512 GB SSD', 104999.00, 100),
('Samsung Galaxy Tab S7', '11-inch, 128 GB, Wi-Fi', 55999.00, 200),
('Bose QC35 II Headphones', 'Wireless Noise Cancelling', 29999.00, 150);

ALTER TABLE Products
ADD Category VARCHAR(50);

UPDATE Products SET Category = 'Electronics' WHERE ProductName IN ('HP Laptop', 'Apple iPhone 15', 'Sony Bravia TV', 'Dell XPS 13', 'Samsung Galaxy Tab S7');
UPDATE Products SET Category = 'Audio' WHERE ProductName IN( 'Headphones', 'Bose QC35 II Headphones');






