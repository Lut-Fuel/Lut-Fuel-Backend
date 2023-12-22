
# Lut-Fuel API

=========

API for Lut-Fuel App.

- Language used : Python
- Framework used : FastAPI
- Database used : PostgreSQL


### To run the API locally, you need to : 

 - Make a virtual environment and activate it
 - Run uvicorn
 - Make a .env file with the required variables and values
 - Install and configure PostgreSQL in your machine
 - Monitor the database from pgAdmin

### Virtual Machine Specs : 

- Machine Type : n1-standard-1
- OS : 
- Boot Disk Size : 10 GB 

### To run the API on Google Cloud Platform, you need to : 
- Create a Cloud SQL instance for PostgreSQL
- Create a database within the Cloud SQL instance
- Ensure the API code is containerized using Docker
- Update the API's configuration to connect to Cloud SQL:
  - Replace local database connection details with Cloud SQL credentials.
  - Use environment variables to store sensitive credentials securely.
- Build a container image of API
- Push the container image to a container registry
- Create a Cloud Run service, specifying:
  - The container image.
  - Memory and CPU allocation.
  - Permissions to access Cloud SQL.
  - Environment variables for database credentials.
- Cloud Run automatically assigns a publicly accessible URL to your API.


