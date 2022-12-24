from flask import render_template, request, redirect
from checks import checks
from checks.find import find as find
from app import app, cache_manager
from app import models


@app.route('/', methods=['POST', 'GET'])
def index():
    recently_searched = cache_manager.get_all()
    if request.method == 'POST':
        bookISBN = request.form['bookISBN']
        book_title = request.form['bookName']
        book_author = request.form['author']

        # if isbn isn't entered
        if bookISBN == "":
            if book_author == "":
                return redirect(f'/{book_title}')
            return redirect(f'/{book_title}+{book_author}')
        return redirect(f'/{bookISBN}')
    else: 
        return render_template('base.html', recently_searched=recently_searched)


@app.route('/<search_term>', methods=['POST', 'GET'])
def search_with_name(search_term):
    recently_searched = cache_manager.get_all()

    # check if book already exists in cache
    if cache_manager.check(search_term):
        print("book already exists in cache")
        display_book = cache_manager.get(search_term)
        return render_template('main.html', book=display_book, recently_searched=recently_searched)
    
    [book_title, search_url, author, isbn] = find(search_term)

    # get price
    waterstones_price, waterstones_url = checks.waterstones(isbn)
    wob_price, wob_url = checks.wob(isbn)
    blackwells_price, blackwells_url = checks.blackwells(isbn)
        
    new_book = models.Book(isbn.strip(), book_title.strip(), author.strip(), search_url.strip(),
                           wob_price.strip(), waterstones_price.strip(), blackwells_price.strip(), wob_url.strip(),
                           waterstones_url.strip(), blackwells_url.strip())

    cache_manager.set(isbn, new_book)
    display_book = str(new_book).split(", ")
        
    recently_searched = cache_manager.get_all()
    return render_template('main.html', book=display_book, recently_searched=recently_searched)
