from django.db import models


class Bank(models.Model):
    amount = models.PositiveBigIntegerField(default=100000000)


