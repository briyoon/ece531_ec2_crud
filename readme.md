# ECE531 EC2 CRUD
Simple CRUD app in a docker container using FastAPI. DB is using sqlite3. Since this is just a toy CRUD assignment, db will reset upon container restart. If you want to make a more permenant solution you would use a traditional SQL db and use docker compose to maintian a separate container just for the db. This is so you can separate db updates with app updates.

## To Run
1. Build docker container
    - docker build -t ec2_crud .
2. Run docker container
    - docker run -p 5000:5000 -e PORT=5000 ec2_crud
3. Goto localhost:5000/docs to read API documentation. It provides the correct CURL commands to execute the routes. You can either copy the command or press "try it out" and execute in browser.