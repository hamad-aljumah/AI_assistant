-- Create sales table
CREATE TABLE IF NOT EXISTS sales (
    id SERIAL PRIMARY KEY,
    date DATE NOT NULL,
    branch VARCHAR(50),
    customer_type VARCHAR(50),
    gender VARCHAR(20),
    product_line VARCHAR(100),
    unit_price DECIMAL(10, 2),
    quantity INTEGER,
    payment VARCHAR(50),
    rating DECIMAL(3, 1),
    total DECIMAL(10, 2),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Insert sample data
INSERT INTO sales (date, branch, customer_type, gender, product_line, unit_price, quantity, payment, rating, total) VALUES
('2024-01-15', 'A', 'Member', 'Female', 'Electronics', 299.99, 2, 'Credit card', 8.5, 599.98),
('2024-01-16', 'B', 'Normal', 'Male', 'Fashion', 49.99, 3, 'Cash', 7.2, 149.97),
('2024-01-17', 'A', 'Member', 'Female', 'Home & lifestyle', 89.99, 1, 'Ewallet', 9.1, 89.99),
('2024-01-18', 'C', 'Normal', 'Male', 'Electronics', 599.99, 1, 'Credit card', 8.8, 599.99),
('2024-01-19', 'B', 'Member', 'Female', 'Food & beverages', 15.99, 5, 'Cash', 6.5, 79.95),
('2024-01-20', 'A', 'Normal', 'Male', 'Sports & travel', 129.99, 2, 'Ewallet', 7.9, 259.98),
('2024-01-21', 'C', 'Member', 'Female', 'Health & beauty', 39.99, 4, 'Credit card', 8.2, 159.96),
('2024-01-22', 'B', 'Normal', 'Male', 'Electronics', 799.99, 1, 'Cash', 9.5, 799.99),
('2024-01-23', 'A', 'Member', 'Female', 'Fashion', 79.99, 2, 'Ewallet', 7.8, 159.98),
('2024-01-24', 'C', 'Normal', 'Male', 'Food & beverages', 25.99, 3, 'Credit card', 6.9, 77.97),
('2024-01-25', 'B', 'Member', 'Female', 'Home & lifestyle', 149.99, 1, 'Cash', 8.7, 149.99),
('2024-01-26', 'A', 'Normal', 'Male', 'Sports & travel', 199.99, 1, 'Ewallet', 8.1, 199.99),
('2024-01-27', 'C', 'Member', 'Female', 'Electronics', 399.99, 2, 'Credit card', 9.2, 799.98),
('2024-01-28', 'B', 'Normal', 'Male', 'Health & beauty', 29.99, 3, 'Cash', 7.5, 89.97),
('2024-01-29', 'A', 'Member', 'Female', 'Fashion', 59.99, 4, 'Ewallet', 8.4, 239.96),
('2024-01-30', 'C', 'Normal', 'Male', 'Food & beverages', 19.99, 6, 'Credit card', 7.1, 119.94),
('2024-02-01', 'B', 'Member', 'Female', 'Electronics', 499.99, 1, 'Cash', 9.0, 499.99),
('2024-02-02', 'A', 'Normal', 'Male', 'Home & lifestyle', 119.99, 2, 'Ewallet', 8.3, 239.98),
('2024-02-03', 'C', 'Member', 'Female', 'Sports & travel', 89.99, 3, 'Credit card', 7.7, 269.97),
('2024-02-04', 'B', 'Normal', 'Male', 'Fashion', 69.99, 2, 'Cash', 8.0, 139.98);

-- Create indexes for better query performance
CREATE INDEX idx_sales_date ON sales(date);
CREATE INDEX idx_sales_branch ON sales(branch);
CREATE INDEX idx_sales_product_line ON sales(product_line);
CREATE INDEX idx_sales_customer_type ON sales(customer_type);

-- Grant permissions
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO postgres;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO postgres;
