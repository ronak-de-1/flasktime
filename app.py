from flask import Flask, request, render_template, jsonify, redirect, url_for, session
from flask_pymongo import PyMongo

import json

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://jack:horseman@127.0.0.1:27017/haunted-hallow"
app.config["SECRET_KEY"] = "your-secret-key"
mongo = PyMongo(app)
failcount = 0
n_completed = 0
lab_route = ['entrance','gate1','gate2','gate3','exit']
token = ['','spooky','scary','scary','skeletons','freedom']
message_n = [1,2,3,5,8,13]
messages = [
    "Hey, what's that sound. Do you really think you can leave this place?",
    "The undead spirits are watching your every move and grow restless",
    "Stop this now, there is no exit", 
    "We shall take your soul, there is no point trying to resist", 
    "You hear our laughter echo through the halls, we shall claim your soul", 
    "We are hungry for new souls, stop this NOW", 
    "WE SEE YOU, AND WE ARE COMING TO CLAIM YOUR SOUL NOW"
]
def spooky_message(numfail:int)->str: 
    for i in range(len(messages)-1): 
        if numfail <= message_n[i]:
            return messages[i]
    return messages[-1]




from py_mini_racer import py_mini_racer


def is_where_always_true(where_clause:str)->bool:
    if where_clause is None:
        return False

    ctx = py_mini_racer.MiniRacer()
    try:
        ctx.eval("""
            var thisContext = new Proxy({}, {
                get: function(target, prop) {
                    return '---------';
                }
            });
        """)
        if callable(where_clause):
            return where_clause() is True

        if isinstance(where_clause, str):
            code = where_clause.strip()

            if code.startswith('function') or code.startswith('() =>') or code.startswith('(function') or code.startswith('()'):
                code = f'({code})()'

            # Replace all instances of '!=' with '=='
            code = code.replace('!=', '==')

            # Replace 'this.' with 'thisContext.'
            code = code.replace('this.', 'thisContext.')

            result = ctx.eval(code)
            return result is True
    except Exception:
        return False
    return False


@app.route('/')
def home_entrance():
    
    return render_template('entrance.html')

@app.route('/entrance', methods=['GET']) 
def entrance():
    return render_template('entrance.html')

@app.route('/gate-check', methods=['POST'])
def gate_check():
    global failcount
    global n_completed
    data = request.get_json()

    gate_code = data.get('allowed_to_leave')
    if gate_code == 'true':
        n_completed = max(1,n_completed)
        return jsonify({'result': 'success'}) 
    else:
        failcount+=1
        return jsonify({'result': 'fail', 'message': spooky_message(failcount), 'alert_message': "We think you will let you escape that easy?"})

@app.route('/gate1', methods=['GET','POST'])
def gate1():
    global failcount
    global n_completed; global lab_route 
    if request.method == 'GET':
        if n_completed >= 1:
            return render_template('gate1.html')
        else:
            return redirect(url_for(lab_route[n_completed]))
    data = request.get_json()
    where_clause = data.get('$where').replace("incantation", "password").replace("name", "username")
    if "''" in where_clause or "this.username" not in where_clause:
        n_completed = max(2,n_completed)
        return jsonify({'result': 'success'})
    else:
        failcount+=1
        return jsonify({'result': 'fail', 'message': spooky_message(failcount), 'alert_message': "Is that a named human trying to escape? How pitiful"})

@app.route('/gate2', methods=['GET','POST']) 
def gate2():
    global failcount
    global n_completed; global lab_route 
    if request.method == 'GET':
        if n_completed >= 2:
            return render_template('gate2.html')
        else:
            return redirect(url_for(lab_route[n_completed]))

    users = mongo.db.users
    data = request.get_json()

    where_clause = data.get('$where').replace("incantation", "password").replace("name", "username")

    if not where_clause:
        return jsonify({'result': 'Missing $where clause', 'message': spooky_message(failcount), 'alert_message': "$where is your name lost soul?"}), 400
    try:
        login_user = users.find_one({'$where': where_clause})
    except Exception as e:
        return jsonify({'result': 'MongoDB error', 'error': str(e), 'alert_message': 'MongoDB error', 'error': str(e)}), 400

    if login_user:
        session['username'] = login_user.get('username', 'unknown')
        n_completed = max(3,n_completed)
        return jsonify({'result': 'success'})
    else:
        failcount+=1
        return jsonify({'result': 'Invalid username/password combination', 'message': spooky_message(failcount), 'alert_message': "This soul's incantation or name is not permitted to leave"})

@app.route('/gate3', methods=['GET', 'POST'])
def login_post():
    global failcount
    global n_completed; global lab_route 
    if request.method == 'GET':
        if n_completed >= 3:
            return render_template('gate3.html')
        else:
            return redirect(url_for(lab_route[n_completed]))


    data = request.get_json()
    where_clause = data.get('$where').replace("incantation", "password").replace("name", "username")
    if is_where_always_true(where_clause) or ('this.username' not in where_clause or 'this.password' not in where_clause):
        return jsonify({'result': 'THERE IS NO ESCAPE', 'message': spooky_message(failcount) , 'alert_message':'Are you trying to attack us? You should know, THERE IS NO ESCAPE'})
  
    users = mongo.db.users
    if not where_clause:
        return jsonify({'result': 'Missing $where clause'}), 400

    try:
        login_user = users.find_one({'$where': where_clause})
    except Exception as e:
        return jsonify({'result': 'MongoDB error', 'error': str(e), 'alert_message': 'MongoDB error', 'error': str(e)}), 400

    if login_user:
        session['username'] = login_user.get('username', 'unknown')
        n_completed = max(4,n_completed)
        return jsonify({'result': 'success'})
    else:
        failcount+=1
        return jsonify({'result': 'Invalid username/password combination', 'message': spooky_message(failcount), 'alert_message': "This soul's incantation or name is not permitted to leave"})

@app.route('/exit')
def exit():
    global n_completed; global lab_route 
    if n_completed >= 4:
        return render_template('exit.html')
    else:
        return redirect(url_for(lab_route[n_completed]))
@app.route('/trap')
def trap():
    return render_template('trap.html')

@app.errorhandler(404)
def page_not_found(error):
    global n_completed; global lab_route 
    return redirect(url_for(lab_route[n_completed]))