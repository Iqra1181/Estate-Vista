# models.py
# This file defines all the database tables using SQLAlchemy ORM.
# Each class = one table in the SQLite database.

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Create the SQLAlchemy instance (will be linked to the Flask app in app.py)
db = SQLAlchemy()


# ─────────────────────────────────────────────
# USER TABLE — stores registered users
# ─────────────────────────────────────────────
class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)                        # Auto-incrementing ID
    name = db.Column(db.String(100), nullable=False)                    # Full name
    email = db.Column(db.String(150), unique=True, nullable=False)      # Email (must be unique)
    password = db.Column(db.String(200), nullable=False)                # Hashed password
    created_at = db.Column(db.DateTime, default=datetime.utcnow)       # Registration time

    # Relationships — one user can have many favorites and inquiries
    favorites = db.relationship('Favorite', backref='user', lazy=True, cascade='all, delete-orphan')
    inquiries = db.relationship('Inquiry', backref='user', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<User {self.email}>'


# ─────────────────────────────────────────────
# PROPERTY TABLE — stores all property listings
# ─────────────────────────────────────────────
class Property(db.Model):
    __tablename__ = 'properties'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)                   # Property title
    price = db.Column(db.Float, nullable=False)                         # Price in INR
    location = db.Column(db.String(200), nullable=False)                # City / area
    property_type = db.Column(db.String(20), nullable=False)            # 'rent' or 'sale'
    size = db.Column(db.Float, nullable=False)                          # Size in sq ft
    description = db.Column(db.Text, nullable=True)                     # Full description
    image = db.Column(db.String(300), nullable=True)                    # Image path or URL
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)  # Posted by which user
    created_at = db.Column(db.DateTime, default=datetime.utcnow)       # When it was listed

    # Relationships
    favorites = db.relationship('Favorite', backref='property', lazy=True, cascade='all, delete-orphan')
    inquiries = db.relationship('Inquiry', backref='property', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Property {self.title}>'


# ─────────────────────────────────────────────
# FAVORITE TABLE — which user saved which property
# ─────────────────────────────────────────────
class Favorite(db.Model):
    __tablename__ = 'favorites'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)         # Which user
    property_id = db.Column(db.Integer, db.ForeignKey('properties.id'), nullable=False) # Which property
    saved_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Favorite user={self.user_id} property={self.property_id}>'


# ─────────────────────────────────────────────
# INQUIRY TABLE — contact messages from users
# ─────────────────────────────────────────────
class Inquiry(db.Model):
    __tablename__ = 'inquiries'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)           # Sender
    property_id = db.Column(db.Integer, db.ForeignKey('properties.id'), nullable=False) # For which property
    name = db.Column(db.String(100), nullable=False)                    # Sender's name
    email = db.Column(db.String(150), nullable=False)                   # Sender's email
    message = db.Column(db.Text, nullable=False)                        # The inquiry message
    sent_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Inquiry from {self.email} for property {self.property_id}>'
