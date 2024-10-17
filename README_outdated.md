**This is an internal, unofficial README.md for the PPDS project.**

# PPDS Backend


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
