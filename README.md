# Tasksync

## Project Description
Tasksync is a task management web application built with Django. It allows users to create, manage, and collaborate on tasks and projects efficiently. The application supports user authentication, project and task management, document uploads, and notifications.

## Features
- User registration and authentication
- Create, update, and delete projects and tasks
- Assign collaborators to projects
- Upload and manage project-related documents
- Dashboard to view tasks and project summaries
- Notifications for task updates and deadlines

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)
- Virtualenv (recommended)

### Setup Steps
1. Clone the repository:
   ```
   git clone <repository-url>
   cd Task-Sync
   ```

2. Create and activate a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

4. Apply migrations:
   ```
   python manage.py migrate
   ```

5. Create a superuser (admin):
   ```
   python manage.py createsuperuser
   ```

6. Run the development server:
   ```
   python manage.py runserver
   ```

7. Open your browser and navigate to `http://127.0.0.1:8000/`

## Usage
- Register a new user or log in with existing credentials.
- Create projects and add tasks under each project.
- Assign collaborators to projects.
- Upload documents related to projects.
- Use the dashboard to monitor your tasks and projects.

## Project Structure
- `task_sync/` - Main Django project folder
- `taskmanager/` - Django app handling task and project management
- `media/` - Uploaded media files
- `templates/` - HTML templates for rendering views
- `static/` - Static files like CSS and JavaScript

## Contributing
Contributions are welcome! Please fork the repository and create a pull request with your changes.

## License
This project is licensed under the MIT License.

## Contact
For any questions or support, please contact the project maintainer.
