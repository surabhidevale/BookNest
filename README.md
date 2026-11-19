# BookNest – Online Bookstore & Book Rental Platform

BookNest is a Django-based web application designed to make buying, browsing, and renting books easier. It provides users with a platform to explore books, view book details, and manage their shopping experience.

## Live Demo

[Visit BookNest](https://surabhi172.pythonanywhere.com/)

## Features

- Browse books by category.
- View book details, descriptions, and prices.
- Preview books through available preview links.
- Explore used books available for buying or renting.
- Add books to the shopping cart.
- Manage cart items and quantities.
- User registration and login.
- Checkout functionality.
- Admin panel for managing book information.

## Technologies Used

- **Backend:** Python, Django
- **Frontend:** HTML, CSS, Bootstrap, JavaScript
- **Database:** Django-supported database
- **Tools:** PyCharm, Git, GitHub

## Project Structure

```text
BookNest/
│
├── BookNest/
├── CoreApp/
├── Static/
├── media/
├── templates/
├── manage.py
├── requirements.txt
├── .gitignore
└── README.md
```

## Installation and Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/surabhidevale/BookNest.git
   ```

2. Navigate to the project directory:

   ```bash
   cd BookNest
   ```

3. Create and activate a virtual environment:

   ```bash
   python -m venv .venv
   ```

   Windows:

   ```bash
   .venv\Scripts\activate
   ```

4. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

5. Create a `.env` file in the project root and configure your Django secret key:

   ```text
   SECRET_KEY=your-secret-key
   ```

6. Apply database migrations:

   ```bash
   python manage.py migrate
   ```

7. Start the development server:

   ```bash
   python manage.py runserver
   ```

8. Open the application in your browser:

   `http://127.0.0.1:8000/`

## Author

**Surabhi Devale**

- GitHub: [surabhidevale](https://github.com/surabhidevale)

---

*BookNest – Making books more accessible, one page at a time.*
