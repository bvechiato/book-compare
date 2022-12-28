from flask import render_template, request, redirect
from app import app, cache_manager
from checks import validate
from app import models


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


@app.route('/<search_term>', methods=['POST', 'GET'])
def search_with_name(search_term):
    recently_searched = cache_manager.get_all()

    # check if book already exists in cache
    if cache_manager.check(search_term):
        display_book = cache_manager.get(search_term)
        return render_template('main.html', book=display_book, recently_searched=recently_searched)
    
    display_book = models.config_book(search_term)

    # get cache to render
    recently_searched = cache_manager.get_all()
    return render_template('main.html', book=display_book, recently_searched=recently_searched)
