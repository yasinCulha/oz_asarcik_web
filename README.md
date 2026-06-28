Öz Asarcık - Driving School Automation & Web Management System 🚗💨
This project is a hybrid (Desktop + Web) automation system developed to both streamline the desktop management processes of a driving school (trainee tracking, classroom management, exam questions) and establish the school's digital presence (live website, WhatsApp integration, dynamic management panel).

The Desktop and Web applications communicate with each other in real-time through a shared, cloud-based database architecture.

🛠️ Technologies & Architecture
💻 Desktop Automation (Desktop Application)
Language / Framework: C# | .NET Windows Forms

Database Driver: Npgsql (PostgreSQL Client)

Architectural Structure: Dynamic lifecycle management between forms (FormClosed and main thread optimizations have been implemented).

Deployment Mode: Portable - Can run directly from a flash drive on any computer with an internet connection, requiring no installation.

🌐 Website & Management Panel (Web Application)
Backend Framework: Python | Django MVT

Database / ORM: Django ORM & PostgreSQL

Deployment (Live): Render Cloud Platform

Additional Features: Dynamic WhatsApp redirection system, responsive (mobile-friendly) interface, static file (WhiteNoise) optimizations.

☁️ Cloud Database
Infrastructure: Neon Tech (Serverless PostgreSQL)

Feature: Both the C# desktop application and the Django website fetch and update data instantly through a shared database schema.

🚀 Project Features
👨‍💼 Desktop Panel Features
Trainee Management: Trainee registration, listing, and status update operations.

Classroom & Tab Management: Screens optimized with dynamic transitions between classrooms and clean memory management.

Exam Question Pool: Listing and managing thousands of rows of question pools migrated from local databases to the cloud for driving school exams.

🕸️ Website Features
Dynamic WhatsApp Button: A quick-action button optimized for international number formats, allowing clients to contact the school directly.

Advanced Management Panel: Ability to update all course content, exam questions, and contact information live via the Django Admin panel.

---

⚙️ Installation and Setup
1. Running the Web Project Locally
Bash
# Clone the project
git clone https://github.com/yasinCulha/oz_asarcik_web.git

# Navigate to the project directory
cd oz_asarcik_web

# Install required dependencies
pip install -r requirements.txt

# Run database migrations
python manage.py migrate

# Start the development server
python manage.py runserver

# Veritabanı geçişlerini yapın
python manage.py migrate

# Projeyi ayağa kaldırın
python manage.py runserver
