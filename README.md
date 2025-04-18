## task manager

This project is a task management system for IT companies, enabling users to
create, assign, and manage tasks. It includes user profile editing, task
management with specific permissions, and extended functionality for
superusers, allowing them to manage all tasks and users.

![image](https://github.com/user-attachments/assets/ecb1c6f1-ba95-4b54-804f-6fc28197b7a3)



## Main Functionalities

1. **User Registration and Authorization:**  
   Users register in the app as regular users, granting them access to the
   system's main features — creating and managing tasks.

   ![image](https://github.com/user-attachments/assets/59b27a42-9b2c-461b-8441-10d02e8dc51c)


3. **User Profile Editing:**  
   Users can edit their personal information on their profile page.

   ![image](https://github.com/user-attachments/assets/4aecb2b4-378f-4490-a0d3-63d2895df9eb)


5. **Task Management:**  
   Each user can create tasks and assign them to any users. Only users who
   are assigned to a specific task can edit or delete that task.

   ![image](https://github.com/user-attachments/assets/4b2dd8ed-8ce5-4e91-8dbf-23c5076dbc5e)


7. **Superuser Functionality:**  
   Superusers have extended capabilities:
    - They can edit and delete any tasks and users.
    - Additional buttons for quick access to editing or deleting records are
      available on the task and user lists pages.


## Setup

1. **Clone & open the repository:**
    - HTTPS
    ```bash
    git clone https://github.com/viktor-77/it-company-task-manager.git
    ```
    - SSH
    ```bash
    git clone git@github.com:viktor-77/it-company-task-manager.git
    ```

   ```bash
   cd it-company-task-manager
   ```

2. **Create a virtual environment:**
    ```bash
    python3 -m venv venv
    ```

3. **Activate the virtual environment:**
    - For Windows:
      ```bash
      .\venv\Scripts\activate
      ```
    - For macOS/Linux:
      ```bash
      source venv/bin/activate
      ```

4. **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

5. **(Optional) Set up environment variables:**
    - Copy `env.example` to `.env` and set correct values.

6. **Apply database migrations:**
    ```bash
    python manage.py migrate
    ```

7. **Load initial data**
    ```bash
    python manage.py loaddata dump.json 
    ```

8. **Run the server:**
    ```bash
    python manage.py runserver
    ```

9. **Open in your browser:**
    ```
    http://127.0.0.1:8000/
    ```

## Demo deployed project

https://it-company-task-manager-ry1b.onrender.com/

* login:  user
* password: user12345
