# app.py
# This is the MAIN entry point of the Flask application.
# It sets up the app, connects the database, registers route blueprints,
# seeds sample data, and starts the server.

import os
from flask import Flask
from realestate.models import db, User, Property
from werkzeug.security import generate_password_hash

# ─────────────────────────────────────────────
# APP FACTORY FUNCTION
# A function that creates and configures the Flask app.
# ─────────────────────────────────────────────
def create_app():
    app = Flask(__name__)

    # ── Configuration ──────────────────────────────────────────────────────────
    app.config['SECRET_KEY'] = 'realestate_secret_key_2024'

    os.makedirs("instance", exist_ok=True)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///instance/realestate.db'

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['UPLOAD_FOLDER'] = os.path.join('static', 'uploads')
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
   
    # ── Initialize Extensions ──────────────────────────────────────────────────
    db.init_app(app)

    from realestate.routes.auth import auth_bp
    from realestate.routes.properties import properties_bp
    from realestate.routes.favorites import favorites_bp
    from realestate.routes.inquiries import inquiries_bp
    from realestate.routes.analytics import analytics_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(properties_bp)
    app.register_blueprint(favorites_bp)
    app.register_blueprint(inquiries_bp)
    app.register_blueprint(analytics_bp)

    with app.app_context():
        db.create_all()
        seed_data()

    return app
# ─────────────────────────────────────────────
# SEED DATA FUNCTION
# Populates the database with sample users and properties
# so the app looks real when you first run it.
# ─────────────────────────────────────────────
def seed_data():
    # Only seed if there are no properties yet
    if Property.query.count() > 0:
        return

    # Create a demo user
    demo_user = User(
        name='Demo User',
        email='demo@realestate.com',
        password=generate_password_hash('password123')
    )
    db.session.add(demo_user)
    db.session.flush()  # Flush to get the user ID before commit

    # Sample property data
    sample_properties = [
        {
            'title': 'Luxury Villa in Baner',
            'price': 15000000,
            'location': 'Pune',
            'property_type': 'sale',
            'size': 3200,
            'description': 'A stunning 4BHK luxury villa with private pool, modular kitchen, and landscaped garden. Located in the premium Baner locality with easy highway access.',
            'image': 'https://images.unsplash.com/photo-1613977257363-707ba9348227?w=800&auto=format&fit=crop',
        },
        {
            'title': 'Modern Studio Apartment',
            'price': 18000,
            'location': 'Bangalore',
            'property_type': 'rent',
            'size': 650,
            'description': 'Fully furnished studio apartment in the heart of Koramangala. Includes WiFi, AC, and is walking distance from cafes and tech parks.',
            'image': 'https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?w=800&auto=format&fit=crop',
        },
        {
            'title': 'Spacious 3BHK Flat',
            'price': 7500000,
            'location': 'Mumbai',
            'property_type': 'sale',
            'size': 1400,
            'description': 'Beautiful 3BHK apartment in Andheri West. Excellent ventilation, two balconies, covered parking. Near schools and hospitals.',
            'image': 'https://images.unsplash.com/photo-1560448204-e02f11c3d0e2?w=800&auto=format&fit=crop',
        },
        {
            'title': 'Sea-Facing Penthouse',
            'price': 45000000,
            'location': 'Mumbai',
            'property_type': 'sale',
            'size': 4800,
            'description': 'Breathtaking sea-facing penthouse in Worli. Private terrace, infinity pool, fully automated smart home system. The ultimate in luxury living.',
            'image': 'https://images.unsplash.com/photo-1512917774080-9991f1c4c750?w=800&auto=format&fit=crop',
        },
        {
            'title': 'Cozy 1BHK Near Metro',
            'price': 12000,
            'location': 'Delhi',
            'property_type': 'rent',
            'size': 550,
            'description': 'Well-maintained 1BHK apartment 5 minutes from Rajouri Garden Metro. Ideal for working professionals. Semi-furnished.',
            'image': 'https://images.unsplash.com/photo-1484154218962-a197022b5858?w=800&auto=format&fit=crop',
        },
        {
            'title': 'IT Park Office Space',
            'price': 85000,
            'location': 'Hyderabad',
            'property_type': 'rent',
            'size': 2500,
            'description': 'Premium Grade-A office space in HITEC City. Open-plan layout, server room, 3 conference rooms, dedicated power backup.',
            'image': 'https://images.unsplash.com/photo-1497366216548-37526070297c?w=800&auto=format&fit=crop',
        },
        {
            'title': 'Heritage Bungalow',
            'price': 28000000,
            'location': 'Jaipur',
            'property_type': 'sale',
            'size': 5000,
            'description': 'A majestic colonial-era bungalow set in 5000 sq ft. Ornate arches, original tilework, sprawling garden. Rare heritage property in the pink city.',
            'image': 'https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?w=800&auto=format&fit=crop',
        },
        {
            'title': 'Garden View 2BHK',
            'price': 22000,
            'location': 'Pune',
            'property_type': 'rent',
            'size': 1050,
            'description': 'Airy 2BHK with a beautiful garden view in Aundh. Gated society with gym, clubhouse, and children\'s play area.',
            'image': 'https://images.unsplash.com/photo-1502672260266-1c1ef2d93688?w=800&auto=format&fit=crop',
        },
        {
            'title': 'Smart Home Apartment',
            'price': 9500000,
            'location': 'Bangalore',
            'property_type': 'sale',
            'size': 1800,
            'description': 'Fully automated smart home in Whitefield. Voice-controlled lights, security cameras, automated AC. 3BHK with premium finishes.',
            'image': 'https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=800&auto=format&fit=crop',
        },
        {
            'title': 'Waterfront Apartment',
            'price': 35000,
            'location': 'Hyderabad',
            'property_type': 'rent',
            'size': 1600,
            'description': 'Spectacular apartment overlooking Hussain Sagar lake. Fully furnished, 3BHK, high-floor unit with panoramic water views.',
            'image': 'https://images.unsplash.com/photo-1567496898669-ee935f5f647a?w=800&auto=format&fit=crop',
        },
        {
            'title': 'Commercial Shop in Market',
            'price': 4500000,
            'location': 'Delhi',
            'property_type': 'sale',
            'size': 300,
            'description': 'Prime ground-floor commercial shop in Lajpat Nagar market. High footfall area, excellent for retail, banking, or food outlet.',
            'image': 'https://images.unsplash.com/photo-1441986300917-64674bd600d8?w=800&auto=format&fit=crop',
        },
        {
            'title': 'Green Township Villa',
            'price': 12500000,
            'location': 'Chennai',
            'property_type': 'sale',
            'size': 2800,
            'description': 'Eco-friendly villa in a gated green township in OMR. Solar panels, rainwater harvesting, 3BHK + study, community park.',
            'image': 'https://images.unsplash.com/photo-1580587771525-78b9dba3b914?w=800&auto=format&fit=crop',
        },
    ]

    for prop_data in sample_properties:
        prop = Property(owner_id=demo_user.id, **prop_data)
        db.session.add(prop)

    db.session.commit()
    print("✅ Sample data seeded successfully!")


# ─────────────────────────────────────────────
# RUN THE APP
# ─────────────────────────────────────────────
app = create_app()   # 👈 ADD THIS LINE HERE (top-level)

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
