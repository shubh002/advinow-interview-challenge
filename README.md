# AdviNow Interview Challenge
This repository will be used as a test case for interview candidates. The application structure is predefined using FastAPI and uvicorn in the "app" directory in the "run.py" module. 
FastAPI creates API docs automatically, and these can be found at "http://127.0.0.1:8013/docs" when the app is running.

Please follow the instructions below to define data modules, generate a database through migration files, and create an API to return symptom data based on business logic.

Below are all the tasks/expectations required to complete this challenge. These tasks are not listed in any defined order, and you may go about these tasks in any order you see best:

**Please organize these tasks and update the ReadMe based on the order you complete them!**

- Create data models - example with sqlalchemy in "app\models.py"
- Create an endpoint that returns business and symptom data
  - Endpoint should take two optional parameters - business_id & diagnostic
  - Endpoint should return Business ID, Business Name, Symptom Code, Symptom Name, and Symptom Diagnostic values based on filter
- Generate migration script and run migration to create database tables - alembic files provided
  - To create a migration file: "alembic revision --autogenerate -m some_comment"
  - To update database with migration file: "alembic upgrade head"
- Design a database mock up based on the provided data - "app\data\business_symptom_data.csv"
- Create an endpoint for importing a CSV file into the database
  - The only requirement is the endpoint requires a CSV file. If needed, other parameters can be used.
- Create a virtual environment and install the requirements - "requirements\requirements.txt"

As a note, FastAPI, uvicorn, sqlalchemy, and alembic are not required to be used and may be changed if desired. 
Any of the existing files or variables can be and may need to be changed or updated, please be prepared to explain changes on the follow-up call.
The final end result should be a filled database, two working APIs, and an accessible API docs page.

## Approach

- Used vsCode WSL to implement.
- Created a virtual environment to install all requirements.
- Created a database using postgreSQL with 2 tables (business, symptom).
- Created both alembic migration scripts to create the database (check versions).
- Loaded the data from csv file into these tables.
- Created a Post endpoint to update the database by importing a csv file.
- Created a get endpoint keeping Business ID and Symptom Diagnostic as optional fields.

## How to Run

- Update values for DB_HOST, DB_NAME, DB_USER & DB_PASSWORD in .env file based on your postgres server.
- Create a new virtual environment (ex: "python -m venv venv").
- Install all the requirements "pip install -r requirements.txt".
- Check db models in models.py
- To create/ update db, run both the scripts
  - alembic revision --autogenerate -m some_comment
  - alembic upgrade head
- To view db/ tables in it use the command "sudo -u postgres psql postgres".
- Use basic sql code to view db/ table values (ex: "select * from business;").
- To run the FastAPI server go to 'app' directory and use command "uvicorn run:app --reload".
- To import a new csv file and update database, 
  - go to "http://localhost:8000/" 
  - choose the csv file to upload and click on Upload button
- To view data on FastAPI
  - go to "http://localhost:8000/data?business_id=1004&diagnostic=true"
  - choose values for business_id & diagnostic (optional)


## Future Improvements

- error handling on removing columns from CSV file (standard format maintenance).
- Validation checks for empty fields/ invalid input.
- change the port to 8013, currently its working on 8000.
