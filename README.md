# it-company-task-manager

## Initialization

1. **Clone the repository:**
   - HTTPS
    ```bash
    git clone https://github.com/viktor-77/it-company-task-manager.git
    ```
   - SSH
    ```bash
    git clone git@github.com:viktor-77/it-company-task-manager.git
    ```

2. **Create a virtual environment:**
    ```bash
    python -m venv venv
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

5. **Set up environment variables:**
    - Copy `env.example` to `.env` and set correct values.

6. **Apply database migrations:**
    ```bash
    python manage.py migrate
    ```

7. **Run the server:**
    ```bash
    python manage.py runserver
    ```

8. **Open in your browser:**
    ```
    http://127.0.0.1:8000/
    ```
