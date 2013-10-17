mocks
=====

Normal way of instalation:

1. install python
2. install django 
3. install database
4. install virtualenv
5. setup environment variables
6. setup heroku configuration

## 1. Python
Download from http://www.python.org/
If you’re running Linux or Mac OS X, you probably already have it installed.

## 2. Django setup
Visit https://docs.djangoproject.com/en/dev/topics/install/ for a comprehensive tutorial on how to install django on your machine
NOTE: DO NOT MODIFY settings.py (if you do please don't commit the changes to github) check the environment variables setup if you want to make any changes in the settings.py file

## 3. Database (Prefered Postgresql)
You could use any Database localy for development and testing. We recommend using PostgreSQL since we are using it in production.

## 4. virtualenv 
Here is where you can learn more about virtual environments:
> https://pypi.python.org/pypi/virtualenv

This is an easy link that sets up your virtualenv on a linux machine:
> http://docs.python-guide.org/en/latest/starting/install/linux/

## 5. Environment variables
You can find in the following file the environment variables. Copy them to your ~/.bashrc file. If you make changes to the configuration do not commit this file to github
> dev_env_vars 

## 6. Setup a heroku environment and configuration
Follow up the instructions on 
> https://devcenter.heroku.com/articles/getting-started-with-django

## Commands

Useful commands: 

> virtualenv venv --distribute

> source venv/bin/activate

> pip install django-toolbelt

then to start the application either one of the commands

> foreman start

> ./manage.py runserver

### Folder/Files structure is just like a normal Django application

## My heroku requirements: 
* Django==1.5.4
* argparse==1.2.1
* dj-database-url==0.2.2
* dj-static==0.0.5
* django-toolbelt==0.0.1
* gunicorn==18.0
* psycopg2==2.5.1
* static==0.4
* wsgiref==0.1.2
