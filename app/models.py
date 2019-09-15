from . import db

class Patient(db.Model):
    __tablename__ = 'patient'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(64), unique=False, nullable = False)
    last_name = db.Column(db.String(64), unique=False, nullable = False)
    email = db.Column(db.String(64), unique = True, nullable = False)
    password = db.Column(db.String(64), unique = False, nullable = False)
    ssn = db.Column(db.Integer, unique = True, nullable = False)
    dob = db.Column(db.DateTime)
    physician_id = db.Column(db.Integer, db.ForeignKey('physician.id'))
    prescriptions = db.relationship('prescription', backref = 'prescribed')

    def __repr__(self):
        return '<Role %r>' % self.first_name

class Physician(db.Model):
    __tablename__ = 'physician'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(64), unique=False, nullable = False)
    last_name = db.Column(db.String(64), unique=False, nullable = False)
    email = db.Column(db.String(64), unique = True, nullable = False)
    password = db.Column(db.String(64), unique = True, nullable = False)
    patients = db.relationship('patient', backref = 'physician')
    prescriptions_issued = db.relationship('prescription', backref = db.backref('prescriptions_issued'))

    def __repr__(self):
        return '<Role %r>' % self.first_name

class Prescription(db.Model):
    __tablename__ = 'prescription'
    medication = db.Column(db.String(64), unique = False, nullable = False)
    date_prescribed = db.Column(db.DateTime, unique = False, nullable = False)
    date_expired = db.Column(db.DateTime, unique = False, nullable = False)
    description = db.Column(db.Text, unique = False, nullable = False)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'))
    physician_id = db.Column(db.Integer, db.ForeignKey('physician.id'))

    def __repr__(self):
        return '<Role %r>' % self.medication

class


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def __repr__(self):
        return '<User %r>' % self.username
