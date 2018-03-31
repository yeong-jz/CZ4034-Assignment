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
from whoosh.fields import ID, TEXT, Schema
from whoosh.analysis import CharsetFilter, StemmingAnalyzer, StopFilter
from whoosh.support.charset import accent_map
from whoosh.reading import TermNotFound
from whoosh.qparser import QueryParser


hsn_analyzer = StemmingAnalyzer() | CharsetFilter(accent_map) | StopFilter()
SCHEMA = Schema(filename=ID(unique=True, stored=True),
                content=TEXT(analyzer=hsn_analyzer, spelling=True),
                )


def get_or_create_index(index_dir):
    if not os.path.exists(index_dir):
        os.mkdir(index_dir)

    if index.exists_in(index_dir):
        return index.open_dir(index_dir)
    else:
        return full_index(index_dir)


def full_index(index_dir):
    idx = index.create_in(index_dir, SCHEMA)
    writer = idx.writer(procs=4, limitmb=1024, multisegment=True)

    datas = []

    # TODO: get data
##    for path, subdirs, files in os.walk(r'D:\Documents\CZ4034\whoosh-tutorial\pdfs'):
##        for filename in files:
##            f = os.path.join(path, filename)
##            fileobj = codecs.open(f, "rb", "utf-8")
##            content = fileobj.read()
##            writer.add_document(filename=filename, content=content)
##            fileobj.close()

##    for path, subdirs, files in os.walk(r'D:\Documents\CZ4034\whoosh-tutorial\text'):
##        for filename in files:
##            f = os.path.join(path, filename)
##            fileobj = codecs.open(f, "rb", "utf-8")
##            content = fileobj.read()
##            writer.add_document(filename=filename, content=content)
##            fileobj.close()

    fileobj = open("HSN_products.json")
    fileobj1 = open("HSN_products_2.json")
    data = json.load(fileobj)
    data1 = json.load(fileobj1)
    for item in data:
        writer.add_document(filename=item["name"], content=json.dumps(item))
    for item in data1:
        writer.add_document(filename=item["name"], content=json.dumps(item))
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
        corrector = searcher.corrector("content")
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
            results = searcher.search(query, limit=50)
        except TermNotFound:
            results = []

        # print results
        print("{} files matched:".format(len(results)))
        # results.fragmenter.maxchars = 100
        for hit in results:
##            filecontents = ''
##            with open(hit['text_filename']) as file_:
##                filecontents = file_.read()
##                highlight = (hit
##                          .highlights("content", text=filecontents, top=2)
##                          .replace("\n", " ").strip())
            print("  * {}".format(hit['filename']))


if __name__ == '__main__':
    try:
        query = input("Enter a query: ")
    except IndexError:
        print('you need to provide a query. assuming "chicken" query.')
        search('chicken', 'index_dir')
    else:
        search(query, 'index_dir')
