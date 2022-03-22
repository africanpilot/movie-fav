# Introduction

This project aims to create a ready to use tech stack with a focus on a development friendly environment. A single script entry point will allow one to transition between local, dev, test, and prod enviornments. The tech stack is meant to be for a monolithic application but some higher level microservices concepts are included in order to improve development time. General tech stack includes Apollo Graphql, Python, Reactjs, Docker/Docker compose, Postgresql.

A working copy of the "Movie Fav" application can be found here https://www.moviefav.xyz 

The focus for the application has been mainly backend, server, and deployment related but there is plenty of client side implementaion to explore. Working more on the client side in the days to come.

The end result has been published on a simple AWS EC2 instance mainly using docker-compose. You can signup with your own email (check spam folder for email verification), or use the included account 
- username:makurichard14@gmail.com
- password:richardMaku1!

Feel free to reach out if you have any improvements, questions, or comments :) makurichard14@gmail.com

# Deployment
- Using ubuntu EC2 on aws.
  - get key pair
  - Create instance
  - configure your .env and install-init.sh files locally
    - you will have to use personal auth token as password (https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token)

  - cd to directory of the .pem file (mine was one folder above my local repo)
  
  ```bash
    sudo scp -i moviefav.pem  movie-fav/.env ubuntu@0.0.0.0:/home/ubuntu/
    sudo scp -i moviefav.pem  movie-fav/admin/tools/install-init.sh ubuntu@0.0.0.0:/home/ubuntu/
    sudo ssh -i moviefav.pem ubuntu@0.0.0.0
    source install-init.sh
    source run.sh deploy prod build
    source run.sh deploy prod up
  ```
  - NOTE: ***update the "0.0.0.0" to the public address of your instance
  
  
# Development
 ### First Time Setup docker dev
 - Install docker and docker-compose
 - rename the sample-env file to .env
 - in .env file change MOVIE_FAV_EMAIL to your email
 - in .env file change SENDGRID_API_KEY to your API ( get api from https://app.sendgrid.com/)
 - run 
  ```bash 
     source run.sh docker dev build
     source run.sh docker dev up
  ```

 ### Enviornments and commands

   - you can run devlopment enviornments and deployments with: 
  
     ```bash 
        source run.sh [script] [enviornment] [command]
     ```
       - script = local, docker, delpoy
       - enviornment = dev, prod, test
       - command = build, up, down

       example: 
        ```bash 
           source run.sh docker dev build
           source run.sh docker dev up
        ```

 ### Running pytest
 - must be in local envirnment

     ```bash 
         source run.sh local test up
         source run.sh local test down
     ```

   example:
     ```python 
       pytest -v -m account server/apps/account
       pytest -v -m account_bench server/apps/account
     ```
# TODO

- [ ] add redis
- [ ] add devops ci/cd pipelines
- [ ] clean up frontend for reusability
- [ ] create test enviornment for frontend
- [ ] possibly add protable kubernetes for orchestration
- [ ] add search