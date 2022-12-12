from flask import Flask, render_template, request, flash, redirect, url_for
import pandas as pd 
import os, sys

app = Flask("__name__")
app.secret_key = "darshan"

@app.route("/index")
def index():
    return render_template("index.html")

@app.route("/validate",methods=['GET','POST'])
def validate():
    if request.method == "POST":
        uploaded_file = request.files['file']
        print("before")
        if uploaded_file.filename != '':
            uploaded_file.save(uploaded_file.filename)
            print(uploaded_file.fielname)
        return redirect(url_for('index'))
    return render_template('index.html')



if __name__ == '__main__':
    app.run(debug=True)

