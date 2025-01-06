# 📚 Library Service

🎉Welcome to the **Library Service API**! This system allows you to manage books, users, and borrowings effectively. It's designed to track books, handle borrow requests, and process payments.

---

## ⚙️ Features

- **✨ Book Management**: Add, update, and delete books in the library.
- **👤 User Registration**: Users can register, log in, and manage their profiles.
- **📖 Borrowing System**: Users can borrow books with an automated return and fee calculation.
- **💳 Payment Tracking**: Keeps track of payments for borrowings.

---

## 🚀 Technologies Used

- **🐍 Django** for backend API
- **🐘 PostgreSQL** for database
- **🔧 Django Rest Framework (DRF)** for API development
- **⏳ Django Celery** for background tasks
- **💳 Stripe** for payment processing
- **📱 Telegram API** for notifications
- **🐋 Docker** for containerization

---

# 🛠️ Setup

## 📝 Prerequisites
* Python 3.12.8+
* Poetry
* Docker & Docker Compose

## **Local** Setup

Follow these steps to set up the project locally. 💻

### 1. 🖇️ Clone the Repository
Clone the repository to your local machine using Git:

```bash
git clone https://github.com/dmytrik/LibraryServiceAPI.git
cd LibraryServiceAPI
```

### 2. 📄 Create a `.env` File
Create a `.env` file based on the `.env.sample` file. You can do this by copying the `.env.sample` to `.env`:

```bash
cp .env.sample .env
```

### 3. 📦 Install Dependencies
Use Poetry to install the necessary dependencies:
```bash
poetry install
```

### 4. 🔄 Apply Migrations
Run the migrations to set up the database schema:
```bash
python manage.py migrate
```

### 5. Install Redis
Redis is required for Celery task management. Follow the instructions for your operating system:
### MacOS:
```bash
brew install redis  
```
Start Redis:
```bash
redis-server
```

### Linux (Ubuntu):
```bash
sudo apt update  
sudo apt install redis-server  
sudo systemctl enable redis  
sudo systemctl start redis  
```

### Windows:
1. Download the Redis installer from [here](https://github.com/microsoftarchive/redis/releases)
2. Install Redis and start the server by running:
```bash
redis-server
```

### 6. 📚 Start Celery Workers and Beat
Start Celery worker and beat scheduler to handle background tasks:
#### Start Celery Worker:
```bash
celery -A core worker --loglevel=info --pool=solo  
```

#### Start Celery Beat:
```bash
celery -A core beat --loglevel=info
```

### 7. 🚀 Start the Server
Run the Django development server:
```bash
python manage.py runserver
```

🌐 Your server will be available at: http://localhost:8000/

---

## 🐋 Running with **Docker**

If you'd like to run the project using Docker, follow the steps below. 🐳

### 1. 🔧 Build and Start the Services
Use Docker Compose to build and run the application and database containers:
```bash
docker-compose up --build
```

### 2. 🌐 Access the API
Once the services are up, the API will be available at: http://localhost:8000/

The PostgreSQL database will be available on port `5432`.

---
## 📚 Components

### 1. 📕 **Books Service**:  
Manages the quantity of books in the library.

- **POST** `/api/books/` - Add a new book  
- **GET** `/api/books/` - Get a list of all books  
- **GET** `/api/books/<id>/` - Get detailed information about a specific book  
- **PUT/PATCH** `/api/books/<id>/` - Update a book (also manages inventory)  
- **DELETE** `/api/books/<id>/` - Delete a book

### 2. 👤 **Users Service**:  
Manages authentication and user registration.

- **POST** `/api/users/register/` - Register a new user  
- **POST** `/api/users/token/` - Get JWT tokens  
- **POST** `/api/users/token/refresh/` - Refresh JWT token  
- **GET** `/api/users/me/` - Get current user profile information  
- **PUT/PATCH** `/api/users/me/` - Update user profile information  

### 3. 📖 **Borrowings Service**:  
Manages users' borrowing actions and keeps track of borrowed books.

- **POST** `/api/borrowings/` - Add a new borrowing (decrease inventory by 1 when borrowing a book)  
- **GET** `/api/borrowings/?user_id=<user_id>&is_active=<active_status>` - Get borrowings by user id and active status  
- **GET** `/api/borrowings/<id>/` - Get specific borrowing details  
- **POST** `/api/borrowings/<id>/return/` - Set the actual return date (increase inventory by 1 when book is returned)  

### 4. 📲 **Notifications Service (Telegram)**:  
Notifies about new borrowings and overdue borrowings.

- Uses Django Celery to manage background tasks.
- Interacts with other services to send notifications to library administrators.
- Leverages Telegram API, Chats, and Bots for communication.

### 5. 💳 **Payments Service (Stripe)**:  
Handles payments for book borrowings via Stripe.

- **GET** `/api/payments/` -
- **GET** `/api/payments/{id}/` -
- **GET** `/api/payments/success/` - Check for successful Stripe payment  
- **GET** `/api/payments/cancel/` - Return a message if the payment was paused or canceled

### 6. 🖥️ **View Service**:  
- Delegated to the Front-end Team (Not implemented in this repository).  
- Provides the user interface for interacting with the library system.

---

## 📄 Documentation
API documentation is available via Redoc at:

🌐 `http://localhost:8000/api/schema/redoc/`

and via Swagger at:

🌐 `http://localhost:8000/api/schema/swagger-ui/`

---

## 📅 Contributing

1. Fork the repository
2. Create a new branch (`git checkout -b feature-name`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature-name`)
5. Open a pull request

---

🚀 Happy Coding and enjoy building with **Library Service API**! 🎉