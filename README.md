# tz_biotech




Dependency installation:

Make sure you have Python and its package manager pip installed. Then install the required dependencies by going to the root directory of the project and run: pip install -r requirements.txt
This command will install all the dependencies specified in the requirements.txt file.

Configuring the database:

Edit the settings.py file to configure the database connection. In our case, you are using PostgreSQL. 
Make sure you have a PostgreSQL server and have created a database named tz_biotech. In the settings.py file, specify the correct settings to connect to the database in the DATABASES section.


Install and start Redis:

For the caching process, you will need a Redis server. Install Redis on your server or local machine.
Follow the instructions on the official Redis website to install and run it. Start the Redis server.

Launch Celery:

Open a terminal and start Celery with the following command: celery -A main worker --loglevel=info
This will allow you to perform asynchronous tasks such as sending OTP codes via email, using Redis to store the results.

Server startup:

After configuring the database, dependencies, and Redis, run the following command, having previously opened 1 more terminal to start the server: python manage.py runserver


Your application will be available at http://127.0.0.1:8000/

API Endpoints:

Your application defines several API endpoints. These can be found in the urls.py file. Here are some of them:

/register/ - user registration
/login/ - user login
/verify-otp/ - verify OTP code
/profile/ - get user profile (authentication required)
/profile/update/ - update user profile (authentication required)
/profile/delete/ - delete user account (authentication required)
Authentication Usage:

For authentication and authorization, the application uses JWT (JSON Web Token). Users can register, login and perform actions such as updating profile and deleting account.

