from flask import Flask, render_template, request
import mysql.connector
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from tabulate import tabulate

app = Flask(__name__)

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="dogsinny",
    port="8889"
)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form['username']
    password = request.form['password']
    email = request.form['email']
    cursor = mydb.cursor()
    query = "INSERT INTO users (name, password, email) VALUES (%s, %s, %s)"
    values = (name, password, email)
    cursor.execute(query, values)
    mydb.commit()
    return render_template('submit.html', name=name)


@app.route('/dashboard/')
def dashboard():
    return render_template("dashboard.html")

@app.route('/rawdogdata', methods=['GET'])
def rawdogdata():
    cursor = mydb.cursor()
    query = "select * from dog limit 100;"
    cursor.execute(query)
    results = cursor.fetchall()
    return render_template('datatableDog.html', data=results)

@app.route('/rawlocdata', methods=['GET'])
def rawlocdata():
    cursor = mydb.cursor()
    query = "select * from location limit 100;"
    cursor.execute(query)
    results = cursor.fetchall()
    return render_template('datatable.html', data = results)

@app.route('/rawdisdata', methods=['GET'])
def rawdisdata():
    cursor = mydb.cursor()
    query = "select * from votingdistrict limit 100;"
    cursor.execute(query)
    results = cursor.fetchall()
    return results

@app.route('/rawdoglocdata', methods=['GET'])
def rawdoglocdata():
    cursor = mydb.cursor()
    query = "select dog.ID, Name, Gender, BirthMonth, Breed, LicenseExpirationDate, LicenseIssueDate, dog.CommunityDistrict, State, ZipCode, City, Borough from dog join location on dog.communitydistrict = location.communitydistrict limit 100;"
    cursor.execute(query)
    results = cursor.fetchall()
    return results

@app.route('/rawdogdisdata', methods=['GET'])
def rawdogdisdata():
    cursor = mydb.cursor()
    query = "select dog.ID, Name, Gender, BirthMonth, Breed, LicenseExpirationDate, LicenseIssueDate, dog.CommunityDistrict, CityCouncilDistrict, CongressionalDistrict, StateSenatorialDistrict, RowNumber, ZipCode from dog join votingdistrict on dog.communitydistrict = votingdistrict.communitydistrict limit 100;"
    cursor.execute(query)
    results = cursor.fetchall()
    return results

@app.route('/rawlocdisdata', methods=['GET'])
def rawlocdisdata():
    cursor = mydb.cursor()
    query = "select * from location join votingdistrict limit 100;"
    cursor.execute(query)
    results = cursor.fetchall()
    return results

@app.route('/rawdoglocdisdata', methods=['GET'])
def rawdoglocdisdata():
    cursor = mydb.cursor()
    query = "select dog.ID, Name, Gender, BirthMonth, Breed, LicenseExpirationDate, LicenseIssueDate, dog.CommunityDistrict, State, location.ZipCode, City, Borough, CityCouncilDistrict, CongressionalDistrict, StateSenatorialDistrict from dog join location on dog.communitydistrict = location.communitydistrict join votingdistrict on dog.communitydistrict = votingdistrict.communitydistrict limit 100;"
    cursor.execute(query)
    results = cursor.fetchall()
    return results


@app.route('/query/', methods=['GET'])
def query():
    return render_template("query.html")

@app.route('/bronx', methods=['GET'])
def bronx():
    cursor = mydb.cursor()
    query = "SELECT Name, breed, gender from dog join location on dog.communitydistrict = location.communitydistrict WHERE borough = 'Bronx' LIMIT 100"
    cursor.execute(query)
    results = cursor.fetchall()
    return results

@app.route('/brooklyn', methods=['GET'])
def brooklyn():
    cursor = mydb.cursor()
    query = "SELECT Name, breed, gender from dog join location on dog.communitydistrict = location.communitydistrict WHERE borough = 'Brooklyn' LIMIT 100"
    cursor.execute(query)
    results = cursor.fetchall()
    return results

@app.route('/manhattan', methods=['GET'])
def manhattan():
    cursor = mydb.cursor()
    query = "SELECT Name, breed, gender from dog join location on dog.communitydistrict = location.communitydistrict WHERE borough = 'Manhattan' LIMIT 100"
    cursor.execute(query)
    results = cursor.fetchall()
    return results

