# Lecture 4 Notes

## SQL

### Create table in SQL database

```
CREATE TABLE flights (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    origin TEXT NOT NULL,
    destination TEXT NOT NULL,
    duration INTEGER NOT NULL
);
```

### Insert command

```
INSERT INTO flights
    (
        origin,
        destination,
        duration
    )
    VALUES (
        "New York",
        "London",
        415
    );
```

### Select Query

Get everything
```
SELECT * FROM flights;
```

A more selective query

```
SELECT origin, destination
FROM flights;
```

Get a subset, filter for primary key
```
SELECT *
FROM flights
WHERE id = 3;
```

Filter by destination name
```
SELECT * FROM flights
WHERE origin = "New York";
```

### Let's play with databases

Create table file

`$touch flights.sql`

Enter SQLite command prompt

`sqlite3 flights.sql`

Create table using the command above...
```
sqlite> CREATE TABLE flights (
   ...> id INTEGER PRIMARY KEY AUTOINCREMENT,
   ...> origin TEXT NOT NULL,
   ...> destination TEXT NOT NULL,
   ...> duration INTEGER NOT NULL );
```


Now, let's check that our table exists, add a row, and query the table to see the row...
```
sqlite> .tables
flights
sqlite>  INSERT INTO flights (origin, destination, duration) VALUES ("New York","London",415);
sqlite> SELECT * FROM flights;
1|New York|London|415
sqlite> 
```

To get nicer formatting
```
sqlite> .mode columns
sqlite> .headers yes
sqlite> SELECT * FROM flights;
id  origin    destination  duration
--  --------  -----------  --------
1   New York  London       415     
sqlite> 
```

More content showing ways to filter.
* OR
* LIKE '%a%' (string contains a, anywhere)

Functions

* AVERAGE
* COUNT
* MAX
* MIN
* SUM
* (etc.)

Update an existing row in the database:

```
UPDATE flights
    SET duration = 430
    WHERE origin = "New York"
    AND destination = "London";
```


Delete a row:

```
DELETE FROM flights WHERE destination = "Tokyo";
```

Other Clauses:

* LIMIT
* ORDER BY
* GROUP BY
* HAVING
* ...


### Joining Tables

Say we want airport codes, just make another table associating the city name with the airport code

Can be organized like this

`id, code, city_name`

flights table can be organized like this:

`id, origin_id, destination_id, duration`

We join the two tables to gete human readable results, while saving memory.

Passengers table -- problematic because each person only gets one flight

`id, first, last, flight_id`

Instead, make a "people" table

`id, first, last` 

Association table, same person can be on multiple flights

`person_id, flight_id`

Obviously, this way of splitting up data isn't easy for humans to read. Hence JOIN clauses.

Example:
```
SELECT first, origin, destination
FROM flights JOIN passengers
    ON passengers.flight_id = flights.id;
```

Results - much more human readable

`first, origin, destination`

Join Types

* JOIN / INNER JOIN
* LEFT OUTER JOIN
* RIGHT OUTER JOIN
* FULL OUTER JOIN

Create Index

* Takes memory to set up, but results in more efficient queries

```
CREATE INDEX name_index on passengers (last);
```

### Security

Beware of SQL Injection attacks

Suppose we store login creds in clear text

Users log in with username & password on web form

Backend query is like this...
```
SELECT * FROM users
WHERE username = "harry" AND password = "12345";
```

If we're not critical of the input, a hacker can do this

Username: hacker"--

SQL query is like this
```
SELECT * from users
WHERE username = "hacker"--" AND password = "";
```
The -- and everything after is ignored and the query becomes this:
```
SELECT * FROM users
WHERE username = "hacker"
```
Thus, the hacker bypasses the password check.

We can fix this in two ways
* Use escape characters so SQL knows to treat the input as part of the string, and not SQL syntax
* Use abstraction layer on top of SQL that takes care of this for us.


### Race Conditions

If stuff is happening in multiple threads, things can happen out of order. E.g. multiple people 'liking' the same post at the same time on a social media site, and we have to count likes.

## Django

Start new project

`$ django-admin startproject airline`

cd into the airline directory, then:

`$ python3 manage.py startapp flights`

In settings.py, add:

```
# Application definition

INSTALLED_APPS = [
    'flights', #New flights app
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]
```

In urls.py:
* import include from django.urls
* add `flights/` path

```
from django.contrib import admin
from django.urls import include, path #import include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('flights/', include("flights.urls")) #Add this path
]
```

In the flights app directory, create another urls.py file
```
from django.urls import path
from . import views

urlpatterns = [
    #Our urls will live here
]
```

### Django Models

Now shift over to models.py, and let's create a class that will become the flights table
```
# Create your models here.
class Flight(models.Model):
    origin = models.CharField(max_length=64)
    destination = models.CharField(max_length=64)
    duration = models.IntegerField()
```

### Migrations

Now let's actually create the table and migrate to database
```
(base) dan@osprey:~/scripts/cs50w/lecture4/airline$ python3 manage.py makemigrations
Migrations for 'flights':
  flights/migrations/0001_initial.py
    - Create model Flight
(base) dan@osprey:~/scripts/cs50w/lecture4/airline$
```

