# Objective
 
The main goal is to see how you would create an easy to industrialize pipeline for storing and analyzing temperatures using different data sources. 
 
You can develop this pipeline using Python, Node.js or Java. Please, use the language you feel the most comfortable with.
Don't worry, we do not expect a streaming application. We would instead expect the application to run every hour. So please take this into account when you design the architecture.
 
# Context
 
A new partner in IoT gives us the measures of temperatures coming from their sensors. 
We can access their measures using the following API.
 
``` 
curl -H "X-API-Key: dd764f40" https://my.api.mockaroo.com/sensor/temperatures
``` 
 
This Rest API will send you back a json with the following schema:
 
```
[
  {
    "id": "1b16b092-e8e8-490b-a9be-0db1580fb164", // An unique id 
        "timestamp": "2019-02-19 14:02:10", // the timestamp at which the record was taken
        "lat": 45.6258385, // latitude
        "lon": 0.0629891, // longitude
        "temperature": 29.4068, // the temperature value
        "country": "France" // the country
  }
]
```
 
Every record contains the temperature at the moment you call the API. If you call the API twice you will then get different results.
 
Our objective is to find out the mean temperature for every region in France.
 
The following link will give you for every town, their GPS coordinates/
 
```
https://www.data.gouv.fr/fr/datasets/listes-des-communes-geolocalisees-par-regions-departements-circonscriptions-nd/
```
(You can also find the file in `/data/coordinates_regions.csv` in this repository.)


Once you aggregate the data, you can send the results to one of our database. You will provide you with the credentials and info.
 
We expect to find at least one table in this database that satisfies the following schema:
 
 * hour (the time at the import was started)
 * region
 * temperature
 * numberOfPoints (the number of points used to compute the mean temperature)
 

## Region definition

The preceeding link provides us with a list of cities with their associated region. However, to perform the matchin, we need to get the GPS coordinates of every region. In order to ease the test, we are going to assume that regions are rectangles. Even though this does not make any sense in the real world, this is a shortcut to make your life easier ;)

If we call `E` the list of cities and their GPS points for a region, then we define the bounding box for the region as : 
``` 
R = ( { min(latitude) in E, min(longitude) in E } ; { max(latitude) in E, max(longitude) in E } )
```

For instance, if for a given region, we get the following list of GPS coordinates:

![Points within region](images/region-points.png)

Then we define the associated region as:

![Region shape](images/region-shape.png)

# SQL
 
Once we get all your data set up, we would like you to write a SQL query that gives us the following information: for every region and every hour, we want the temperature at this hour and also the temperature 3 hours before.
 
The dataset should then look like :
 
| Region  | Hour  | Temperature  | Temperature3HoursBefore  |
|---|---|---|---|
| ...  | ...  | ...  |  ... |
 
# Scalability 
 
If you were to develop the same application where the dataset was a few hundreds of terabytes, what would you do differently ? What technological choices would you make ? The goal here is not to develop anything but rather explain the ideal solution.

# Versioning

If our data source was to emit multiple versions (corrections for instance) of the same data, what could be the different applicable strategies ?

# Operations

What processes, infrastructure, products,... would you use to make sure the whole pipeline runs fine in production ?

# Key Points
 
The key points we will be looking at are:
 
    * Architecture and design. 
    * Code quality.
    * Test
    * Tech choices.
    * Scalability
    * Error Handling
    * Backup
    * Continuous integration
 
We know you may not have the time to make everything work fine, so it's ok to create dummy functions i.e functions that do nothing but are important for the process. Take your time to comment / show your ideas. 
 
