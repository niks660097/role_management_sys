from django.db import models

class Resource(models.Model):#assuming that for every resource there is entry in this table.
    name = models.CharField(max_length=15)
    value = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

