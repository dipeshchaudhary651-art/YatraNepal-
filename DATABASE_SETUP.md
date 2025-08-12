# Database Setup Guide for YatraNepal

This guide will help you set up and connect the database to your YatraNepal tourism management system.

## Database Overview

The YatraNepal system uses SQLite as the database, which is perfect for development and small to medium-scale applications. The database includes the following tables:

1. **user** - User accounts and authentication
2. **hotel** - Hotel listings with pricing in NPR and USD
3. **tour_package** - Tour packages with pricing in NPR and USD
4. **booking** - User bookings for hotels and tours
5. **review** - User reviews and ratings
6. **contact** - Contact form submissions

## Setup Instructions

### Method 1: Using the Python Script (Recommended)

1. **Run the database initialization script:**
   ```bash
   python3 init_database.py
   ```

   This will:
   - Create the database file at `instance/yatra_nepal.db`
   - Create all necessary tables
   - Insert sample data (hotels and tour packages)
   - Create an admin user (username: `admin`, password: `admin123`)

### Method 2: Using SQL Commands

1. **Create the database file:**
   ```bash
   mkdir -p instance
   sqlite3 instance/yatra_nepal.db
   ```

2. **Run the SQL commands from `create_tables.sql`:**
   ```bash
   sqlite3 instance/yatra_nepal.db < create_tables.sql
   ```

### Method 3: Using Flask's Built-in Database Creation

1. **Run the Flask application:**
   ```bash
   python3 app.py
   ```

   The application will automatically create the database and tables when it starts for the first time.

## Database Connection

The database is already configured in your Flask application (`app.py`):

```python
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///yatra_nepal.db'
```

This configuration:
- Uses SQLite database
- Stores the database file in the `instance` folder
- Automatically creates the database if it doesn't exist

## Database Schema

### Users Table
```sql
CREATE TABLE user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(80) UNIQUE NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    password_hash VARCHAR(120) NOT NULL,
    is_admin BOOLEAN DEFAULT FALSE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

### Hotels Table
```sql
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
```

### Tour Packages Table
```sql
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
```

### Bookings Table
```sql
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
```

### Reviews Table
```sql
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
```

### Contact Table
```sql
CREATE TABLE contact (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(120) NOT NULL,
    subject VARCHAR(200) NOT NULL,
    message TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

## Sample Data

The initialization script includes sample data:

### Hotels
- Dwarika's Resort (Pokhara)
- Yak & Yeti Hotel (Kathmandu)
- Everest View Hotel (Namche Bazaar)
- Gokarna Forest Resort (Kathmandu)
- Fishtail Lodge (Pokhara)
- Aloft Kathmandu (Kathmandu)

### Tour Packages
- Everest Base Camp Trek (14 days)
- Annapurna Circuit Trek (21 days)
- Chitwan Safari (3 days)
- Pokhara Adventure (5 days)
- Kathmandu Valley Tour (4 days)
- Lumbini Pilgrimage (2 days)

## Admin Access

After setup, you can access the admin panel with:
- **Username:** admin
- **Password:** admin123
- **URL:** http://localhost:8000/admin

## Database Management

### View Database Contents
```bash
sqlite3 instance/yatra_nepal.db
.tables                    # List all tables
.schema user              # Show table schema
SELECT * FROM user;       # View all users
SELECT * FROM hotel;      # View all hotels
SELECT * FROM tour_package; # View all tour packages
.quit                     # Exit SQLite
```

### Backup Database
```bash
cp instance/yatra_nepal.db instance/yatra_nepal_backup.db
```

### Reset Database
```bash
rm instance/yatra_nepal.db
python3 init_database.py
```

## Troubleshooting

### Common Issues

1. **Database file not found:**
   - Ensure the `instance` directory exists
   - Run the initialization script again

2. **Permission errors:**
   - Check file permissions on the `instance` directory
   - Ensure write permissions for the current user

3. **SQLite not installed:**
   - On macOS: `brew install sqlite3`
   - On Ubuntu: `sudo apt-get install sqlite3`
   - On Windows: Download from sqlite.org

4. **Flask-SQLAlchemy errors:**
   - Ensure all required packages are installed: `pip install -r requirements.txt`

### Verification

To verify the database is working correctly:

1. **Start the application:**
   ```bash
   python3 app.py
   ```

2. **Visit the homepage:** http://localhost:8000

3. **Check if hotels and tours are displayed**

4. **Try registering a new user**

5. **Login with admin credentials and check the admin panel**

## Next Steps

Once the database is set up:

1. **Customize sample data** - Modify hotels and tour packages in the admin panel
2. **Add real images** - Replace placeholder image URLs with actual hotel/tour images
3. **Configure payment gateways** - Set up real Stripe, eSewa, and PayPal credentials
4. **Set up email notifications** - Configure email for booking confirmations
5. **Add more features** - Extend the system with additional functionality

## Security Notes

- Change the default admin password after first login
- Use environment variables for sensitive configuration
- Regularly backup the database
- Consider using a more robust database (PostgreSQL, MySQL) for production 