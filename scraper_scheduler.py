"""
This module is called every 24h to trigger the data update in the controller.
This is called by a scheduler application on our Heroku webserver.
"""
from controller.controller import controllerObject

print("Daily data Update started...")
controllerObject.updateArticleData()
print("Daily data update finished successfully!")


