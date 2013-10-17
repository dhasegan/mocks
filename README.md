mocks
=====
Stub
TODO

# Requirements: 
Django==1.5.4
argparse==1.2.1
dj-database-url==0.2.2
dj-static==0.0.5
django-toolbelt==0.0.1
gunicorn==18.0
psycopg2==2.5.1
static==0.4
wsgiref==0.1.2

# This configuration should be setup in an virtual environment

# To check out the setting check file
mocks/settings.py
# which uses the environment variables define in file
dev_env_vars
# copy this to the your ~/.bashrc file and run it once in the terminal (for the current session)



# For seting up postgresql check the following link
#   https://jordanktakayama.wordpress.com/2013/02/20/lessons-learned-from-deploying-django-on-heroku/

# Create a virtual environment and install 
# if you have problems check out the links:
#   https://devcenter.heroku.com/articles/getting-started-with-django#prerequisites
virtualenv venv --distribute
source venv/bin/activate
pip install django-toolbelt

# start the application (either one of the following commands)
foreman start
./manage.py runserver
