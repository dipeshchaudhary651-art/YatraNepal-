-- YatraNepal Database Tables Creation
-- Run these commands to create all necessary tables

-- Users table
CREATE TABLE user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(80) UNIQUE NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    password_hash VARCHAR(120) NOT NULL,
    is_admin BOOLEAN DEFAULT FALSE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Hotels table
CREATE TABLE hotel (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) NOT NULL,
    description TEXT NOT NULL,
    location VARCHAR(100) NOT NULL,
    price_nrp FLOAT NOT NULL,
    price_usd FLOAT NOT NULL,
    rating FLOAT DEFAULT 0.0,
    image_url VARCHAR(200),
    amenities TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Tour Packages table
CREATE TABLE tour_package (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) NOT NULL,
    description TEXT NOT NULL,
    duration VARCHAR(50) NOT NULL,
    price_nrp FLOAT NOT NULL,
    price_usd FLOAT NOT NULL,
    rating FLOAT DEFAULT 0.0,
    image_url VARCHAR(200),
    destinations TEXT,
    included_services TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Bookings table
CREATE TABLE booking (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    booking_type VARCHAR(20) NOT NULL,
    item_id INTEGER NOT NULL,
    check_in_date DATE NOT NULL,
    check_out_date DATE NOT NULL,
    guests INTEGER DEFAULT 1,
    total_amount FLOAT NOT NULL,
    currency VARCHAR(3) DEFAULT 'NPR',
    payment_status VARCHAR(20) DEFAULT 'pending',
    booking_status VARCHAR(20) DEFAULT 'confirmed',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES user (id)
);

-- Reviews table
CREATE TABLE review (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    review_type VARCHAR(20) NOT NULL,
    item_id INTEGER NOT NULL,
    rating INTEGER NOT NULL,
    comment TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES user (id)
);

-- Contact messages table
CREATE TABLE contact (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(120) NOT NULL,
    subject VARCHAR(200) NOT NULL,
    message TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for better performance
CREATE INDEX idx_user_username ON user(username);
CREATE INDEX idx_user_email ON user(email);
CREATE INDEX idx_booking_user_id ON booking(user_id);
CREATE INDEX idx_booking_type ON booking(booking_type);
CREATE INDEX idx_review_user_id ON review(user_id);
CREATE INDEX idx_review_type ON review(review_type);
CREATE INDEX idx_hotel_location ON hotel(location);
CREATE INDEX idx_tour_duration ON tour_package(duration);

-- Insert sample data for testing

-- Insert admin user
INSERT INTO user (username, email, password_hash, is_admin) VALUES 
('admin', 'admin@yatra.com', 'pbkdf2:sha256:600000$your_hash_here', 1);

-- Insert sample hotels
-- INSERT INTO hotel (name, description, location, price_nrp, price_usd, rating, image_url, amenities) VALUES 
-- ('Dwarika''s Resort', 'Luxury resort with mountain views', 'Pokhara', 15000, 150, 4.5, '/static/images/hotel1.jpg', 'WiFi, Pool, Spa, Restaurant'),
-- ('Yak & Yeti Hotel', 'Historic hotel in city center', 'Kathmandu', 8000, 80, 4.2, '/static/images/hotel2.jpg', 'WiFi, Restaurant, Bar'),
-- ('Everest View Hotel', 'Mountain view hotel', 'Namche Bazaar', 12000, 120, 4.8, '/static/images/hotel3.jpg', 'WiFi, Restaurant, Mountain View'),
-- ('Gokarna Forest Resort', 'Forest resort with golf course', 'Kathmandu', 20000, 200, 4.6, '/static/images/hotel4.jpg', 'WiFi, Pool, Golf, Spa'),
-- ('Fishtail Lodge', 'Lakeside resort', 'Pokhara', 18000, 180, 4.4, '/static/images/hotel5.jpg', 'WiFi, Pool, Restaurant, Lake View'),
-- ('Aloft Kathmandu', 'Modern business hotel', 'Kathmandu', 10000, 100, 4.0, '/static/images/hotel6.jpg', 'WiFi, Gym, Restaurant, Business Center');

-- Insert sample tour packages
INSERT INTO tour_package (name, description, duration, price_nrp, price_usd, rating, image_url, destinations, included_services) VALUES 
('Everest Base Camp Trek', 'Classic trek to Everest Base Camp', '14 days', 120000, 1200, 4.9, '/static/images/tour1.jpg', 'Lukla, Namche Bazaar, Everest Base Camp', 'Guide, Porter, Accommodation, Meals'),
('Annapurna Circuit Trek', 'Complete Annapurna circuit trek', '21 days', 180000, 1800, 4.7, '/static/images/tour2.jpg', 'Besisahar, Manang, Thorong La Pass', 'Guide, Porter, Accommodation, Meals'),
('Chitwan Safari', 'Wildlife safari in Chitwan National Park', '3 days', 25000, 250, 4.5, '/static/images/tour3.jpg', 'Chitwan National Park', 'Guide, Accommodation, Meals, Safari'),
('Pokhara Adventure', 'Adventure activities in Pokhara', '5 days', 35000, 350, 4.3, '/static/images/tour4.jpg', 'Pokhara, Sarangkot, Phewa Lake', 'Guide, Accommodation, Activities'),
('Kathmandu Valley Tour', 'Cultural tour of Kathmandu Valley', '4 days', 20000, 200, 4.4, '/static/images/tour5.jpg', 'Kathmandu, Patan, Bhaktapur', 'Guide, Transportation, Accommodation'),
('Lumbini Pilgrimage', 'Buddhist pilgrimage to Lumbini', '2 days', 15000, 150, 4.6, '/static/images/tour6.jpg', 'Lumbini, Maya Devi Temple', 'Guide, Transportation, Accommodation'); 