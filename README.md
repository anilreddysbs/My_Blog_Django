# My Blog Django

A simple blog web application built with Django. Users can read, create, edit, and delete blog posts through a clean web interface.

## Features

- User authentication (login, logout, register)
- Create, edit, and delete blog posts
- List and detail views for posts
- Responsive design with Bootstrap (if used)
- Admin panel for managing posts and users

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/anilreddysbs/My_Blog_Django.git
   cd My_Blog_Django
   ```

2. **Create and activate a virtual environment (optional but recommended):**
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
   *(If `requirements.txt` is missing, install Django manually: `pip install django`)*

4. **Apply migrations:**
   ```bash
   python manage.py migrate
   ```

5. **Create a superuser (admin):**
   ```bash
   python manage.py createsuperuser
   ```

6. **Run the development server:**
   ```bash
   python manage.py runserver
   ```

7. **Open your browser and visit:**  
   [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

## Usage

- Register a new user or log in with your credentials.
- Create, edit, and delete your blog posts.
- Access the admin panel at `/admin/` for advanced management.

## Folder Structure

```
My_Blog_Django/
├── blog/           # Django app for blog logic
├── my_blog/        # Django project settings
├── templates/      # HTML templates
├── static/         # Static files (CSS, JS, images)
├── manage.py
└── requirements.txt
```

## Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.

## License

[MIT](LICENSE)

---

*Start your own blog with Django!*
