**This is an internal, unofficial, and prelimnary README.md for our PPDS project, that we will keep building on.**

# NYU Event Sync: Google Calendar Integration with NYU Engage

## Project Overview

The finished project will be a web application that aims to streamline event management by integrating NYU Engage with Google Calendar. The app scrapes event data from NYU Engage based on a user's preferences and automatically populates the events into their Google Calendar. The user can accept or reject invites, with accepted invites redirecting them to RSVP, and rejected ones removing the clutter from their calendar.

## Problem Solved

This application solves the problem of manually managing event invitations and RSVPs for NYU students. By automating the process of adding events to Google Calendar, the app makes it easier to stay organized and keep track of relevant events, eliminating manual work and reducing calendar clutter.


## Project Structure

This week's project uses **FastAPI** for the backend and **MongoDB** as the database to store user and event data. The app integrates with Google Calendar and uses API routes to manage user and event operations.

### Files:

- **main.py**:  
  The entry point of the application. It sets up the FastAPI instance, connects to the MongoDB database, and includes the API routes. It handles the startup and shutdown of the database connection.

  Key functions:
  - `startup_db_client`: Connects to MongoDB using credentials stored in environment variables.
  - `shutdown_db_client`: Closes the MongoDB connection.

- **routes.py**:  
  Contains the API routes that handle the operations related to users and events. The routes include creating, updating, and fetching users and events.

  Key routes:
  - `/users/`: Manage user operations (GET, POST, PUT).
  - `/events/`: Manage event operations (GET, POST, PUT).

- **models.py**:  
  Defines the data models for MongoDB collections using Pydantic. It includes models for the User and Event, as well as a custom handler for the ObjectId used by MongoDB.

  Key models:
  - `User`: Represents the user with attributes such as name, email, and netid.
  - `Event`: Represents events with attributes like title, description, date, and location.


## Setup Instructions

1. Create a virtual environment:
   ```
   python -m venv venv
   ```

2. Activate the virtual environment:
   - On Windows:
     ```
     venv\Scripts\activate
     ```
   - On macOS and Linux:
     ```
     source venv/bin/activate
     ```

3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   - Create a `.env` file in the root directory
   - Add the following variables:
     ```
     MONGODB_USERNAME=your_mongodb_username
     MONGODB_PASSWORD=your_mongodb_password
     ```

5. Start the FastAPI server:
   ```
   cd backend
   uvicorn main:app --reload
   ```

The server should now be running at `http://localhost:8000`. You can access the API documentation at `http://localhost:8000/docs`.

## Test the API

You can test the API using tools like cURL, Postman, or any HTTP client. Here are some example requests for testing the API endpoints:

Base URL: `http://localhost:8000/api`

For more detailed documentation of the API endpoints, including request/response schemas and available operations, please visit: [API Documentation](http://localhost:8000/docs)

### User Collection

1. Get all users:
   ```
   GET /users/
   ```

2. Get a single user:
   ```
   GET /users/{user_id}
   ```

3. Create a new user:
   ```
   POST /users/
   Content-Type: application/json

   {
     "name": "John Doe",
     "email": "john@example.com",
     "password": "securepassword"
   }
   ```

4. Update a user:
   ```
   PUT /users/{user_id}
   Content-Type: application/json

   {
     "name": "John Updated",
     "email": "johnupdated@example.com"
   }
   ```

5. OAuth 2.0 login (to be implemented):
   ```
   POST /login
   Content-Type: application/json

   {
     "oauthToken": {
       "access_token": "your_oauth_access_token"
     }
   }
   ```

### Event Collection

1. Get all events:
   ```
   GET /events/
   ```

2. Get a single event:
   ```
   GET /events/{event_id}
   ```

3. Create a new event:
   ```
   POST /events/
   Content-Type: application/json

   {
     "title": "Team Meeting",
     "description": "Weekly team sync",
     "date": "2023-06-15T14:00:00Z",
     "location": "Conference Room A"
   }
   ```

4. Update an event:
   ```
   PUT /events/{event_id}
   Content-Type: application/json

   {
     "title": "Updated Team Meeting",
     "description": "Rescheduled weekly team sync"
   }
   ```

Replace `{user_id}` and `{event_id}` with actual IDs when testing. For the OAuth 2.0 login, you'll need to obtain a valid OAuth access token from the authentication provider.

## Postman Tests

To test the API using Postman:

1. Test each URL (`/users/`, `/events/`, etc.).
2. Record the request body sent for `POST` and `PUT` methods, e.g.,
   ```json
   {
     "title": "Sample Event",
     "description": "This is a sample event",
     "date": "2024-10-17T10:00:00Z"
   }

## Credits

AI-generated code was used in assisting the structuring of this README.