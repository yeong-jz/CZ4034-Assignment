import re
import json
import csv
import io

fileobj = open("HSN_products.json")
fileobj1 = open("HSN_products_2.json")
data = json.load(fileobj)
data1 = json.load(fileobj1)

categories = []
num_of_training = 100000

c1 = c2 = c3 = c4 = c5 = c6 = c7 = c8 = c9 = c10 = c11 = 0
count = 0
# iterate through items and get list of categories to be processed
for item in data and data1:
    # remove those categories which are too few for training
    if not re.match(r"(?i)(null|more|gift store|baby|barware)", item["product_category"]):
        if item["product_category"] not in categories:
            categories.append(item["product_category"])
            
num_of_records = num_of_training/len(categories)


# create training records file
with open('training.csv', 'w', encoding='utf-8', newline='') as csvfile:
    writer = csv.writer(csvfile, delimiter=',')
    writer.writerow(["Category","Item Name"])
    for item in data and data1:
        if not re.match(r"(?i)(null|more|gift store|baby|barware)", item["product_category"]):
            if count<num_of_training:
                if item["product_category"] == categories[0] and c1<num_of_records:
                    c1+=1
                    writer.writerow([item["product_category"], item["name"]])
                elif item["product_category"] == categories[1] and c2<num_of_records:
                    c2+=1
                    writer.writerow([item["product_category"], item["name"]])
                elif item["product_category"] == categories[2] and c3<num_of_records:
                    c3+=1
                    writer.writerow([item["product_category"], item["name"]])
                elif item["product_category"] == categories[3] and c4<num_of_records:
                    c4+=1
                    writer.writerow([item["product_category"], item["name"]])
                elif item["product_category"] == categories[4] and c5<num_of_records:
                    c5+=1
                    writer.writerow([item["product_category"], item["name"]])
                elif item["product_category"] == categories[5] and c6<num_of_records:
                    c6+=1
                    writer.writerow([item["product_category"], item["name"]])
                elif item["product_category"] == categories[6] and c7<num_of_records:
                    c7+=1
                    writer.writerow([item["product_category"], item["name"]])
                elif item["product_category"] == categories[7] and c8<num_of_records:
                    c8+=1
                    writer.writerow([item["product_category"], item["name"]])
                elif item["product_category"] == categories[8] and c9<num_of_records:
                    c9+=1
                    writer.writerow([item["product_category"], item["name"]])
                elif item["product_category"] == categories[9] and c10<num_of_records:
                    c10+=1
                    writer.writerow([item["product_category"], item["name"]])
                elif item["product_category"] == categories[10] and c11<num_of_records:
                    c11+=1
                    writer.writerow([item["product_category"], item["name"]])
                count = c1 + c2 + c3 + c4 + c5 + c6 + c7 + c8 + c9 + c10 + c11

# create test records file
with open('test.csv', 'w', encoding='utf-8', newline='') as csvfile:
    writer = csv.writer(csvfile, delimiter=',')
    writer.writerow(["Category","Item Name"])
    for item in data and data1:
        if not re.match(r"(?i)(null|more|gift store|baby|barware)", item["product_category"]):
            writer.writerow([item["product_category"], item["name"]])
