from django.db import models


"""This modules manages the models necessary for domain administration

The following models are present here:

    - Node: table storing a Geographical location, using a GeoJSON point
    - Address: table storing a Geographical location, using an address
        (an address can have many nodes)
"""

from api.models import Customer


class Address(models.Model):
    class Meta:
        verbose_name = 'Address'
        verbose_name_plural = 'Addresses'
        ordering = ['country', 'city', 'street', 'street_number']

    country = models.CharField(max_length=64)
    country_code = models.CharField(max_length=64)
    postcode = models.CharField(max_length=64)
    state = models.CharField(max_length=64)
    state_district = models.CharField(max_length=64)
    city = models.CharField(max_length=64)
    street = models.CharField(max_length=64)
    street_number = models.PositiveIntegerField()
    owner = models.ForeignKey(Customer, on_delete=models.CASCADE)


class Node(models.Model):
    class Meta:
        verbose_name = 'Node'
        verbose_name_plural = 'Nodes'
        ordering = ['name']

    name = models.CharField(max_length=64)
    latitude = models.FloatField()
    longitude = models.FloatField()
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
