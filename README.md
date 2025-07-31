# 🚗 Vehicle Parking Management System

## 📖 Project Overview
The Vehicle Parking Management System is a web-based platform developed to efficiently handle parking lot operations, spot allocations, and vehicle reservations. It provides administrators with tools to oversee and control parking areas, while registered users can reserve available spots and manage current bookings with ease.

---

## 📌 Key Features

🛡️ Admin Panel: Create and manage parking lots and monitor user activities.

🚙 User Panel: Reserve parking spots and handle reservation records.

🔑 Login and Role Control: Distinct login access for admin and regular users.

💻 Mobile-Friendly Design: Built with Bootstrap to ensure a smooth experience across devices

## 🛠️ Technologies Used

Flask: Lightweight Python framework used to build the server-side logic of the application

SQLAlchemy with Flask-SQLAlchemy: ORM libraries that help in managing database operations using Python classes

SQLite: Embedded database used for storing all application data locally

Bootstrap: Frontend toolkit used to create responsive and visually appealing UI (loaded via CDN)

Flask-Dotenv & python-dotenv: Tools for managing configuration through environment variables securely

---

## 🚩 Milestones

1. **Database Models and Schema Setup**
   - Defined models for User, ParkingLot, ParkingSpot, and Reservation.
   - Set up relationships and initialized the SQLite database.

2. **Authentication and Role Management**
   - Implemented user registration and login.
   - Role-based access for admin and user dashboards.

3. **Admin Dashboard and Management**
   - Admins can add, edit, and delete parking lots and spots.

4. **User Dashboard and Parking Spot Booking**
   - Users can search for available parking lots and book spots.


5. **Search Functionality**
   - Search for users, lots, spots, and reservations by various fields.
   - Role-based search: admins have full access, users see only their data.

6. **Environment Configuration**
   - Used .env file for configuration and secret management.

---

## 🗂️ Models

User: Holds data related to each user, including login credentials and their access level (admin or regular user).

ParkingLot: Defines each parking location along with its address, pricing, and other relevant details.

ParkingSpot: Denotes individual parking spaces within a lot and their current availability status.

Reservation: Maintains records of spot bookings, including entry/exit times and vehicle-related information.

---


## 🗂️ Folder Structure 🗂️
C:.
│   .env
│   .gitignore
│   run.py
│   db_setup.py
│   models.py
│   README.md
│   requirements.txt
│   routes.py
│   
├───instance
│       parking_app.db
│       
├───static
│   │   constant.py
│   └───__pycache__
│
└───templates
    │   index.html
    │   login.html
    │   navbar.html
    │   search.html
    │   sign_up.html
    │   slide_carousal.html
    ├───admin_dashboard
    │   │   add_parking_lot_modal.html
    │   │   adminUI.html
    │   │   edit_parking_lot_modal.html
    │   │   occupied_parking_spot_detail_modal.html      
    │   │   parking_card_lot.html
    │   │   view_delete_parking_lot_modal.html
    │   └───user_list
    │           user_list.html
    └───user_dashboard
            history.html
            parking_lot.html
            parking_modals.html
            recent_parking_history.html
            releasing_modals.html
            user_dashboard.html
            
## 🗺️ Example ER Diagram

![ER Diagram]()  

