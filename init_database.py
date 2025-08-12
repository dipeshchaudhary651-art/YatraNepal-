#!/usr/bin/env python3
"""
Database Initialization Script for YatraNepal
This script creates all necessary tables and inserts sample data
"""

import sqlite3
import os
from werkzeug.security import generate_password_hash

def init_database():
    """Initialize the database with tables and sample data"""
    
    # Database file path
    db_path = 'instance/yatra_nepal.db'
    
    # Create instance directory if it doesn't exist
    os.makedirs('instance', exist_ok=True)
    
    # Connect to database (creates it if it doesn't exist)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    print("Creating database tables...")
    
    # Create Users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username VARCHAR(80) UNIQUE NOT NULL,
            email VARCHAR(120) UNIQUE NOT NULL,
            password_hash VARCHAR(120) NOT NULL,
            is_admin BOOLEAN DEFAULT FALSE,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create Hotels table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS hotel (
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
        )
    ''')
    
    # Create Tour Packages table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tour_package (
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
        )
    ''')
    
    # Create Bookings table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS booking (
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
        )
    ''')
    
    # Create Reviews table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS review (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            review_type VARCHAR(20) NOT NULL,
            item_id INTEGER NOT NULL,
            rating INTEGER NOT NULL,
            comment TEXT NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES user (id)
        )
    ''')
    
    # Create Contact table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS contact (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(100) NOT NULL,
            email VARCHAR(120) NOT NULL,
            subject VARCHAR(200) NOT NULL,
            message TEXT NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create indexes for better performance
    print("Creating indexes...")
    indexes = [
        'CREATE INDEX IF NOT EXISTS idx_user_username ON user(username)',
        'CREATE INDEX IF NOT EXISTS idx_user_email ON user(email)',
        'CREATE INDEX IF NOT EXISTS idx_booking_user_id ON booking(user_id)',
        'CREATE INDEX IF NOT EXISTS idx_booking_type ON booking(booking_type)',
        'CREATE INDEX IF NOT EXISTS idx_review_user_id ON review(user_id)',
        'CREATE INDEX IF NOT EXISTS idx_review_type ON review(review_type)',
        'CREATE INDEX IF NOT EXISTS idx_hotel_location ON hotel(location)',
        'CREATE INDEX IF NOT EXISTS idx_tour_duration ON tour_package(duration)'
    ]
    
    for index in indexes:
        cursor.execute(index)
    
    # Check if admin user exists
    cursor.execute('SELECT COUNT(*) FROM user WHERE username = ?', ('admin',))
    admin_exists = cursor.fetchone()[0] > 0
    
    if not admin_exists:
        print("Creating admin user...")
        admin_password_hash = generate_password_hash('admin123')
        cursor.execute('''
            INSERT INTO user (username, email, password_hash, is_admin) 
            VALUES (?, ?, ?, ?)
        ''', ('admin', 'admin@yatra.com', admin_password_hash, True))
    
    # Check if sample hotels exist
    cursor.execute('SELECT COUNT(*) FROM hotel')
    hotels_count = cursor.fetchone()[0]
    
    if hotels_count == 0:
        print("Inserting sample hotels...")
        hotels = [
            ('Dwarika\'s Resort', 'Luxury resort with mountain views', 'Pokhara', 15000, 150, 4.5, '/static/images/hotel1.jpg', 'WiFi, Pool, Spa, Restaurant'),
            ('Yak & Yeti Hotel', 'Historic hotel in city center', 'Kathmandu', 8000, 80, 4.2, '/static/images/hotel2.jpg', 'WiFi, Restaurant, Bar'),
            ('Everest View Hotel', 'Mountain view hotel', 'Namche Bazaar', 12000, 120, 4.8, '/static/images/hotel3.jpg', 'WiFi, Restaurant, Mountain View'),
            ('Gokarna Forest Resort', 'Forest resort with golf course', 'Kathmandu', 20000, 200, 4.6, '/static/images/hotel4.jpg', 'WiFi, Pool, Golf, Spa'),
            ('Fishtail Lodge', 'Lakeside resort', 'Pokhara', 18000, 180, 4.4, '/static/images/hotel5.jpg', 'WiFi, Pool, Restaurant, Lake View'),
            ('Aloft Kathmandu', 'Modern business hotel', 'Kathmandu', 10000, 100, 4.0, '/static/images/hotel6.jpg', 'WiFi, Gym, Restaurant, Business Center')
        ]
        
        cursor.executemany('''
            INSERT INTO hotel (name, description, location, price_nrp, price_usd, rating, image_url, amenities) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', hotels)
    
    # Check if sample tours exist
    cursor.execute('SELECT COUNT(*) FROM tour_package')
    tours_count = cursor.fetchone()[0]
    
    if tours_count == 0:
        print("Inserting sample tour packages...")
        tours = [
            ('Everest Base Camp Trek', 'Classic trek to Everest Base Camp', '14 days', 120000, 1200, 4.9, '/static/images/tour1.jpg', 'Lukla, Namche Bazaar, Everest Base Camp', 'Guide, Porter, Accommodation, Meals'),
            ('Annapurna Circuit Trek', 'Complete Annapurna circuit trek', '21 days', 180000, 1800, 4.7, '/static/images/tour2.jpg', 'Besisahar, Manang, Thorong La Pass', 'Guide, Porter, Accommodation, Meals'),
            ('Chitwan Safari', 'Wildlife safari in Chitwan National Park', '3 days', 25000, 250, 4.5, '/static/images/tour3.jpg', 'Chitwan National Park', 'Guide, Accommodation, Meals, Safari'),
            ('Pokhara Adventure', 'Adventure activities in Pokhara', '5 days', 35000, 350, 4.3, '/static/images/tour4.jpg', 'Pokhara, Sarangkot, Phewa Lake', 'Guide, Accommodation, Activities'),
            ('Kathmandu Valley Tour', 'Cultural tour of Kathmandu Valley', '4 days', 20000, 200, 4.4, '/static/images/tour5.jpg', 'Kathmandu, Patan, Bhaktapur', 'Guide, Transportation, Accommodation'),
            ('Lumbini Pilgrimage', 'Buddhist pilgrimage to Lumbini', '2 days', 15000, 150, 4.6, '/static/images/tour6.jpg', 'Lumbini, Maya Devi Temple', 'Guide, Transportation, Accommodation')
        ]
        
        cursor.executemany('''
            INSERT INTO tour_package (name, description, duration, price_nrp, price_usd, rating, image_url, destinations, included_services) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', tours)
    
    # Commit changes
    conn.commit()
    conn.close()
    
    print(f"Database initialized successfully at {db_path}")
    print("Admin credentials: username=admin, password=admin123")
    print("Sample hotels and tour packages have been added.")

if __name__ == '__main__':
    init_database() 