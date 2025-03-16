CREATE TABLE product_staging_table (
    id INT AUTO_INCREMENT PRIMARY KEY,
    file_name VARCHAR(255),
    file_location VARCHAR(255),
    created_date TIMESTAMP ,
    updated_date TIMESTAMP ,
    status VARCHAR(1)
);


CREATE TABLE customer (
    customer_id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    address VARCHAR(255),
    pincode VARCHAR(10),
    phone_number VARCHAR(20),
    customer_joining_date DATE
);

-- Insert command for customer
INSERT INTO customer (first_name, last_name, address, pincode, phone_number, customer_joining_date) VALUES ('Saanvi', 'Krishna', 'Delhi', '122009', '9173121081', '2021-01-20');
INSERT INTO customer (first_name, last_name, address, pincode, phone_number, customer_joining_date) VALUES ('Dhanush', 'Sahni', 'Delhi', '122009', '9155328165', '2022-03-27');
INSERT INTO customer (first_name, last_name, address, pincode, phone_number, customer_joining_date) VALUES ('Yasmin', 'Shan', 'Delhi', '122009', '9191478300', '2023-04-08');
INSERT INTO customer (first_name, last_name, address, pincode, phone_number, customer_joining_date) VALUES ('Vidur', 'Mammen', 'Delhi', '122009', '9119017511', '2020-10-12');
INSERT INTO customer (first_name, last_name, address, pincode, phone_number, customer_joining_date) VALUES ('Shamik', 'Doctor', 'Delhi', '122009', '9105180499', '2022-10-30');
INSERT INTO customer (first_name, last_name, address, pincode, phone_number, customer_joining_date) VALUES ('Ryan', 'Dugar', 'Delhi', '122009', '9142616565', '2020-08-10');
INSERT INTO customer (first_name, last_name, address, pincode, phone_number, customer_joining_date) VALUES ('Romil', 'Shanker', 'Delhi', '122009', '9129451313', '2021-10-29');
INSERT INTO customer (first_name, last_name, address, pincode, phone_number, customer_joining_date) VALUES ('Krish', 'Tandon', 'Delhi', '122009', '9145683399', '2020-01-08');
INSERT INTO customer (first_name, last_name, address, pincode, phone_number, customer_joining_date) VALUES ('Divij', 'Garde', 'Delhi', '122009', '9141984713', '2020-11-10');
INSERT INTO customer (first_name, last_name, address, pincode, phone_number, customer_joining_date) VALUES ('Hunar', 'Tank', 'Delhi', '122009', '9169808085', '2023-01-27');
INSERT INTO customer (first_name, last_name, address, pincode, phone_number, customer_joining_date) VALUES ('Zara', 'Dhaliwal', 'Delhi', '122009', '9129776379', '2023-06-13');
INSERT INTO customer (first_name, last_name, address, pincode, phone_number, customer_joining_date) VALUES ('Sumer', 'Mangal', 'Delhi', '122009', '9138607933', '2020-05-01');
INSERT INTO customer (first_name, last_name, address, pincode, phone_number, customer_joining_date) VALUES ('Rhea', 'Chander', 'Delhi', '122009', '9103434731', '2023-08-09');
INSERT INTO customer (first_name, last_name, address, pincode, phone_number, customer_joining_date) VALUES ('Yuvaan', 'Bawa', 'Delhi', '122009', '9162077019', '2023-02-18');
INSERT INTO customer (first_name, last_name, address, pincode, phone_number, customer_joining_date) VALUES ('Sahil', 'Sabharwal', 'Delhi', '122009', '9174928780', '2021-03-16');
INSERT INTO customer (first_name, last_name, address, pincode, phone_number, customer_joining_date) VALUES ('Tiya', 'Kashyap', 'Delhi', '122009', '9105126094', '2023-03-23');
INSERT INTO customer (first_name, last_name, address, pincode, phone_number, customer_joining_date) VALUES ('Kimaya', 'Lala', 'Delhi', '122009', '9115616831', '2021-03-14');
INSERT INTO customer (first_name, last_name, address, pincode, phone_number, customer_joining_date) VALUES ('Vardaniya', 'Jani', 'Delhi', '122009', '9125068977', '2022-07-19');
INSERT INTO customer (first_name, last_name, address, pincode, phone_number, customer_joining_date) VALUES ('Indranil', 'Dutta', 'Delhi', '122009', '9120667755', '2023-07-18');
INSERT INTO customer (first_name, last_name, address, pincode, phone_number, customer_joining_date) VALUES ('Kavya', 'Sachar', 'Delhi', '122009', '9157628717', '2022-05-04');
INSERT INTO customer (first_name, last_name, address, pincode, phone_number, customer_joining_date) VALUES ('Manjari', 'Sule', 'Delhi', '122009', '9112525501', '2023-02-12');
INSERT INTO customer (first_name, last_name, address, pincode, phone_number, customer_joining_date) VALUES ('Akarsh', 'Kalla', 'Delhi', '122009', '9113226332', '2021-03-05');
INSERT INTO customer (first_name, last_name, address, pincode, phone_number, customer_joining_date) VALUES ('Miraya', 'Soman', 'Delhi', '122009', '9111455455', '2023-07-06');
INSERT INTO customer (first_name, last_name, address, pincode, phone_number, customer_joining_date) VALUES ('Shalv', 'Chaudhary', 'Delhi', '122009', '9158099495', '2021-03-14');
INSERT INTO customer (first_name, last_name, address, pincode, phone_number, customer_joining_date) VALUES ('Jhanvi', 'Bava', 'Delhi', '122009', '9110074097', '2022-07-14');


