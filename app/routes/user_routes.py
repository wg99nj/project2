from flask import Blueprint, request, jsonify, g
from app.controllers.user_controller import update_profile, upgrade_to_professional
from app.models.user import User

user_routes = Blueprint('user_routes', __name__)

@user_routes.before_request
def load_user():
    token = request.headers.get('Authorization')
    if token:
        token = token.replace('Bearer ', '')
        user = User.query.filter_by(token=token).first()
        if user:
            g.user = user
        else:
            return jsonify({'error': 'Invalid token'}), 401
    else:
        g.user = None

# Route to update user profile fields
@user_routes.route('/api/users/profile', methods=['PUT'])
def update_user_profile():
    if not g.user:
        return jsonify({'error': 'Unauthorized'}), 401
    return update_profile(request)

# Route for managers and admins to upgrade user to professional status
@user_routes.route('/api/users/<user_id>/upgrade', methods=['POST'])
def upgrade_user(user_id):
    if not g.user:
        return jsonify({'error': 'Unauthorized'}), 401
    return upgrade_to_professional(user_id)

