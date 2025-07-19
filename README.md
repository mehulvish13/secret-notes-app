# 📒 Secret Notes App – Single Page Flask Application

A secure and lightweight **Flask web app** to manage private notes with CRUD operations, password-protected sharing, and client-side search.

This project uses **only one HTML template (`index.html`)** for all views, simplifying layout management.

---

## 🚀 Features

| Feature                   | Description                                          |
|---------------------------|------------------------------------------------------|
| 🔐 **Login System**        | Single-author login with Flask session management     |
| 📝 **CRUD Operations**     | Create, read, update, and delete notes               |
| 🔗 **Note Sharing**        | Share notes securely via password-protected links    |
| 🔍 **Client-side Search**  | Real-time note filtering in the dashboard            |
| 📅 **Timestamps**          | Each note has `created_at` and `updated_at`          |
| 🗃️ **JSON Storage**        | No database; uses `notes.json` for persistence       |
| 🎨 **Custom Styling**      | Styled with `static/style.css`                       |
| 🧩 **Single HTML File**    | All views handled in `templates/index.html`          |

---

## 🧱 Project Structure

```
secret-notes-app/
├── app.py               # Flask backend
├── notes.json           # Data storage (JSON file)
├── requirements.txt     # Python dependencies
├── static/
│   └── style.css        # Custom CSS styling
└── templates/
    └── index.html      # Single-page HTML template (all views)
```

---

## 🛠️ Getting Started

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/yourusername/secret-notes-app.git
cd secret-notes-app
```

### 2️⃣ Create a Virtual Environment (Recommended)

```powershell
python -m venv venv
venv\Scripts\activate
```

### 3️⃣ Install Dependencies

```powershell
pip install -r requirements.txt
```

### 4️⃣ Run the Application

```powershell
python app.py
```

Visit: http://localhost:5000

---

## 🔑 Default Login Credentials

Set in `app.py`:

```python
AUTHOR_USERNAME = "author"
AUTHOR_PASSWORD_HASH = hashlib.sha256('your-password'.encode()).hexdigest()
```

> **Note:** Replace `'your-password'` with your own secure password. The password is hashed using SHA256 for security.

---

## 🔗 Sharing Notes Securely

Click **Share** on a note to set a password.
A secure URL like `/shared/<uuid>` will be generated.
Anyone with the link must enter the correct password to view the note.

---

## 📦 Requirements

Minimal dependencies:

```ini
Flask==3.1.1
```

To regenerate `requirements.txt`:

```powershell
pip freeze > requirements.txt
```

---

## 🌍 Deployment Guide (Render.com)

Push your project to GitHub.

On Render.com:
- Create a Web Service
- Build Command:
  ```powershell
  pip install -r requirements.txt
  ```
- Start Command:
  ```powershell
  python app.py
  ```

---

## 🎯 Optional Features & Roadmap

| Feature                | Status    |
|------------------------|-----------|
| 🌙 Dark Mode           | 🔲 Optional|
| 📝 Markdown Support    | 🔲 Optional|
| 🗂️ SQLite Upgrade      | 🔲 Optional|
| ⏳ Expiring Share Links| 🔲 Optional|
| 📎 File Attachments    | 🔲 Optional|
| 💾 Auto-save while typing| 🔲 Optional|