Apply Migrations
```
(base) dan@osprey:~/scripts/cs50w/lecture4/airline$ python3 manage.py migrate
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, flights, sessions
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying auth.0001_initial... OK
  Applying admin.0001_initial... OK
  Applying admin.0002_logentry_remove_auto_add... OK
  Applying admin.0003_logentry_add_action_flag_choices... OK
  Applying contenttypes.0002_remove_content_type_name... OK
  Applying auth.0002_alter_permission_name_max_length... OK
  Applying auth.0003_alter_user_email_max_length... OK
  Applying auth.0004_alter_user_username_opts... OK
  Applying auth.0005_alter_user_last_login_null... OK
  Applying auth.0006_require_contenttypes_0002... OK
  Applying auth.0007_alter_validators_add_error_messages... OK
  Applying auth.0008_alter_user_username_max_length... OK
  Applying auth.0009_alter_user_last_name_max_length... OK
  Applying auth.0010_alter_group_name_max_length... OK
  Applying auth.0011_update_proxy_permissions... OK
  Applying auth.0012_alter_user_first_name_max_length... OK
  Applying flights.0001_initial... OK
  Applying sessions.0001_initial... OK
(base) dan@osprey:~/scripts/cs50w/lecture4/airline$ 
```

## Shell


Open console to run commands:
```
python3 manage.py shell
```
Let's add a flight using the console, instead of a SQL command:
```
>>> from flights.models import Flight
>>> f = Flight(origin="New York", destination="London", duration=415)
>>> f
<Flight: Flight object (None)>
>>> f.save()
>>> Flight.objects.all()
<QuerySet [<Flight: Flight object (1)>]>
>>> 
```
This would be nicer if we could get a string representation of the flight...

in flights/models.py, add a string representation to the class
```
    def __str__(self):
        return f"{self.id}: {self.origin} to {self.destination}"
```

If we refresh the shell, now we can see this string representation...
```
(base) dan@osprey:~/scripts/cs50w/lecture4/airline$ python3 manage.py shell
Python 3.8.3 (default, Jul  2 2020, 16:21:59) 
[GCC 7.3.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
(InteractiveConsole)
>>> from flights.models import Flight
>>> flights = Flight.objects.all()
>>> flights
<QuerySet [<Flight: 1: New York to London>]>
>>> flight = flights.first()
>>> flight
<Flight: 1: New York to London>
>>> flight.id
1
>>> flight.origin
'New York'
>>> flight.destination
'London'
>>> 
```


We have now set up a second table in the database, and used foreign keys for destinations and origins
```
from django.db import models

# Create your models here.
class Airport(models.Model):
    code = models.CharField(max_length=3)
    city = models.CharField(max_length=64)
    def __str__(self):
        return f"{self.city} ({self.code})"


class Flight(models.Model):
    #origin = models.CharField(max_length=64)
    origin = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name="departures")
    #destination = models.CharField(max_length=64)
    destination = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name="arrivals")
    duration = models.IntegerField()

    def __str__(self):
        return f"{self.id}: {self.origin} to {self.destination}"
```

First, delete that first flight row, because otherwise we get a prompt to set a default value. But after that, run `python3 manage.py makemigrations`
```
(base) dan@osprey:~/scripts/cs50w/lecture4/airline$ python3 manage.py makemigrations
It is impossible to add a non-nullable field 'destination' to flight without specifying a default. This is because the database needs something to populate existing rows.
Please select a fix:
 1) Provide a one-off default now (will be set on all existing rows with a null value for this column)
 2) Quit and manually define a default value in models.py.
Select an option: 1
Please enter the default value as valid Python.
The datetime and django.utils.timezone modules are available, so it is possible to provide e.g. timezone.now as a value.
Type 'exit' to exit this prompt
>>> "London"
Migrations for 'flights':
  flights/migrations/0003_flight_destination.py
    - Add field destination to flight
(base) dan@osprey:~/scripts/cs50w/lecture4/airline$
```
Add some airports, and a flight
```
>>> lhr = Airport(code="LHR",city="London")
>>> lhr.save()
>>> cdg = Airport(code=
... "CDG",city="Paris")
>>> cdg.save()
>>> nrt=Airport(code="NRT",city="Tokyo")
>>> nrt.save()
>>> f = Flight(origin=jfk, destination=lhr, duration=415)
>>> f.save()
>>> f.origin
<Airport: New York (JFK)>
>>> f.origin.city
'New York'
>>> lhr.arrivals.all()
<QuerySet [<Flight: 1: New York (JFK) to London (LHR)>]>
>>> 
```

Next, add an index view to views.py, and add a couple of html templates
* Add index view to views.py
* Create layout.html template, and index.html file
* add url to urls.py

The flight is now listed on the webpage.

