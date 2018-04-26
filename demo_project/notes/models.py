from django.db import models


class Country(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Country'
        verbose_name_plural = 'Countries'


class City(models.Model):
    name = models.CharField(max_length=100, unique=True)
    country = models.ForeignKey(Country)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'City'
        verbose_name_plural = 'Cities'


class Person(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    city = models.ForeignKey(City)

    def __str__(self):
        return '{} {}'.format(self.first_name, self.last_name)

    class Meta:
        verbose_name = 'Person'
        verbose_name_plural = 'People'
