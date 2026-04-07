# routes/analytics.py
# Provides data for Chart.js visualizations.
# Returns JSON data consumed by the frontend JavaScript.

from flask import Blueprint, jsonify, render_template
from models import db, Property
from sqlalchemy import func

analytics_bp = Blueprint('analytics', __name__)


# ─────────────────────────────────────────────
# ANALYTICS DASHBOARD PAGE
# ─────────────────────────────────────────────
@analytics_bp.route('/analytics')
def analytics():
    return render_template('analytics.html')


# ─────────────────────────────────────────────
# API: Average price per location
# Used by Chart.js bar chart
# ─────────────────────────────────────────────
@analytics_bp.route('/api/avg-price-by-location')
def avg_price_by_location():
    # Group properties by location, compute average price
    results = db.session.query(
        Property.location,
        func.avg(Property.price).label('avg_price'),
        func.count(Property.id).label('count')
    ).group_by(Property.location).all()

    data = {
        'labels': [r.location for r in results],
        'values': [round(r.avg_price) for r in results],
        'counts': [r.count for r in results]
    }
    return jsonify(data)


# ─────────────────────────────────────────────
# API: Number of listings per property type
# Used by Chart.js pie/doughnut chart
# ─────────────────────────────────────────────
@analytics_bp.route('/api/listings-by-type')
def listings_by_type():
    results = db.session.query(
        Property.property_type,
        func.count(Property.id).label('count')
    ).group_by(Property.property_type).all()

    data = {
        'labels': [r.property_type.capitalize() for r in results],
        'values': [r.count for r in results]
    }
    return jsonify(data)


# ─────────────────────────────────────────────
# API: Price distribution (histogram buckets)
# Used by Chart.js line chart
# ─────────────────────────────────────────────
@analytics_bp.route('/api/price-distribution')
def price_distribution():
    props = Property.query.with_entities(Property.price, Property.location).all()

    buckets = {
        'Under ₹10L': 0,
        '₹10L–₹50L': 0,
        '₹50L–₹1Cr': 0,
        '₹1Cr–₹3Cr': 0,
        'Above ₹3Cr': 0
    }

    for p in props:
        price = p.price
        if price < 1_000_000:
            buckets['Under ₹10L'] += 1
        elif price < 5_000_000:
            buckets['₹10L–₹50L'] += 1
        elif price < 10_000_000:
            buckets['₹50L–₹1Cr'] += 1
        elif price < 30_000_000:
            buckets['₹1Cr–₹3Cr'] += 1
        else:
            buckets['Above ₹3Cr'] += 1

    return jsonify({
        'labels': list(buckets.keys()),
        'values': list(buckets.values())
    })
