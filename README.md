## PASSWORD MANAGER



This application implements a backend system for managing users and their tasks, based on the FastAPI framework and PostgresDB.

## Core libraries

- fastapi
- uvicorn
- SQLAlchemy
- pydantic
- alembic
- bcrypt


## Endpoints


### Password

- **POST** `/password/` - Create a new password
- **GET** `/password/{service_name}` - Retrieve a specific password by service name
- **GET** `/password/?service_name={service_name}` - Search a specific passwords by service name

## Examples of Requests Using Postman
1. **Create a new password**
   - Method: `POST`
   - URL: `http://localhost:8000/password/`
   - Body (JSON):
     ```json
        {
                "service_name": "service",
                "password": "1234567890qwe"
        }  
     ```
   - Response (JSON):
     ```json
        {
            "service_name": "service",
            "password": "1234567890qwe"
        }  
     ```

2. **Retrieve a password**
   - Method: `GET`
   - URL: `http://localhost:8000/password/?service_name=serv`
   - Response (JSON):
     ```json
        {
            "service_name": "service",
            "password": "1234567890qwe"
        }  
     ```

3. **Search a passwords**
   - Method: `GET`
   - URL: `http://localhost:8000/password/?service_name=service`
   - Response (JSON):
     ```json
        [
            {
                "service_name": "service",
                "password": "1234567890qwe"
            },
            {
                "service_name": "service2",
                "password": "qwe123123123123123123q"
            }
        ]
     ```
## Setup

1. Perform comand
```bash
git clone https://github.com/RaynerDelgado/didenok_team_password_manager.git
cd didenok_team_password_manager
pip install -r requirements.txt
```

2. Fill in the .env.example data (ENV = TEST), change filename to .env

3. Perform migrations for test database
```bash
alembic upgrade head
```
4.  Perform test
```bash
pytest
```

5. If tests is ok then change .env file -> ENV = DEV. Perform migrations for dev database. 
```bash
alembic upgrade head
```

6. Start the server
```bash
uvicorn src.main:app --reload
```

## Setup Docker

1. Perform comand
```bash
git clone https://github.com/RaynerDelgado/didenok_team_password_manager.git
cd didenok_team_password_manager
pip install -r requirements.txt
```

2. Fill in the .env.example data (ENV = DEV, DB_HOST = db), change filename to .env

3. Running multi-container application
```bash
docker-compose up --build
```