#!/usr/bin/env python
import codecs
import sys
import os
import os.path
import json
import re
from syn import synonyms
from senticnet.senticnet import SenticNet
from whoosh import index, sorting
from whoosh import highlight
from whoosh.spelling import Corrector, QueryCorrector
from whoosh.fields import ID, TEXT, Schema, NUMERIC
from whoosh.analysis import CharsetFilter, StemmingAnalyzer, StopFilter
from whoosh.support.charset import accent_map
from whoosh.reading import TermNotFound
from whoosh.qparser import QueryParser
from django.db.models import signals
from django.conf import settings

# initialise sentic net
sn = SenticNet()
# does stemming, removes accents so you can match words like cafe, facade etc and removes stopwords
hsn_analyzer = StemmingAnalyzer() | CharsetFilter(accent_map) | StopFilter()

SCHEMA = Schema(filename=ID(unique=True, stored=True),
                content=TEXT(analyzer=hsn_analyzer, spelling=True, stored=True),
                price=NUMERIC(sortable=True, stored=True),
                rating=NUMERIC(sortable=True, stored=True),
                noOfReviews=NUMERIC(sortable=True, stored=True),
                savings=NUMERIC(sortable=True, stored=True),
                percentageSavings=NUMERIC(sortable=True,stored=True),
                review=TEXT(analyzer=hsn_analyzer, spelling=True),
                reviewPolarity=NUMERIC(sortable=True, stored=True),
                countryOfOrigin=TEXT(sortable=True, stored=True),
                )

# function to check if a string contains a float
def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def average(a, b):
    return (a + b) / 2.0

# get or initialise index
def update_index(sender=None, **kwargs):
    if not os.path.exists(index_dir):
        os.mkdir(settings.index_dir)
        storage = store.FileStorage(settings.WHOOSH_INDEX)
        ix = index.Index(storage, schema=WHOOSH_SCHEMA, create=True)

    user_input = input("Make a new index(Y/N)? :")
    while not re.match(r"(?i)(YES|Y|N|NO)", user_input):
        user_input = input("Enter Y/N: ")
    if re.match(r"(?i)(YES|Y)", user_input):
        return full_index(index_dir)
    else:
        if index.exists_in(index_dir):
            return index.open_dir(index_dir)
        else:
            print("No index found. Making a new one for you =).")
            return full_index(index_dir)
