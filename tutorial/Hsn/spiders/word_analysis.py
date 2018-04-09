from collections import Counter
import json
fileobj = open("HSN_products.json")
fileobj1 = open("HSN_products_2.json")
data = fileobj.read() + fileobj1.read() 
c = Counter(data.split())
keyValues = list(c.keys())
print("Unique words :" ,len(keyValues))

    

