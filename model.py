from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, ForeignKey, PrimaryKeyConstraint


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///parking.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User (db.Model):

    __tablename__ = "USERS"
    user_id = db.Column(db.Integer,primary_key = True, autoincrement = True)
    user_name = db.Column(db.String(60), unique = True, nullable = False)
    password = db.Column(db.String(100), nullable = False)
    email = db.Column(db.String(100), unique = True, nullable = False)
    address = db.Column(db.String(250), nullable =  True)
    state = db.Column(db.String,nullable =  True)
    city = db.Column(db.String,nullable =  True)
    locality = db.Column(db.String,nullable =  True)

    pincode = db.Column(db.Integer,nullable =  True)
    # role means here we have to defined a new member shoule have which role , eigther he/she is user or admin
    role  = db.Column(db.String,nullable = False, default = 'user')
    # relatonship is used for one to many rekationship ,and back_populates means we have two way reservation system or we also use backref for that
    reservations =db.relationship("Reservation", back_populates = "user")

# Now i havw to create parking lot table which will be managed by admin and every area have their own parking lot
class Parkinglots (db.Model):
    __tablename__ = "PARKING_LOTS"
    id = db.Column(db.Integer,primary_key = True)
    prime_location = db.Column(String(100), nullable = False)
    address = db.Column(String(100), nullable = False)
    pincode = db.Column(db.Integer, nullable =  True)
    price = db.Column(Float, nullable =  False)
    max_no_of_spots = db.Column(Integer, nullable = False)
    spots = db.relationship("ParkingSpots", back_populates = "lot", cascade = "all, delete-orphan")
#it means  one parking lot have many parking spot whatever admin needed he will be manage

 #now i have to make a parking spot table 


class ParkingSpots (db.Model):
    __tablename__ = "PARKING_SPOTS"
    id = db.Column(db.Integer,primary_key = True)

    lot_id = db.Column(db.Integer, db.ForeignKey('PARKING_LOTS.id'), nullable=False)
    # A shows available and O shows occupied
    status = db.Column(db.String(1), default = 'A',nullable = False)
    lot = db.relationship("Parkinglots", back_populates = "spots")
    reservations = db.relationship("Reservation", back_populates="spot", cascade = "all, delete-orphan")


class Reservation(db.Model):
    __tablename__ = "RESERVATIONS"
    id = db.Column(Integer,primary_key = True)
    spot_id = db.Column(Integer, ForeignKey('PARKING_SPOTS.id'),nullable = False)
    user_id = db.Column(Integer, ForeignKey('USERS.id'),nullable = False)
    Parking_cost_price = db.Column(Float, nullable = False)
    vechile_no = db.Column(String, nullable = False)
    parking_time = db.Column(DateTime, default =datetime.utcnow)
    leving_time = db.Column(DateTime)
    spot = db.relationship("ParkingSpots", back_populates = "RESERVATIONS")
    user = db.relationship("User", back_populates = "RESERVATIONS")

    # now we have to initilize databse
with app.app_context():
    db.create_all()

    # now i have to make an admin
    if not User.query.filter_by(role=True).first():
        admin = User(username='23f1002948', password='admin@123', is_admin=True)
        db.session.add(admin)
        db.session.commit()















    