@app.route('/queens', methods=['GET'])
def queens():
    cursor = mydb.cursor()
    query = "SELECT Name, breed, gender from dog join location on dog.communitydistrict = location.communitydistrict WHERE borough = 'Queens' LIMIT 100"
    cursor.execute(query)
    results = cursor.fetchall()
    return results

@app.route('/staten', methods=['GET'])
def staten():
    cursor = mydb.cursor()
    query = "SELECT Name, breed, gender from dog join location on dog.communitydistrict = location.communitydistrict WHERE borough = 'Staten Island' LIMIT 100"
    cursor.execute(query)
    results = cursor.fetchall()
    return results

@app.route('/terrier', methods=['GET'])
def terrier():
    cursor = mydb.cursor()
    query = "SELECT borough, count(*) as 'Terriers' from dog join location on dog.communitydistrict = location.communitydistrict where breed like 'Terrier%' group by location.borough;"
    cursor.execute(query)

    borough = []
    count = []
    for i in cursor:
        borough.append(i[0])
        count.append(i[1])

    plt.bar(borough,count)
    plt.xlabel('Borough')
    plt.ylabel('Count of Terriers')
    plt.title('Terriers in New York')
    plt.xticks(rotation = 45)
    plt.show()

    cursor = mydb.cursor()
    query = "SELECT borough, count(*) as 'Terriers' from dog join location on dog.communitydistrict = location.communitydistrict where breed like 'Terrier%' group by location.borough;"
    cursor.execute(query)
    results = cursor.fetchall()

    return results

@app.route('/bronxbreeds/', methods=['GET'])
def bronxbreeds():
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
                  
    return render_template('query.html')

@app.route('/brookbreeds/', methods=['GET'])
def brookbreeds():
    cursor = mydb.cursor()
    query = ("SELECT breed, COUNT(*) FROM dogsinny.dog JOIN dogsinny.location ON dogsinny.dog.CommunityDistrict = dogsinny.location.CommunityDistrict WHERE borough = 'Brooklyn' GROUP BY Breed ORDER BY COUNT(*) DESC LIMIT 10;")
                  
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
    plt.title('Breed Count in Brooklyn')
    plt.xticks(rotation = 45)
    plt.show()
                  
    return render_template('query.html')

@app.route('/manbreeds/', methods=['GET'])
def manbreeds():
    cursor = mydb.cursor()
    query = ("SELECT breed, COUNT(*) FROM dogsinny.dog JOIN dogsinny.location ON dogsinny.dog.CommunityDistrict = dogsinny.location.CommunityDistrict WHERE borough = 'Manhattan' GROUP BY Breed ORDER BY COUNT(*) DESC LIMIT 10;")
                  
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
    plt.title('Breed Count in Manhattan')
    plt.xticks(rotation = 45)
    plt.show()
                  
    return render_template('query.html')

@app.route('/queensbreeds/', methods=['GET'])
def queensbreeds():
    cursor = mydb.cursor()
    query = ("SELECT breed, COUNT(*) FROM dogsinny.dog JOIN dogsinny.location ON dogsinny.dog.CommunityDistrict = dogsinny.location.CommunityDistrict WHERE borough = 'Queens' GROUP BY Breed ORDER BY COUNT(*) DESC LIMIT 10;")
                  
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
    plt.title('Breed Count in Queens')
    plt.xticks(rotation = 45)
    plt.show()
                  
    return render_template('query.html')

@app.route('/statenbreeds/', methods=['GET'])
def statenbreeds():
    cursor = mydb.cursor()
    query = ("SELECT breed, COUNT(*) FROM dogsinny.dog JOIN dogsinny.location ON dogsinny.dog.CommunityDistrict = dogsinny.location.CommunityDistrict WHERE borough = 'Staten Island' GROUP BY Breed ORDER BY COUNT(*) DESC LIMIT 10;")
                  
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
    plt.title('Breed Count in Staten Island')
    plt.xticks(rotation = 45)
    plt.show()
                  
    return render_template('query.html')

if __name__ == "__main__":
    app.run()
