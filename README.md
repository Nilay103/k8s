## Microservice Architecture and System Design with Python & Kubernetes

### Project Title: Video to MP3 Converter


This repository refers to the [freeCodeCamp.org](https://www.freecodecamp.org/) hands-on [tutorial]((https://www.youtube.com/watch?v=hmkF77F9TLw)) about microservices architecture and distributed systems using below frameworks and tools:

 - Kubernetes
 - Docker
 - Flask
 - Mysql
 - Mongo
 - Celery (Redis as a broker)

The application has been divided into chunks:

 - Auth
 - Converter
 - Notification


Kubernetes component division: 

 - Flask Auth Microservice
 - Flask Converter Microservice
 - Flask Notification Microservice
 - MySQL Microservice
 - Mongo Microservice
 - Celery Microservice
 
### Steps to setting up to repository:

 - Clone repo
 - Install [colima](https://formulae.brew.sh/formula/colima) (ps. I have used colima as docker runner instead docker desktop, you can use any alternative to run docker locally.)
 - Install [Kubernetes](https://kubernetes.io/docs/tasks/tools/)
 - Install [MiniKube](https://minikube.sigs.k8s.io/docs/start/)
 - Run ```colima start``` or ```colima start --cpu 4 --memory --8``` (you can set up cpu and memory according to your system's specifications)
 - Run ```minikube start```
 - Go inside each application's manifest folder 
   - Run ```kubectl apply -f ./```
 - To set up mysql user and database for the first time
   - Get inside mysql pod using ```k exec -it podname sh```
   - Run ```mysql -p```
   - Insert password ```root```
   - Inside mysql shell run commands which are defined in auth/init.sql file.
 - to bind port externally to send API using curl or postman:
   - Run ```minikube service service_name --url localhost:port_number```

Special note: If you're interested in running this project using docker, If you are new to docker and willing to learn docker first, then you can also run it using docker directly.

[Docker Repo](https://hub.docker.com/u/nilay103) &
[Postman Collection](https://www.postman.com/zoro-enma/workspace/kubernetes-project/collection/29585969-f587274b-ed83-4fda-a2ca-f934bbbe4355)
can be found here.

If you're interested in learning kubernetes by reading a book, [Kubernetes Book](https://nigelpoulton.com/books/) can be a good resource to start as a beginner.