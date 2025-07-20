"""
Secret Notes App - Flask Backend
-------------------------------
This is a secure note-taking application built with Flask that allows users to:
1. Register and login to their accounts
2. Create, read, update, and delete notes
3. Add tags to notes for organization
4. Share notes securely with password protection
5. Search and filter notes by content or tags

File Structure:
- app.py: Main application file (this file)
- templates/index.html: Single page template for all views
- static/style.css: Application styling
- notes.json: Note storage
- users.json: User account storage

Author: Your Name
Version: 1.0.0
"""

# Required Flask modules
from flask import Flask, request, render_template, redirect, url_for, session, jsonify

# Standard library imports
import os          # For file operations
import json        # For JSON data handling
import uuid        # For generating unique IDs for shared notes
import hashlib     # For password hashing
from datetime import datetime  # For timestamp management

# Initialize Flask application
app = Flask(
    __name__,
    static_folder='static',     # Folder for CSS, JS, images
    static_url_path='/static'   # URL path for static files
)

# Secret key for session management (in production, use environment variable)
app.secret_key = "super-secret-key"

# File paths for data storage
NOTES_FILE = "notes.json"  # File to store notes
USERS_FILE = "users.json"  # File to store user data

# Ensure data files exist
for file in [NOTES_FILE, USERS_FILE]:
    if not os.path.exists(file):
        with open(file, "w") as f:
            json.dump([], f)

# Load users from file
def load_users():
    """Load all users from the JSON file."""
    with open(USERS_FILE, "r") as f:
        return json.load(f)

# Save users to file
def save_users(users):
    """Save all users to the JSON file."""
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=2)

# Read notes from file
def load_notes():
    """Load all notes from the JSON file."""
    with open(NOTES_FILE, "r") as f:
        return json.load(f)

# Save updated notes back to file
def save_notes(notes):
    """Save all notes to the JSON file."""
    with open(NOTES_FILE, "w") as f:
        json.dump(notes, f, indent=2)

# Simple decorator to protect routes
def login_required(fn):
    """Decorator to require login for certain routes."""
    def wrapper(*args, **kwargs):
        if session.get("logged_in"):
            return fn(*args, **kwargs)
        return redirect("/login")  # Redirect to login if not logged in
    wrapper.__name__ = fn.__name__
    return wrapper

# Registration page
@app.route("/register", methods=["GET", "POST"])
def register():
    """Registration route: handles new user signup."""
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        
        # Hash password for security
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        
        # Load existing users
        users = load_users()
        
        # Check if username exists
        if any(u["username"] == username for u in users):
            return render_template("index.html", view="register", error="Username already exists")
        
        # Add new user
        users.append({
            "username": username,
            "password_hash": password_hash,
            "created_at": datetime.now().isoformat()
        })
        save_users(users)
        return redirect("/login")
    return render_template("index.html", view="register", error=None)

# Login page
@app.route("/login", methods=["GET", "POST"])
def login():
    """Login route: handles user authentication."""
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        
        # Load users and check credentials
        users = load_users()
        user = next((u for u in users if u["username"] == username and u["password_hash"] == password_hash), None)
        
        if user:
            session["logged_in"] = True
            session["username"] = username
            return redirect("/")
        return render_template("index.html", view="login", error="Invalid credentials")
    return render_template("index.html", view="login", error=None)

# Logout
@app.route("/logout")
@login_required
def logout():
    """Logout route: clears session and redirects to login."""
    session.clear()
    return redirect("/login")

# Home page - shows notes
@app.route("/")
@login_required
def index():
    """Home page: displays notes UI."""
    return render_template("index.html", view="notes")

# API: Get all notes for current user
@app.route("/api/notes", methods=["GET"])
@login_required
def get_notes():
    """API endpoint: returns all notes as JSON."""
    notes = load_notes()
    # Filter notes by owner
    user_notes = [n for n in notes if n.get("owner") == session.get("username")]
    return jsonify(user_notes)