--store table
CREATE TABLE store (
    id INT PRIMARY KEY,
    address VARCHAR(255),
    store_pincode VARCHAR(10),
    store_manager_name VARCHAR(100),
    store_opening_date DATE,
    reviews TEXT
);

--data of store table
INSERT INTO store (id, address, store_pincode, store_manager_name, store_opening_date, reviews)
VALUES
    (121,'Delhi', '122009', 'Vyom', '2022-01-15', 'Great store with a friendly staff.'),
    (122,'Delhi', '110011', 'Suresh', '2021-08-10', 'Excellent selection of products.'),
    (123,'Delhi', '201301', 'Vishal', '2023-01-20', 'Clean and organized store.'),
    (124,'Delhi', '400001', 'Rakesh', '2020-05-05', 'Good prices and helpful staff.');


-- product table
CREATE TABLE product (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255),
    current_price DECIMAL(10, 2),
    old_price DECIMAL(10, 2),
    created_date TIMESTAMP ,
    updated_date TIMESTAMP ,
    expiry_date DATE
);


--product table data
INSERT INTO product (name, current_price, old_price, created_date, updated_date, expiry_date)
VALUES
    ('quaker oats', 212, 212, '2022-05-15', NULL, '2025-01-01'),
    ('sugar', 50, 50, '2021-08-10', NULL, '2025-01-01'),
    ('maida', 20, 20, '2023-03-20', NULL, '2025-01-01'),
    ('besan', 52, 52, '2020-05-05', NULL, '2025-01-01'),
    ('refined oil', 110, 110, '2022-01-15', NULL, '2025-01-01'),
    ('clinic plus', 1.5, 1.5, '2021-09-25', NULL, '2025-01-01'),
    ('dantkanti', 100, 100, '2023-07-10', NULL, '2025-01-01'),
    ('nutrella', 40, 40, '2020-11-30', NULL, '2025-01-01');


--sales team table
CREATE TABLE sales_team (
    id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    manager_id INT,
    is_manager CHAR(1),
    address VARCHAR(255),
    pincode VARCHAR(10),
    joining_date DATE
);


