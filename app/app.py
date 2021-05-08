from flask import Flask, render_template, request
import pickle
import numpy as np
import pandas as pd
import string
import nltk
from nltk.stem.porter import PorterStemmer


app = Flask(__name__)

@app.route("/",methods=['GET','POST'])
def index():
    response = None
    if request.method == "POST":
        clf = request.form['clf']
        review = request.form['review']

        # load vectorizer
        file = open("./models/vectorizer.pkl",'rb')
        vectorizer = pickle.load(file)
        file.close()

        # remove punctuations
        review = [letter for letter in review if letter not in string.punctuation]
        review = ''.join(review)

        # remove stopwords
        review = [word for word in review.split(' ') if word not in nltk.corpus.stopwords.words('english')]
        review = ' '.join(review)

        # stemming
        ps = PorterStemmer()
        review = [ps.stem(word) for word in review.split(' ')]
        review = ' '.join(review)

        # to dataframe
        x = pd.DataFrame({
            'input':[review]
        })

        # vectorize and predict
        x = vectorizer.transform(x['input'])


        if clf == "RFC":
            
            # loading random forest model
            file = open("./models/RFC.pkl",'rb')
            rfc = pickle.load(file)
            file.close()
            
            # making predictions
            response = rfc.predict_proba(x)[0][1]*100

        elif clf == "NBC":
            
            # loading multinomial naive bayes
            file = open("./models/MNBC.pkl",'rb')
            NBC = pickle.load(file)
            file.close()

            # making predictions
            response = round(NBC.predict_proba(x)[0][1]*100,2)
        
        else:

            # loading random forest model
            file = open("./models/RFC.pkl",'rb')
            rfc = pickle.load(file)
            file.close()
            
            # making predictions
            response = rfc.predict_proba(x)[0][1]*100

            # loading multinomial naive bayes
            file = open("./models/MNBC.pkl",'rb')
            NBC = pickle.load(file)
            file.close()

            # making predictions
            response = round((NBC.predict_proba(x)[0][1]*100 + response)/2,2)

    return render_template("index.html", response=response)

if __name__ == "__main__":
    app.run(debug=True)