# Superhero API (su-py-heroes)

## Description

**su-py-heroes** is a Flask-based REST API that manages a database of superheroes, their powers, and the relationships between them. This API allows you to list heroes and powers, retrieve individual records, update power descriptions, and associate heroes with various superpowers.

This project demonstrates RESTful API design using Flask and SQLAlchemy ORM with SQLite as the database backend.

## Owner

**Project Owner**: Lewis

## Features

- **Hero Management**: List all heroes and retrieve individual hero details
- **Power Management**: List all powers and retrieve individual power information
- **Power Updates**: Update power descriptions via PATCH requests
- **Hero-Power Associations**: Create relationships between heroes and their powers
- **Data Validation**: Ensures data integrity with proper validation rules
- **Serialization**: Proper JSON serialization with relationship handling to avoid circular references
- **Database Migrations**: Alembic-based migrations for schema management

## Setup Instructions

### Prerequisites

- Python 3.8 or higher
- pip or pipenv for dependency management

### Installation

1. **Clone the repository**

   ```bash
   git clone <repository-url>
   cd su-py-heroes
   ```

2. **Install dependencies**

   Using pipenv (recommended):

   ```bash
   pipenv install
   ```

   Or using pip:

   ```bash
   pip install -r requirements.txt
   ```

   Note: The required packages are:

   - Flask
   - Flask-SQLAlchemy
   - Flask-Migrate
   - SQLAlchemy-Serializer

3. **Initialize the database**

   ```bash
   flask db init
   flask db migrate -m "initial migration"
   flask db upgrade
   ```

4. **Seed the database with sample data**

   ```bash
   python seed.py
   ```

5. **Run the application**

   ```bash
   python app.py
   ```

   The server will start on `http://localhost:5555`

### Testing the API

You can import the provided Postman collection to test the API endpoints:

1. Open Postman
2. Import `challenge-2-superheroes.postman_collection.json`
3. Use the collection to test all endpoints

Alternatively, you can use curl or any HTTP client:

```bash
# Get all heroes
curl http://localhost:5555/heroes

# Get all powers
curl http://localhost:5555/powers

# Get a specific hero
curl http://localhost:5555/heroes/1

# Get a specific power
curl http://localhost:5555/powers/1

# Update a power (PATCH)
curl -X PATCH http://localhost:5555/powers/1 \
  -H "Content-Type: application/json" \
  -d '{"description": "Updated power description here"}'

# Create hero-power relationship (POST)
curl -X POST http://localhost:5555/hero_powers \
  -H "Content-Type: application/json" \
  -d '{"strength": "Strong", "power_id": 1, "hero_id": 1}'
```

## API Endpoints

| Method | Endpoint           | Description                          |
| ------ | ------------------ | ------------------------------------ |
| GET    | `/`                | Welcome message                      |
| GET    | `/heroes`          | Retrieve all heroes                  |
| GET    | `/heroes/<int:id>` | Retrieve a specific hero by ID       |
| GET    | `/powers`          | Retrieve all powers                  |
| GET    | `/powers/<int:id>` | Retrieve a specific power by ID      |
| PATCH  | `/powers/<int:id>` | Update a power's description         |
| POST   | `/hero_powers`     | Create a new hero-power relationship |

### Response Format

All endpoints return JSON responses with appropriate HTTP status codes.

**Success Response (200/201):**

```json
{
  "id": 1,
  "name": "Kamala Khan",
  "super_name": "Ms. Marvel",
  "heropower": []
}
```

**Error Response (404):**

```json
{
  "error": "Hero not found"
}
```

**Error Response (400):**

```json
{
  "errors": ["validation errors"]
}
```

## Database Schema

### Power Description

- Must be at least 20 characters long
- If validation fails, returns: `{"errors": ["description must be at least 20 characters long"]}`

### Hero Power Strength

- Must be one of: 'Strong', 'Weak', or 'Average'
- If validation fails, returns: `{"errors": ["strength must be one of 'Strong', 'Weak', or 'Average'"]}`

### Hero and Power Existence

- When creating hero-power relationships, both hero_id and power_id must exist
- Returns 400 error if either is missing


## Project Structure

```
su-py-heroes/
├── app.py                          # Main Flask application
├─- Pipfile                         # Python dependencies
├── Pipfile.lock                    # Locked dependency versions
├── README.md                     
├── seed.py                         # Database seeding script
├── challenge-2-superheroes.postman_collection.json  # API tests
├── migrations/                     # Flask-Migrate migrations
│   ├── versions/
│   │   └── 38412831300f_initial_migration.py
│   └── alembic.ini
└── instance/                       # SQLite database storage
    ├── heroes.db
    └── powers.db
```

## Troubleshooting

### Port already in use

If port 5555 is already in use, modify the last line of `app.py`:

```python
app.run(debug=True, port=YOUR_PORT)
```

### Database errors

If you encounter database issues, reset the database:

```bash
rm instance/*.db
python seed.py
```

### Migration issues

If migrations are out of sync:

```bash
flask db migrate --reset
flask db upgrade
python seed.py
```

## License

This project is provided as-is for educational and development purposes. Feel free to modify and extend it for your own use.

## Support

For questions or issues related to this project, please refer to:

- Flask Documentation: https://flask.palletsprojects.com/
- SQLAlchemy Documentation: https://docs.sqlalchemy.org/
- SQLAlchemy-Serializer: https://pypi.org/project/SQLAlchemy-Serializer/

---

**Built with Flask and SQLAlchemy**
