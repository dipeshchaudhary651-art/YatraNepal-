# YatraNepal - Advanced Tourism Management System

A comprehensive tourism management system built with Python Flask, featuring modern UI/UX design, dual payment gateways, recommendation algorithms, and complete booking management.

## 🌟 Features

### User Features
- **User Authentication**: Secure login/signup with password validation and eye icon for password visibility
- **Hotel Booking**: Browse and book hotels with date validation
- **Tour Packages**: Explore and book tour packages with detailed information
- **Dual Payment Gateway**: Support for both NPR and USD with currency selection
- **Review System**: Rate and review hotels and tours
- **Personalized Recommendations**: AI-powered recommendation algorithm based on user preferences
- **Booking Management**: View and manage all bookings with status tracking
- **Contact System**: Send messages and inquiries

### Admin Features
- **Admin Dashboard**: Comprehensive overview with statistics and quick actions
- **Hotel Management**: Add, edit, and manage hotel listings
- **Tour Management**: Create and manage tour packages
- **Booking Management**: View and manage all user bookings
- **Contact Management**: Handle customer inquiries and messages

### Technical Features
- **Modern UI/UX**: Beautiful, responsive design with animations
- **Hero Section**: Animated destination photos on homepage
- **Date Validation**: Comprehensive booking date validation
- **Currency Support**: NPR and USD with real-time switching
- **Database Management**: SQLite database with SQLAlchemy ORM
- **Security**: Password hashing, form validation, and secure sessions

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd YatraNepal
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   Create a `.env` file in the root directory:
   ```env
   SECRET_KEY=your-secret-key-here
   STRIPE_SECRET_KEY=your-stripe-secret-key
   STRIPE_PUBLIC_KEY=your-stripe-public-key
   ```

5. **Run the application**
   ```bash
   python app.py
   ```

6. **Access the application**
   Open your browser and go to `http://localhost:5000`

## 📁 Project Structure

```
YatraNepal/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── README.md             # Project documentation
├── templates/            # HTML templates
│   ├── base.html         # Base template with navigation
│   ├── index.html        # Homepage with hero section
│   ├── login.html        # User login page
│   ├── register.html     # User registration page
│   ├── hotels.html       # Hotel listing page
│   ├── hotel_detail.html # Hotel detail page
│   ├── tours.html        # Tour listing page
│   ├── tour_detail.html  # Tour detail page
│   ├── booking.html      # Booking form
│   ├── payment.html      # Payment gateway
│   ├── my_bookings.html  # User bookings
│   ├── contact.html      # Contact page
│   ├── recommendations.html # Personalized recommendations
│   └── admin/            # Admin templates
│       ├── dashboard.html
│       ├── add_hotel.html
│       └── add_tour.html
└── yatra_nepal.db       # SQLite database (created automatically)
```

## 🎨 UI/UX Features

### Design Elements
- **Modern Color Scheme**: Primary orange (#ff6b35), secondary orange (#f7931e), accent yellow (#ffd23f)
- **Responsive Design**: Mobile-first approach with Bootstrap 5
- **Animations**: AOS (Animate On Scroll) library for smooth animations
- **Hero Section**: Animated destination photos with floating shapes
- **Interactive Elements**: Hover effects, transitions, and micro-interactions

### User Experience
- **Intuitive Navigation**: Clear navigation with breadcrumbs
- **Form Validation**: Real-time validation with helpful error messages
- **Loading States**: Visual feedback during form submissions
- **Currency Switching**: Seamless currency toggle between NPR and USD
- **Password Visibility**: Eye icon to show/hide passwords

## 💳 Payment Integration

### Supported Payment Methods
- **Stripe**: Credit/debit card payments
- **Cash on Arrival**: Local payment option

### Currency Support
- **NPR (Nepalese Rupee)**: Primary currency
- **USD (US Dollar)**: International currency
- **Real-time Switching**: Dynamic currency conversion

## 🤖 Recommendation Algorithm

The system uses a collaborative filtering approach:

1. **User Preference Analysis**: Analyzes user's previous bookings and reviews
2. **Similarity Matching**: Finds similar hotels/tours based on location, duration, and ratings
3. **Popularity Fallback**: Recommends popular items when no preferences exist
4. **Personalized Suggestions**: Tailored recommendations based on user behavior

## 🔧 Configuration

### Environment Variables
```env
SECRET_KEY=your-secret-key-here
STRIPE_SECRET_KEY=sk_test_your_stripe_secret_key
STRIPE_PUBLIC_KEY=pk_test_your_stripe_public_key
```

### Database Configuration
The application uses SQLite by default. To use other databases:
1. Update `SQLALCHEMY_DATABASE_URI` in `app.py`
2. Install appropriate database drivers

## 👥 Default Admin Account

After first run, a default admin account is created:
- **Username**: admin
- **Password**: admin123
- **Email**: admin@yatra.com

**Important**: Change the default password after first login!

## 🛠️ Customization

### Adding New Features
1. **New Models**: Add to `app.py` in the models section
2. **New Routes**: Add route functions in `app.py`
3. **New Templates**: Create HTML files in `templates/` directory
4. **Styling**: Modify CSS in `templates/base.html`

### Styling Customization
- **Colors**: Update CSS variables in `templates/base.html`
- **Fonts**: Change Google Fonts import
- **Animations**: Modify AOS settings

## 📱 Mobile Responsiveness

The application is fully responsive and optimized for:
- **Desktop**: Full-featured experience
- **Tablet**: Optimized layout for medium screens
- **Mobile**: Touch-friendly interface with simplified navigation

## 🔒 Security Features

- **Password Hashing**: bcrypt for secure password storage
- **Session Management**: Flask-Login for user sessions
- **Form Validation**: Server-side and client-side validation
- **CSRF Protection**: Built-in Flask-WTF protection
- **Input Sanitization**: Proper data sanitization and validation

## 🚀 Deployment

### Local Development
```bash
python app.py
```

### Production Deployment
1. **Set up a production server** (e.g., Ubuntu with Nginx)
2. **Install dependencies**: `pip install -r requirements.txt`
3. **Configure environment variables**
4. **Use Gunicorn**: `gunicorn -w 4 -b 0.0.0.0:8000 app:app`
5. **Set up reverse proxy** with Nginx

### Docker Deployment
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 📞 Support

For support and questions:
- **Email**: info@yatranepal.com
- **Phone**: +977-1-4444444
- **Address**: Thamel, Kathmandu, Nepal

## 🎯 Future Enhancements

- [ ] Multi-language support
- [ ] Advanced search and filtering
- [ ] Email notifications
- [ ] Mobile app development
- [ ] Integration with external booking systems
- [ ] Advanced analytics dashboard
- [ ] Social media integration
- [ ] Virtual tour experiences

---

**YatraNepal** - Discover the beauty of Nepal with our comprehensive tourism platform! 🏔️✨ 