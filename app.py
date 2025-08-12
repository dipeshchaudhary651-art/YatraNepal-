from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
from functools import wraps
from flask import abort
import os
from werkzeug.utils import secure_filename
import json
import bcrypt
from dotenv import load_dotenv


load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secret-key-here')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///yatra_nepal.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Payment configuration - Cash only

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Database Models
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    bookings = db.relationship('Booking', backref='user', lazy=True)
    reviews = db.relationship('Review', backref='user', lazy=True)

class Hotel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    location = db.Column(db.String(100), nullable=False)
    price_nrp = db.Column(db.Float, nullable=False)
    price_usd = db.Column(db.Float, nullable=False)
    rating = db.Column(db.Float, default=0.0)
    image_url = db.Column(db.String(200))
    amenities = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class TourPackage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    duration = db.Column(db.String(50), nullable=False)
    price_nrp = db.Column(db.Float, nullable=False)
    price_usd = db.Column(db.Float, nullable=False)
    rating = db.Column(db.Float, default=0.0)
    image_url = db.Column(db.String(200))
    destinations = db.Column(db.Text)
    included_services = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    booking_type = db.Column(db.String(20), nullable=False)  # 'hotel' or 'tour'
    item_id = db.Column(db.Integer, nullable=False)
    check_in_date = db.Column(db.Date, nullable=False)
    check_out_date = db.Column(db.Date, nullable=False)
    guests = db.Column(db.Integer, default=1)
    total_amount = db.Column(db.Float, nullable=False)
    currency = db.Column(db.String(3), default='NPR')
    payment_status = db.Column(db.String(20), default='pending')
    booking_status = db.Column(db.String(20), default='confirmed')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    review_type = db.Column(db.String(20), nullable=False)  # 'hotel' or 'tour'
    item_id = db.Column(db.Integer, nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    subject = db.Column(db.String(200), nullable=False)
    message = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

@app.context_processor
def inject_request():
    return dict(request=request)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_admin:
            flash("Access denied: Admins only!", "danger")
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function


# Routes
@app.route('/')
def index():
    hotels = Hotel.query.limit(6).all()
    tours = TourPackage.query.limit(6).all()
    return render_template('index.html', hotels=hotels, tours=tours)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        if User.query.filter_by(username=username).first():
            flash('Username already exists!', 'error')
            return redirect(url_for('register'))

        if User.query.filter_by(email=email).first():
            flash('Email already registered!', 'error')
            return redirect(url_for('register'))

        password_hash = generate_password_hash(password)
        user = User(
            username=username,
            email=email,
            password_hash=password_hash,
            is_admin=False  # ✅ Mark as normal user
        )
        db.session.add(user)
        db.session.commit()

        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            flash('Login successful!', 'success')
            
            # ✅ Redirect based on role
            if user.is_admin:
                return redirect(url_for('admin'))
            else:
                return redirect(url_for('index'))
        else:
            flash('Invalid username or password!', 'danger')
    
    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully!', 'success')
    return redirect(url_for('index'))

@app.route('/hotels')
@login_required
def hotels():
    if current_user.is_admin:
        flash('Admins cannot access user hotel listings.', 'warning')
        return redirect(url_for('admin'))
    hotels = Hotel.query.all()
    
    # Get user's existing bookings for hotels
    user_bookings = {}
    if current_user.is_authenticated:
        bookings = Booking.query.filter_by(user_id=current_user.id, booking_type='hotel').all()
        for booking in bookings:
            user_bookings[booking.item_id] = booking
    
    return render_template('hotels.html', hotels=hotels, user_bookings=user_bookings)



@app.route('/hotel/<int:hotel_id>')
@login_required
def hotel_detail(hotel_id):
    if current_user.is_admin:
        flash('Admins cannot access user hotel details.', 'warning')
        return redirect(url_for('admin'))
    hotel = Hotel.query.get_or_404(hotel_id)
    reviews = Review.query.filter_by(review_type='hotel', item_id=hotel_id).all()
    
    # Check if user has existing booking for this hotel
    existing_booking = None
    if current_user.is_authenticated:
        existing_booking = Booking.query.filter_by(
            user_id=current_user.id,
            booking_type='hotel',
            item_id=hotel_id
        ).first()
    
    return render_template('hotel_detail.html', hotel=hotel, reviews=reviews, existing_booking=existing_booking)

@app.route('/tours')
@login_required
def tours():
    if current_user.is_admin:
        flash('Admins cannot access user tour listings.', 'warning')
        return redirect(url_for('admin'))
    tours = TourPackage.query.all()
    
    # Get user's existing bookings for tours
    user_bookings = {}
    if current_user.is_authenticated:
        bookings = Booking.query.filter_by(user_id=current_user.id, booking_type='tour').all()
        for booking in bookings:
            user_bookings[booking.item_id] = booking
    
    return render_template('tours.html', tours=tours, user_bookings=user_bookings)

@app.route('/tour/<int:tour_id>')
@login_required
def tour_detail(tour_id):
    if current_user.is_admin:
        flash('Admins cannot access user tour details.', 'warning')
        return redirect(url_for('admin'))
    tour = TourPackage.query.get_or_404(tour_id)
    reviews = Review.query.filter_by(review_type='tour', item_id=tour_id).all()
    
    # Check if user has existing booking for this tour
    existing_booking = None
    if current_user.is_authenticated:
        existing_booking = Booking.query.filter_by(
            user_id=current_user.id,
            booking_type='tour',
            item_id=tour_id
        ).first()
    
    return render_template('tour_detail.html', tour=tour, reviews=reviews, existing_booking=existing_booking)

@app.route('/book/<string:type>/<int:item_id>', methods=['GET', 'POST'])
@login_required
def book(type, item_id):
    if current_user.is_admin:
        flash('Admins cannot make bookings.', 'warning')
        return redirect(url_for('admin'))

    item = Hotel.query.get_or_404(item_id) if type == 'hotel' else TourPackage.query.get_or_404(item_id)

    # Check if user already has an active booking for this item
    existing_booking = Booking.query.filter_by(
        user_id=current_user.id,
        booking_type=type,
        item_id=item_id,
        payment_status='completed'
    ).first()
    
    if existing_booking:
        flash(f'You already have an active booking for this {type}. Only one booking per {type} is allowed.', 'warning')
        return redirect(url_for('my_bookings'))

    if request.method == 'POST':
        check_in = datetime.strptime(request.form['check_in'], '%Y-%m-%d').date()
        check_out = datetime.strptime(request.form['check_out'], '%Y-%m-%d').date()
        guests = int(request.form['guests'])
        currency = request.form['currency']

        if check_in < datetime.now().date():
            flash('Check-in date cannot be in the past!', 'danger')
            return redirect(url_for('book', type=type, item_id=item_id))
        
        if check_out <= check_in:
            flash('Check-out date must be after check-in!', 'danger')
            return redirect(url_for('book', type=type, item_id=item_id))

        # Check if user already has a pending booking for this item
        pending_booking = Booking.query.filter_by(
            user_id=current_user.id,
            booking_type=type,
            item_id=item_id,
            payment_status='pending'
        ).first()
        
        if pending_booking:
            flash(f'You already have a pending booking for this {type}. Please complete your existing booking first.', 'warning')
            return redirect(url_for('my_bookings'))

        nights = (check_out - check_in).days
        if type == 'hotel':
            total_amount = (item.price_nrp if currency == 'NPR' else item.price_usd) * guests * nights
        else:
            total_amount = (item.price_nrp if currency == 'NPR' else item.price_usd) * guests
        
        booking = Booking(
            user_id=current_user.id,
            booking_type=type,
            item_id=item_id,
            check_in_date=check_in,
            check_out_date=check_out,
            guests=guests,
            total_amount=total_amount,
            currency=currency
        )
        db.session.add(booking)
        db.session.commit()

        session['booking_id'] = booking.id
        flash('Booking created! Proceed to payment.', 'success')
        return redirect(url_for('payment'))

    return render_template('booking.html', item=item, type=type, currencies=['NPR', 'USD'])

@app.route('/payment', methods=['GET', 'POST'])
@login_required
def payment():
    if current_user.is_admin:
        flash('Admins cannot make payments.', 'error')
        return redirect(url_for('admin'))

    booking_id = session.get('booking_id')
    if not booking_id:
        return redirect(url_for('index'))
    
    booking = Booking.query.get_or_404(booking_id)

    if request.method == 'POST':
        # Only allow cash payment
        payment_method = request.form['payment_method']
        if payment_method == 'cash':
            booking.payment_status = 'completed'
            db.session.commit()
            flash('Payment successful! Please pay cash on arrival.', 'success')
            return redirect(url_for('my_bookings'))
        else:
            flash('Invalid payment method. Only cash is accepted.', 'error')
            return redirect(url_for('payment'))

    return render_template('payment.html', booking=booking)
    
@app.route('/my_bookings')
@login_required
def my_bookings():
    if current_user.is_admin:
        flash('Admins cannot view user bookings.', 'warning')
        return redirect(url_for('admin'))
    bookings = Booking.query.filter_by(user_id=current_user.id).order_by(Booking.created_at.desc()).all()
    
    # Get hotel and tour data for each booking
    for booking in bookings:
        if booking.booking_type == 'hotel':
            booking.item_details = Hotel.query.get(booking.item_id)
        else:
            booking.item_details = TourPackage.query.get(booking.item_id)
    
    return render_template('my_bookings.html', bookings=bookings)

@app.route('/add_review', methods=['POST'])
@login_required
def add_review():
    if current_user.is_admin:
        flash('Admins cannot add reviews.', 'warning')
        return redirect(url_for('admin'))

    review_type = request.form['review_type']
    item_id = int(request.form['item_id'])
    rating = int(request.form['rating'])
    comment = request.form['comment']
    
    review = Review(
        user_id=current_user.id,
        review_type=review_type,
        item_id=item_id,
        rating=rating,
        comment=comment
    )
    db.session.add(review)
    db.session.commit()
    
    flash('Review added successfully!', 'success')
    return redirect(request.referrer)


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        subject = request.form['subject']
        message = request.form['message']
        
        contact = Contact(name=name, email=email, subject=subject, message=message)
        db.session.add(contact)
        db.session.commit()
        
        flash('Message sent successfully!', 'success')
        return redirect(url_for('contact'))
    
    return render_template('contact.html')

# Admin routes
@app.route('/dashboard_user')
@login_required
def dashboard_user():
    if current_user.is_admin:
        flash('Admins do not have a user dashboard.', 'warning')
        return redirect(url_for('admin'))
    return render_template('user/dashboard_user.html')  # Create this template

@app.route('/admin')
@login_required
@admin_required
def admin():
    hotels = Hotel.query.all()
    tours = TourPackage.query.all()
    bookings = Booking.query.all()
    contacts = Contact.query.all()
    return render_template('admin/dashboard.html', hotels=hotels, tours=tours, bookings=bookings, contacts=contacts)



# Define the upload folder
UPLOAD_FOLDER = os.path.join('static', 'uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/admin/add_hotel', methods=['GET', 'POST'])
@login_required
@admin_required
def add_hotel():
    if request.method == 'POST':
        image = request.files['image']
        if image and allowed_file(image.filename):
            filename = secure_filename(image.filename)
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            image.save(image_path)
            image_url = '/' + image_path  # Path to use in HTML src
            
            hotel = Hotel(
                name=request.form['name'],
                description=request.form['description'],
                location=request.form['location'],
                price_nrp=float(request.form['price_nrp']),
                price_usd=float(request.form['price_usd']),
                image_url=image_url,
                amenities=request.form['amenities']
            )
            db.session.add(hotel)
            db.session.commit()
            flash('Hotel added successfully!', 'success')
            return redirect(url_for('admin'))
        else:
            flash('Invalid image format. Only PNG, JPG, JPEG, GIF allowed.', 'danger')
    
    return render_template('admin/add_hotel.html')

@app.route('/admin/add_tour', methods=['GET', 'POST'])
@login_required
@admin_required
def add_tour():
    if request.method == 'POST':
        image = request.files['image']
        if image and allowed_file(image.filename):
            filename = secure_filename(image.filename)
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            image.save(image_path)
            image_url = '/' + image_path  # for use in HTML src

            tour = TourPackage(
                name=request.form['name'],
                description=request.form['description'],
                duration=request.form['duration'],
                price_nrp=float(request.form['price_nrp']),
                price_usd=float(request.form['price_usd']),
                image_url=image_url,
                destinations=request.form['destinations'],
                included_services=request.form['included_services']
            )
            db.session.add(tour)
            db.session.commit()
            flash('Tour package added successfully!', 'success')
            return redirect(url_for('admin'))
        else:
            flash('Invalid image format. Only PNG, JPG, JPEG, GIF allowed.', 'danger')

    return render_template('admin/add_tour.html')

@app.route('/admin/hotels')
@login_required
@admin_required
def admin_hotel_list():
    hotels = Hotel.query.all()
    return render_template('admin/hotel_list.html', hotels=hotels)



@app.route('/admin/hotels/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_hotel(id):
    hotel = Hotel.query.get_or_404(id)

    if request.method == 'POST':
        hotel.name = request.form['name']
        hotel.location = request.form['location']
        hotel.description = request.form['description']
        hotel.price_nrp = request.form['price_nrp']
        hotel.price_usd = request.form['price_usd']
        hotel.amenities = request.form['amenities']

        # Check if a new file is uploaded
        file = request.files.get('image_file')
        if file and file.filename != '':
            filename = secure_filename(file.filename)
            file_path = os.path.join('static/uploads/hotels', filename)  # adjust path accordingly
            file.save(file_path)
            hotel.image_url = url_for('static', filename='uploads/hotels/' + filename)
            # You can also delete old file here if you want

        # If no new file uploaded, keep existing hotel.image_url as is

        db.session.commit()
        flash('Hotel updated successfully!', 'success')
        return redirect(url_for('admin_hotel_list'))

    return render_template('edit_hotel.html', hotel=hotel)

@app.route('/admin/hotels/delete/<int:id>', methods=['POST'])
@login_required
@admin_required
def delete_hotel(id):  # parameter name changed to 'id'
    hotel = Hotel.query.get_or_404(id)
    db.session.delete(hotel)
    db.session.commit()
    flash('Hotel deleted successfully!', 'success')
    return redirect(url_for('admin_hotel_list'))

@app.route('/admin/tours')
@login_required
@admin_required
def admin_tour_list():
    tours = TourPackage.query.all()
    return render_template('admin/tour_list.html', tours=tours)

@app.route('/admin/tours/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_tour(id):
    tour = TourPackage.query.get_or_404(id)
    
    if request.method == 'POST':
        tour.name = request.form['name']
        tour.duration = request.form['duration']
        tour.description = request.form['description']
        tour.price_nrp = float(request.form['price_nrp'])
        tour.price_usd = float(request.form['price_usd'])
        tour.destinations = request.form['destinations']
        tour.included_services = request.form.get('included_services', '')
        
        image = request.files.get('image')
        if image and image.filename != '':
            if allowed_file(image.filename):
                filename = secure_filename(image.filename)
                image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                image.save(image_path)
                tour.image_url = '/' + image_path  # adjust if needed
            else:
                flash('Invalid image format. Allowed: png, jpg, jpeg, gif', 'danger')
                return redirect(request.url)
        
        db.session.commit()
        flash('Tour package updated successfully!', 'success')
        return redirect(url_for('admin_tour_list'))
    
    return render_template('admin/edit_tour.html', tour=tour)


@app.route('/admin/tours/delete/<int:id>', methods=['POST'])
@login_required
@admin_required
def delete_tour(id):
    tour = TourPackage.query.get_or_404(id)
    db.session.delete(tour)
    db.session.commit()
    flash('Tour package deleted successfully!', 'success')
    return redirect(url_for('admin_tour_list'))


@app.route('/payment_success')
@login_required
def payment_success():
    # Retrieve the booking ID you stored in session
    booking_id = session.pop('booking_id', None)
    if not booking_id:
        flash('No booking found for confirmation.', 'warning')
        return redirect(url_for('index'))

    # Lookup and update booking status
    booking = Booking.query.get(booking_id)
    if not booking:
        flash('Booking record not found.', 'danger')
        return redirect(url_for('index'))

    # Mark payment as completed
    booking.payment_status = 'completed'
    booking.booking_status = 'confirmed'
    db.session.commit()

    return render_template('payment_success.html', booking=booking)


@app.route('/payment_failure')
@login_required
def payment_failure():
    # Optionally, you can pop booking_id or keep it for retry
    booking_id = session.pop('booking_id', None)

    flash('Payment failed or was cancelled. Please try again.', 'danger')
    return render_template('payment_failure.html', booking_id=booking_id)








# Recommendation algorithm
@app.route('/recommendations')
def recommendations():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    
    # Get user's booking history and preferences
    user_bookings = Booking.query.filter_by(user_id=current_user.id).all()
    user_reviews = Review.query.filter_by(user_id=current_user.id).all()
    
    # Build user profile based on preferences
    user_profile = {
        'preferred_locations': [],
        'preferred_price_ranges': [],
        'preferred_durations': [],
        'preferred_amenities': [],
        'preferred_destinations': [],
        'rating_preferences': []
    }
    
    # Analyze user's booking history
    for booking in user_bookings:
        if booking.booking_type == 'hotel':
            hotel = Hotel.query.get(booking.item_id)
            if hotel:
                user_profile['preferred_locations'].append(hotel.location)
                user_profile['preferred_price_ranges'].append(hotel.price_nrp)
                if hotel.amenities:
                    user_profile['preferred_amenities'].extend(hotel.amenities.split(','))
        else:
            tour = TourPackage.query.get(booking.item_id)
            if tour:
                user_profile['preferred_durations'].append(tour.duration)
                user_profile['preferred_price_ranges'].append(tour.price_nrp)
                if tour.destinations:
                    user_profile['preferred_destinations'].extend(tour.destinations.split(','))
    
    # Analyze user's reviews
    for review in user_reviews:
        if review.rating >= 4:  # Only consider positive preferences
            user_profile['rating_preferences'].append(review.rating)
            if review.review_type == 'hotel':
                hotel = Hotel.query.get(review.item_id)
                if hotel:
                    user_profile['preferred_locations'].append(hotel.location)
                    if hotel.amenities:
                        user_profile['preferred_amenities'].extend(hotel.amenities.split(','))
            else:
                tour = TourPackage.query.get(review.item_id)
                if tour:
                    user_profile['preferred_durations'].append(tour.duration)
                    if tour.destinations:
                        user_profile['preferred_destinations'].extend(tour.destinations.split(','))
    
    # Calculate average preferences
    avg_price = sum(user_profile['preferred_price_ranges']) / len(user_profile['preferred_price_ranges']) if user_profile['preferred_price_ranges'] else 0
    avg_rating = sum(user_profile['rating_preferences']) / len(user_profile['rating_preferences']) if user_profile['rating_preferences'] else 3.5
    
    # Get all hotels and tours for scoring
    all_hotels = Hotel.query.all()
    all_tours = TourPackage.query.all()
    
    # Score hotels based on user preferences
    hotel_scores = []
    for hotel in all_hotels:
        score = 0
        
        # Location preference (40% weight)
        if hotel.location in user_profile['preferred_locations']:
            score += 40
        
        # Price preference (25% weight)
        if avg_price > 0:
            price_diff = abs(hotel.price_nrp - avg_price) / avg_price
            if price_diff <= 0.2:  # Within 20% of preferred price
                score += 25
            elif price_diff <= 0.5:  # Within 50% of preferred price
                score += 15
        
        # Rating preference (20% weight)
        if hotel.rating >= avg_rating:
            score += 20
        
        # Amenities preference (15% weight)
        if hotel.amenities:
            hotel_amenities = set(hotel.amenities.split(','))
            user_amenities = set(user_profile['preferred_amenities'])
            if user_amenities:
                amenity_match = len(hotel_amenities.intersection(user_amenities)) / len(user_amenities)
                score += amenity_match * 15
        
        hotel_scores.append((hotel, score))
    
    # Score tours based on user preferences
    tour_scores = []
    for tour in all_tours:
        score = 0
        
        # Duration preference (35% weight)
        if tour.duration in user_profile['preferred_durations']:
            score += 35
        
        # Price preference (25% weight)
        if avg_price > 0:
            price_diff = abs(tour.price_nrp - avg_price) / avg_price
            if price_diff <= 0.2:
                score += 25
            elif price_diff <= 0.5:
                score += 15
        
        # Rating preference (20% weight)
        if tour.rating >= avg_rating:
            score += 20
        
        # Destinations preference (20% weight)
        if tour.destinations:
            tour_destinations = set(tour.destinations.split(','))
            user_destinations = set(user_profile['preferred_destinations'])
            if user_destinations:
                destination_match = len(tour_destinations.intersection(user_destinations)) / len(user_destinations)
                score += destination_match * 20
        
        tour_scores.append((tour, score))
    
    # Sort by score and get top recommendations
    hotel_scores.sort(key=lambda x: x[1], reverse=True)
    tour_scores.sort(key=lambda x: x[1], reverse=True)
    
    recommended_hotels = [hotel for hotel, score in hotel_scores[:6] if score > 0]
    recommended_tours = [tour for tour, score in tour_scores[:6] if score > 0]
    
    # If no personalized recommendations, show popular items
    if not recommended_hotels:
        recommended_hotels = Hotel.query.order_by(Hotel.rating.desc()).limit(6).all()
    
    if not recommended_tours:
        recommended_tours = TourPackage.query.order_by(TourPackage.rating.desc()).limit(6).all()
    
    return render_template('recommendations.html', 
                         hotels=recommended_hotels, 
                         tours=recommended_tours,
                         user_profile=user_profile)

# Admin route to view all bookings
@app.route('/admin/bookings')
@login_required
@admin_required
def admin_bookings():
    bookings = Booking.query.order_by(Booking.created_at.desc()).all()
    
    # Get hotel and tour data for each booking
    for booking in bookings:
        if booking.booking_type == 'hotel':
            booking.item_details = Hotel.query.get(booking.item_id)
        else:
            booking.item_details = TourPackage.query.get(booking.item_id)
    
    return render_template('admin/bookings.html', bookings=bookings)

# Admin route to update booking status
@app.route('/admin/bookings/<int:booking_id>/update', methods=['POST'])
@login_required
@admin_required
def update_booking_status(booking_id):
    booking = Booking.query.get_or_404(booking_id)
    new_status = request.form.get('status')
    
    if new_status in ['completed', 'pending']:
        booking.payment_status = new_status
        db.session.commit()
        flash(f'Booking #{booking_id} status updated to {new_status}', 'success')
    else:
        flash('Invalid status', 'danger')
    
    return redirect(url_for('admin_bookings'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        
        # Create admin user if not exists
        admin_user = User.query.filter_by(username='admin').first()
        if not admin_user:
            admin_user = User(
                username='admin',
                email='admin@yatra.com',
                password_hash=generate_password_hash('admin123'),
                is_admin=True
            )
            db.session.add(admin_user)
            db.session.commit()
    
    app.run(debug=True, port=8001) 