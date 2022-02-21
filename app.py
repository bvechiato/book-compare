from flask import Flask, render_template, request
import checks_with_selenium, checks_with_bs4

app = Flask(__name__)
  
@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        bookName = request.form['bookName']
        bookISBN = request.form['bookISBN']

        if bookISBN == "":
            bookISBN = checks_with_bs4.goodreads_with_bookName(bookName)

        price_waterstones = checks_with_bs4.waterstones(bookISBN)
        price_wob = checks_with_bs4.wob(bookISBN)

        price_blackwells = checks_with_bs4.blackwells(bookISBN)

        return render_template('main.html', wob=price_wob, waterstones=price_waterstones, blackwells=price_blackwells)
    else: 
        return render_template('base.html')
    
if __name__ == "__main__":
    app.run(debug=True)
