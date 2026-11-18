# This project is a course project for "Software Documentation and Design Patterns"

## Project Structure

The project consists of two main parts:

* `backend/` — the server-side application built with Python Flask. Responsible for the REST API, authentication, managing users, doctors, appointments, reminders, reports and interaction with PostgreSQL.
* `frontend/` — the client-side application built with Vue.js. Responsible for the user interface for patients, doctors and administrators.

Main structure:

```text
backend/
├── app/
│   ├── models/
│   ├── routes/
│   ├── services/
│   ├── patterns/
│   └── utils/
├── migrations/
├── .env
├── requirements.txt
├── seed.py
└── run.py

frontend/
├── src/
│   ├── assets/
│   ├── components/
│   ├── router/
│   ├── services/
│   ├── stores/
│   └── views/
├── .env
├── package.json
└── vite.config.js
```

The project uses three design patterns:
* Strategy — for selecting the method of sending reminders via email or SMS.
* Observer — for reacting to registration and appointment creation events.
* State — for managing appointment states (scheduled, completed, cancelled).

## Prerequisites
* Have Python 3 installed
* Have Vue.js installed
* Have Terraform installed
* Have AWS CLI installed
* Have an AWS account and be logged into it through AWS CLI

## How to Run?
* `cd <path to the folder where you saved this repository>/terraform`
* `terraform init`
* `terraform apply --auto-approve`
* In your AWS account, in addition to RDS, a secret named `doctor-appointment-system/postgres` will be created. You will retrieve values from it later.
* Create the file `<path to the folder where you saved the project>/backend/.env`
* Add the required changes to it (see below)
* `cd <path to the folder where you saved this repository>/backend`
* `pip install -r requirements.txt`
* `flask --app run.py db init`
* `flask --app run.py db migrate -m "Initial migration"`
* `flask --app run.py db upgrade`
* `python seed.py`
* `python run.py`
* Create the file `<path to the folder where you saved the project>/frontend/.env`
* Add the required changes to it (see below)
* Open a new terminal window (keep the previous window open)
* `cd <path to the folder where you saved this repository>/frontend`
* `npm install`
* `npm run dev`
* Open your browser, go to `http://localhost:5173` and that's it.
* Note: To log in as a patient, register a new user and log in with that account. To log in as a doctor, use the example doctor account (email: `doctor1@medbook.com`, password: `Doctor123!`). To log in as an administrator, use email: `admin@medbook.com`, password: `Admin123!`.

## What Variables Should Be Added to `frontend/.env`?
* Only one variable is required here:
`VITE_API_URL=<URL where the backend is running>`

## What Variables Should Be Added to `backend/.env`?
* More variables are required here:

```env
FLASK_ENV=development - optional
FLASK_DEBUG=true - optional

SECRET_KEY=<Your Secret Key>
JWT_SECRET_KEY=<Your JWT Secret Key>

DB_HOST=<URL of your database in AWS (host)>
DB_PORT=<port of your database in AWS (port)>
DB_NAME=<name of your database in AWS (database)>
DB_USER=<your database username in AWS (username)>
DB_PASSWORD=<password of your database in AWS (password)>

FRONTEND_URL=<URL where the frontend is running>

REMINDER_HOURS_BEFORE=<number of hours before the reminder (0 - immediately)>

SMTP_HOST=<SMTP URL>
SMTP_PORT=<SMTP port>
SMTP_USER=(SMTP username)
SMTP_PASSWORD=(SMTP password)
SMTP_FROM=(email address from which messages will be sent)

TWILIO_ACCOUNT_SID=<Twilio SID for Twilio>
TWILIO_AUTH_TOKEN=<Auth Token for Twilio>
TWILIO_PHONE_NUMBER=<phone number for Twilio>
```