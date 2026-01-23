# Connectly

Connectly is a full-featured social media platform built with Django. It provides a real-time, interactive experience for users to connect, share content, and communicate. The application includes a dynamic feed, user profiles, notifications, and a real-time chat system powered by Django Channels and WebSockets.

## Features

*   **User Authentication**: Secure user signup, login, and logout functionality.
*   **Social Feed**: A central feed displaying posts from all users in chronological order, with infinite scrolling.
*   **Posts, Likes, and Comments**: Create text-based posts, and interact with them by liking and commenting.
*   **User Profiles**: View user profiles, see their posts, and check follower/following counts.
*   **Follow System**: Follow and unfollow other users to customize your social graph.
*   **Real-time Notifications**: Receive instant notifications for new likes, comments, and follows.
*   **Live Chat**: Engage in one-on-one real-time messaging with other users.
*   **REST API**: Exposes endpoints for authentication and fetching the feed, secured with token authentication.
*   **Dark Mode**: A sleek, user-toggleable dark mode for comfortable viewing.
*   **Responsive Design**: A clean and responsive user interface that works across different screen sizes.

## Tech Stack

*   **Backend**: Python, Django
*   **API**: Django REST Framework
*   **Real-time Communication**: Django Channels, WebSockets
*   **Database**: SQLite (default), configured with `dj-database-url` for easy switching.
*   **Message Broker**: Redis (for Django Channels)
*   **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
*   **Deployment**: Gunicorn, Uvicorn, Whitenoise

## Setup and Installation

To run this project locally, follow these steps:

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/rifatsh3ikh/Connectly.git
    cd Connectly
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    python -m venv venv
    # On Windows
    venv\Scripts\activate
    # On macOS/Linux
    source venv/bin/activate
    ```

3.  **Install dependencies:**
    The project relies on several Python packages. Install them using pip:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up environment variables:**
    Create a `.env` file in the root directory and add the following variables.
    ```env
    SECRET_KEY='your-secret-django-key'
    REDIS_URL='redis://127.0.0.1:6379'
    ```

5.  **Start Redis Server:**
    Ensure you have a Redis server instance running on the default port (`6379`). You can download and run it from the [official Redis website](https://redis.io/download).

6.  **Apply database migrations:**
    ```bash
    python manage.py migrate
    ```

7.  **Run the development server:**
    ```bash
    python manage.py runserver
    ```

The application will be available at `http://127.0.0.1:8000/`.

## API Endpoints

The application provides the following REST API endpoints:

#### Login
*   **Endpoint:** `POST /api/login/`
*   **Description:** Authenticates a user and returns an authentication token.
*   **Body:**
    ```json
    {
        "username": "your_username",
        "password": "your_password"
    }
    ```
*   **Response:**
    ```json
    {
        "token": "your_auth_token"
    }
    ```

#### Feed
*   **Endpoint:** `GET /api/feed/`
*   **Description:** Retrieves the latest 20 posts from the feed. Requires authentication.
*   **Headers:**
    ```
    Authorization: Token your_auth_token
    ```
*   **Response:** An array of post objects.
    ```json
    [
        {
            "id": 1,
            "author": {
                "id": 1,
                "username": "testuser"
            },
            "content": "This is my first post on Connectly!",
            "created_at": "2024-01-01T12:00:00Z"
        },
        ...
    ]

## 🤝 Contributing

Contributions are welcome!
To contribute:

Fork the project

Create a feature branch (git checkout -b feature/your‑idea)

Commit your changes (git commit -m "Add feature")

Push to your branch (git push)

Open a Pull Request

## 📬 Contact

Maintained by rifatsh3ikh
