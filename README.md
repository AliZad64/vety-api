# vety-api

### *_Note:_* for the frontend code its available on this [repo](https://github.com/BQBB/VETY)

# how to run the django program

## **install python**
  
you need to have [Python](https://www.github.com "Python") installed in your machine




## **virtual machine**

after cloning the repo, you need to create virtual machine so you can install the required packages in the project.
Inside the project repo open your terminal and write the following code to create virtual enviornment

```
python -m venv venv
```

or

```
py -m venv venv
```

now for activating the virtual enviorment there are different way to write the code depending on the machine your are using:

- for mac and linux

```
source venv/bin/activate
```

- for windows using git bash

```
source venv/Scripts/activate
```

or cmd

```
.\venv\Scripts\activate
```

## **installing required packages**


to install required packages for the project write this code in your terminal while your virtual enviornment is on:

```py
pip install -r requirements.txt
```

## **django migrations**


```py
python manage.py makemigrations
```

then

```py
python manage.py migrate
```

## **run the program**


```py
python manage.py runserver
```

then go to the following header `http://127.0.0.1:8000/api/docs`
