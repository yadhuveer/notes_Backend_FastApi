# Notes Backend

A FastAPI backend for a Notes app with MySQL database using Docker.

## Features
- FastAPI backend
- MySQL database
- Dockerized setup
- SQLAlchemy ORM

## Requirements
- Docker & Docker Compose
- Git

## Instruction to install and run

1.Create a `.env.docker` file in the project root:
DATABASE_USER=root,
DATABASE_PASS=password,
DATABASE_HOST=db,
DATABASE_NAME=notes_db   
  2. Clone the repository:
git clone  https://github.com/yadhuveer/notes_Backend_FastApi.git
cd notes-backend  

3.Build and start Docker containers:
 docker-compose up --build  

4.Access API at
  http://localhost:8000/

