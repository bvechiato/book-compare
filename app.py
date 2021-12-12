from flask import Flask, json, render_template, request
from flask_sqlalchemy import SQLAlchemy
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
import random, string

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)
  
@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        bookName = request.form['bookName']
        bookISBN = request.form['bookISBN']

        # selenium
        driver = webdriver.Chrome()

        if bookISBN == None:
            driver.get("isbnsearch.org")
            searchBar = WebDriverWait(driver, 20).until(EC.visibility_of_all_elements_located((By.ID, "searchQuery")))
            searchBar.send_keys(bookName)
            searchBar.send_keys(Keys.RETURN)
            firstSearchResult = driver.find_element(By.XPATH, "//*[@id='searchresults']/li[1]/div[2]/h2/a") 
            foundISBN = firstSearchResult.get_attribute('href')[6:]
            bookISBN = foundISBN

        ## waterstones
        

        elements = WebDriverWait(driver, 20).until(EC.visibility_of_all_elements_located((By.CLASS_NAME, "content")))

        # isbnsearch.org
        # amazon
        # world of books
        # waterstones - https://www.waterstones.com/books/search/term/[ISBN]
        return render_template('main.html')
    else: 
        return render_template('base.html')
    
if __name__ == "__main__":
    app.run(debug=True)