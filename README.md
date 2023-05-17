# google-translate-fastapi by koviTek solutions
=============================================

### Description

This is a microservice built with FastAPI that provides an API for working with word translations using Google Translate. It allows you to retrieve word details, store words in a database, and perform filtering and pagination on the stored words. The API besides translations, also provides additional attributes such as;
 
- alternative translation
- synonyms (in source language)
- definition (in source language)
- example use (in source language)

The solution utilises googletrans python package an unofficial Google Translate API as the official
tool only provides translation, no additional characteristics. This API is hosted and deployed on AWS using their ECS service and uses NGINX as a reverse proxy.

### Features

- Retrieve word details including definitions, synonyms, translations, and examples from Google Translate.
- Store word details in a database (this solution uses mongoDB).
- Get a list of words stored in the database with support for pagination, sorting, and filtering.
- Delete a word from the database.
- Customizable response based on query parameters.
- Handle validation errors

### User Manual

The API is available at: http://kovitek-google-translate-489384591.eu-west-2.elb.amazonaws.com domain

Here is the API documentation on how to use the various endpoints and what are the required query parameters: http://kovitek-google-translate-489384591.eu-west-2.elb.amazonaws.com/docs

Here is an example how a successful request looks like to the '\translations\<word>' route;

![image](https://github.com/r7kowi/fastapi-google-translate/assets/58402318/67c6dbf8-e9ce-42a2-9ec4-fe9269fe8efb)

The above currently is hosted on AWS through their ECS service but since its dockerized it can be hosted on any cloud platform. If you want to replicate the above solution to run it on on your host machine please follow the below instructions. 

### Requirements

- Docker
- MongoDB

### Installation 

1. Clone the repository:

   ```bash
   git clone https://github.com/r7kowi/fastapi-google-translate.git

2. Navigate to the project directory:

   ```bash
   cd fastapi-google-translate

3. Set up the environment variables by creating a .env file in the root folder and filling in the necessary values (you need to sign-up to mongodb and setup a server):

   ```bash
   MONGO_DB_CONNECTION_URI=<your_database_url>
   MONGO_DB_NAME = yourDb
   
4. Run docker compose to build and run the containers

   ```bash
   docker-compose up --build
   
The application will be accessible at http://localhost:80.
   
   
