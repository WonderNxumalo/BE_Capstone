This is a Cohort 7 ALX Backend Capstone Project: Events Mananagement API by Wonder Nxumalo

# Event Management API

This is a comprehensive Event Management API built using Django and Django REST Framework (DRF), designed to handle user authentication, event CRUD operations, capacity management (including waitlists), and user feedback/comments. 

## 1. Setup and Installation

### Prerequisites

* Python 3.8+
* pip

### Local Setup

1.  **Clone the repository:**
    ```bash
    git clone [your_repo_url]
    cd event_manager_project
    ```
2.  **Create and activate a virtual environment:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```
3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Run migrations:**
    ```bash
    python manage.py migrate
    ```
5.  **Create a Superuser (for Admin access):**
    ```bash
    python manage.py createsuperuser
    ```
6.  **Start the development server:**
    ```bash
    python manage.py runserver
    ```
    The API will be available at `http://127.0.0.1:8000/api/v1/`.

## 2. Authentication (JWT)

All authenticated endpoints require a JSON Web Token (JWT) provided in the `Authorization` header as `Bearer <token>`.

| Endpoint | Method | Description | Request Body |
| :--- | :--- | :--- | :--- |
| `/api/v1/register/` | `POST` | Creates a new user account. | `{"username": "...", "email": "...", "password": "..."}` |
| `/api/v1/token/` | `POST` | Obtain Access and Refresh tokens. | `{"username": "...", "password": "..."}` |
| `/api/v1/token/refresh/` | `POST` | Get a new Access token using the Refresh token. | `{"refresh": "..."}` |

## 3. Event Endpoints

The primary endpoint for viewing, creating, and managing events. Only the event organizer can update/delete an event.

| Endpoint | Method | Description | Authentication |
| :--- | :--- | :--- | :--- |
| `/api/v1/events/` | `GET` | List all **upcoming** events (paginated). | Optional |
| `/api/v1/events/` | `POST` | Create a new event. | Required |
| `/api/v1/events/{id}/` | `GET` | Retrieve a specific event. | Optional |
| `/api/v1/events/{id}/` | `PUT`/`PATCH` | Update an event (Organizer only). | Required |
| `/api/v1/events/{id}/` | `DELETE` | Delete an event (Organizer only). | Required |
| `/api/v1/events/{id}/register/` | `POST` | Toggle user registration status (Register/Unregister). | Required |
| `/api/v1/events/{id}/waitlist_toggle/` | `POST` | Toggle user waitlist status (Used if capacity is full). | Required |

### Filtering and Search (GET /api/v1/events/)

The list endpoint supports several URL query parameters:

| Parameter | Example | Description |
| :--- | :--- | :--- |
| `title` | `?title=meetup` | Case-insensitive search by event title. |
| `location` | `?location=conference` | Case-insensitive search by location. |
| `date_and_time` | `?date_and_time=2026-01-01T10:00:00Z` | Exact match for date and time. |
| `date_range_start`| `?date_range_start=2026-01-01` | Filter events starting on or after this date. |
| `date_range_end` | `?date_range_end=2026-02-01` | Filter events ending on or before this date. |

## 4. Comments and Feedback (Nested)

This feature allows users to submit comments and ratings for specific events.

| Endpoint | Method | Description | Authentication |
| :--- | :--- | :--- | :--- |
| `/api/v1/events/{event_id}/comments/` | `GET` | List all comments for the specified event. | Optional |
| `/api/v1/events/{event_id}/comments/` | `POST` | Create a new comment/rating. | Required |
| `/api/v1/events/{event_id}/comments/{id}/` | `PUT`/`PATCH` | Update a comment (Owner only). | Required |
| `/api/v1/events/{event_id}/comments/{id}/` | `DELETE` | Delete a comment (Owner only). | Required |

**Example POST Request Body (Create Comment):**
```json
{
    "content": "Lekker event!",
    "rating": 5
}

## 5. User Endpoint (User Management)

Users can view and update their own profiles
| Endpoint | Method | Description | Authentication |
| :--- | :--- | :--- | :--- |

| `/api/v1/users/{id}` | `GET` | Retrieve specific user details. | Required |
| `/api/v1/users/{id}` | `PATCH` | Update a user's details (User must match ID). | Required |
