# import libraries
from logging import config
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import mysql.connector
import os
from dotenv import load_dotenv
from mysql.connector import Error 


# ====================== 1. CONFIG ======================
# Database connection details 

load_dotenv()  # Load environment variables from .env file


app = FastAPI()
security = HTTPBasic()


@app.get("/test2s.py")  # whatever your test_script is hitting
async def protected_route(credentials: HTTPBasicCredentials = Depends(security)):
    # Optional: actually validate username/password here
    # 
    #     raise HTTPException(
    #         status_code=status.HTTP_401_UNAUTHORIZED,
    #         detail="Invalid credentials",
    #         headers={"WWW-Authenticate": "Basic realm=\"MySQL Connection API\""},  # <-- this is what the RFC requires
    #     )
    conn = mysql.connector.connect()       # **config         # connect to the existing MySQL connection
    # ... do whatever you need with the connection
    return {"status": "connected", "message": "MySQL connection successful"}


# ====================== 3. ESTABLISH CONNECTION ======================
# Establising a connection to the MYSQL database using mysql.connector

try:
    # Establish the connection
    connection = mysql.connector.connect(host=os.getenv('MYSQL_HOST'), user=os.getenv('MYSQL_USER'), password=os.getenv('MYSQL_PASSWORD'), database=os.getenv('MYSQL_DB'))  # **config
   
    # Print message if connection is successful 
    if connection.is_connected():
        print("Successful connected to the databse")

        # Create a curser object to execute SQL queries
        cursor = connection.cursor()

        # Execute a query 
        cursor.execute("SHOW DATABASES")

        # Table already created
        # cursor.execute("SELECT COUNT(*) FROM resume_pipeline.resumes LIMIT 1")
        cursor.fetchall()  # Fetch the results to ensure the query is executed
        print("Table created or already exists")
    


except Error as e:
    print(f"Error connecting to MYSQL: {e}")
finally:
    # Close the cursor and connection
    if 'cursor' in locals() and cursor:
        cursor.close()
    if 'connection' in locals() and connection.is_connected():
        connection.close()
        print("Connection closed")

