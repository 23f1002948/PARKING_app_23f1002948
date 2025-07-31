from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from static.constant import form_fields, stateCityMap
from models import db, User, ParkingLot, ParkingSpot, Reservation, SpotStatus
import datetime

main = Blueprint('main', __name__)
# this function ensure that the user is logged in and has authorisation to access the admin pages
def require_admin():
    if 'role' not in session or session['role'] != 'admin':
        flash('You are not authorized to access this page. Admins only.', 'danger')
        return redirect(url_for('main.user_dashboard'))
    return None

@main.route('/')
def home():
    #check if user is logged or not if not redirect to login page
    
    redirect_user = validate_session()

    if redirect_user:
        return redirect_user
    #if user is rolled in as admin or user redirect to their respective dashboard
    role = session['role']
    if role == 'user':
        return redirect(url_for('main.user_dashboard'))
    elif role == 'admin':
        return redirect(url_for('main.admin_dashboard'))
    return "Invalid role!", 403

@main.route('/admin_dashboard')
def admin_dashboard():
    #fetch all parking lots from database
    lots_data = ParkingLot.query.all()
    return render_template('admin_dashboard/adminUI.html', Lots=lots_data, SpotStatus=SpotStatus)

@main.route('/user_dashboard')
def user_dashboard():
    if 'user_id' not in session or session.get('role') != 'user':
        return redirect(url_for('main.login'))
    # fetch all lots and reservation for thr logged in user
    lots = ParkingLot.query.all()
    reserve = Reservation.query.filter_by(user_id=session['user_id']).all()
    return render_template('user_dashboard/user_dashboard.html', lots=lots, reservations=reserve, SpotStatus=SpotStatus)
# define this rote to show and handle the login page
@main.route('/login', methods=['GET', 'POST'])
def login():
    if "username" and "role" in session:
        return redirect(url_for('main.home'))

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        if len(password) > 10:
            return "Error: Password must not exceed 10 characters."
        # check if user exists in database and match tje password

        user = User.query.filter_by(email=email).first()
        if user and user.password == password:
            session['user_id'] = user.id
            session['username'] = user.username
            session['role'] = user.role
            flash('Login successful!', 'success')

            if user.role == 'admin':
                return redirect(url_for('main.admin_dashboard'))
            else:
                return redirect(url_for('main.user_dashboard'))
        else:
            flash('Invalid email or password', 'danger')

    return render_template('login.html')

@main.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully.', 'success')
    return redirect(url_for('main.login'))

@main.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        email = request.form['email']
        address = request.form['address']
        state = request.form['state']
        city = request.form['city']

        if password != confirm_password:
            flash('Passwords do not match.', 'danger')
            return redirect(url_for('main.signup'))
        # check if the username and email are allready taken or not
        if User.query.filter_by(username=username).first():
            flash('Username already taken.', 'danger')
            return redirect(url_for('main.signup'))

        if User.query.filter_by(email=email).first():
            flash('Email already registered.', 'danger')
            return redirect(url_for('main.signup'))

        new_user = User(
            username=username,
            password=password,
            email=email,
            address=address,
            state=state,
            city=city,
            role='user'
        )

        db.session.add(new_user)
        db.session.commit()
        flash('Signup successful! Please login.', 'success')
        return redirect(url_for('main.login'))

    return render_template('sign_up.html', form_fields=form_fields, stateCityMap=stateCityMap)

# this route is used to fetch all the users from database and display them in admin dashboard
@main.route('/fetchUser')
def fetch_user():
    users = User.query.all()
    return render_template('admin_dashboard/user_list/user_list.html', users=users)

# this route is used to edit the user details by admin
@main.route('/users/edit/<int:id>', methods=['GET', 'POST'])
def edit_user(id):
    user = User.query.get_or_404(id)
    if request.method == 'POST':
        user.username = request.form['username']
        user.password = request.form['password']
        user.email = request.form['email']
        user.address = request.form['address']
        user.state = request.form['state']
        user.city = request.form['city']

        db.session.commit()
        flash('User details updated.', 'success')
        return redirect(url_for('main.home'))

    return render_template('sign_up.html', user=user, form_fields=form_fields, stateCityMap=stateCityMap)

