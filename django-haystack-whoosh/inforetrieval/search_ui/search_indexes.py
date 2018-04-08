import datetime
from haystack import indexes
from search_ui.models import Product


class ProductIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)

    filename = indexes.CharField(model_attr='filename')
    price = indexes.CharField(model_attr='price')
    rating = indexes.CharField(model_attr='rating')
    noOfReviews = indexes.CharField(model_attr='noOfReviews')
    savings = indexes.CharField(model_attr='savings')
    percentageSavings = indexes.CharField(model_attr='percentageSavings')
    reviewPolarity = indexes.CharField(model_attr='reviewPolarity')
    countryOfOrigin = indexes.CharField(model_attr='countryOfOrigin')

    def get_model(self):
        return Product
