# routes/favorites.py
# Handles the ❤️ Favorites system:
# - Toggle save/unsave a property
# - View all saved properties for a user

from flask import Blueprint, redirect, url_for, session, flash, render_template, jsonify
from models import db, Favorite, Property

favorites_bp = Blueprint('favorites', __name__)


# ─────────────────────────────────────────────
# TOGGLE FAVORITE
# Adds the property to favorites if not saved,
# removes it if already saved (toggle behavior)
# ─────────────────────────────────────────────
@favorites_bp.route('/favorite/<int:property_id>', methods=['POST'])
def toggle_favorite(property_id):
    # Must be logged in
    if 'user_id' not in session:
        return jsonify({'error': 'Login required', 'redirect': url_for('auth.login')}), 401

    user_id = session['user_id']

    # Check if already favorited
    existing = Favorite.query.filter_by(user_id=user_id, property_id=property_id).first()

    if existing:
        # ── Unsave ───────────────────────────────────────
        db.session.delete(existing)
        db.session.commit()
        return jsonify({'status': 'removed', 'message': 'Removed from favorites'})
    else:
        # ── Save ─────────────────────────────────────────
        fav = Favorite(user_id=user_id, property_id=property_id)
        db.session.add(fav)
        db.session.commit()
        return jsonify({'status': 'added', 'message': 'Added to favorites'})


# ─────────────────────────────────────────────
# VIEW ALL FAVORITES
# ─────────────────────────────────────────────
@favorites_bp.route('/favorites')
def my_favorites():
    if 'user_id' not in session:
        flash('Please log in to view your favorites.', 'warning')
        return redirect(url_for('auth.login'))

    # Get all favorite records for this user, join with property info
    user_id = session['user_id']
    favorites = Favorite.query.filter_by(user_id=user_id).all()
    # Get the actual property objects
    properties = [f.property for f in favorites]
    fav_ids = [p.id for p in properties]

    return render_template('favorites.html', properties=properties, user_favorites=fav_ids)
