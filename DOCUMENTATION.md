# Code Documentation Guide

## Project Structure
```
secret-notes-app/
├── app.py               # Main Flask application
│   ├── Routes          # HTTP endpoints
│   ├── Data Models     # Note and user handling
│   └── Authentication  # Login and security
├── static/
│   └── style.css       # Application styling
├── templates/
│   └── index.html      # Single-page template
├── notes.json          # Note storage
└── users.json          # User account storage
```

## Key Components

### 1. Flask Backend (app.py)
- **Authentication System**: Uses session-based auth with password hashing
- **Note Management**: CRUD operations for notes with owner tracking
- **Data Persistence**: JSON file-based storage
- **API Endpoints**: RESTful design for note operations
- **Share System**: UUID-based sharing with password protection

### 2. Frontend Template (index.html)
- **View System**: Uses Jinja2 conditional rendering
- **Components**:
  - Login/Register forms
  - Note creation and display
  - Tag management
  - Search and filtering
  - Share modal
- **JavaScript Features**:
  - AJAX for async operations
  - Dynamic content updates
  - Client-side filtering
  - Tag cloud generation

### 3. Styling (style.css)
- **Responsive Design**: Mobile-first approach
- **Component Styles**: Modular CSS organization
- **Interactive Elements**: Hover states and animations
- **Modal System**: Overlay and dialog styling

## Authentication Flow
1. User submits login/register form
2. Password is hashed using SHA-256
3. User data is stored/verified
4. Session is created on success

## Note Operations
1. **Create**: POST to /api/notes
2. **Read**: GET from /api/notes
3. **Update**: PUT to /api/notes/<id>
4. **Delete**: DELETE to /api/notes/<id>

## Share System Flow
1. User clicks share button
2. Sets share password
3. Backend generates UUID
4. Share link created
5. Recipients use password to access

## Tag System
- Tags stored with notes
- Client-side filtering
- Tag cloud shows usage frequency
- Click to filter by tag

## Security Features
- Password hashing
- Session management
- CSRF protection
- Share link encryption

## Error Handling
- Form validation
- API error responses
- User feedback
- Error state display

## Future Improvements
- Email verification
- Password reset
- Note encryption
- Collaborative editing
- Mobile app version