# this route is used to handle the query for lots
@main.route('/search', methods=['GET', 'POST'])
def search():
    results = []
    search_by = request.args.get('search_by', '') or request.form.get('search_by', '')
    query = request.args.get('query', '').strip() or request.form.get('query', '').strip()

    user_fields = ['user_id', 'username', 'user_email', 'user_address', 'user_city', 'user_state']
    lot_fields = ['lot_id', 'prime_location_name', 'lot_address', 'pin_code']
    spot_fields = ['spot_id', 'spot_status']
    reservation_fields = ['reservation_id', 'reservation_user_id', 'reservation_spot_id']

    if search_by in user_fields:
        parent_field = 'user'
    elif search_by in lot_fields:
        parent_field = 'lot'
    elif search_by in spot_fields:
        parent_field = 'spot'
    elif search_by in reservation_fields:
        parent_field = 'reservation'
    else:
        parent_field = None

    user_id = session.get('user_id')
    user_role = session.get('role')

    if user_role == 'admin':
        if search_by == 'user_id' and query.isdigit():
            results = User.query.filter(User.id == int(query)).all()
        elif search_by == 'username':
            results = User.query.filter(User.username.ilike(f"%{query}%")).all()
        elif search_by == 'user_email':
            results = User.query.filter(User.email.ilike(f"%{query}%")).all()
        elif search_by == 'user_address':
            results = User.query.filter(User.address.ilike(f"%{query}%")).all()
        elif search_by == 'user_city':
            results = User.query.filter(User.city.ilike(f"%{query}%")).all()
        elif search_by == 'user_state':
            results = User.query.filter(User.state.ilike(f"%{query}%")).all()
        elif search_by == 'lot_id' and query.isdigit():
            results = ParkingLot.query.filter(ParkingLot.id == int(query)).all()
        elif search_by == 'prime_location_name':
            results = ParkingLot.query.filter(ParkingLot.prime_location_name.ilike(f"%{query}%")).all()
        elif search_by == 'lot_address':
            results = ParkingLot.query.filter(ParkingLot.address.ilike(f"%{query}%")).all()
        elif search_by == 'pin_code':
            results = ParkingLot.query.filter(ParkingLot.pin_code.ilike(f"%{query}%")).all()
        elif search_by == 'spot_id' and query.isdigit():
            results = ParkingSpot.query.filter(ParkingSpot.id == int(query)).all()
        elif search_by == 'spot_status':
            results = ParkingSpot.query.filter(ParkingSpot.status == query.upper()).all()
        elif search_by == 'reservation_id' and query.isdigit():
            results = Reservation.query.filter(Reservation.id == int(query)).all()
        elif search_by == 'reservation_user_id' and query.isdigit():
            results = Reservation.query.filter(Reservation.user_id == int(query)).all()
        elif search_by == 'reservation_spot_id' and query.isdigit():
            results = Reservation.query.filter(Reservation.spot_id == int(query)).all()

    elif user_role == 'user':
        if search_by in ['reservation_user_id', 'reservation_id', 'reservation_spot_id']:
            if search_by == 'reservation_user_id' and query.isdigit() and int(query) == user_id:
                results = Reservation.query.filter(Reservation.user_id == user_id).all()
            elif search_by == 'reservation_id' and query.isdigit():
                reservation = Reservation.query.filter(Reservation.id == int(query), Reservation.user_id == user_id).first()
                if reservation:
                    results = [reservation]
            elif search_by == 'reservation_spot_id' and query.isdigit():
                results = Reservation.query.filter(Reservation.spot_id == int(query), Reservation.user_id == user_id).all()
        else:
            flash("You don't have access to this data.", "danger")
            return redirect(url_for('main.search'))
    else:
        flash("Please log in to continue.", "danger")
        return redirect(url_for('main.login'))

    return render_template('search.html', results=results, search_by=search_by, query=query, parent_field=parent_field, SpotStatus=SpotStatus)

@main.route('/add_lot', methods=['POST'])
def add_lot():
    prime_location_name = request.form['prime_location_name']
    address = request.form['address']
    pin_code = request.form['pin_code']
    price = float(request.form['price'])
    max_spots = int(request.form['maximum_number_of_spots'])

    lot = ParkingLot(
        prime_location_name=prime_location_name,
        address=address,
        pin_code=pin_code,
        price=price,
        maximum_number_of_spots=max_spots
    )
    db.session.add(lot)
    db.session.flush()

    for _ in range(max_spots):
        spot = ParkingSpot(lot_id=lot.id, status=SpotStatus.AVAILABLE)
        db.session.add(spot)

    db.session.commit()
    flash('New lot and spots added.', 'success')
    return redirect(url_for('main.admin_dashboard'))

