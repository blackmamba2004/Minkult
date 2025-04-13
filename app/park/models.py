from django.db import models


class Park(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255, null=True)
    description = models.TextField(null=True)
    category = models.CharField(max_length=100, null=True)
    status = models.CharField(max_length=50, null=True)

    full_address = models.CharField(max_length=512, null=True)
    street = models.CharField(max_length=255, null=True)
    lat = models.FloatField(null=True)
    lon = models.FloatField(null=True)

    class Meta:
        db_table = "park"

    def __str__(self):
        return self.name
