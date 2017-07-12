from flask import Flask, session, request, redirect, render_template
from mysqlconnection import MySQLConnector

app = Flask(__name__)
mysql = MySQLConnector(app, 'full_friends')

@app.route('/')
def root_route():
    return redirect('/users')

# Viewing all users
@app.route('/users')
def index():
    query = 'select id, concat(first_name, " ", last_name) as name, age, date_format(friend_since, "%b %D, %Y") as date from friends'
    all_users = mysql.query_db(query)
    return render_template('index.html', all_users = all_users)

# Viewing specific users
@app.route('/users/<id>')
def show(id):
    query = 'select id, concat(first_name, " ", last_name) as name, age, date_format(friend_since, "%b %D, %Y") as date from friends where id = :id'
    data = {'id': id}
    user_info = mysql.query_db(query, data)
    user = user_info[0]
    return render_template('show.html', user = user)

# Creating new users
@app.route('/users/new')
def new():
    return render_template('new.html')

@app.route('/users/create', methods = ['POST'])
def create():
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    age = request.form['age'] 
    insert = 'insert into friends (first_name, last_name, age, friend_since) values(:first_name, :last_name, :age, NOW())'
    data = {
        'first_name': first_name,
        'last_name': last_name,
        'age': age    
    }
    id = str(mysql.query_db(insert, data))
    return redirect('/users/' + id)

# Editing existing users
@app.route('/users/<id>/edit')
def edit(id):
    query = 'select id, first_name, last_name, age from friends where id = :id'
    data = {'id': id}
    user_info = mysql.query_db(query, data)
    user = user_info[0]
    return render_template('edit.html', user = user)

@app.route('/users/<id>/update', methods = ['POST'])
def update(id):
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    age = request.form['age'] 
    update = 'update friends set first_name = :first_name, last_name = :last_name, age = :age where id = :id'
    data = {
        'first_name': first_name,
        'last_name': last_name,
        'age': age,  
        'id': id  
    }
    mysql.query_db(update, data)
    return redirect('/users/' + id)

# Destroying a user
@app.route('/users/<id>/destroy')
def destroy(id):
    delete = 'delete from friends where id = :id'
    data = {'id': id}
    mysql.query_db(delete, data)
    return redirect('/users')

app.run(debug=True)