# API: Create new note with tags
@app.route("/api/notes", methods=["POST"])
@login_required
def create_note():
    """API endpoint: creates a new note from JSON data."""
    notes = load_notes()
    note = request.get_json()
    
    # Clean and validate tags
    tags = note.get("tags", [])
    if isinstance(tags, str):
        # Handle comma-separated string of tags
        tags = [t.strip() for t in tags.split(',') if t.strip()]
    
    # Assign a unique ID, timestamps, owner, and tags to the new note
    note["id"] = max([n["id"] for n in notes], default=0) + 1
    note["created_at"] = datetime.now().isoformat()
    note["updated_at"] = datetime.now().isoformat()
    note["owner"] = session.get("username")
    note["tags"] = tags
    
    notes.append(note)
    save_notes(notes)
    return jsonify(note), 201

# API: Update a note
@app.route("/api/notes/<int:note_id>", methods=["PUT"])
@login_required
def update_note(note_id):
    """API endpoint: updates an existing note by ID."""
    notes = load_notes()
    data = request.get_json()
    for n in notes:
        if n["id"] == note_id and n["owner"] == session.get("username"):
            n["title"] = data["title"]
            n["body"] = data["body"]
            n["updated_at"] = datetime.now().isoformat()
            save_notes(notes)
            return jsonify({"status": "updated"})
    return jsonify({"error": "Note not found"}), 404

# Note: Original share_note function removed to fix duplicate route
    notes = load_notes()
    note = next((n for n in notes if n["id"] == note_id and n["owner"] == session.get("username")), None)
    
    if not note:
        return jsonify({"error": "Note not found"}), 404
        
    # Generate unique sharing ID and hash password
    share_id = str(uuid.uuid4())
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    
    # Store sharing details with the note
    note["shared_id"] = share_id
    note["shared_password_hash"] = password_hash
    note["shared_at"] = datetime.now().isoformat()
    save_notes(notes)
    
    # Return the shareable URL
    share_url = f"/shared/{share_id}"
    return jsonify({
        "message": "Note shared successfully",
        "url": share_url
    })

# Access shared note
# Note: Original access_shared_note function removed to fix duplicate route

# API: Delete a note
@app.route("/api/notes/<int:note_id>", methods=["DELETE"])
@login_required
def delete_note(note_id):
    """API endpoint: deletes a note by ID."""
    notes = load_notes()
    notes = [n for n in notes if n["id"] != note_id]
    save_notes(notes)
    return jsonify({"status": "deleted"})

# API: Share note with password
@app.route("/api/notes/<int:note_id>/share", methods=["POST"])
@login_required
def share_note(note_id):
    """API endpoint: creates a shareable link with password protection.
    
    Args:
        note_id (int): ID of the note to share
        
    Returns:
        JSON response with share URL or error
    """
    data = request.get_json()
    password = data.get("password")
    if not password:
        return jsonify({"error": "Password required"}), 400

    notes = load_notes()
    for note in notes:
        if note["id"] == note_id and note["owner"] == session.get("username"):
            # Generate a unique share ID and store hashed password
            note["shared_id"] = str(uuid.uuid4())
            note["shared_password_hash"] = hashlib.sha256(password.encode()).hexdigest()
            save_notes(notes)
            return jsonify({
                "msg": "Note shared",
                "url": f"/shared/{note['shared_id']}"
            })
    return jsonify({"error": "Note not found"}), 404

# Public: Access shared note by visiting share link
@app.route("/shared/<shared_id>", methods=["GET", "POST"])
def access_shared_note(shared_id):
    """Public route: allows access to a shared note via a link and password."""
    notes = load_notes()
    note = next((n for n in notes if n.get("shared_id") == shared_id), None)
    if not note:
        return "Note not found", 404

    if request.method == "POST":
        password = request.form["password"]
        # Check if password matches the shared password hash
        hashed = hashlib.sha256(password.encode()).hexdigest()
        if hashed == note["shared_password_hash"]:
            return f"<h2>{note['title']}</h2><p>{note['body']}</p>"
        else:
            return render_template("index.html", view="shared", error="Incorrect password")

    # Show password entry form
    return render_template("index.html", view="shared", error=None)

# Entry point: run the Flask development server
if __name__ == "__main__":
    app.run(debug=True)
