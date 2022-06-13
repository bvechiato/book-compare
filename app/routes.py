from flask import render_template, request
from checks import checks_with_bs4, checks_with_selenium
from app import app

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        bookName = request.form['bookName']
        bookISBN = request.form['bookISBN']

        # if isbn isn't entered
        if bookISBN == "":
            bookISBN = checks_with_bs4.goodreads_with_bookName(bookName)
        book_info = checks_with_bs4.goodreads_with_ISBN(bookISBN)
        print(f"Book info: {book_info[0]}")

        price_waterstones = checks_with_bs4.waterstones(bookISBN)
        price_wob = checks_with_bs4.wob(bookISBN)
        price_blackwells = checks_with_bs4.blackwells(bookISBN)

        return render_template('main.html', isbn=bookISBN, book=book_info, wob=price_wob, waterstones=price_waterstones, blackwells=price_blackwells)
    else: 
        return render_template('base.html')