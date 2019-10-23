#the relationship is established with db.relationship()
#where the backref, specifies the reverse direction of the relationship
#in adding the backreference, you can access the relational model as an object
#rather than a list etc.

from . import db

class Physician(db.Model):
    __tablename__ = 'Physician'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(64), unique=False, nullable = False)
    last_name = db.Column(db.String(64), unique=False, nullable = False)
    email = db.Column(db.String(64), unique=True, nullable = False)
    password = db.Column(db.String(64), unique = False, nullable = False)
    patients = db.relationship('Patient', backref = 'physician')
    prescriptions_issued = db.relationship('Prescription')
    appointments = db.relationship('Appointment')
    hospital = db.Column(db.Integer, db.ForeignKey('Hospital.id'))
    def __repr__(self):
        return '<Physician %r>' % self.first_name

class Patient(db.Model):
    __tablename__ = 'Patient'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(64), unique=False, nullable = False)
    last_name = db.Column(db.String(64), unique=False, nullable = False)
    email = db.Column(db.String(64), unique = True, nullable = False)
    password = db.Column(db.String(64), unique = False, nullable = False)
    ssn = db.Column(db.Integer, unique = True, nullable = False)
    dob = db.Column(db.DateTime)
    physician_id = db.Column(db.Integer, db.ForeignKey('Physician.id'))
    prescriptions = db.relationship('Prescription', backref = 'prescribed')
    appointments = db.relationship('Appointment', backref = 'patient')

    def __repr__(self):
        return '<Patient %r>' % self.first_name

class Prescription(db.Model):
    __tablename__ = 'Prescription'
    medication = db.Column(db.String(64), unique = False, nullable = False, primary_key = True)
    date_prescribed = db.Column(db.DateTime, unique = False, nullable = False, primary_key = True)
    date_expired = db.Column(db.DateTime, unique = False, nullable = False)
    description = db.Column(db.Text, unique = False, nullable = False)
    patient_id = db.Column(db.Integer, db.ForeignKey('Patient.id'), primary_key = True)
    physician_id = db.Column(db.Integer, db.ForeignKey('Physician.id'), primary_key = True)

    def __repr__(self):
        return '<Prescription %r>' % self.medication

class Appointment(db.Model):
    __tablename__ = 'Appointment'
    appointment_id = db.Column(db.Integer, primary_key = True)
    start_time = db.Column(db.DateTime, unique = False, nullable = False)
    end_time = db.Column(db.DateTime, unique = False, nullable = False)
    physician_id = db.Column(db.Integer, db.ForeignKey('Physician.id'))
    patient_id = db.Column(db.Integer, db.ForeignKey('Patient.id'))

    def __repr__(self):
        return '<Appointment %r>' % self.appointment_id

class Room(db.Model):
    __tablename__ = 'Room'
    room_number = db.Column(db.Integer, primary_key = True)
    building = db.Column(db.String(64), unique = False, nullable = False)
    hospital = db.Column(db.Integer, db.ForeignKey('Hospital.id'))


    def __repr__(self):
        return '<Room %r>' % self.room_number

class Hospital(db.Model):
    __tablename__ = 'Hospital'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(64), nullable = False)
    country = db.Column(db.String(64), unique = False, nullable = False)
    state = db.Column(db.String(64), unique = False, nullable = False)
    city = db.Column(db.String(64), unique = False, nullable = False)
    zipcode = db.Column(db.String(64), unique = False, nullable = False)
    rooms = db.relationship('Room')
    physicians = db.relationship('Physician')

    def __repr__(self):
        return '<Hospital %r>' % self.name


# Alexanders-MacBook-Pro:~ bogdanowicz$ mysqld
# 2019-09-18T10:06:40.401736Z 0 [System] [MY-010116] [Server] /usr/local/Cellar/mysql/8.0.17_1/bin/mysqld (mysqld 8.0.17) starting as process 60711
# 2019-09-18T10:06:40.413738Z 0 [Warning] [MY-010159] [Server] Setting lower_case_table_names=2 because file system for /usr/local/var/mysql/ is case insensitive
# 2019-09-18T10:06:41.047652Z 0 [Warning] [MY-010068] [Server] CA certificate ca.pem is self signed.
# 2019-09-18T10:06:41.120228Z 0 [System] [MY-010931] [Server] /usr/local/Cellar/mysql/8.0.17_1/bin/mysqld: ready for connections. Version: '8.0.17'  socket: '/tmp/mysql.sock'  port: 3306  Homebrew.
# 2019-09-18T10:06:41.180187Z 0 [System] [MY-011323] [Server] X Plugin ready for connections. Socket: '/tmp/mysqlx.sock' bind-address: '::' port: 33060

# It's going through mysqldb which is going through port 33060
#That's the default port that it runs on
# it's also helpful to note where it's launching from as mysqldb
# is using a tmp/mysql.sock.lock which is why we can't connect to mamp
# http://mysql-python.sourceforge.net/MySQLdb.html
#Helpful link ^^
## https://dev.mysql.com/doc/mysql-startstop-excerpt/5.7/en/mysqld-multi.html
