# Django Messaging App

A secure Django REST API for a messaging application with robust authentication, permissions, pagination, and filtering.

## Features

### Authentication
- **JWT Authentication**: Secure user authentication using JSON Web Tokens
- **Custom User Registration**: User registration with email validation
- **Token Management**: Obtain, refresh, and verify JWT tokens

### Conversations
- **Create Conversations**: One-on-one and group conversations
- **Participant Management**: Add and remove participants to conversations
- **Access Control**: Only conversation participants can access messages

### Messages
- **Send/Receive Messages**: Exchange messages within conversations
- **Read Status Tracking**: Track read status of messages
- **Bulk Actions**: Mark all messages as read

### Security
- **Custom Permissions**: Granular permission system for conversations and messages
  - `IsOwner`: Only owners can access their objects
  - `IsParticipantOfConversation`: Only participants can access conversations
  - `IsOwnerOrReadOnly`: Anyone can read, only owners can modify
  - `IsAuthenticatedForAPI`: API-wide authentication requirement

### Data Management
- **Pagination**: 
  - 20 messages per page for messages
  - 10 items per page for conversations
  - Custom pagination response metadata
- **Filtering**:
  - Messages: Filter by sender, content, date range, read status
  - Conversations: Filter by participant, title, creation date, group status

## API Endpoints

### Authentication
- `POST /api/register/`: Register a new user
- `POST /api/token/`: Login and obtain JWT token
- `POST /api/token/refresh/`: Refresh JWT token
- `POST /api/token/verify/`: Verify JWT token validity

### Users
- `GET /api/users/me/`: Get current user profile

### Conversations
- `GET /api/conversations/`: List user's conversations
- `POST /api/conversations/`: Create a new conversation
- `GET /api/conversations/{id}/`: Get conversation details
- `PATCH /api/conversations/{id}/`: Update conversation
- `POST /api/conversations/{id}/add_participant/`: Add a participant

### Messages
- `GET /api/conversations/{id}/messages/`: List messages in a conversation
- `POST /api/conversations/{id}/messages/`: Send a new message
- `GET /api/conversations/{id}/messages/{message_id}/`: Get message details
- `POST /api/conversations/{id}/messages/{message_id}/mark_read/`: Mark a message as read
- `POST /api/conversations/{id}/messages/mark_all_read/`: Mark all messages as read

## Technical Stack

- **Framework**: Django + Django REST Framework
- **Authentication**: djangorestframework-simplejwt
- **Database**: SQLite (default)
- **Filtering**: django-filter
- **API Organization**: Nested routers for resource hierarchy

## Setup & Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/alx-backend-python.git
   cd alx-backend-python/messaging_app
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Apply migrations:
   ```bash
   python manage.py migrate
   ```

5. Run the development server:
   ```bash
   python manage.py runserver
   ```

## Testing with Postman

The project includes a comprehensive Postman collection (`post_man-Collections/Messaging_App_API_Tests.json`) that tests all API endpoints.

### Setting Up Postman
1. Import the collection into Postman
2. Create a Postman environment with the following variables:
   - `baseUrl` (default: http://localhost:8000)

### Test Flow
The collection is organized to test the application in a logical flow:

1. **Authentication**:
   - Register test users
   - Login to get JWT tokens
   - Verify and refresh tokens
   - Test unauthorized access

2. **Conversations**:
   - Create conversations
   - Get conversation details
   - Add participants
   - Test access permissions

3. **Messages**:
   - Send messages in conversations
   - List and retrieve messages
   - Mark messages as read
   - Test message filtering

4. **Filtering & Pagination**:
   - Test paginated results
   - Filter messages by various criteria
   - Filter conversations by type

### Running the Tests
1. Start the Django server
2. Run the Postman collection
3. Observe results in the Postman console

## License

This project is licensed under the MIT License - see the LICENSE file for details.
