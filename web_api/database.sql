CREATE DATABASE IF NOT EXISTS waste_sorting;
USE waste_sorting;

DROP TABLE IF EXISTS scan_records;

CREATE TABLE scan_records (
    scan_id INT AUTO_INCREMENT PRIMARY KEY,
    region_name VARCHAR(100) NOT NULL,
    category VARCHAR(20) NOT NULL,
    item_name VARCHAR(100) NOT NULL,
    scan_date DATE NOT NULL
);

INSERT INTO scan_records (region_name, category, item_name, scan_date) VALUES
    ('Dortmund', 'Recyclable', 'Plastic bottle', '2026-10-12'),
    ('Dortmund', 'Compostable', 'Banana peel', '2026-10-12'),
    ('Bochum', 'Landfill', 'Used tissue', '2026-10-11'),
    ('Bochum', 'Recyclable', 'Soda can', '2026-10-10'),
    ('Essen', 'Recyclable', 'Glass jar', '2026-10-09');
