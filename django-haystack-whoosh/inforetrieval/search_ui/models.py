from django.db import models


class Product(models.Model):
    filename = models.CharField(max_length=300)
    price = models.CharField(max_length=50)
    rating = models.CharField(max_length=50)
    noOfReviews = models.CharField(max_length=50)
    savings = models.CharField(max_length=50)
    percentageSavings = models.CharField(max_length=50)
    reviewPolarity = models.CharField(max_length=50)
    countryOfOrigin = models.CharField(max_length=50)
    #productDesc = models.TextField()

    def __unicode__(self):
        return self.filename
