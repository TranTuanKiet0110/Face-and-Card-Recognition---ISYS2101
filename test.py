from flask import (
    Flask,
    redirect,
    render_template,
    request,
    session,

)

app = Flask(__name__)
app.secret_key = 'hihihaha'

user = {"username": "admin", "password": "admin"}

@app.route('/login', methods=['POST', 'GET'])
def login():
    if (request.method == 'POST'):
        username = request.form.get('username')
        password = request.form.get('password')
        if username == user['username'] and password == user['password']:
            session['user'] = username
            return redirect('/adminAuth')

        return "<h1>Wrong username or password</h1>"

    return render_template("LogInLogOut.html")


@app.route('/adminAuth')
def adminAuth():
    if ('user' in session and session['user'] == user['username']):
        return render_template("adminAuthentication.html")

    return '<h1>You are not logged in.</h1>'

if __name__== '__main__':
    app.run(host='localhost', port=5500, debug=True)