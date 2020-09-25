# Nathan Shulkin
# data visualizing


#
# pip install mysql-connector-python
# pip install numpy
# pip install matplotlib
# pip install pandas
#

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
    select = "select * from artistTOT ORDER BY (uniqTOT/numbSongs) DESC LIMIT 6"
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
        plt.annotate(str(artist[0]), (artist[1], artist[2]))

        # get unique and total scores, round them
        uScore = round(artist[2]/artist[3], 1)
        tScore = round(artist[1]/artist[3], 1)
        uwScore.append(uScore)
        twScore.append(tScore)

    # plotting the data, with labels on axisssss
    plt.plot(x_axis, y_axis, 'ro')
    plt.xlabel('total words')
    plt.ylabel('unique words')
    plt.title('Artist Total Words vs. Unique Words')
    #plt.show()

    # bar graph hopefully
    xLength = np.arange(len(artists))  # the label locations
    width1 = 0.3  # the width of the bars

    # sect up our rectangles/bars
    fig1, ax1 = plt.subplots()
    rectangs = ax1.bar(xLength + width1 / 4, uwScore, width1, label='unique words/# songs')
    artistWords = []
    i = 0

    for rectang in rectangs:
        height = rectang.get_height()
        artistWords.append(str(artists[i]) + '\n' + '(' + str(height) + ')')
        i += 1

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax1.set_ylabel('Words per Song')
    ax1.set_title('Unique Words per Song')
    ax1.set_xticks(xLength)
    ax1.set_xticklabels(artistWords)
    ax1.legend()

    fig1.tight_layout()
    #plt.show()

    # bar graph hopefully
    x = np.arange(len(artists))  # the label locations
    width = 0.3  # the width of the bars

    # sect up our rectangles/bars
    fig, ax = plt.subplots()
    rects1 = ax.bar(x - width / 2, twScore, width, label='total words/# songs')
    rects2 = ax.bar(x + width / 2, uwScore, width, label='unique words/# songs')

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('Words per Song')
    ax.set_title('Total and Unique Words per Song')
    ax.set_xticks(x)
    unScore = []
    artistScore = []
    i = 0
    for t in twScore:
        roundScore = round((uwScore[i]/t) * 100, 2)
        #percScore = str(roundScore * 100) + "%"
        unScore.append(str(roundScore) + "%")
        i += 1
    i = 0
    for ar in artists:
        artistScore.append(str(ar) + "\n" + str(unScore[i]))
        i += 1

    ax.set_xticklabels(artistScore)
    ax.legend()


    def autolabel(rects):
        """Attach a text label above each bar in *rects*, displaying its height."""
        for rect in rects:
            height = rect.get_height()
            ax.annotate('{}'.format(height),
                        xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 3),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom')


    autolabel(rects1)
    autolabel(rects2)

    fig.tight_layout()

    plt.show()

# single artist
else:
    print(records)
