# Day 1

## Setting up the Django Books Api app.

1. Create a directory for the application in your projects directory:

```bash
mkdir ~/code/ga/projects/django-books-api
cd ~/code/ga/projects/django-books-api
```

2. Install the package by running `pipenv install django`. After this you should have 2 files: Pipfile and Pipfile.lock.
   These are essentially the same as a package.json and a package-lock.json in a node/express app.

```bash
pipenv install django
```

The terminal output will look something like this:

<div>
    <img src="../images/terminal-pipenv-install-django.png" width="500px" />
</div>

3. Enter the shell by running `pipenv shell`

```bash
pipenv shell
```

The output will look a bit like this:

<div>
    <img src="../images/terminal-pipenv-shell.png" width="500px" />
</div>

4. To start a project run `django-admin startproject project .`

```bash
django-admin startproject project .
```

You should see that a folder called project has been created in the project directory, along with a `manage.py` file.

5. Run `pipenv install psycopg2-binary` (this is a db-adapter which allows us to use postgresql)

```bash
pipenv install psycopg2-binary
```

If you look in your Pipfile now, you should see that you have 2 dependencies: django and psycopg2-binary.

<div>
    <img src="../images/terminal-pipenv-shell.png" width="500px" />
</div>

```bash
pipenv install autopep8 -dev
```

8. Now run this to start postgres `brew services start postgresql@16`

```bash
brew services start postgresql@16
```

## VSCode

- Head to your `project/settings.py` file in the project folder
- Replace the `DATABASES` object with the following:

```py
DATABASES = { # added this to use postgres as the database instead of the default sqlite. do this before running the initial migrations or you will need to do it again
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'books-api',
        'HOST': 'localhost',
        'PORT': 5432
    }
}
```

### Terminal

- Make a database by running `createdb books-api`

  > This name must match the name of the db in the settings.py file

- Run the server `python manage.py runserver`

if:

- If you get an error about importing Django, run this: `pip install django psycopg2-binary`

if not:

- Notice the first error that comes up and nudge students that they will need to run migrations.
- Stop the server `ctrl+c`
- Migrate the app `python manage.py migrate`
- Run the server again `python manage.py runserver`
- No Errors! Boom.

  > You should now be able to see the landing page if you navigate to http://localhost:8000 in the browser

<div>
    <img src="../images/django-landing-page.png" width="500px" />
</div>

- Stop the server `ctrl+c`
- Create superuser `python manage.py createsuperuser`
- Now start a new app `django-admin startapp books`

### VSCode

- In `settings.py` in the `project` folder, add name of the app to the `INSTALLED_APPS` array
<div>
    <img src="../images/project-installed-apps.png" width="500px" />
</div>

- Move to `models.py` in the `books` folder
- Create the model:

```py
class Book(models.Model):
  def __str__(self):
    return f'{self.title} - {self.author}'
  title = models.CharField(max_length=80, unique=True)
  author = models.CharField(max_length=50)
  genre = models.CharField(max_length=60)
  year = models.FloatField()
```

> Fields are required by default so no need to specify

- Go to the apps `admin.py` and import your model: `from .models import Book`
- Then register your site: `admin.site.register(Book)`
  > Registering the model here so the admin site can pick it up

## Terminal

- Run `python manage.py makemigrations`
- Then run `python manage.py migrate`
- Restart the server `python manage.py runserver`
- Navigate to http://localhost:8000/admin and login to create some database entries
- Add in a function to format the string to make it more readable: (if this doesn’t work, check that the function is indented into the class)

### REST

## Terminal

- Stop the server `ctrl+c`
- Install the django rest framework `pipenv install djangorestframework`

### VSCode

- Register this in our `project/settings.py` `INSTALLED_APPS` :
  `’rest_framework’` above our own app

```py
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'books'
]
```

- Inside the books folder create a new file called `serializers.py`

  > We need a serializer to convert python objects into JSON

- In the `serializers.py` file add these imports:

```py
from rest_framework import serializers
from .models import Book
```

- Build out the serializer. Here we define the model that the JSON will be using and specify which fields to look at:

```py
class BookSerializer(serializers.ModelSerializer):
  class Meta:
    model = Book
    fields = '__all__'
```

- Move into `views.py` and delete the default imports
- Add the following imports:

```py
from rest_framework.views import APIView # this imports rest_frameworks APIView that we'll use to extend to our custom view
from rest_framework.response import Response # Response gives us a way of sending a http response to the user making the request, passing back data and other information
from rest_framework import status # status gives us a list of official/possible response codes

from .models import Book
from .serializers import BookSerializer
```

