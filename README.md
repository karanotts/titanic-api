```
  _______ __              _      ___    ____  ____
 /_  __(_) /_____ _____  (_)____/   |  / __ \/  _/
  / / / / __/ __ `/ __ \/ / ___/ /| | / /_/ // /  
 / / / / /_/ /_/ / / / / / /__/ ___ |/ ____// /   
/_/ /_/\__/\__,_/_/ /_/_/\___/_/  |_/_/   /___/   
                                                   
```
Simple API that allows performing CRUD operations on an attached database. 

This solution allows to import the data from attached CSV file into MongoDB database and performing operations.


Get all passenger entries from the database:
``` 
curl -X 'GET' \
  'http://localhost:8000/people' \
  -H 'accept: application/json' 
```

Get one passenger entry from the database: 
``` 
curl -X 'GET' \
  'http://localhost:8000/people/6113c435d7312012f95be756' \
  -H 'accept: application/json'
```

Creat new passenger entry in the database: 
``` 
curl -X 'POST' \
  'http://localhost:8000/people' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "Survived": false,
  "Pclass": 3,
  "Name": "Mr. Owen Harris Braund",
  "Sex": "male",
  "Age": 22,
  "Siblings/Spouses Aboard": 1,
  "Parents/Children Aboard": 0,
  "Fare": 7.25
}'
```

Update one passenger entry in the database:
``` 
curl -X 'PUT' \
  'http://localhost:8000/people/6113c435d7312012f95be756' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "Survived": false,
  "Pclass": 3,
  "Name": "Mr. Owen Harris Braund",
  "Sex": "male",
  "Age": 22,
  "Siblings/Spouses Aboard": 1,
  "Parents/Children Aboard": 0,
  "Fare": 7.25
}'
```

Delete one passenger entry from the database:
``` 
curl -X 'DELETE' \
  'http://localhost:8000/people/6113c435d7312012f95be756' \
  -H 'accept: application/json'
```


## How to use this app
### TRY THE APP LOCALLY (Dev mode, Linux)
-----------------------------------------
You can test the API app locally on a Linux system with docker installed. Clone the repository and navigate to root directory and then:
- run `make install` to fetch dependencies
- run `make db` to start mongo docker contrainer and import data from `titanic.csv` file
- run `make test` to run tests
- run `make clean` to clean up environment

### RUN THE APP IN DOCKER (Linux)
---------------------------------
Ensure you got docker installed on your machine. Clone this repository and from the root directory and then:
- run `docker-compose build` to fetch database images from the registry and build the image app from `Dockerfile`
- run `docker-compose up` (or `docker-compose up -d` to run task in background) and navigate to `http://localhost:8000/` in your browser to see the app
- to stop the app, hit `Ctrl+C` if you run it in foreground, or type `docker-compose down` if you run it in background

### RUN THE APP IN KUBERNETES (Linux)
-------------------------------------
You can use `deploy_k8s.sh` script to run this app on Kubernetes.
The script will create reasources from Kubernetes manifests located in `k8s/` directory, and then import the database into pod that runs `mongo`. 
Navigate to `http://localhost:8000/` in your browser to see the app. 
Run `cleanup_k8s.sh` to delete Kubernetes resources.
