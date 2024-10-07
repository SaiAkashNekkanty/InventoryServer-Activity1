1. How to bring up your containers:
I am using docker compose to bring up both containers, i.e., server & client.

Start the containers using Docker Compose: 
command: docker-compose up --build

2. For running the python script to process CSV files:
The client_file.py script is automatically invoked when the container starts. The container monitors the /data folder for CSV files and processes them immediately upon detection.

command: python client_file.py /app/data 20 

this is command used in my docker-compose which points that , once the containers are up and running , the client file is automatically invoked based on the command given in the docker compose.

3. To test it local in our machine :
server url in the client_file.py has to be pointed to localhost , which is http://localhost:5000.
Once the server URL is changes to local machine , deloy the server and then you can run the client_file to see the logs or console outputs.