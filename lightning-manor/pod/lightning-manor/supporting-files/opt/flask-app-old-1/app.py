from flask import Flask, request, render_template, jsonify, redirect, url_for, session
from flask_pymongo import PyMongo

import json

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://jack:horseman@127.0.0.1:27017/haunted-hallow"
app.config["SECRET_KEY"] = "your-secret-key"
mongo = PyMongo(app)

@app.route('/')
def login():
    return render_template('entrance.html')

@app.route('/login', methods=['GET','POST'])
def login_post():
    if request.method == 'GET':
        return render_template('login.html')

    users = mongo.db.users
    data = request.get_json()

    
    login_user = users.find_one({'$where': data['$where']})


    if login_user:
        session['username'] = login_user['username']
        return jsonify({'result': 'success'})
    else:
        return jsonify({'result': 'Invalid username/password combination'})


@app.route('/prizes')
def prizes():
    if 'username' in session:
        results = mongo.db.prizes.find({})
        return render_template('prizes.html', results=results)
    else:
        return redirect(url_for('login'))

@app.route('/entrance', methods=['GET']) # Added GET method
def entrance():
    return render_template('entrance.html')



@app.route('/gate-check', methods=['POST'])
def gate_check():
    data = request.get_json()

    # Example logic — change as needed
    gate_code = data.get('gateCode')
    if gate_code == 'letmein':
        return jsonify({'valid': True})
    else:
        return jsonify({'valid': False})