@main.route('/edit_lot/<int:lot_id>', methods=['POST'])
def edit_lot(lot_id):
    lot = ParkingLot.query.get_or_404(lot_id)
    lot.prime_location_name = request.form['prime_location_name']
    lot.address = request.form['address']
    lot.pin_code = request.form['pin_code']
    lot.price = float(request.form['price'])
    new_spots_len = int(request.form['maximum_number_of_spots'])

    current_spots = len(lot.spots)
    lot.maximum_number_of_spots = new_spots_len
    db.session.commit()

    if new_spots_len > current_spots:
        for _ in range(new_spots_len - current_spots):
            db.session.add(ParkingSpot(lot_id=lot.id, status=SpotStatus.AVAILABLE))
    elif new_spots_len < current_spots:
        to_remove = current_spots - new_spots_len
        available_spots = [s for s in lot.spots if s.status == SpotStatus.AVAILABLE][:to_remove]
        for s in available_spots:
            db.session.delete(s)

    db.session.commit()
    flash('Lot updated successfully.', 'success')
    return redirect(request.referrer or url_for('main.admin_dashboard'))

@main.route('/delete_lot/<int:lot_id>', methods=['POST'])
def delete_lot(lot_id):
    lot = ParkingLot.query.get_or_404(lot_id)
    if any(s.status == SpotStatus.OCCUPIED for s in lot.spots):
        flash('Lot contains occupied spots and cannot be deleted.', 'danger')
        return redirect(request.referrer or url_for('main.admin_dashboard'))

    db.session.delete(lot)
    db.session.commit()
    flash('Lot deleted successfully.', 'success')
    return redirect(request.referrer or url_for('main.admin_dashboard'))

@main.route('/delete_spot/<int:spot_id>', methods=['POST'])
def delete_spot(spot_id):
    spot = ParkingSpot.query.get_or_404(spot_id)
    if spot.reservations:
        flash('This spot has reservations and cannot be removed.', 'danger')
        return redirect(request.referrer or url_for('main.admin_dashboard'))

    lot = spot.lot
    db.session.delete(spot)
    db.session.commit()
    lot.maximum_number_of_spots = len(lot.spots)
    db.session.commit()
    flash('Spot removed.', 'success')
    return redirect(request.referrer or url_for('main.admin_dashboard'))

def validate_session():
    if 'user_id' not in session or 'role' not in session:
        flash('Please log in first.', 'warning')
        return redirect(url_for('main.login'))
    return None


@main.route('/reserve/<int:lot_id>', methods=['POST'])
def reserve_spot(lot_id):
    if 'user_id' not in session or session.get('role') != 'user':
        return redirect(url_for('main.login'))

    lot = ParkingLot.query.get_or_404(lot_id)
    spot = ParkingSpot.query.filter_by(lot_id=lot.id, status=SpotStatus.AVAILABLE).first()

    if not spot:
        flash('No empty spots available right now.', 'danger')
        return redirect(url_for('main.user_dashboard'))

    vehicle_no = request.form.get('vehicle_no')

    reservation = Reservation(
        spot_id=spot.id,
        user_id=session['user_id'],
        parking_timestamp=datetime.datetime.now(),
        parking_cost=0,
        vehicle_number=vehicle_no
    )

    spot.status = SpotStatus.OCCUPIED
    db.session.add(reservation)
    db.session.commit()

    flash(f'Spot #{spot.id} has been reserved!', 'success')
    return redirect(url_for('main.user_dashboard'))

@main.route('/release/<int:reservation_id>', methods=['POST'])
def release_spot(reservation_id):
    reservation = Reservation.query.get_or_404(reservation_id)
    if reservation.user_id != session.get('user_id'):
        flash('Access denied.', 'danger')
        return redirect(url_for('main.user_dashboard'))

    if reservation.leaving_timestamp:
        flash('This reservation is already closed.', 'info')
        return redirect(url_for('main.user_dashboard'))

    reservation.leaving_timestamp = datetime.datetime.now()
    lot = reservation.spot.lot
    duration_hours = (reservation.leaving_timestamp - reservation.parking_timestamp).total_seconds() / 3600
    reservation.parking_cost = round(duration_hours * 60 * lot.price, 2)
    reservation.spot.status = SpotStatus.AVAILABLE
    db.session.commit()

    flash(f'Spot released. Total charge: ₹{reservation.parking_cost}', 'success')
    return redirect(url_for('main.user_dashboard'))

