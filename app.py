from flask import Flask, request, render_template, redirect, url_for, session, jsonify  # Import Flask and related modules
import os, json, uuid, hashlib  # Import standard Python modules
from datetime import datetime  # For timestamps

app = Flask(__name__, static_folder='static', static_url_path='/static')  # Create Flask app instance
app.secret_key = "super-secret-key"  # Secret key for session management (use env variable in production)

# Hardcoded author credentials (for demo purposes)
AUTHOR_USERNAME = "author"
AUTHOR_PASSWORD_HASH = hashlib.sha256('secret123'.encode()).hexdigest()

NOTES_FILE = "notes.json"  # File to store notes

# Ensure notes.json file exists, create if missing
if not os.path.exists(NOTES_FILE):
    with open(NOTES_FILE, "w") as f:
        json.dump([], f)

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

# Login page
@app.route("/login", methods=["GET", "POST"])
def login():
    """Login route: handles user authentication."""
    if request.method == "POST":
        user = request.form["username"]
        pw = request.form["password"]
        # Check credentials
        if user == AUTHOR_USERNAME and hashlib.sha256(pw.encode()).hexdigest() == AUTHOR_PASSWORD_HASH:
            session["logged_in"] = True  # Mark user as logged in
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

# API: Get all notes
@app.route("/api/notes", methods=["GET"])
@login_required
def get_notes():
    """API endpoint: returns all notes as JSON."""
    return jsonify(load_notes())

# API: Create new note
@app.route("/api/notes", methods=["POST"])
@login_required
def create_note():
    """API endpoint: creates a new note from JSON data."""
    notes = load_notes()
    note = request.get_json()
    # Assign a unique ID and timestamps to the new note
    note["id"] = max([n["id"] for n in notes], default=0) + 1
    note["created_at"] = datetime.now().isoformat()
    note["updated_at"] = datetime.now().isoformat()
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
        if n["id"] == note_id:
            n["title"] = data["title"]
            n["body"] = data["body"]
            n["updated_at"] = datetime.now().isoformat()
    save_notes(notes)
    return jsonify({"status": "updated"})

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
    """API endpoint: shares a note with a password, generates a share link."""
    password = request.get_json().get("password")
    if not password:
        return jsonify({"error": "Password required"}), 400

    notes = load_notes()
    for note in notes:
        if note["id"] == note_id:
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
