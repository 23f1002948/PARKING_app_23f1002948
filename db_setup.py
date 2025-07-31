from models import db, User, ParkingLot, ParkingSpot, Reservation, SpotStatus
import datetime

def create_admin_user():
    """Default admin user create karega agar pehle se nahi hai."""
    existing_admin = User.query.filter_by(username="admin_user", role="admin").first()

    if not existing_admin:
        new_admin = User(
            username="admin_user",
            password="admin123",  # Production me hash karna chahiye
            email="admin@example.com",
            address="Admin Address",
            state="Admin State",
            city="Admin City",
            role="admin"
        )
        db.session.add(new_admin)
        db.session.commit()
        print("✅ Admin user created.")
    else:
        print("ℹ️ Admin user already exists.")

def seed_dummy_data():
    """Dummy parking lots aur spots create karega agar database empty hai."""
    if not ParkingLot.query.first():
        all_data = []

        # Mumbai
        mumbai = ParkingLot(
            prime_location_name="Bandra West",
            price=50.0,
            address="Hill Road, Mumbai",
            pin_code="400050",
            maximum_number_of_spots=2
        )
        mumbai_spots = [
            ParkingSpot(lot=mumbai, status=SpotStatus.AVAILABLE),
            ParkingSpot(lot=mumbai, status=SpotStatus.OCCUPIED)
        ]
        mumbai_res = Reservation(
            spot=mumbai_spots[1],
            user_id=1,
            parking_timestamp=datetime.datetime.utcnow() - datetime.timedelta(hours=2),
            leaving_timestamp=None,
            parking_cost=0.0,
            vehicle_number="MH12AB9999"
        )
        all_data.append((mumbai, mumbai_spots, mumbai_res))

        # New York
        ny = ParkingLot(
            prime_location_name="Times Square",
            price=75.0,
            address="Broadway, New York, NY",
            pin_code="10036",
            maximum_number_of_spots=3
        )
        ny_spots = [
            ParkingSpot(lot=ny, status=SpotStatus.AVAILABLE),
            ParkingSpot(lot=ny, status=SpotStatus.OCCUPIED),
            ParkingSpot(lot=ny, status=SpotStatus.AVAILABLE)
        ]
        ny_res = Reservation(
            spot=ny_spots[1],
            user_id=1,
            parking_timestamp=datetime.datetime.utcnow() - datetime.timedelta(minutes=90),
            leaving_timestamp=None,
            parking_cost=0.0,
            vehicle_number="NY9876ZX"
        )
        all_data.append((ny, ny_spots, ny_res))

        # London
        london = ParkingLot(
            prime_location_name="Oxford Street",
            price=65.0,
            address="Oxford Street, London",
            pin_code="W1D 1BS",
            maximum_number_of_spots=2
        )
        london_spots = [
            ParkingSpot(lot=london, status=SpotStatus.AVAILABLE),
            ParkingSpot(lot=london, status=SpotStatus.OCCUPIED)
        ]
        london_res = Reservation(
            spot=london_spots[1],
            user_id=1,
            parking_timestamp=datetime.datetime.utcnow() - datetime.timedelta(hours=3),
            leaving_timestamp=None,
            parking_cost=0.0,
            vehicle_number="UK19CAR001"
        )
        all_data.append((london, london_spots, london_res))

        # Save to DB
        for lot, spots, reservation in all_data:
            db.session.add(lot)
            db.session.add_all(spots)
            db.session.add(reservation)

        db.session.commit()
        print("✅ Dummy data seeded.")

def initialize_database():
    """Database setup, admin creation aur dummy data insert karta hai."""
    db.create_all()
    create_admin_user()
    seed_dummy_data()
    print("✅ Database setup complete.")

# Run this scripts only when this file is excecuted.
if __name__ == '__main__':
    from run import app
    with app.app_context():
        initialize_database()

