from flask import Flask, render_template, request
import checks

app = Flask(__name__)
  
@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        bookName = request.form['bookName']
        bookISBN = request.form['bookISBN']

        if bookISBN == "":
            bookISBN = checks.findISBN(bookName)

        price_waterstones = checks.waterstones(bookISBN)
        price_wob = checks.wob(bookISBN)
        price_amazon = checks.amazon(bookISBN)

        return render_template('main.html', wob=price_wob, waterstones=price_waterstones, amazon=price_amazon)
    else: 
        return render_template('base.html')
    
if __name__ == "__main__":
    app.run(debug=True)
