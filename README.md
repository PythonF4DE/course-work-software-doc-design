# Цей проект це курсова робота з "Документування програмного забезпечення та шаблони проектування"

## Структура проекту

Проект складається з двох основних частин:

* `backend/` — серверна частина на Python Flask. Відповідає за REST API, авторизацію, роботу з користувачами, лікарями, записами, нагадуваннями, звітами та взаємодію з PostgreSQL.
* `frontend/` — клієнтська частина на Vue.js. Відповідає за користувацький інтерфейс для пацієнтів, лікарів і адміністратора.

Основна структура:

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

У проекті використовуються три шаблони проектування:
* Strategy — для вибору способу надсилання нагадувань через e-mail або SMS.
* Observer — для реакції системи на події реєстрації та створення записів.
* State — для керування станами запису до лікаря (scheduled, completed, cancelled).

## Попередні вимоги
* Мати завантажений python 3
* Мати завантажений Vue.js
* Мати завантажений Terraform
* Мати завантажений AWS CLI
* Мати AWS акаунт та залогіниись в нього через AWS CLI

## Як запустити?
* `cd <папка куди Ви зберегли цей репозиторій>/terraform`
* `terraform init`
* `terraform apply --auto-approve`
* У вашому AWS окрім RDS створиться secret `doctor-appointment-system/postgres`, пізніше Ви братимите з нього значення.
* Створіть файл `<шлях до папки, де Ви зберегли проект>/backend/.env`
* Додайте до нього потрібні зміни (дивіться нижче)
* `cd <папка куди Ви зберегли цей репозиторій>/backend`
* `pip install -r requirements.txt`
* `flask --app run.py db init`
* `flask --app run.py db migrate -m "Initial migration"`
* `flask --app run.py db upgrade`
* `python seed.py`
* `python run.py`
* Створіть файл `<шлях до папки, де Ви зберегли проект>/frontend/.env`
* Додайте до нього потрібні зміни (дивіться нижче)
* Відкрийте нове вікно у терміналі (залиште поперднє вікно відкритим)
* `cd <папка куди Ви зберегли цей репозиторій>/frontend`
* `npm install`
* `npm run dev`
* Відкрийте браузер, зайдіть на `http://localhost:5173` і це все.
* Примітка: щоб зайти як пацієнт - зареєструйте нового користувача і зайдіть з нього. Щоб зайти як лікар використайте лікаря, який створений як приклад (email: `doctor1@medbook.com`, password: `Doctor123!`). Щоб зайти як адміністратор використайте email: `admin@medbook.com`, password: `Admin123!`.

## Які змінні додати в `frontend/.env`?
* Тут потрібна всього одна змінна:
`VITE_API_URL=<посилання на місце де запущенний backend>`

## Які змінні додати в `backend/.env`?
* Тут потрібно більше змін:
```
FLASK_ENV=development - опціонально
FLASK_DEBUG=true - опціонально

SECRET_KEY=<Ваш Secret Key>
JWT_SECRET_KEY=<Ваш JWT Secret Key>

DB_HOST=<посилання на Вашу БД в AWS (host)>
DB_PORT=<порт Вашої бази даних в AWS (port)>
DB_NAME=<назва Вашої бази даних в AWS (database)>
DB_USER=<Ваш юзернейм для БД в AWS (username)>
DB_PASSWORD=<пароль від Вашої бази даних в AWS (password)>

FRONTEND_URL=<посилання на те де запущений frontend>

REMINDER_HOURS_BEFORE=<кількість годин перед нагадуванням (0 - миттєво)>

SMTP_HOST=<URL для SMTP>
SMTP_PORT=<порт для SMTP>
SMTP_USER=(користувач для SMTP)
SMTP_PASSWORD=(пароль для SMTP)
SMTP_FROM=(пошта, з якої надходитимуть листи)

TWILIO_ACCOUNT_SID=<SID Twilio для Twilio>
TWILIO_AUTH_TOKEN=<Auth Token для Twilio>
TWILIO_PHONE_NUMBER=<номер телефону для Twilio>
```