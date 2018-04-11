from collections import Counter
import json
##fileobj = open("HSN_products.json")
##fileobj1 = open("HSN_products_2.json")
fileobj = open("HSN_products_3.json")
count=0
data = fileobj.read()
for i in data.split():
    count+=1
c = Counter(data.split())
keyValues = list(c.keys())
print("Unique words :" ,len(keyValues))
print("Total no. of words:", count)
    

