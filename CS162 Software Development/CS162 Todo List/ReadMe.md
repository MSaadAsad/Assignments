**Running the App**

**For the first terminal:**
```bash
cd todo_list
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
python3 app.py
```

**Ideally, set the environment to:**
```bash
FLASK_ENV=development
```

**For the second terminal:**
```bash
cd web_app_react
npm install
npm start
```

## Introduction

This is a simple Todo List app. It keeps track of a user's different tasks to be done. The app allows the user to add tasks to various lists categorized by their type. Each main task can have an infinite number of subtasks. The features include:

- Adding new tasks
- Editing tasks
- Marking tasks as complete
- Deleting tasks
- Revealing or concealing subtasks
- Moving tasks across any level to be a subtask of an "uncle task." An "uncle task" is defined as a task whose parent tasks are subtasks of the same parent task.

## Features

The application consists of three main web pages:

- **Register**: Allows users to register with the app.
- **Login**: Provides JWT authentication for users to access the app.
- **Todo List**: Displays the user's complete todo list.

In terms of components, the application includes a header and a footer.

## Code Structure

### Backend (Flask API):

- `__init__.py`: Initializes app configurations.
- `models.py`: Represents the database structure. In my design, I treated a "list" as a special kind of task without a parent ID. This decision eliminated the need for a separate List table in the database, which I deemed redundant. However, this approach complicates the frontend, and in hindsight, I might reconsider this choice.
- `views.py`: Handles JWT token authentication, registration, login, and basic CRUD functionalities. It also contains functions to manage the recursive nature of tasks and subtasks, especially for retrieving all subtasks. The `get-tasks` endpoint sends the entirety of a user's task list in a single JSON response. This design choice reduces backend server requests, which can be beneficial when handling many users. However, it also means sending larger JSON files, which could be problematic if a user has an extensive task list. For demonstration purposes, such a large task list is unlikely.

By separating the frontend and backend through API endpoints, we achieve abstraction. This ensures the frontend focuses solely on endpoints and the derived JSON files.

### Frontend (React):

- **Login and Register Pages**: Target the respective API endpoints for authentication.
- **Header and Footer**: Used for layout and formatting. A logout button is available, which redirects users to the login page and deletes the saved token. This button is only visible on the Todo List page.
- **TodoList and TaskList**: Render the actual task list. Features include:
  - Editing tasks (sends a PUT request).
  - Marking tasks as complete (sends a PUT request and strikes through the text).
  - Deleting tasks (sends a DELETE request for the task and its subtasks after confirmation).
  - Revealing or concealing subtasks using a chevron icon.
  - "Move To" dropdown: Allows tasks to be moved to their "Uncle" tasks. Due to potential task volume, this functionality is limited to tasks sharing the same "grandparent task" or, in cases without grandparents, moving to other lists. This action sends a PUT request updating the `parent_id` in the database.
  
As previously mentioned, a "List" is essentially a task without a parent. This distinction is used during rendering to differentiate between regular tasks and lists.

## Assets

The assets directory contains `.png` files which represent the icons used for editing and deleting functionalities.

## Improvements

The UI/UX of the website can be significantly enhanced. This could be achieved by:
- Incorporating more containers and components.
- Improving the CSS or adopting custom themes.
- Making the List names more prominent than task names.
- In an extended version, I would introduce a Welcome page and populate placeholders like "Privacy Policy" and similar links.
- I realized the need for a task description section after setting up the databases. However, incorporating this shouldn't be a particularly challenging task to address.
- Currently, JWT tokens have an expiration time of one hour. This could be extended using sliding tokens.

Demo Link: https://youtu.be/leCrpVSrAvo

## Unit Testing

The frontend was tested directly, while the backend API underwent testing using the tool Insomnia. The database was examined using DB Browser.

Photos of my unit test have been added to the file.

## Acknowledgments

ChatGPT was used in ideation, code generation, and commenting.

## Learning

Learning
This assignment has made me deeply sympathetic towards Front End Developers and will be invaluable when I create my API for the final project. While I primarily had experience with the backend, from that perspective, I aimed to simplify as much as possible. This included removing database tables and treating Lists as a special category of a Task, all in an effort to minimize requests to the backend. While this approach resulted in a streamlined backend design, it inadvertently shifted much of the complex parsing to the frontend. Although this was feasible, it made the writing frontend react logic considerably challenging. Having backend experience and stepping into the shoes of a frontend developer has taught me the importance of balancing both perspectives. It has provided me with a clearer understanding of effective app design.