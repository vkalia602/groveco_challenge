# Store Locator CLI tool
A lightweight tool to search for stores near given address.

## Environment
This is a Python 3 project. 

## Dependencies
* __Database:__ local csv file
* __Other Packages:__

## Instructions
* Before running the program make sure all the dependencies listed in the requirements.txt are installed.
* run program: run ```./app.py``` - This will give you instructions on how the programs accept arguments
    * example: ```./app.py --address="248 Sunrise Hwy, Freeport, NY"```
* run test suite: ```python3 -m unittest```

## Caveat
This program finds the nearest stores from the user provided address. It is a basic CLI tool with address capabilities. The distance is implemented with the haversine's formula to determine distance. The program can be optimized by dumping the CSV data into a NOSQL database where it can be easily accessed with Latitude and Longitude. Creating the boundary box helps narrow down data choices from the list of stores but it limits the radius to a hard coded distance. This can be acquired fromt the user by adding another flag like --radius. All the distance calculations are done in Km by default. This is another feature that can be added into the code. Basic features were implemented in the given time constraint but features could be drastically improved to give user more control over various things like the output format, distance calculations etc. 

## Author
Vasudha kalia
    

