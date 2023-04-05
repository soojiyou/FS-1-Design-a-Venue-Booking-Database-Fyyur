
# Full Stack Project 1 - Fyyur

## Demo Website (Render)
https://fs-fyyur.onrender.com

## Introduction

Fyyur is an online platform for discovering and booking shows between local performing artists and venues. This musical venue and artist booking site enables users to list new artists and venues, search for them, and create shows featuring artists as a venue owner.


## Goal
The objective of the project is to develop data models that support the API endpoints for the Fyyur website. This involves connecting to a PostgreSQL database to store, query, and manage information related to artists and venues on Fyyur.

* creating new venues, artists, and creating new shows.
* searching for venues and artists.
* learning more about a specific artist or venue.


## Getting Started:

### Tech Stack (Dependencies)

This information is in package.json (Frontend Dependencies) and in requirements.txt (Backend Dependencies)

### 1. Frontend Dependencies

Install Requirements with the following command:
```
npm install
```

### 2. Backend Dependencies
Our tech stack will include the following:
 * **virtualenv** as a tool to create isolated Python environments
 * **SQLAlchemy ORM** to be our ORM library of choice
 * **PostgreSQL** as our database of choice
 * **Python3** and **Flask** as our server language and server framework
 * **Flask-Migrate** for creating and running schema migrations

Install Requirements with the following command:
```
npm install
```

#### Development Setup

1. **Initialize and activate a virtualenv using:**
```
python -m virtualenv env
source env/bin/activate
```
>**Note** - In Windows, the `env` does not have a `bin` directory. Therefore, you'd use the analogous command shown below:
```
source env/Scripts/activate
```

2. **Install the dependencies:**
```
pip install -r requirements.txt
```

3. **Run the development server:**
```
export FLASK_APP=myapp
export FLASK_ENV=development # enables debug mode
python3 app.py
```

4. **Verify on the Browser**<br>
Navigate to project homepage [http://127.0.0.1:5000/](http://127.0.0.1:5000/) or [http://localhost:5000](http://localhost:5000) 


## Main Files: Project Structure

  ```sh
  ├── README.md
  ├── app.py *** the main driver of the app. Includes your SQLAlchemy models.
                    "python app.py" to run after installing dependencies
  ├── config.py *** Database URLs, CSRF generation, etc
  ├── error.log
  ├── forms.py *** Your forms
  ├── requirements.txt *** The dependencies we need to install with "pip3 install -r requirements.txt"
  ├── static
  │   ├── css 
  │   ├── font
  │   ├── ico
  │   ├── img
  │   └── js
  └── templates
      ├── errors
      ├── forms
      ├── layouts
      └── pages
  ```

Overall:
* Models are located in the `MODELS` section of `app.py`.
* Controllers are also located in `app.py`.
* The web frontend is located in `templates/`, which builds static assets deployed to the web server at `static/`.
* Web forms for creating data are located in `form.py`


## Features
### User

mainpage

<img src="https://user-images.githubusercontent.com/79179847/229996532-5ec1344b-ea3c-4bf0-872d-863a4c123d88.png" alt="Image Description" width="500" >


venue list

<img src="https://user-images.githubusercontent.com/79179847/229997056-8b16d234-ee0b-4343-a472-778a874b9e9d.png" alt="Image Description" width="500" >


venue detail

<img src="https://user-images.githubusercontent.com/79179847/229997167-da05144c-2dd0-45b1-8023-05aace85ccbe.png" alt="Image Description" width="500" >


create new artist

<img src="https://user-images.githubusercontent.com/79179847/229997543-cd2c64e6-e5b6-4184-91d1-cfc4f5e5ae6a.png" alt="Image Description" width="500" >


Artist list

<img src="https://user-images.githubusercontent.com/79179847/229997629-9ba516df-da92-426b-9e2a-0b6d4e6a2502.png" alt="Image Description" width="500" >



Arrange venue with artist
post show

<img src="https://user-images.githubusercontent.com/79179847/229997786-ed9f3982-0026-4fd4-8fb3-02a5eea68a70.png" alt="Image Description" width="500" >


result show

<img src="https://user-images.githubusercontent.com/79179847/229997913-0a307c40-5cf0-4659-91bb-67897758fac2.png" alt="Image Description" width="500" >





