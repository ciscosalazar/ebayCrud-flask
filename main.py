from logging import debug
import sqlite3
from flask import Flask, render_template, request, redirect
from werkzeug.datastructures import auth_property
from flask_sqlalchemy  import SQLAlchemy

# Codigo para el CRUD empleando base de datos dataebay.db
# Por: Francisco Salazar | ciscosalazarm@gmail.com

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dataebay.db'
db = SQLAlchemy

@app.route('/')
def home():
    sqlite = "SELECT * FROM categories;"
    conn = sqlite3.connect('dataebay.db')
    c = conn.cursor()
    c.execute(sqlite)

    categories = c.fetchall()
    # print(categories)

    conn.commit()
    return render_template('index.html', categories=categories )

@app.route('/store', methods=['POST'])
def storege():
    _name =request.form["txtName"]
    _best_offer = request.form["txtBestOffer"]
    _auto_pay = request.form["txtAutoPay"]
    _level = request.form["numberLevel"]
    _parent_id = request.form["numberParentId"]
    _id = request.form["numberId"]
    _leaf = request.form["txtLeaf"]

    sqlite = "INSERT OR REPLACE INTO categories VALUES (?, ?, ?, ?, ?, ?, ?);"
    data = (_name, _best_offer, _auto_pay, _level, _parent_id, _id, _leaf)
    conn = sqlite3.connect('dataebay.db')
    c = conn.cursor()
    c.execute(sqlite,data)
    conn.commit()
    return redirect('/')

@app.route('/destroy/<int:id>')
def destroy(id):
    conn = sqlite3.connect('dataebay.db')
    c = conn.cursor()

    c.execute("DELETE FROM categories WHERE id=?;", (id,))

    conn.commit()
    return redirect('/')

@app.route('/edit/<int:id>')
def edit(id):

    conn = sqlite3.connect('dataebay.db')
    c = conn.cursor()
    c.execute("SELECT * FROM categories WHERE id=?;", (id,))

    categories = c.fetchall()

    conn.commit()
    return render_template('edit.html', categories=categories)

@app.route('/create')
def create():
    return render_template('create.html')

@app.route('/update', methods=['POST'])
def update():

    conn = sqlite3.connect('dataebay.db')
    c = conn.cursor()
    
    _name =request.form["txtName"]
    _best_offer = request.form["txtBestOffer"]
    _auto_pay = request.form["txtAutoPay"]
    _level = request.form["numberLevel"]
    _parent_id = request.form["numberParentId"]
    _id = request.form["numberId"]
    _leaf = request.form["txtLeaf"]

    sqlite = """UPDATE categories SET 'name'=?, 'best_offer'=?,'auto_pay'=?,'level'=?,'parent_id'=?,'id'=?, 'leaf'=? WHERE id=?;"""

    data = (_name, _best_offer, _auto_pay, _level, _parent_id, _id, _leaf, _id)
    
    c.execute(sqlite,data)
    
    conn.commit()

    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)
