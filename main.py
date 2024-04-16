from flask import Flask, url_for, request, redirect, render_template

app = Flask(__name__)

@app.route('/')
def bootstrap():
    return render_template('bootstrap_template.html')

@app.route('/main')
def main():
    return '<h1 style="text-align: center;">Вы успешно зарегистрировались</h1>'

if __name__ == '__main__':
    app.run('127.0.0.1', 8080)
