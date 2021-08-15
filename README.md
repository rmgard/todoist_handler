# todoist_handler
Quick application that handles webscraping and posting in Todoist via their API


At the moment, I simply run this application constantly using a cronjob. In order to do this, I do the following:

`crontab -e`

On the top line of the crontab:

`* * * * * /home/<path to virtual env>/todoist_handler/venv/bin/python /home/<path to main.py>/todoist_handler/main.py`

:qw 
