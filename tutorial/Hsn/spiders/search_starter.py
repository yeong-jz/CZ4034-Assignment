#!/usr/bin/env python
import codecs
import sys
import os
import os.path
import json
import re
from whoosh import index
from whoosh import highlight
from whoosh.spelling import Corrector, QueryCorrector
from whoosh.fields import ID, TEXT, Schema, NUMERIC
from whoosh.analysis import CharsetFilter, StemmingAnalyzer, StopFilter
from whoosh.support.charset import accent_map
from whoosh.reading import TermNotFound
from whoosh.qparser import QueryParser


hsn_analyzer = StemmingAnalyzer() | CharsetFilter(accent_map) | StopFilter()
SCHEMA = Schema(filename=ID(unique=True, stored=True),
                content=TEXT(analyzer=hsn_analyzer, spelling=True, stored=True),
                price=NUMERIC(sortable=True, stored=True),
                rating=NUMERIC(sortable=True, stored=True),
                noOfReviews=NUMERIC(sortable=True, stored=True),
                savings=NUMERIC(sortable=True, stored=True),
                review=TEXT(analyzer=hsn_analyzer, spelling=True),
                )
def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def get_or_create_index(index_dir):
    if not os.path.exists(index_dir):
        os.mkdir(index_dir)

    if index.exists_in(index_dir):
        #uncomment if running for first time
        #return full_index(index_dir)
        return index.open_dir(index_dir)
    else:
        return full_index(index_dir)


def full_index(index_dir):
    idx = index.create_in(index_dir, SCHEMA)
    writer = idx.writer(procs=4, limitmb=1024, multisegment=True)

    datas = []
    fileobj = open("HSN_products.json")
    fileobj1 = open("HSN_products_2.json")
    data = json.load(fileobj)
    data1 = json.load(fileobj1)
    for item in data:
        # check if the string contains price data
        if is_number(item["price"][1:].strip()):
            # convert to float type for sorting
            item_price = float(item["price"][1:])
        else:
            item_price = 100000
        if is_number(item["noOfReviews"][0:2].strip()):
            # convert to float type for sorting
            item_num_reviews = float(item["noOfReviews"][0:2])
        else:
            item_num_reviews = 100000
        if is_number(item["rating"][0:2].strip()):
            # convert to float type for sorting
            item_rating = float(item["rating"][0:2])
        else:
            item_rating = 100000
        writer.add_document(filename=item["name"], content=json.dumps(item), price=item_price, rating=item_rating, noOfReviews=item_num_reviews, review=item["review"])
    for item in data1:
        if is_number(item["price"][1:].strip()):
            # convert to float type for sorting
            item_price = float(item["price"][1:])
        else:
            item_price = 100000
        if is_number(item["noOfReviews"][0:2].strip()):
            # convert to float type for sorting
            item_num_reviews = float(item["noOfReviews"][0:2])
        else:
            item_num_reviews = 100000
        if is_number(item["rating"][0:2].strip()):
            # convert to float type for sorting
            item_rating = float(item["rating"][0:2])
        else:
            item_rating = 100000
        writer.add_document(filename=item["name"], content=json.dumps(item),price=item_price, rating=item_rating, noOfReviews=item_num_reviews, review=item["review"])
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
        # do search
        try:
            results = searcher.search(query, limit=50, sortedby="price")
        except TermNotFound:
            results = []

        # print results
        print("{} files matched:".format(len(results)))
        # results.fragmenter.maxchars = 100
        for hit in results:
            if hit["price"] == 100000:
                price = "No price stated."
                print("  * {}".format(hit['filename']) +"\n" +"Price : {}".format(price))
            else:
                print("  * {}".format(hit['filename']) +"\n" +"Price : ${}".format(str(hit["price"])))


if __name__ == '__main__':
    try:
        query = input("Enter a query: ")
    except IndexError:
        print('you need to provide a query. assuming "chicken" query.')
        search('chicken', 'index_dir')
    else:
        search(query, 'index_dir')
