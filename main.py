from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

def create_table():
    conn = sqlite3.connect('userdata.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY, surname TEXT, name TEXT, patronymic TEXT,
                 birthdate TEXT, education TEXT, sex TEXT, about TEXT)''')
    conn.commit()
    conn.close()

def insert_data(surname, name, patronymic, birthdate, education, sex, about):
    conn = sqlite3.connect('userdata.db')
    c = conn.cursor()
    c.execute('''INSERT INTO users (surname, name, patronymic, birthdate, education, sex, about)
                 VALUES (?, ?, ?, ?, ?, ?, ?)''', (surname, name, patronymic, birthdate, education, sex, about))
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return render_template('bootstrap_template.html')

@app.route('/main', methods=['POST'])
def main():
    # Получение данных из формы
    surname = request.form.get('surname')
    name = request.form.get('name')
    patronymic = request.form.get('patronymic')
    birthdate = request.form.get('birthdate')
    education = request.form.get('education')
    sex = request.form.get('sex')
    about = request.form.get('about')

    # Проверка полученных данных
    print("Surname:", surname)
    print("Name:", name)
    print("Patronymic:", patronymic)
    print("Birthdate:", birthdate)
    print("Education:", education)
    print("Sex:", sex)
    print("About:", about)

    # Вставка данных в базу данных
    insert_data(surname, name, patronymic, birthdate, education, sex, about)

    # Перенаправление на страницу профиля
    return redirect(url_for('profile', surname=surname, name=name, patronymic=patronymic, birthdate=birthdate,
                            education=education, sex=sex, about=about))


@app.route('/account')
def profile():
    # Получение данных из URL
    surname = request.args.get('surname')
    name = request.args.get('name')
    patronymic = request.args.get('patronymic')
    birthdate = request.args.get('birthdate')
    education = request.args.get('education')
    sex = request.args.get('sex')
    about = request.args.get('about')
    conn = sqlite3.connect ('userdata.db')
    c = conn.cursor ()
    c.execute ('SELECT * FROM users ORDER BY id DESC LIMIT 1')
    user_data = c.fetchone ()
    conn.close ()

    # Отображение шаблона с передачей данных
    return render_template('profile.html', surname=surname, name=name, patronymic=patronymic,
                           birthdate=birthdate, education=education, sex=sex, about=about)

@app.route('/course')
def course():
    return 'asd'


if __name__ == '__main__':
    app.run('127.0.0.1', 8080)
