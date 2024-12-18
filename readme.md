# Project Overview

This project is a Flask-based web application with user management features, including profile updates and upgrading users to professional status. The application also includes an admin panel for managing users.

## Features

- User profile update
- Upgrade user to professional status
- Admin panel for managing users
- Token-based authentication
- User role management

## Setup

### Prerequisites

- Python 3.10+
- Flask
- Flask-SQLAlchemy
- pytest

### Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/your-repo/project2.git
    cd project2
    ```

2. Create a virtual environment and activate it:
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the dependencies:
    ```sh
    pip install -r requirements.txt
    ```

4. Set up the database:
    ```sh
    flask db upgrade
    ```

5. Run the application:
    ```sh
    flask run
    ```

## Project Structure

```
project2/
│
├── app/
│   ├── __init__.py
│   ├── controllers/
│   │   └── user_controller.py
│   ├── models/
│   │   ├── user.py
│   │   └── notification.py
│   ├── routes/
│   │   └── user_routes.py
│   ├── static/
│   │   └── js/
│   │       └── profile.js
│   ├── templates/
│   │   ├── profile.html
│   │   └── admin.html
│   └── routers/
│       └── user_routes.py
│
├── tests/
│   └── user_controller/
│       └── test_user_controller.py
│
└── README.md
```

## Routes

### User Routes

- `PUT /api/users/profile`: Update user profile fields.
- `POST /api/users/<user_id>/upgrade`: Upgrade user to professional status.
- `GET /api/users/<user_id>`: Get user details by ID.

### Admin Routes

- `GET /admin`: Admin panel for managing users.

## Models

### User Model

```python
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    bio = db.Column(db.String(200))
    location = db.Column(db.String(100))
    professional_status = db.Column(db.Boolean, default=False)
    token = db.Column(db.String(200), unique=True)
    role = db.Column(db.String(50), default='user')

    def save(self):
        db.session.add(self)
        db.session.commit()

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'bio': self.bio,
            'location': self.location,
            'professional_status': self.professional_status
        }
```

### Notification Model

```python
class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    message = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    def save(self):
        db.session.add(self)
        db.session.commit()
```

## Tests

### User Controller Tests

Located in `tests/user_controller/test_user_controller.py`.

- `test_update_user_profile`: Test updating user profile.
- `test_update_user_profile_validation`: Test profile update validation.
- `test_update_user_profile_missing_fields`: Test profile update with missing fields.
- `test_update_user_profile_invalid_token`: Test profile update with invalid token.
- `test_upgrade_user_to_professional`: Test upgrading user to professional status.
- `test_upgrade_user_to_professional_invalid_token`: Test upgrading user with invalid token.
- `test_upgrade_user_to_professional_non_admin`: Test upgrading user by non-admin.
- `test_get_user_profile`: Test getting user profile.
- `test_get_user_profile_invalid_token`: Test getting user profile with invalid token.
- `test_get_user_profile_non_existent_user`: Test getting non-existent user profile.

## Static Files

### JavaScript

Located in `app/static/js/profile.js`.

```javascript
document.addEventListener('DOMContentLoaded', () => {
    const form = document.querySelector('form');
    form.addEventListener('submit', (event) => {
        const name = document.getElementById('name').value;
        const bio = document.getElementById('bio').value;
        const location = document.getElementById('location').value;

        if (!name || !bio || !location) {
            event.preventDefault();
            alert('All fields are required.');
        }
    });
});
```

## Templates

### Profile Template

Located in `app/templates/profile.html`.

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <!-- ...existing code... -->
</head>
<body>
    <!-- ...existing code... -->
    <div class="profile">
        <h1>Profile</h1>
        <form action="/api/users/profile" method="POST">
            <input type="hidden" name="_method" value="PUT">
            <label for="name">Name:</label>
            <input type="text" id="name" name="name" value="{{ user.name }}">
            <label for="bio">Bio:</label>
            <textarea id="bio" name="bio">{{ user.bio }}</textarea>
            <label for="location">Location:</label>
            <input type="text" id="location" name="location" value="{{ user.location }}">
            <button type="submit">Update Profile</button>
        </form>
        <p>Professional Status: {{ 'Yes' if user.professional_status else 'No' }}</p>
    </div>
    <!-- ...existing code... -->
</body>
</html>
```

### Admin Template

Located in `app/templates/admin.html`.

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <!-- ...existing code... -->
</head>
<body>
    <!-- ...existing code... -->
    <div class="admin">
        <h1>Admin Panel</h1>
        <form action="/upgrade" method="GET">
            <label for="search">Search Users:</label>
            <input type="text" id="search" name="search">
            <button type="submit">Search</button>
        </form>
        <div id="user-list">
            {% for user in users %}
                <div class="user">
                    <p>{{ user.name }} ({{ user.email }})</p>
                    <form action="/api/users/{{ user.id }}/upgrade" method="POST">
                        <button type="submit">Upgrade to Professional</button>
                    </form>
                </div>
            {% endfor %}
        </div>
    </div>
    <!-- ...existing code... -->
</body>
</html>
```

## API Documentation

The API documentation is available at `/docs` when the application is running.

## License

This project is licensed under the MIT License.
