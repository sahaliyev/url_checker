### Setup env
1. create virtual env and install requirements.txt file. 
2. migrate and create super user to have access to django admin
3. add/edit/delete urls in UrlsToMonitor model
4. for simple user there is register page. They can register and login to see status of urls. 
5. url are checking by celery task in a given time interval. We can specifiy time interval in django admin (Intervals) and assign it to task in PeriodicTasks model. (This is all done by django-celery-beat)
6. In order to disable url being checked next time unselect check_needed and save
7. Status is auto defined. First time left it blank. 
8. You need to have redis on your machine to test the project. 
9. You need to run three commands:
  1. python manage.py runserver
  2. celery -A project  worker --loglevel=info
  3. celery -A project beat -l info -S django
