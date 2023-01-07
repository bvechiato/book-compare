from flask import render_template, request, redirect
from app import app, cache_manager
from app.checks import validate
from app import models
from fb import db, user


@app.route('/', methods=['POST', 'GET'])
def index():
    recently_searched = cache_manager.get_all()
    if request.method == 'POST':
        # get values from form
        bookISBN = request.form['bookISBN']
        book_title = request.form['bookName']
        book_author = request.form['author']

        # validate isbn
        has_error, error_message = validate.isbn(bookISBN)

        if book_title != "":
            has_error, error_message, bookISBN = validate.title(book_title, book_author)

        if has_error:
            return render_template('base.html', error=error_message, recently_searched=recently_searched)

        return redirect(f'/{bookISBN}')
    else: 
        return render_template('base.html', recently_searched=recently_searched)


@app.route('/<book_isbn>', methods=['POST', 'GET'])
def search(book_isbn):
    # check if book already exists in cache
    if cache_manager.check(book_isbn):
        display_book = cache_manager.get(book_isbn)
    elif db.get_book(book_isbn):
        display_book = models.create_from_dict(db.get_book(book_isbn))
    else:
        display_book = models.config_book(book_isbn)

    # get cache to render
    recently_searched = cache_manager.get_all()

    display_book = display_book.make_dict()
    return render_template('main.html', book=display_book, recently_searched=recently_searched)


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']
        successful, token = user.sign_in(email, password)

        if not successful:
            return render_template('login.html', error="Email and/or password incorrect")
        return render_template('login.html', error="Successfully logged in")
    else:
        return render_template('login.html')


@app.route('/register', methods=['POST', 'GET'])
def register():
    return render_template('register.html')


@app.route('/saved', methods=['POST', 'GET'])
def view_saved():
    # if already signed in, not sure how to check that for now
    return redirect('/login')


@app.route('/success', methods=['POST', 'GET'])
def success():
    # if already signed in, not sure how to check that for now
    return "Nice"
