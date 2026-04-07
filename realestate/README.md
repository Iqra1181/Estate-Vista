# 🏠 EstateVista — Real Estate Web Application

A full-stack real estate web application built with **Python Flask**, **SQLite**, and **Bootstrap 5**. Designed as a complete, beginner-friendly project that looks and works like a production app.

---

## 📁 Project Structure

```
realestate/
├── app.py                  # Main Flask app — configuration, startup, seed data
├── models.py               # Database models (User, Property, Favorite, Inquiry)
├── requirements.txt        # Python dependencies
│
├── routes/                 # Route handlers (split by feature)
│   ├── __init__.py
│   ├── auth.py             # Signup, Login, Logout
│   ├── properties.py       # Listings, Detail, Add, Price Estimator
│   ├── favorites.py        # Save/Unsave properties
│   ├── inquiries.py        # Contact / Inquiry system
│   └── analytics.py        # Chart data APIs
│
├── templates/              # Jinja2 HTML templates
│   ├── base.html           # Master layout (navbar, footer, dark mode)
│   ├── index.html          # Home page — listings + search + filters
│   ├── detail.html         # Property detail page
│   ├── add_property.html   # Add new property form
│   ├── favorites.html      # Saved properties
│   ├── inquiries.html      # Inquiries inbox
│   ├── analytics.html      # Charts & data visualization
│   └── auth/
│       ├── login.html
│       └── signup.html
│
├── static/
│   ├── css/
│   │   └── style.css       # All custom styles + dark mode CSS variables
│   ├── js/
│   │   └── main.js         # Dark mode toggle, favorites, utility functions
│   └── uploads/            # User-uploaded property images (auto-created)
│
└── instance/
    └── realestate.db       # SQLite database (auto-created on first run)
```

---

## 🗃️ Database Tables

| Table        | Description                                      |
|--------------|--------------------------------------------------|
| `users`      | Registered users — name, email, hashed password |
| `properties` | Property listings — all details + owner         |
| `favorites`  | Saves which user bookmarked which property       |
| `inquiries`  | Contact messages from users to property owners  |

---

## ✨ Features

### Core
- 📋 Responsive property card grid layout
- 🔍 Search by location
- 🔽 Filter by type (rent/sale) and price range
- ↕️ Sort by price (low→high, high→low)
- 📄 Pagination (6 properties per page)
- 📝 Add new property with image upload or URL

### Intermediate
- ❤️ Favorites system (save/unsave with instant toggle)
- 🔐 User authentication (signup, login, logout, sessions)
- 🔒 Password hashing with Werkzeug
- 📍 Google Maps embed on property detail pages
- 🌙 Dark mode toggle (persists in localStorage)
- 🆕 Recently added properties section
- 📩 Contact/Inquiry system with inbox for owners

### Advanced
- 📊 Price Estimator (formula-based by city × size)
- 🧠 Smart Recommendations (similar location/price)
- 📈 Analytics Dashboard with 3 Chart.js charts
- 📸 Image file upload + URL support
- 🌐 RESTful JSON APIs for chart data

---

## 🚀 How to Run Locally

### Step 1 — Clone / Download the project
```bash
git clone https://github.com/yourusername/estatevista.git
cd estatevista
```

### Step 2 — Create a virtual environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3 — Install dependencies
```bash
pip install -r requirements.txt
```

### Step 4 — Run the app
```bash
python app.py
```

### Step 5 — Open in browser
Visit: **http://127.0.0.1:5000**

> ✅ The database is created automatically on first run.
> ✅ 12 sample properties are seeded automatically.
> ✅ Demo login: `demo@realestate.com` / `password123`

---

## 📖 How Each Feature Works (for Viva)

### Flask Blueprints
Instead of putting all routes in one file, we split them into **Blueprints** — each Blueprint is like a mini Flask app for a specific feature. This keeps the code clean and modular.

```python
# In app.py — registering blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(properties_bp)
```

### SQLAlchemy ORM
We use **SQLAlchemy** to work with the database using Python classes instead of raw SQL. Each class = one table.
```python
class Property(db.Model):
    id    = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    price = db.Column(db.Float)
    ...
```

### Flask Sessions
Sessions store data between requests. When a user logs in, we save their ID:
```python
session['user_id'] = user.id  # Login
session.clear()               # Logout
```

### Jinja2 Templating
HTML templates use `{% %}` for logic and `{{ }}` for values:
```html
{% for prop in properties %}
  <h6>{{ prop.title }}</h6>
{% endfor %}
```

### Dark Mode
CSS variables change based on `data-theme` attribute on `<html>`. JavaScript toggles the attribute and saves to `localStorage` for persistence.

### Price Estimator
A simple API endpoint at `/estimate-price`:
- Input: location + size (sq ft)
- Logic: `estimated_price = size × rate_per_sqft`
- Rate varies by city (Mumbai=₹18,000, Jaipur=₹6,500, etc.)
- JavaScript calls this with `fetch()` and shows result without page reload

### Smart Recommendations
On the detail page, we query for properties that share the same location OR have a price within ±30% of the current property.

### Chart.js Analytics
- `analytics.html` defines `<canvas>` elements
- JavaScript fetches JSON from Flask APIs (`/api/avg-price-by-location`, etc.)
- Chart.js draws interactive bar, doughnut, and horizontal bar charts

---

## ☁️ Deploying to Render (Free Hosting)

### Step 1 — Add a `gunicorn` dependency
```bash
pip install gunicorn
pip freeze > requirements.txt
```

### Step 2 — Create `Procfile` (no extension)
```
web: gunicorn app:create_app()
```

### Step 3 — Update `app.py` for production
Change the secret key to an environment variable:
```python
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'fallback_key')
```

### Step 4 — Push to GitHub
```bash
git init
git add .
git commit -m "Initial commit: EstateVista"
git branch -M main
git remote add origin https://github.com/yourusername/estatevista.git
git push -u origin main
```

### Step 5 — Deploy on Render
1. Go to [render.com](https://render.com) → Sign up / Log in
2. Click **New → Web Service**
3. Connect your GitHub repository
4. Configure:
   - **Runtime**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn "app:create_app()"`
5. Add environment variable: `SECRET_KEY` → any random string
6. Click **Deploy** 🚀

> ⚠️ Note: Render's free tier uses an ephemeral filesystem — uploaded images won't persist. For production, use **Cloudinary** or **AWS S3** for image storage.

---

## 📦 Pushing to GitHub

```bash
# First time
git init
git add .
git commit -m "feat: complete EstateVista real estate app"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/estatevista.git
git push -u origin main

# Future updates
git add .
git commit -m "fix: describe what you changed"
git push
```

---

## 🛠️ Tech Stack Summary

| Layer      | Technology                         |
|------------|-------------------------------------|
| Backend    | Python 3, Flask 3.x                |
| Database   | SQLite + SQLAlchemy ORM            |
| Frontend   | HTML5, CSS3, JavaScript (ES6+)     |
| UI Library | Bootstrap 5 + Bootstrap Icons      |
| Charts     | Chart.js 4                         |
| Auth       | Flask Sessions + Werkzeug hashing  |
| Maps       | Google Maps Embed API (free)       |
| Fonts      | Google Fonts (Playfair Display + DM Sans) |

---

## 👨‍💻 Built by

A 2nd-year Computer Science student as a full-stack portfolio project.

**Skills demonstrated:** Flask routing, SQLAlchemy ORM, REST APIs, session-based auth, password hashing, file uploads, responsive design, dark mode, Chart.js, and deployment.
