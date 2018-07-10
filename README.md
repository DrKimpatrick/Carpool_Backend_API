[![Build Status](https://travis-ci.org/DrKimpatrick/Andela_bootcamp_week_2.svg?branch=master)](https://travis-ci.org/DrKimpatrick/Andela_bootcamp_week_2)
[![Coverage Status](https://coveralls.io/repos/github/DrKimpatrick/Andela_bootcamp_week_2/badge.svg?branch=master)](https://coveralls.io/github/DrKimpatrick/Andela_bootcamp_week_2?branch=master)
[![Maintainability](https://api.codeclimate.com/v1/badges/70062b7c4a5089d378a7/maintainability)](https://codeclimate.com/github/DrKimpatrick/Andela_bootcamp_week_2/maintainability)

# Ride-my-way (Carpool Andela Bootcamp 09 Project)

Ride-my-way App is a carpooling application that provides drivers with the ability to create ride oﬀers  and passengers to join available ride oﬀers.

## Overview
- ## User (s)
The users of the application are travelers and commuters who want to go from one place to 
another or users that are driving a trip and want to find passengers. Users can act as both passengers and 
drivers while using an application

- ### Driver
A driver is any person that owns a car and wants to go from one place to another and publishes 
his trip on the application in order to find passengers to share the ride with.

- ### Passenger
A passenger is any person that doesn’t own a car and wants to join a driver in a trip he posted 
and agrees to all the conditions specified (price and general behavior). 


**Features**

    - Register a user
    - Login a user 
    - Fetch all available rides 
    - Fetch the details of a single ride
    - Make a ride request
    - Create a ride offer 
    - Fetch all ride requests
    - Get rides for the current user
**API end points**

- POST api/v1/auth/signup (create account) 
- POST api/v1/auth/login (login user)
- GET api/v1/users/rides (Create ride offer)
- GET api/v1/rides (get all rides)
- GET api/v1/users/rides/#/requests (view a list of ride requests to the ride)
- GET api/v1/this/user/rides (rides given)
- PUT api/v1/users/rides/5/reaction (reject or accept request)
- POST api/v1/rides/#/requests (Make ride request)
- GET api/v1/users (List all application users)

**Getting Started**

These instructions will enable you to run the project on your local machine.

**Prerequisites**

Below are the things you need to get the project up and running.

- git : To update and clone the repository
- python3: Language used to develop the api
- pip: A python package used to install project requirements specified in the requirements text file.

**Installing the project**

Type: 
        
       "https://github.com/DrKimpatrick/Andela_bootcamp_week_2.git"
  in the terminal or git bash or command prompt.

To install the requirements. run:

      pip install -r requirements.txt

cd to the folder ride-my-way
And from the root of the folder, type:
      
      python run.py
      
To run the tests and coverage, from the root folder, type: 
        
        coverage run -m pytest
        coverage report
