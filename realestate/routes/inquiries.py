# routes/inquiries.py
# Handles the 📩 Contact / Inquiry system
# Users send messages about a property; stored in DB

from flask import Blueprint, request, redirect, url_for, flash, session, render_template
from models import db, Inquiry, Property

inquiries_bp = Blueprint('inquiries', __name__)


# ─────────────────────────────────────────────
# SEND INQUIRY (POST only)
# ─────────────────────────────────────────────
@inquiries_bp.route('/inquire/<int:property_id>', methods=['POST'])
def send_inquiry(property_id):
    # Make sure the property exists
    prop = Property.query.get_or_404(property_id)

    name = request.form.get('name', '').strip()
    email = request.form.get('email', '').strip()
    message = request.form.get('message', '').strip()

    # Basic validation
    if not name or not email or not message:
        flash('All inquiry fields are required.', 'danger')
        return redirect(url_for('properties.detail', property_id=property_id))

    # Save inquiry to database
    inquiry = Inquiry(
        user_id=session.get('user_id'),   # None if not logged in (guests can inquire too)
        property_id=property_id,
        name=name,
        email=email,
        message=message
    )
    db.session.add(inquiry)
    db.session.commit()

    flash('Your inquiry has been sent! The owner will contact you soon. 📬', 'success')
    return redirect(url_for('properties.detail', property_id=property_id))


# ─────────────────────────────────────────────
# VIEW INQUIRIES (for property owner)
# ─────────────────────────────────────────────
@inquiries_bp.route('/my-inquiries')
def my_inquiries():
    if 'user_id' not in session:
        flash('Please log in to view inquiries.', 'warning')
        return redirect(url_for('auth.login'))

    # Get properties owned by this user
    from models import Property
    my_props = Property.query.filter_by(owner_id=session['user_id']).all()
    prop_ids = [p.id for p in my_props]

    # Get all inquiries for those properties
    inquiries = Inquiry.query.filter(
        Inquiry.property_id.in_(prop_ids)
    ).order_by(Inquiry.sent_at.desc()).all()

    return render_template('inquiries.html', inquiries=inquiries)