- Build out `views.py` to return all data eg. ListView:

```py
class BookListView(APIView):

  def get(self, _request):
    books = Book.objects.all()
    serialized_books = BookSerializer(books, many=True)
    return Response(serialized_books.data, status=status.HTTP_200_OK)
```

- Make a new file called `urls.py` . Add the imports for the views and the path for the index/list view:

```py
from django.urls import path
from .views import BookListView

urlpatterns = [
  path('', BookListView.as_view()),
]
```

- inside `project/urls.py` add to `urlpatterns` :
- remember to update import to add `include` as well as `path`

```py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('books/', include('books.urls')),
]
```

# Day 2

## DJANGO API - CREATE & SHOW

1. In `books/views.py`, let's add another method to the BookListView class which will handle POST requests.

Add this under the get function:

```py
    def post(self, request):
        book_to_add = BookSerializer(data=request.data)
        try:
            book_to_add.is_valid()
            book_to_add.save()
            return Response(book_to_add.data, status=status.HTTP_201_CREATED)
        # exceptions are like a catch in js, but if we specify an exception like we do below then the exception thrown has to match to fall into it
        # For example the below is the exception thrown when we miss a required field
        # link: (this documentation entry is empty but shows it exists) https://docs.djangoproject.com/en/4.0/ref/exceptions/#django.db.IntegrityError
        except Exception as e:
            print('ERROR')
            # the below is necessary because two different formats of errors are possible. string or object format.
            # if it's string then e.__dict__ returns an empty dict {}
            # so we'll check it's a dict first, and if it's empty (falsey) then we'll use str() to convert to a string
            return Response(e.__dict__ if e.__dict__ else str(e), status=status.HTTP_422_UNPROCESSABLE_ENTITY)
```

At this point, the whole books/views.py should look like this:

```py
from rest_framework.views import APIView # this imports rest_frameworks APIView that we'll use to extend to our custom view
from rest_framework.response import Response # Response gives us a way of sending a http response to the user making the request, passing back data and other information
from rest_framework import status # status gives us a list of possible response codes


from .models import Book
from .serializers import BookSerializer

class BookListView(APIView):

  def get(self, _request):
    books = Book.objects.all()
    serialized_books = BookSerializer(books, many=True)
    return Response(serialized_books.data, status=status.HTTP_200_OK)

  def post(self, request):
    book_to_add = BookSerializer(data=request.data)
    try:
        book_to_add.is_valid()
        book_to_add.save()
        return Response(book_to_add.data, status=status.HTTP_201_CREATED)
    # exceptions are like a catch in js, but if we specify an exception like we do below then the exception thrown has to match to fall into it
    # For example the below is the exception thrown when we miss a required field
    # link: (this documentation entry is empty but shows it exists) https://docs.djangoproject.com/en/4.0/ref/exceptions/#django.db.IntegrityError
    except Exception as e:
        print('ERROR')
        # the below is necessary because two different formats of errors are possible. string or object format.
        # if it's string then e.__dict__ returns an empty dict {}
        # so we'll check it's a dict first, and if it's empty (falsey) then we'll use str() to convert to a string
        return Response(e.__dict__ if e.__dict__ else str(e), status=status.HTTP_422_UNPROCESSABLE_ENTITY)
```

Because the BookListView is associated with the /books endpoint, simply adding the post function to the BookListView is enough to be able to now create new books through our API. Try it in postman.

2. Now let's work on the "Show" page. We will call it `BookDetailView`.

Let's add the new BookDetailView class underneath the BookListView.
We are also going to need another import at the top of the file. Add this to the imports section at the top of books/views.py:

```py
from rest_framework.exceptions import NotFound # This provides a default response for a not found
```

and then add the serializer underneath the BookListView:

```py
class BookDetailView(APIView):
    def get(self, _request, pk):
        try:
            # different API methods https://docs.djangoproject.com/en/4.0/ref/models/querysets/#methods-that-do-not-return-querysets
            book = Book.objects.get(pk=pk)
            serialized_book = BookSerializer(book)
            return Response(serialized_book.data, status=status.HTTP_200_OK)
        except Book.DoesNotExist:
            raise NotFound(detail="🆘 Can't find that book!")
```

At this point, the whole file should look like this:

