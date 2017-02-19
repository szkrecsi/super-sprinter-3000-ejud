from connectdatabase import ConnectDatabase
from peewee import *


class UserStories(Model):

    story_title = TextField()
    user_story = TextField()
    acceptance_criteria = TextField()
    business_value = IntegerField()
    estimation = FloatField()
    status = TextField()

    class Meta:
        database = ConnectDatabase.db
