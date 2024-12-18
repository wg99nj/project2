from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    bio = db.Column(db.String(200))
    location = db.Column(db.String(100))
    professional_status = db.Column(db.Boolean, default=False)

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