signals.post_syncdb.connect(update_index)
# initialise index and populate with records
def full_index(index_dir):
    idx = index.create_in(index_dir, SCHEMA)
    # for higher performance : processes = 4, RAM limit = 1024, multi segmented indexing = true
    writer = idx.writer(procs=4, limitmb=1024, multisegment=True)

    #open and load product files for indexing
    fileobj = open("HSN_products.json")
    fileobj1 = open("HSN_products_2.json")
    data = json.load(fileobj)
    data1 = json.load(fileobj1)
    
    # processing data for more sorting functions
    for item in data:
        # check if the string contains price data
        if is_number(item["price"][1:].strip()):
            # convert to float type for sorting
            item_price = float(item["price"][1:])
        else:
            # give arbitrary number if no price was stated on website
            item_price = 100000
        if is_number(item["noOfReviews"][0:2].strip()):
            # convert to float type for sorting
            item_num_reviews = float(item["noOfReviews"][0:2])
        else:
            # give zero if null
            item_num_reviews = 0
        if is_number(item["rating"][0:2].strip()):
            # convert to float type for sorting
            item_rating = float(item["rating"][0:2])
        else:
            # give 0 if no rating was stated on website
            item_rating = 0
        # check if there is a value in savings
        if is_number(item["savings"][1:].strip()):
            # convert to float type for sorting
            item_savings = float(item["savings"][1:])
        else:
            # give 0 if no savings were stated on website
            item_savings = 0
        # try to get country of origin of product
        try:
            temp = json.loads(item["productDesc"])
            country = temp["Country of Origin:"]
            for i in country.split():
                if i in synonyms["countries"]:
                    break
                else:
                    country = "null"
        except KeyError:
            country = "null"
        # check if string contains reviews
        if len(item["review"]) == 0:
            # for no reviews, assign a neutral score
            averageIntensity = 0
        else:
            # initialise review polarity variable to store value of each review
            intensityValueReview = 0
            # iterate through each review in the list
            for i in item["review"]:
                # initialise word polarity variable to store value of each word
                intensityValueWord = 0
                # iterate through each word by using split otherwise will iterate by letter
                for j in i.split():
                    # catch exception when the word is not found in sentic net
                    try:
                        # add value of all the words
                        intensityValueWord += float(sn.polarity_intense(j))
                    except KeyError:
                        # if not found in sentic net assign neutral value
                        intensityValueWord += 0
                # add the value of all the words to get the overall review score
                intensityValueReview += intensityValueWord
            # divide the total score of the reviews added together by the number of reviews to get an average value
            averageIntensity = intensityValueReview/len(item["review"])
        if item_price != 100000:
            writer.add_document(filename=item["name"], content=json.dumps(item), price=item_price, rating=item_rating, noOfReviews=item_num_reviews, savings=item_savings, percentageSavings=(item_savings*100)/(item_savings+item_price), review=item["review"], reviewPolarity=averageIntensity, countryOfOrigin=country)
    for item in data1:
        if is_number(item["price"][1:].strip()):
            # convert to float type for sorting
            item_price = float(item["price"][1:])
        else:
            # give arbitrary number if no price was stated on website
            item_price = 100000
        if is_number(item["noOfReviews"][0:2].strip()):
            # convert to float type for sorting
            item_num_reviews = float(item["noOfReviews"][0:2])
        else:
            # give 0 if no reviews
            item_num_reviews = 0
        if is_number(item["rating"][0:2].strip()):
            # convert to float type for sorting
            item_rating = float(item["rating"][0:2])
        else:
            # give 0 if no rating was stated on website
            item_rating = 0
        # check if there is a value in savings
        if is_number(item["savings"][1:].strip()):
            # convert to float type for sorting
            item_savings = float(item["savings"][1:])
        else:
            # give 0 if no savings were stated on website
            item_savings = 0
        try:
            temp = json.loads(item["productDesc"])
            country = temp["Country of Origin:"]
            for i in country.split():
                if i in synonyms["countries"]:
                    break
                else:
                    country = "null"
        except KeyError:
            country = "null"
        # check if string contains reviews
        if len(item["review"]) == 0:
            # for no reviews, assign a neutral score
            averageIntensity = 0
        else:
            # initialise review polarity variable to store value of each review
            intensityValueReview = 0
            # iterate through each review in the list
            for i in item["review"]:
                # initialise word polarity variable to store value of each word
                intensityValueWord = 0
                # iterate through each word by using split otherwise will iterate by letter
                for j in i.split():
                    # catch exception when the word is not found in sentic net
                    try:
                        # add value of all the words
                        intensityValueWord += float(sn.polarity_intense(j))
                    except KeyError:
                        # if not found in sentic net assign neutral value
                        intensityValueWord += 0
                # add the value of all the words to get the overall review score
                intensityValueReview += intensityValueWord
            # divide the total score of the reviews added together by the number of reviews to get an average value
            averageIntensity = intensityValueReview/len(item["review"])
        if item_price != 100000:
            writer.add_document(filename=item["name"], content=json.dumps(item), price=item_price, rating=item_rating, noOfReviews=item_num_reviews, savings=item_savings, percentageSavings=(item_savings*100)/(item_savings+item_price), review=item["review"], reviewPolarity=averageIntensity, countryOfOrigin=country)
    writer.commit()
    return idx


