from flask import Blueprint, request, jsonify
from app.controllers.user_controller import update_profile, upgrade_to_professional

user_routes = Blueprint('user_routes', __name__)

# Route to update user profile fields
@user_routes.route('/api/users/profile', methods=['PUT'])
def update_user_profile():
    return update_profile(request)

# Route for managers and admins to upgrade user to professional status
@user_routes.route('/api/users/<user_id>/upgrade', methods=['POST'])
def upgrade_user(user_id):
    return upgrade_to_professional(user_id)
