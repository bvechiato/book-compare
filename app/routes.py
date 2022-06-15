from flask import render_template, request, redirect
from checks import checks_with_selenium, checks_with_isbn, checks_with_title
from app import app, cache_manager
from app import models


@app.route('/', methods=['POST', 'GET'])
def index():
    recently_searched = cache_manager.get_all()
    if request.method == 'POST':
        bookISBN = request.form['bookISBN']
        book_title = request.form['bookName']

        # if isbn isn't entered
        if bookISBN == "":
            return redirect(f'/{book_title}')
        return redirect(f'/{bookISBN}')
    else: 
        return render_template('base.html', recently_searched=recently_searched)
    
@app.route('/<int:bookISBN>', methods=['POST', 'GET'])
def search_with_isbn(bookISBN):
    recently_searched = cache_manager.get_all()
    bookISBN = str(bookISBN)
    book_info = checks_with_isbn.goodreads(bookISBN)
        
    # check if book already exists in cache
    if cache_manager.check(bookISBN):
        display_book = cache_manager.get(bookISBN)
        return render_template('main.html', book=display_book, recently_searched=recently_searched)

    # get price
    waterstones = checks_with_isbn.waterstones(bookISBN)
    wob = checks_with_isbn.wob(bookISBN)
    blackwells = checks_with_isbn.blackwells(bookISBN)
        
    new_book = models.Book(bookISBN, book_info[0], book_info[1], wob[0], waterstones[0], blackwells[0], wob[1], waterstones[1], blackwells[1])
    cache_manager.set(bookISBN, new_book)
    display_book = str(new_book).split(", ")
        
    recently_searched = cache_manager.get_all()
    return render_template('main.html', book=display_book, recently_searched=recently_searched)


@app.route('/<book_title>', methods=['POST', 'GET'])
def search_with_name(book_title):
    recently_searched = cache_manager.get_all()
    
    book_info = checks_with_title.goodreads(book_title)
    
    # check if book already exists in cache
    if cache_manager.check(book_info[0]):
        display_book = cache_manager.get(book_info[0])
        return render_template('main.html', book=display_book, recently_searched=recently_searched)
    
    
    # get price
    waterstones = checks_with_title.waterstones(book_info[0])
    wob = checks_with_title.wob(book_info[0])
    blackwells = checks_with_title.blackwells(book_info[0])
        
    new_book = models.Book("", book_info[0], book_info[1], wob[0], waterstones[0], blackwells[0], wob[1], waterstones[1], blackwells[1])
    cache_manager.set(book_info[0], new_book)
    display_book = str(new_book).split(", ")
        
    recently_searched = cache_manager.get_all()
    return render_template('main.html', book=display_book, recently_searched=recently_searched)