def search(user_query, index_dir):
    # get index to search
    idx = get_or_create_index(index_dir)

    # parse the user_query
    qp = QueryParser("content", schema=idx.schema)
    query = qp.parse(user_query)

    # get searcher
    with idx.searcher() as searcher:
        # typo checker - checks if the user's query matches words in our content field by default, possible to add other dictionaries as well
        corrected = searcher.correct_query(query, user_query)
        if corrected.query != query:
            print("Did you mean", corrected.string + "?")
            ans = input("Enter Y/N: ")
            try:
                while not re.match(r"(?i)(YES|Y|N|NO)", ans):
                    ans = input("Enter Y/N: ")
                if re.match(r"(?i)(YES|Y)", ans):
                    query = qp.parse(corrected.string)
                else:
                    query = qp.parse(input("Please enter your query again: "))
            except IndexError:
                print('you need to provide a query. assuming "chicken" query.')
                search('chicken', 'index_dir')
        # query user for sorting method
        sortMethod = input("Search by :\n1. Price(ascending)\n2. Price(descending)\n3. Reviews\n4. Ratings\n5. Absolute savings\n6. Percentage Savings\n7. Reviews & Ratings\n8. Price, Reviews & Ratings\n9. Search by price range\n10.Country of Origin\nPlease enter your selection(1-10): ")

        while not re.match(r"[1-9]|10", sortMethod):
            sortMethod = input("Search by :\n1. Price(ascending)\n2. Price(descending)\n3. Reviews\n4. Ratings\n5. Absolute savings\n6. Percentage Savings\n7. Reviews & Ratings\n8. Price, Reviews & Ratings\n9. Search by price range\n10.Country of Origin\nPlease enter your selection(1-10): ")
        # ascending order by price
        if sortMethod == "1":
            try:
                results = searcher.search(query, limit=20, sortedby="price")
            except TermNotFound:
                results = []
        # descending order by price
        elif sortMethod == "2":
            try:
                results = searcher.search(query, limit=20, sortedby="price", reverse=True)
            except TermNotFound:
                results = []
        # sort by review polarity value with highest values first
        elif sortMethod == "3":
            try:
                results = searcher.search(query, limit=20, sortedby="reviewPolarity", reverse=True)
            except TermNotFound:
                results = []
        # sort by rating with highest values first
        elif sortMethod == "4":
            try:
                results = searcher.search(query, limit=20, sortedby="rating", reverse=True)
            except TermNotFound:
                results = []
        # sort by highest savings absolute value
        elif sortMethod == "5":
            try:
                results = searcher.search(query, limit=20, sortedby="savings", reverse=True)
            except TermNotFound:
                results = []
        # sort by highest savings percentage
        elif sortMethod == "6":
            try:
                results = searcher.search(query, limit=20, sortedby="percentageSavings", reverse=True)
            except TermNotFound:
                results = []
        # sort by highest review polarity value and highest ratings
        elif sortMethod == "7":
            try:
                rP = sorting.FieldFacet("reviewPolarity", reverse=True)
                r = sorting.FieldFacet("rating", reverse=True)
                weightedValue = sorting.TranslateFacet(average, rP, r)
                results = searcher.search(query, limit=20, sortedby=weightedValue)
            except TermNotFound:
                results = []
        # sort by lowest price, highest review polarity value, highest ratings
        elif sortMethod == "8":
            try:
                rP = sorting.FieldFacet("reviewPolarity", reverse=True)
                r = sorting.FieldFacet("rating", reverse=True)
                weightedValue = sorting.TranslateFacet(average, rP, r)
                results = searcher.search(query, limit=20, sortedby=[weightedValue, "price"])
            except TermNotFound:
                results = []
        # search by price range
        elif sortMethod == "9":
            try:
                priceRangeLow = int(input("Enter the minimum price : "))
                priceRangeHigh = int(input("Enter the maximum price : "))
                numResultsDisplayed = int(input("Enter the number of records to be shown : "))
                results = searcher.search(query, limit=None, sortedby="price")
            except TermNotFound:
                results = []
        elif sortMethod == "10":
            try:
                countryData = input("Enter the country of origin : ")
                if re.match(r"(?i)(us)", countryData):
                    countryData = "usa"
                numResultsDisplayed = int(input("Enter the number of records to be shown : "))
                scores = sorting.ScoreFacet()
                results = searcher.search(qp.parse(user_query+" "+countryData), limit=None, sortedby=scores)
            except TermNotFound:
                results = []
        

        # print results
        print("{} files matched:".format(len(results)))
        # print individual records
        if sortMethod == "9":
            count = 0
            for hit in results:
                if priceRangeLow <= hit["price"] <= priceRangeHigh and count<numResultsDisplayed:
                    count+=1
                    print("Result {} : * {} *".format(count, hit['filename']) +"\n" +"Price : ${}".format(str(hit["price"]))+ "\n" + "Review score(higher is better) : {0:.2f}".format(hit["reviewPolarity"]) + "\n" + "Rating(higher is better) : {0:.2f}".format(hit["rating"]))
        elif sortMethod == "5" or sortMethod == "6":
            for hit in results:
                print(" * {} *".format(hit['filename']) +"\n" +"Price : ${}".format(str(hit["price"]))+ "\nSavings : ${}".format(str(hit["savings"]))+"\n% Savings : {0:.1f}%".format((hit["percentageSavings"])))
        elif sortMethod == "10":
            count = 0
            for hit in results:
                if count<numResultsDisplayed:
                    count+=1
                    print("Result {} : * {} *".format(count, hit['filename']) +"\nPrice : ${}".format(str(hit["price"]))+ "\nReview score(higher is better) : {0:.2f}".format(hit["reviewPolarity"]) + "\nRating(out of 5) : {0:.2f}".format(hit["rating"]) + "\nCountry of origin : {}".format(hit["countryOfOrigin"]))
        else:
            for hit in results:
                print(" * {} *".format(hit['filename']) +"\n" +"Price : ${}".format(str(hit["price"]))+ "\n" + "Review score(higher is better) : {0:.2f}".format(hit["reviewPolarity"]) + "\n" + "Rating(higher is better) : {0:.2f}".format(hit["rating"]))


if __name__ == '__main__':
    try:
        # get user query
        query = input("Enter a query: ")
    except IndexError:
        print('you need to provide a query. assuming "chicken" query.')
        search('chicken', 'index_dir')
    else:
        search(query, 'index_dir')
