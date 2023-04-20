import mysql
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
         
mydb = mysql.connector.connect(
         host="localhost",
         user="root",
         password="root",
         database="dogsinny"
)

cursor = mydb.cursor()
         
query = ("SELECT breed, COUNT(*) FROM dogsinny.dog JOIN dogsinny.location ON dogsinny.dog.CommunityDistrict = dogsinny.location.CommunityDistrict WHERE borough = 'Bronx' GROUP BY Breed ORDER BY COUNT(*) DESC LIMIT 10;")
         
cursor.execute(query)
result = cursor.fetchall
         
breed = []
count = []
for i in cursor:
         breed.append(i[0])
         count.append(i[1])
         
plt.bar(breed,count)
plt.xlabel('Dog Breed')
plt.ylabel('Count of Breed')
plt.title('Breed Count in the Bronx')
plt.xticks(rotation = 45)
plt.show()
         
cursor.close()
mydb.close()
