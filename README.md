# Introduction

This project aims to create a ready to use tech stack with a focus on a development friendly environment. A single script entry point will allow one to transition between local, dev, test, and prod enviornments. The tech stack is meant to be for a monolithic application but some higher level microservices concepts are included in order to improve development time. General tech stack includes Apollo Graphql, Python, Reactjs, Docker/Docker compose, Postgresql, and Redis.

A working copy of the "Movie Fav" application can be found here https://www.moviefav.xyz 

The focus for the application has been mainly backend, server, and deployment related but there is plenty of client side implementaion to explore. Working more on the client side in the days to come.

The end result has been published on a simple AWS EC2 instance mainly using docker-compose. You can signup with your own email (check spam folder for email verification), or use the included account 
- username:makurichard14@gmail.com
- password:richardMaku1!

Feel free to reach out if you have any improvements, questions, or comments :) makurichard14@gmail.com

# Deployment
- for continuos deployment after initial set-up
  ```bash
      source run.sh pipeline prod up
  ```
  
# Development
 ### First Time Setup all dev
 - Install prerequisites in from admin/docs/linuxLocalDev.md
 - rename the sample-env file to .env and configure
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
       - script = local, docker, delpoy, pipeline
       - enviornment = dev, prod, test
       - command = build, up, down

       example: 
        ```bash 
           source run.sh docker dev build
           source run.sh docker dev up
        ```

 ### Running pytest
 - must be in local environment

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

- [x] add redis
- [x] add ci/cd pipelines
- [ ] add search
- [ ] clean up frontend for reusability
- [ ] create test enviornment for frontend
- [ ] possibly add protable kubernetes for orchestration
- [ ] add Cython or C extensions
- [ ] add multithreading
