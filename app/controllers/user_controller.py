from flask import request, jsonify, g
from app.models.user import User
from app.models.notification import Notification
from app import db

def validate_profile_data(data):
    if not data.get('name') or not data.get('bio') or not data.get('location'):
        return False, "All fields (name, bio, location) are required."
    return True, ""

def update_profile(request):
    try:
        user_id = g.user.id
        updates = request.json
        is_valid, message = validate_profile_data(updates)
        if not is_valid:
            return jsonify({'error': message}), 400
        user = User.query.filter_by(id=user_id).first()
        if not user:
            return jsonify({'error': 'User not found'}), 404
        for key, value in updates.items():
            setattr(user, key, value)
        db.session.commit()
        return jsonify(user.serialize()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

def upgrade_to_professional(user_id):
    try:
        user = User.query.filter_by(id=user_id).first()
        if not user:
            return jsonify({'error': 'User not found'}), 404
        user.professional_status = True
        db.session.commit()
        notification = Notification(user_id=user_id, message='Your account has been upgraded to professional status.')
        notification.save()
        return jsonify(user.serialize()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400


