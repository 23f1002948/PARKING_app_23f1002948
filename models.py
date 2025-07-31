import enum
# enum should be used to kept fixed values such as spotstauts
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()  
import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime, Enum

class SpotStatus(enum.Enum):
    OCCUPIED = "O"
    AVAILABLE = "A"

# here we will have to make user table in which we will have to store user details 
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    address = db.Column(db.String, nullable=True)
    state = db.Column(db.String, nullable=True)
    city = db.Column(db.String, nullable=True)
    #back_populates shold be used to make relation betwen two tables (one to many)
    reservations = db.relationship("Reservation", back_populates="user")
    #
    role = db.Column(db.String, nullable=False, default='user')  # 'admin' or 'user' user can only reserve or relese spot,admin can do every thing


# now we have to make parking lot table in which we will have to stores parking details
class ParkingLot(db.Model):
    __tablename__ = 'parking_lots'
    id = db.Column(Integer, primary_key=True, autoincrement=True)
    prime_location_name = db.Column(String, nullable=False)
    price = db.Column(Float, nullable=False)
    address = db.Column(String, nullable=False)
    pin_code = db.Column(String, nullable=False)
    maximum_number_of_spots = db.Column(Integer, nullable=False)

    # one to many reltion with parking spt means one parking lot can have many parking spots.
    spots = db.relationship("ParkingSpot", back_populates="lot", cascade="all, delete-orphan")

# here we make parking spot table in which we will have to
class ParkingSpot(db.Model):
    __tablename__ = 'parking_spots'
    id = db.Column(Integer, primary_key=True, autoincrement=True)
    lot_id = db.Column(Integer, ForeignKey('parking_lots.id'), nullable=False)
    status = db.Column(Enum(SpotStatus), default=SpotStatus.AVAILABLE, nullable=False)
    # this spot is related to which lot
    lot = db.relationship("ParkingLot", back_populates="spots")
    
    reservations = db.relationship("Reservation", back_populates="spot", cascade="all, delete-orphan")
 
 # here we make reservation table in which we store reservation details
class Reservation(db.Model):
    __tablename__ = 'reservations'
    id = db.Column(Integer, primary_key=True, autoincrement=True)
    spot_id = db.Column(Integer, ForeignKey('parking_spots.id'), nullable=False)
    user_id = db.Column(Integer, ForeignKey('users.id'), nullable=False)
    parking_timestamp = db.Column(DateTime, default=datetime.datetime.utcnow)
    leaving_timestamp = db.Column(DateTime, nullable=True)
    parking_cost = db.Column(Float, nullable=False)
    vehicle_number = db.Column(String, nullable=False)  
    # this reservation is related to which spot and which user.
    spot = db.relationship("ParkingSpot", 
     back_populates="reservations")
    user = db.relationship("User", back_populates="reservations")


# here ,initialize the datadb.Model
def init_db(app):
    db.init_app(app)



















    