Next, add another flight
```
>>> from flights.models import *
>>> Airport.objects.all()
<QuerySet [<Airport: New York (JFK)>, <Airport: London (LHR)>, <Airport: Paris (CDG)>, <Airport: Tokyo (NRT)>]>
>>> Airport.objects.filter(city="New York")
<QuerySet [<Airport: New York (JFK)>]>
>>> Airport.objects.filter(city="New York").first()
<Airport: New York (JFK)>
>>> Airport.objects.get(city="New York")
<Airport: New York (JFK)>
>>> jfk = Airport.objects.get(city="New York")
>>> cdg = Airport.objects.get(city="Paris")
>>> f = Flight(origin=jfk,destination=cdg,duration=435)
>>> f.save()
```

Okay, but it sucks to take the webpage down, go into the shell, and add the airport and flight. What if we had a webpage to handle this?

## Django Admin

In CLI, type out:
```
$ python3 manage.py createsuperuser
```

Add our tables to the admin.py file
```
from django.contrib import admin
from .models import Flight, Airport

# Register your models here.
admin.site.register(Airport)
admin.site.register(Flight)
```

If you now run the server, go to `localhost:8000/admin` and log in.

Once logged in, you can now add new rows to each table using a built-in web GUI. Very nice!

Now let's create a separate page for each flight.

In flights/urls.py:
```
    path("<int:flight_id>", views.flight, name="flight")
```

In flights/views.py:
```
def flight(request, flight_id):
    flight = Flight.objects.get(pk=flight_id) #pk = primary key
    return render(request, "flights/flight.html", {
        "flight":flight
    })
```

Next, create a layout for the page under templates. Once finished, we can now view each flight's detailed info (duration).

## Many-to-Many Relationships

Add new class for passengers to flights/models.py
```
class Passenger(models.Model):
    first = models.CharField(max_length=64)
    last = models.CharField(max_length=64)
    flights = models.ManyToManyField(Flight, blank=True, related_name="passengers")

    def __str__(self):
        return f"{self.first} {self.last}"
```

Next:
* `$ python manage.py makemigrations`
* `$ python manage.py migrate`

Finally, add Passengers to admin.py, like with Airports and Flights.

Suppose we want to show who is on which flight in the flight page...

In views:
```
def flight(request, flight_id):
    flight = Flight.objects.get(pk=flight_id) #pk = primary key
    return render(request, "flights/flight.html", {
        "flight":flight,
        "passengers":flight.passengers.all()
    })
```

In flight.html

```
<h2>Passengers</h2>

<ul>
    {% for passenger in passengers %}
        <li>{{passenger}}</li>
    {% empty %}
        <li>No passengers</li>
    {% endfor %}
</ul>
<a href="{% url 'index' %}">Back to Flight List</a>
```

In index.html:
```    
<h1>Flights</h1>
    <ul>
        {% for flight in flights %}
        <li>     
            <a href="{% url 'flight' flight.id %}">
                Flight {{flight.id}}: {{flight.origin}} to {{flight.destination}}
            </a>
        </li>
        {% endfor %}

    </ul>
```

Booking a flight

add url path
```
path("<int:flight_id>/book", views.book, name="book")
```

add view
```
def book(request, flight_id):
    if request.method == "POST":
        flight = Flight.objects.get(pk=flight_id)
        #assume that the request form has the passenger info
        passenger = Passenger.objects.get(pk=int(request.POST["passenger"]))
        #add passenger to their flight
        passenger.flights.add(flight)
        return HttpResponseRedirect(reverse("flight", args=(flight.id,)))
```

Add non_passengers to flights view
```
        "non_passengers": Passenger.objects.exclude(flights=flight).all()
```

Add booking functionality to flight.html
```
<h2>Add Passenger</h2>

<form action="{% url 'book' flight.id %}" method="post">
    {% csrf_token %}
    <select name="passenger">
        {% for passenger in non_passengers %}
            <option value="{{ passenger.id }}">{{ passenger }}</option>
        {% endfor %}
    </select>
    <input type="submit">
</form>
```

Customize Admin page by adding FlightAdmin class:
```
from django.contrib import admin
from .models import Flight, Airport, Passenger

# Register your models here.
class FlightAdmin(admin.ModelAdmin):
    list_display = ("id", "origin","destination", "duration")

admin.site.register(Airport)
admin.site.register(Flight, FlightAdmin)
admin.site.register(Passenger)
```

## Users

Create a new app to manage users
```
python manage.py startapp users
```

Add users app to airline/settings.py
```
INSTALLED_APPS = [
    'flights', #New flights app
    'users', #New users app
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]
```

create users/urls.py, copy in the following:
```
from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout")
]
```

create login HTML page (extends a layout page)
```
{% extends "users/layout.html" %}

{% block body %}

<h2>cs50 Airlines Login</h2>
<form action="{% url 'login' %}" method="post">
    {% csrf_token %}
    <input type="text" name="username" placeholder="Username">
    <input type="text" name="password" placeholder="Password">
    <input type="submit" value="Login">
</form>

{% endblock %}
```

Create views (logout is TODO)
```
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout

# Create your views here.
def index(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    

def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "users/login.html"), {
                "message":"Invalid credentials."
            }


def logout_view(request):
    pass
```
