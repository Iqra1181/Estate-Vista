# routes/properties.py
# Handles all property-related routes:
# - Home page with listings
# - Property detail page
# - Add new property
# - Search / Filter / Sort
# - Price estimator
# - Image upload

import os
from flask import (Blueprint, render_template, request, redirect,
                   url_for, session, flash, current_app, jsonify)
from models import db, Property, Favorite
from werkzeug.utils import secure_filename

properties_bp = Blueprint('properties', __name__)

# Allowed image extensions for upload
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

def allowed_file(filename):
    """Check if uploaded file has an allowed extension."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# ─────────────────────────────────────────────
# HOME / INDEX — Main listing page
# Supports: search, filter, sort, pagination
# ─────────────────────────────────────────────
@properties_bp.route('/')
def index():
    # Get all query parameters from the URL
    search = request.args.get('search', '').strip()
    prop_type = request.args.get('type', '')           # 'rent' or 'sale' or ''
    min_price = request.args.get('min_price', type=float)
    max_price = request.args.get('max_price', type=float)
    sort = request.args.get('sort', '')                 # 'price_asc' or 'price_desc'
    page = request.args.get('page', 1, type=int)       # Current page number

    # Start with all properties
    query = Property.query

    # ── Apply Filters ────────────────────────────────────
    if search:
        # Search by location (case-insensitive)
        query = query.filter(Property.location.ilike(f'%{search}%'))

    if prop_type in ('rent', 'sale'):
        query = query.filter(Property.property_type == prop_type)

    if min_price is not None:
        query = query.filter(Property.price >= min_price)

    if max_price is not None:
        query = query.filter(Property.price <= max_price)

    # ── Apply Sorting ────────────────────────────────────
    if sort == 'price_asc':
        query = query.order_by(Property.price.asc())
    elif sort == 'price_desc':
        query = query.order_by(Property.price.desc())
    else:
        query = query.order_by(Property.created_at.desc())  # Default: newest first

    # ── Pagination ───────────────────────────────────────
    PER_PAGE = 6  # Show 6 properties per page
    pagination = query.paginate(page=page, per_page=PER_PAGE, error_out=False)
    properties = pagination.items

    # ── Recently Added (for sidebar section) ─────────────
    recent = Property.query.order_by(Property.created_at.desc()).limit(4).all()

    # ── Get user's favorites (for heart icon state) ───────
    user_favorites = []
    if 'user_id' in session:
        favs = Favorite.query.filter_by(user_id=session['user_id']).all()
        user_favorites = [f.property_id for f in favs]

    return render_template('index.html',
                           properties=properties,
                           pagination=pagination,
                           recent=recent,
                           user_favorites=user_favorites,
                           search=search,
                           prop_type=prop_type,
                           min_price=min_price,
                           max_price=max_price,
                           sort=sort)


# ─────────────────────────────────────────────
# PROPERTY DETAIL PAGE
# ─────────────────────────────────────────────
@properties_bp.route('/property/<int:property_id>')
def detail(property_id):
    # Get property by ID, return 404 if not found
    prop = Property.query.get_or_404(property_id)

    # Smart Recommendations: same location OR similar price range (±30%)
    low = prop.price * 0.7
    high = prop.price * 1.3
    similar = Property.query.filter(
        Property.id != prop.id,  # Not the current property
        db.or_(
            Property.location == prop.location,
            db.and_(Property.price >= low, Property.price <= high)
        )
    ).limit(3).all()

    # Check if current user has favorited this property
    is_favorited = False
    if 'user_id' in session:
        fav = Favorite.query.filter_by(
            user_id=session['user_id'],
            property_id=property_id
        ).first()
        is_favorited = fav is not None

    return render_template('detail.html',
                           prop=prop,
                           similar=similar,
                           is_favorited=is_favorited)


# ─────────────────────────────────────────────
# ADD PROPERTY
# ─────────────────────────────────────────────
@properties_bp.route('/add', methods=['GET', 'POST'])
def add_property():
    # Only logged-in users can add properties
    if 'user_id' not in session:
        flash('Please log in to add a property.', 'warning')
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        price = request.form.get('price', type=float)
        location = request.form.get('location', '').strip()
        prop_type = request.form.get('property_type', '')
        size = request.form.get('size', type=float)
        description = request.form.get('description', '').strip()
        image_url = request.form.get('image_url', '').strip()

        # ── Validation ──────────────────────────────────
        if not all([title, price, location, prop_type, size]):
            flash('Please fill in all required fields.', 'danger')
            return render_template('add_property.html')

        # ── Handle Image: Upload or URL ──────────────────
        image_path = image_url  # Default to URL if provided

        file = request.files.get('image_file')
        if file and file.filename and allowed_file(file.filename):
            # Save uploaded file to static/uploads/
            filename = secure_filename(file.filename)
            upload_folder = current_app.config['UPLOAD_FOLDER']
            os.makedirs(upload_folder, exist_ok=True)
            file.save(os.path.join(upload_folder, filename))
            image_path = f'uploads/{filename}'  # Relative to /static/

        # ── Save to Database ────────────────────────────
        new_prop = Property(
            title=title,
            price=price,
            location=location,
            property_type=prop_type,
            size=size,
            description=description,
            image=image_path,
            owner_id=session['user_id']
        )
        db.session.add(new_prop)
        db.session.commit()

        flash('Property listed successfully! 🎉', 'success')
        return redirect(url_for('properties.detail', property_id=new_prop.id))

    return render_template('add_property.html')


# ─────────────────────────────────────────────
# PRICE ESTIMATOR — API endpoint (returns JSON)
# Called by JavaScript via fetch()
# ─────────────────────────────────────────────
@properties_bp.route('/estimate-price')
def estimate_price():
    location = request.args.get('location', '').strip().lower()
    size = request.args.get('size', type=float)

    if not location or not size:
        return jsonify({'error': 'Location and size are required'}), 400

    # Base price per sq ft varies by city (simple estimation model)
    PRICE_MAP = {
        'mumbai':    18000,
        'delhi':     12000,
        'bangalore': 11000,
        'hyderabad':  9000,
        'pune':       8500,
        'chennai':    8000,
        'jaipur':     6500,
        'kolkata':    7000,
    }

    # Find matching city (partial match)
    rate = 7000  # Default rate if city not found
    for city, city_rate in PRICE_MAP.items():
        if city in location:
            rate = city_rate
            break

    estimated = size * rate

    return jsonify({
        'location': location.title(),
        'size': size,
        'rate_per_sqft': rate,
        'estimated_price': estimated,
        'formatted': f'₹{estimated:,.0f}'
    })
