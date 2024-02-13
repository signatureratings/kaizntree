# Kaizntree

django backend 

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

What things you need to install the software and how to install them.

- Python 3.8+
- Django 3.2+
- A virtual environment (optional, but recommended)

### Installing

A step by step series of examples that tell you how to get a development environment running.

1. Clone the repository:
    ```
    git clone https://github.com/signatureratings/kaizntree.git 
    ```

2. Navigate to the project directory:
    ```
    cd kaizntree
    ```

3. (Optional) Create a virtual environment and activate it:
    ```
    python3 -m venv env
    source env/bin/activate 
    ```

4. Install the requirements:
    ```
    pip install -r requirements.txt
    ```

5. create a .env file  with the fields mentioned below. The fields are submitted in the email

    ```
    DB_DATABASE 
    DB_USERNAME 
    DB_PASSWORD 
    DB_HOST
    ```

5. Apply migrations:
    ```
    python manage.py migrate
    ```

6. Run the development server:
    ```
    python manage.py runserver
    ```

Now, you should be able to see the application running at localhost:8000 in your web browser.

    - To access the API got through using the postman.
    - POST: /api/register
    - POST: /api/login
    - POST: /api/logout
    - GET: /api/items
    - POST: /api/item
    - GET: /api/item

## Running the tests

```
python manage.py test inventory.tests
```

## Deployment



## Built With
 
Django, PostgreSQL, Django Rest Framework, Reactjs, Nodejs

## Authors

* **Name** - Sairam Balu
* **Email** - sairam.balu@rutgers.edu

