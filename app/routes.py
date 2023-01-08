from flask import render_template, request, redirect, session
from app import app, cache_manager, models
from app.checks import validate
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
            return render_template('base.html', negative=True, message=error_message, recently_searched=recently_searched)

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
            return render_template('login.html', negative=True, message="Email and/or password incorrect")
        session['id'] = token
        return render_template('login.html', negative=False, message="Successfully logged in")
    else:
        return render_template('login.html')


@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']
        successful = user.register(email, password)

        if not successful:
            return render_template('register.html', negative=True, message="Try again later")
        return render_template('register.html', negative=False, message="Successfully registered")
    else:
        return render_template('register.html')


@app.route('/logout', methods=['POST', 'GET'])
def logout():
    session.pop("id", None)
    return render_template('login.html', negative=False, message="Successfully logged out")


@app.route('/saved', methods=['POST', 'GET'])
def view_saved():
    if not session.get("id"):
        return redirect('/login')
    return render_template('saved.html')
