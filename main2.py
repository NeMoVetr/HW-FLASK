from flask import Flask, render_template, request, redirect, url_for, make_response

app = Flask(__name__)


@app.route('/')
def input_text():
    return render_template('index.html')


@app.route('/set_cookie', methods=['POST'])
def set_cookie():
    username = request.form['username']
    email = request.form['email']

    response = make_response(redirect(url_for('greet')))
    response.set_cookie('username', username)
    response.set_cookie('email', email)
    return response


@app.route('/greet')
def greet():
    username = request.cookies.get('username')
    email = request.cookies.get('email')
    return render_template('greet.html', username=username, email=email)


@app.route('/delite', methods=['POST'])
def delite():
    response = make_response(redirect(url_for('input_text')))
    response.delete_cookie('username')
    response.delete_cookie('email')
    return response


if __name__ == '__main2__':
    app.run(debug=True)
