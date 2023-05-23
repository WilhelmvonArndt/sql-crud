#Munge
import csv
import datetime
import random
import pandas as pd 

rows = []
with open("data/posts.csv", 'r') as file:
    csvreader = csv.reader(file)
    for row in csvreader:
        rows.append(row)


edited_rows = []



na = "NULL"

for row in rows[1:]:
    int = random.randint(1,2)
    
    if int == 1: #Treatment if post is story
        row[2] = ""
        row[3] = ""
        row[4] = ""
    
    if int == 2: #Treatment if post is message
        row[5] = ""

df = pd.DataFrame(rows)

df.to_csv('output.csv', index=False)