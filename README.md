# Getting Started with Project

Before running the project, make sure you have Python and pip installed on your system.

## Installation Steps

1. **Install Dependencies**:
   
   Run the following command to install project dependencies listed in `requirements.txt`: `pip install -r requirements.txt`


2. **Database Configuration**:

    Create a `.env` file at the root of the project and provide values for the following environment variables to establish a connection with MySQL:
   
   `DB_USER=<MySQL user>`
   
   `DB_PASSWORD=<Password for MySQL user>`


3. **Database Migrations**:

    Execute database migrations using the following command: `python manage.py migrate`


4. **Run the Server**:

    Start the server using the following command: `python manage.py runserver`


## Accessing the Website

Once the server is running, you can access the website by navigating to `localhost:8000` in your web browser.




