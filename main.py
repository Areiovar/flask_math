from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

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

    # Перенаправление на страницу профиля с передачей данных
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

    # Отображение шаблона с передачей данных
    return render_template('profile.html', surname=surname, name=name, patronymic=patronymic,
                           birthdate=birthdate, education=education, sex=sex, about=about)


if __name__ == '__main__':
    app.run('127.0.0.1', 8080)