--sales team data
INSERT INTO sales_team (first_name, last_name, manager_id, is_manager, address, pincode, joining_date)
VALUES
    ('Rahul', 'Verma', 10, 'N', 'Delhi', '122007', '2020-05-01'),
    ('Priya', 'Singh', 10, 'N', 'Delhi', '122007', '2020-05-01'),
    ('Amit', 'Sharma', 10, 'N', 'Delhi', '122007', '2020-05-01'),
    ('Sneha', 'Gupta', 10, 'N', 'Delhi', '122007', '2020-05-01'),
    ('Neha', 'Kumar', 10, 'N', 'Delhi', '122007', '2020-05-01'),
    ('Vijay', 'Yadav', 10, 'N', 'Delhi', '122007', '2020-05-01'),
    ('Anita', 'Malhotra', 10, 'N', 'Delhi', '122007', '2020-05-01'),
    ('Alok', 'Rajput', 10, 'N', 'Delhi', '122007', '2020-05-01'),
    ('Monica', 'Jain', 10, 'N', 'Delhi', '122007', '2020-05-01'),
    ('Rajesh', 'Gupta', 10, 'Y', 'Delhi', '122007', '2020-05-01');





--s3 bucket table
CREATE TABLE s3_bucket_info (
    id INT AUTO_INCREMENT PRIMARY KEY,
    bucket_name VARCHAR(255),
    file_location VARCHAR(255),
    created_date TIMESTAMP ,
    updated_date TIMESTAMP ,
    status VARCHAR(20)
);


--s3 bucket data
INSERT INTO s3_bucket_info (bucket_name, status, created_date, updated_date)
VALUES ('project-testing', 'active', NOW(), NOW());


-- Customers Data Mart
CREATE TABLE customers_data_mart (
    customer_id INT, -- Unique identifier for each customer
    full_name VARCHAR(100), -- Concatenated first and last name of the customer
    address VARCHAR(200), -- Full address of the customer
    phone_number VARCHAR(20), -- Contact phone number
    sales_date_month VARCHAR(7), -- Month of sales transactions in 'YYYY-MM' format
    total_sales DECIMAL(10, 2), -- Total sales made by the customer across all purchases
    customer_lifetime_value DECIMAL(10, 2), -- Total value of the customer to the business over their lifetime
    first_purchase_month VARCHAR(7), -- The month of the customer's first purchase
    last_purchase_month VARCHAR(7), -- The month of the customer's most recent purchase
    purchase_frequency INT, -- Total number of purchases made by the customer
    monetary_value DECIMAL(10, 2), -- Average amount spent per transaction by the customer
    avg_monthly_spending DECIMAL(10, 2), -- Average spending by the customer per month
    max_single_transaction DECIMAL(10, 2), -- The highest amount spent in a single transaction
    avg_time_between_purchases DECIMAL(10, 2), -- Average time (in days) between consecutive purchases
    inactive_status BOOLEAN DEFAULT FALSE, -- Indicates if the customer is inactive (TRUE = inactive)
    customer_segment VARCHAR(50) -- Segment or category the customer belongs to (e.g., Premium, Regular, etc.)
);

-- Sales Team Data Mart
CREATE TABLE sales_team_data_mart (
    store_id INT, -- Unique identifier for each store
    sales_person_id INT, -- Unique identifier for each salesperson
    full_name VARCHAR(255), -- Full name of the salesperson
    sales_month VARCHAR(10), -- Month of sales in 'YYYY-MM' format
    total_sales DECIMAL(10, 2), -- Total sales made by the salesperson during the month
    avg_sales_per_month DECIMAL(10, 2), -- Average monthly sales for the salesperson
    incentive DECIMAL(10, 2), -- Monetary incentive earned by the salesperson based on performance
    sales_growth_rate DECIMAL(10, 2), -- Growth rate of sales compared to the previous month (in percentage)
    top_performance_rank INT, -- Rank of the salesperson in the store based on total sales
    year_to_date_sales DECIMAL(10, 2), -- Cumulative sales made by the salesperson for the year
    month_over_month_variance DECIMAL(10, 2), -- Difference in total sales compared to the previous month
    first_sale_month VARCHAR(10), -- Month of the salesperson's first recorded sale
    last_sale_month VARCHAR(10), -- Month of the salesperson's most recent sale
    total_transactions INT, -- Total number of sales transactions handled by the salesperson
    avg_transaction_value DECIMAL(10, 2), -- Average value of each sales transaction
    max_single_transaction DECIMAL(10, 2), -- Highest value of a single transaction
    sales_contribution_percentage DECIMAL(10, 2) -- Percentage contribution of the salesperson's sales to the store's total sales
);