```py
from rest_framework.views import APIView # this imports rest_frameworks APIView that we'll use to extend to our custom view
from rest_framework.response import Response # Response gives us a way of sending a http response to the user making the request, passing back data and other information
from rest_framework import status # status gives us a list of possible response codes
from rest_framework.exceptions import NotFound # This provides a default response for a not found

from .models import Book
from .serializers import BookSerializer

class BookListView(APIView):

  def get(self, _request):
    books = Book.objects.all()
    serialized_books = BookSerializer(books, many=True)
    return Response(serialized_books.data, status=status.HTTP_200_OK)

  def post(self, request):
    book_to_add = BookSerializer(data=request.data)
    try:
        book_to_add.is_valid()
        book_to_add.save()
        return Response(book_to_add.data, status=status.HTTP_201_CREATED)
    # exceptions are like a catch in js, but if we specify an exception like we do below then the exception thrown has to match to fall into it
    # For example the below is the exception thrown when we miss a required field
    # link: (this documentation entry is empty but shows it exists) https://docs.djangoproject.com/en/4.0/ref/exceptions/#django.db.IntegrityError
    except Exception as e:
        print('ERROR')
        # the below is necessary because two different formats of errors are possible. string or object format.
        # if it's string then e.__dict__ returns an empty dict {}
        # so we'll check it's a dict first, and if it's empty (falsey) then we'll use str() to convert to a string
        return Response(e.__dict__ if e.__dict__ else str(e), status=status.HTTP_422_UNPROCESSABLE_ENTITY)


class BookDetailView(APIView):
    def get(self, _request, pk):
        try:
            # different API methods https://docs.djangoproject.com/en/4.0/ref/models/querysets/#methods-that-do-not-return-querysets
            book = Book.objects.get(pk=pk)
            serialized_book = BookSerializer(book)
            return Response(serialized_book.data, status=status.HTTP_200_OK)
        except Book.DoesNotExist:
            raise NotFound(detail="🆘 Can't find that book!")
```

2. We need to add a route so that we can specify the book ID that we want to retrieve (that pk=pk is talking about the primary key/id). But let's have a look at how Django handles things if we make a request to a url that doesn't exist yet. Try to make a get request to `/books/1` and see what happens.

3. Let's add the url to the books/urls.py so that it can use the BookDetailView to handle this endpoint. Go to books/urls.py and add the BookDetailView to the the imports and then add the following path to the urlpatterns list:

```py
path('<int:pk>/', BookDetailView.as_view()),
```

so the whole urls.py file should look like this:

```py
from django.urls import path
from .views import BookListView, BookDetailView

urlpatterns = [
  path('', BookListView.as_view()),
  path('<int:pk>/', BookDetailView.as_view()),
  # the above <int:pk> is known as a captured value - it works the same as a placeholder in react/express: ":id"
  # It's made up of two parts:
  # on the left is the path converter - in this case we've specified an integer or "int"
  # on the right is the placeholder - in this case pk but could be anything
  # the path converter is optional, but you should use it to ensure it's the type you expect
  # without it, the captured value would be written like: <pk>
]
```

4. Try testing the endpoint again with a valid book id and you should see the data returned in postman/insomnia. Try it with an invalid book ID and you'll see that our error handling is working!

5. So far, everything is working, BUT - there's something in our code that isn't great. In our BookDetailView get function, we get a book from the database, serialise it and return it. We also handle the errors if we can't find the book. All of these steps are just the FIRST PARTS of what needs to happen with other actions. For example - if we were going to update a book, we would need to get it, serialise it, return it and handle errors if that book didn't exist, and only then would we be able to update the book and save it back to the database. So in the interest in making our code DRY and not repeating ourselves, let's move some of these steps into a reusable function.

We are going to end up creating a new function inside our BookDetailView which will be called get_book and then we will use this function inside the existing get function. Then we can use get_book inside our update and delete functions too.

Let's create our new get_book function as the first function in the BookDetialView:

```py
    # This will be used by all of the routes
    def get_book(self, pk):
        try:
            return Book.objects.get(pk=pk)
        except Book.DoesNotExist:
            raise NotFound(detail="🆘 Can't find that book!")
```

And then let's update our get function to use the get_show function:

```py
    def get(self, _request, pk):
        book = self.get_book(pk=pk) # using key word arguments here
        # querying using a primary key is always going to return a single result.
        # this will never be a list, so no need to add many=True on the serializer
        serialized_book = BookSerializer(book)
        return Response(serialized_book.data, status=status.HTTP_200_OK)
```

To add update and delete functions, add these to the BookDetailView:

```py
    def put(self, request, pk):
        book_to_update = self.get_book(pk=pk)
        updated_book = BookSerializer(book_to_update, data=request.data)
        if updated_book.is_valid():
            updated_book.save()
            return Response(updated_book.data, status=status.HTTP_202_ACCEPTED)

        return Response(updated_book.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    def delete(self, _request, pk):
        book_to_delete = self.get_book(pk=pk)
        book_to_delete.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
```
