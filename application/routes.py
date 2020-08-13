from flask import Flask, render_template
from application import app
import requests

######################################################
# Problem:                          
# "Build an API which calls the API
# https://bpdts-test-app.herokuapp.com 
# and returns people who are listed as either living
# in London, or whose current coordinates are 
# within 50 miles of London.  
######################################################

@app.route('/')
@app.route('/home', methods=['GET'])
def home():
    url = 'https://bpdts-test-app.herokuapp.com'
    """
    /city/London/users
    /instructions
    /users/{id}
    /users
    """

    # get London user data
    data_london_user = requests.get(url + '/city/London/users')

    # get user data
    data_user = requests.get(url + '/users')

    # set London coordinates
    # https://www.latlong.net/place/london-the-uk-14153.html
    london_latitude = '51.509865'
    london_longitude = '-0.118092'

    users_50_miles_result =[] # store result for users within 50 miles from London

    # Loop through users data and return indecies of those within 50 miles from London
    count = 0
    
    while count < 1000: # there are 999 users
        # get user coordinates
        user_latitude = str(data_user.json()[count]['latitude'])
        user_longitude = str(data_user.json()[count]['longitude'])

        # used Coordinate Distance Calculator, another option was to register with
        # freemium account with APIs geolocation services and get API keys

        # get distance between London and user location
        data = requests.get('http://boulter.com/gps/distance/?from=' + london_latitude + '%2C' + london_longitude + '&to=' + user_latitude + '%2C' + user_longitude + '&units=m#more')

        # get index where the ditance number in API url result
        miles_indx = [i for i in range(len(data.text)) if data.text.startswith('miles', i)]

        # get string of distance result
        result = data.text[miles_indx[0]-20:miles_indx[0]-1:]

        # get distance as number
        result = float(result[result.find("<TD>") + 4::])

        # check if distance more than 50 miles from London
        if (50 - result) >= 0:
            # true only user is inside London
            users_50_miles_result.append(data_user.json()[count])
        count += 1
    
    london_users_result = data_london_user.json()
    return render_template('home.html',result1=london_users_result, result2=users_50_miles_result)