from app.src import models


class Activity(object):

    @classmethod
    def log(cls, data):
        """ Log activity to database """

        l = models.Activity(**data)
        models.Activity.Proxy.post(l.to_dict())
