from flask import render_template, request
from checks import checks_with_bs4, checks_with_selenium
from app import app, cache_manager
from app import models


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        bookISBN = request.form['bookISBN']

        # if isbn isn't entered
        if bookISBN == "":
            bookISBN = checks_with_bs4.goodreads_with_bookName(request.form['bookName'])
        book_info = checks_with_bs4.goodreads_with_ISBN(bookISBN)
        
        # check if book already exists in cache
        if cache_manager.check(bookISBN):
            display_book = cache_manager.get(bookISBN)
            return render_template('main.html', book=display_book)

        waterstones = checks_with_bs4.waterstones(bookISBN)
        wob = checks_with_bs4.wob(bookISBN)
        blackwells = checks_with_bs4.blackwells(bookISBN)
        
        new_book = models.Book(bookISBN, book_info[0], book_info[1], wob[0], waterstones[0], blackwells[0], wob[1], waterstones[1], blackwells[1])
        cache_manager.set(bookISBN, new_book)
        display_book = str(new_book).split(", ")
            
        return render_template('main.html', book=display_book)
    else: 
        recently_searched = cache_manager.get_all()
        return render_template('base.html', recently_searched=recently_searched)