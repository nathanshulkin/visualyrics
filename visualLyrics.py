# Nathan Shulkin
# data visualizing


#
# pip install mysql-connector-python
# pip install numpy
# pip install matplotlib
# pip install pandas
#
# pip install plotly
from plotly.graph_objs import Scatter, Bar
from plotly.subplots import make_subplots
from plotly import offline

import mysql.connector
import numpy as np
import matplotlib.pyplot as plt
# import pandas as pd


print('what is the password?')
psswd = str(input())

# create DB
# DB MUST EXIST/BE CREATED IN MYSQL (USE TERMINAL) AND CREATE TABLE IN DB
lyricDB = mysql.connector.connect(
    host="192.168.0.6",  # IP address
    user="root",
    password=psswd,  # computer user password
    database="lyricDB"
)

# initialize DB
lyricCursor = lyricDB.cursor()

print('what database would you like to use?')
dbChoice = str(input())

dbCheck = 0
while dbCheck == 0:
    try:
        # initialize DB
        check = "select * from " + dbChoice
        lyricCursor.execute(check)
        checkords = lyricCursor.fetchall()
        dbCheck = 1
    except:
        print('\nsorry that was not one of the databases. Try again.')
        dbChoice = str(input())


print('what artist?')
choice = str(input())
print('\n\n')


# select from database
if choice == 'top':
    select = "select * from artistTOT ORDER BY (uniqTOT/numbSongs) DESC"
elif choice == 'all':
    select = "select * from artistTOT ORDER by artist"
else:
    select = "select * from artistTOT where artist like \"" + str(choice) + "\""

lyricCursor.execute(select)

records = lyricCursor.fetchall()


# plotting data
artists = []
uwScore = []
twScore = []
x_axis = []
y_axis = []


if choice == 'top' or choice == 'all':
    # for each artist get total and unique words and scores, make x and y axis
    for artist in records:
        artists.append(artist[0])
        x_axis.append(artist[1])
        y_axis.append(artist[2])

        # get unique and total scores, round them
        uScore = round(artist[2]/artist[3], 1)
        tScore = round(artist[1]/artist[3], 1)
        uwScore.append(uScore)
        twScore.append(tScore)

    # plotting with plotly
    # scatter plot, color gradient
    scatterData = [{
        'type': 'scatter',
        'x': x_axis,
        'y': y_axis,
        'text': artists,
        'mode': 'markers',
        # 'size': 10,
        'marker': {
            'colorscale': 'Bluered',
            'color': y_axis,
            'colorbar': {'title': 'Value'},
        }
    }]

    # layout as dictionary/json for graph object
    scatLayout = {
        'title': 'Artist Total Words vs. Unique Words',
        'xaxis': {
            'title': 'Total Words',
        },
        'yaxis': {
            'title': 'Unique Words',
        },
    }

    offline.plot({'data': scatterData, 'layout': scatLayout}, filename='lyricGraph.html')


# single artist
else:
    print(records)
