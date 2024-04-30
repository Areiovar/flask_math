from werkzeug.security import generate_password_hash
from flask import Flask, render_template, request, redirect, url_for, Markup, jsonify
import sqlite3
import random
import math

app = Flask(__name__)

def create_table():
    conn = sqlite3.connect('userdata.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY, surname TEXT, name TEXT, patronymic TEXT,
                 birthdate TEXT, password TEXT, sex TEXT, about TEXT)''')
    conn.commit()
    conn.close()


def insert_data(surname, name, patronymic, birthdate, password, sex, about):
    hashed_password = generate_password_hash(password)
    conn = sqlite3.connect('userdata.db')
    c = conn.cursor()
    c.execute('''INSERT INTO users (surname, name, patronymic, birthdate, password, sex, about)
                 VALUES (?, ?, ?, ?, ?, ?, ?)''', (surname, name, patronymic, birthdate, hashed_password, sex, about))
    conn.commit()
    conn.close()


def generate_coefficients():
    while True:
        a = random.randint(1, 10)
        b = random.randint(1, 10)
        c = random.randint(1, 10)
        discriminant = b**2 - 4 * a * c
        if 0 <= discriminant == math.isqrt(discriminant) ** 2:
            return a, b, c


@app.route('/')
def index():
    return render_template('bootstrap_template.html')


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/main', methods=['POST'])
def main():
    surname = request.form.get('surname')
    name = request.form.get('name')
    patronymic = request.form.get('patronymic')
    birthdate = request.form.get('birthdate')
    password = request.form.get('password')
    sex = request.form.get('sex')
    about = request.form.get('about')

    insert_data(surname, name, patronymic, birthdate, password, sex, about)

    return redirect(url_for('profile', surname=surname, name=name, patronymic=patronymic, birthdate=birthdate,
                            password=password, sex=sex, about=about))


@app.route('/account')
def profile():
    surname = request.args.get('surname')
    name = request.args.get('name')
    patronymic = request.args.get('patronymic')
    birthdate = request.args.get('birthdate')
    password = request.args.get('password')
    sex = request.args.get('sex')
    about = request.args.get('about')

    conn = sqlite3.connect('userdata.db')
    c = conn.cursor()
    c.execute('SELECT * FROM users ORDER BY id DESC LIMIT 1')
    user_data = c.fetchone()
    conn.close()

    return render_template('profile.html', surname=surname, name=name, patronymic=patronymic,
                           birthdate=birthdate, password=password, sex=sex, about=about)


@app.route('/course')
def course():
    return render_template('course.html')


@app.route('/course/lesson1', methods=['POST'])
def lesson1_post():
    user_answer = request.form.get('answer')
    correct_answer = request.form.get('correct_answer')

    # Validate the user's answer
    if user_answer is not None and correct_answer is not None:
        try:
            user_answer = int(user_answer)
            correct_answer = int(correct_answer)
            if user_answer == correct_answer:
                return jsonify({'result': 'correct'})
            else:
                return jsonify({'result': 'incorrect'})
        except ValueError:
            return jsonify({'error': 'Invalid input. Please enter a valid number.'})
    else:
        return jsonify({'error': 'Missing user answer or correct answer.'})


@app.route('/course/lesson1')
def lesson1():
    title = "Решение квадратных уравнений"
    lesson_title = "Урок 1: Решение квадратных уравнений"

    a, b, c = generate_coefficients()
    correct_answer = max(round((-b + (b**2 - 4*a*c)**0.5) / (2*a)),
                         round((-b - (b**2 - 4*a*c)**0.5) / (2*a)))

    lesson_content = f"""
            <p>Уравнение вида ax&sup2;+bx+c=0, где а, b и c – некоторые числа, причем а ≠ 0, а х – переменная, называется квадратным.<br><br>
            Примеры: 2x&sup2;+2x+1=0; -3x&sup2;+4x=0; 9x&sup2;-25=0. В каждом из уравнений назвать, чему равны коэффициенты.<br><br>
            Определение. Если в уравнении вида ax&sup2;+bx+c=0 хотя бы один из коэффициентов b или c равен 0, то уравнение называют неполным квадратным.<br><br>
            1. Если c=0, то уравнение имеет вид ax&sup2;+bx=0. Оно решается разложением на множители. Уравнение данного вида всегда имеет два корня, всегда один из них равен нулю.<br><br> 
            Пример: 4x&sup2;+16x=0 Решить самостоятельно:<br>
            4x (x+4) = 0<br>
            3x&sup2;-6x=0<br>
            4x=0 или x+4=0<br>
            x=0 x= -4<br>
            Ответ: x=0, x=-4.<br><br>
            2. Если b=0, то уравнение имеет вид ax&sup2;+c=0. Оно решается только тогда, когда у коэффициентов а и с разные знаки. При решении уравнений применяет формулу разности квадратов.<br><br>
            Пример: 1) 1-4y&sup2;=0 2) 6x&sup2;+12=0<br>
            (1-2y) (1+2y) =0 Решений нет, так как это сумма квадратов, а не разность.<br>
            1-2y=0 или 1+2y=0<br>
            Решить самостоятельно -x&sup2;+3=0<br>
            2y=1 2y= -1<br>
            (3-x)(3+x)=0<br>
            y=0,5 y=-0,5<br>
            3-x=0 или 3+x=0<br>
            Ответ: y=0,5; y=-0,5; x=3; x=-3.<br><br>
            3. Если b=0 и с=0, то уравнение имеет вид ax&sup2;=0. Уравнение имеет единственный корень x=0.<br><br>
            Решение полных квадратных уравнений<br><br>
            Определение. Выражение вида D=b&sup2;-4ac называют дискриминантом квадратного уравнения.<br><br>
            Примеры. Вычислите дискриминант<br><br>
            2x&sup2;+3x+1=0, a=2, b=3, c=1 D=3&sup2;-4* 2* 4= -23<br>
            5x&sup2;-2x-1=0, a=5, b=-2, c=-1 D=(-2)&sup2;-4* 5* (-1)= 24</p>
            <p>Уравнение вида {a}x&sup2;+{b}x+{c}=0, где а, b и c – некоторые числа, причем а ≠ 0, а х – переменная, называется квадратным.<br><br>
            Решите уравнение и введите больший из корней:</p>


        <form id="lessonForm">
            <label for="answer">Введите больший из корней:</label>
            <input type="text" id="answer" name="answer">
            <input type="hidden" id="correctAnswer" name="correct_answer" value="{correct_answer}">
            <button type="button" onclick="checkAnswer()">Проверить</button>
            <p id="result"></p>
        </form>

        <script>
            function checkAnswer() {{
                var userAnswer = document.getElementById("answer").value;
                var correctAnswer = document.getElementById("correctAnswer").value;
                userAnswer = parseInt(userAnswer);
                if (!isNaN(userAnswer)) {{
                    fetch('/course/lesson1', {{
                        method: 'POST',
                        body: new URLSearchParams({{ answer: userAnswer, correct_answer: correctAnswer }}),
                        headers: {{ 'Content-Type': 'application/x-www-form-urlencoded' }}
                    }})
                    .then(response => response.json())
                    .then(data => {{
                        if (data.result === 'correct') {{
                            document.getElementById("result").innerHTML = "Правильно";
                        }} else if (data.result === 'incorrect') {{
                            document.getElementById("result").innerHTML = "Неправильно. Попробуйте еще раз!";
                        }} else if (data.error) {{
                            document.getElementById("result").innerHTML = data.error;
                        }}
                    }})
                    .catch(error => {{
                        console.error('Error:', error);
                    }});
                }} else {{
                    document.getElementById("result").innerHTML = "Пожалуйста, введите число.";
                }}
            }}
        </script>
    """
    return render_template('lesson.html', title=title, lesson_title=lesson_title,
                           lesson_content=Markup(lesson_content))

@app.route('/course/lesson2')
def lesson2():
    title = "Одночлены и их свойства"
    lesson_title = "Урок 2: Одночлены и их свойства"
    lesson_content = """
        <p>Выражения 15a&sup2;b, 3ху • 2у, –3c&sup2; представляют собой произведения чисел, переменных и их степеней. Такие выражения называют одночленами. Числа, переменные и их степени также считаются одночленами. Например, выражения –11, а, а&sup2; — одночлены.</p>
        <p>Одночлен 5a&sup2;b • 2ab&sup3; можно упростить, если воспользоваться свойствами умножения и правилом умножения степеней с одинаковыми основаниями. Тогда получим: 5a&sup2;b • 2ab&sup3; = 5 • 2a&sup2; • a • b • b&sup3; = 10a&sup3;b⁴.</p>
        <p>Мы представили данный одночлен в виде произведения числового множителя, записанного на первом месте, и степеней различных переменных. Такой вид одночлена называют стандартным видом. Числа, переменные, их степени также считаются одночленами стандартного вида.</p>
        <p>Коэффициент и степень одночлена: Любой одночлен можно преобразовать так, чтобы получился одночлен стандартного вида. Если одночлен записан в стандартном виде, то числовой множитель называют коэффициентом одночлена. Например, в одночлене –10a&sup2;b⁴ коэффициент равен –10. Если коэффициент одночлена равен 1 или –1, то его обычно не пишут.</p>
        <p>Степенью одночлена стандартного вида называют сумму показателей степеней входящих в него переменных. Если одночлен представляет собой число, отличное от нуля, то его степень считается равной нулю.</p>
        <p>Умножение одночленов: При умножении одночленов снова получается одночлен, который обычно записывают в стандартном виде, используя для этого свойства умножения и правило умножения степеней с одинаковыми основаниями.</p>
        <p>Возведение одночлена в степень: Рассмотрим сначала правила возведения в степень произведения и степени. Преобразуем четвёртую степень произведения ab:</p>
        <p>(ab)⁴ = (ab)(ab)(ab)(ab) = (aaaa)(bbbb) = a⁴b⁴, т.е. (ab)⁴ = a⁴b⁴.</p>
        <p>Четвёртая степень произведения равна произведению четвёртых степеней множителей. Аналогичным свойством обладает любая натуральная степень произведения двух множителей.</p>  
        <p>Если а и b — произвольные числа и n — любое натуральное число, то (ab)ⁿ = aⁿbⁿ.</p>
        <p>Стандартным видом одночлена 0.01ab*100a:</p>
        <ol>
          <li>10a²b</li>
          <li>10b</li>
          <li>a²b</li>
          <li>ab</li>
        </ol>
        <form onsubmit="return checkAnswer()">
            <p>Введите номер правильного варианта ответа:</p>
            <input type="radio" id="option1" name="answer" value="1">
            <label for="option1">1</label><br>
            <input type="radio" id="option2" name="answer" value="2">
            <label for="option2">2</label><br>
            <input type="radio" id="option3" name="answer" value="3">
            <label for="option3">3</label><br>
            <input type="radio" id="option4" name="answer" value="4">
            <label for="option4">4</label><br><br>
            <button onclick="checkAnswer()">Проверить</button>
        </form>
        <p id="result"></p>
        <script>
            function checkAnswer() {
                var userAnswer = document.querySelector('input[name="answer"]:checked');
                if (userAnswer === null) {
                    alert("Выберите один из вариантов ответа!");
                    return false;
                }
                var selectedAnswer = userAnswer.value;
                var correctAnswer = "3";
                if (selectedAnswer === correctAnswer) {
                    document.getElementById("result").innerHTML = "Правильно";
                } else {
                    document.getElementById("result").innerHTML = "Неправильно. Попробуйте еще раз!";
                }
                return false;
            }
        </script>
    """
    return render_template('lesson.html', title=title, lesson_title=lesson_title, lesson_content=Markup(lesson_content))


@app.route('/course/lesson3')
def lesson3():
    title = "Теория вероятностей"
    lesson_title = "Урок 3: Теория вероятностей"
    all_cards = generate_deck_size()
    black_cards = all_cards // 2

    lesson_content = f"""
        <p>Теория вероятностей — это наука, которая изучает мир случайностей и пытается их предсказать. Здесь встречаются такие понятия, как «события» и «вероятности», у которых, в свою очередь, есть свои свойства и операции — о них мы поговорим чуть позже.</p>
        <p>Проще всего продемонстрировать, как работает теория вероятностей, на примере подбрасывания монетки. В этом случае у нас есть два варианта: орёл или решка, а значит, шанс выпадения каждой из сторон одинаковый и составляет 50%.</p>
        <p>Событие — это всё, что может произойти, когда мы совершаем какое-то действие. Например, если мы бросаем монетку, то событие — это выпадение орла или решки. Чтобы обозначать события, используют заглавные буквы латинского алфавита. Например, для орла можем выбрать букву A, а для решки — B.</p>
        <p>Существует много разных видов и классификаций событий, но в этой статье мы остановимся на основных четырёх:</p>
        <ul>
            <li>Достоверные — те, которые точно произойдут. Если бросить стакан на пол, то с вероятностью 100% он полетит вниз.</li>
            <li>Невозможные — те, которые никогда не произойдут. Если бросить тот же стакан на пол, то он никогда не полетит вверх (мораль: не стоит бросать стаканы на пол, если, конечно, вы не на МКС).</li>
            <li>Случайные — те, которые могут произойти, а могут и не произойти. Например, если мы бросаем игральный кубик, то не можем с уверенностью сказать, что выпадет число 2.</li>
            <li>Несовместимые — те, которые исключают друг-друга. Например, при подбрасывании монетки может выпасть либо орёл, либо решка — оба одновременно они выпасть не могут.</li> 
        </ul>

        <p><b>Задание:</b></p>
        <p>Предположим, у вас есть колода из {all_cards} стандартных карт. Какова вероятность того, что вы вытянете черную карту (пики или червы)?</p>
        <div>
            <label for="answer">Введите ваш ответ в виде десятичной дроби:</label>
            <input type="text" id="answer" name="answer">
            <button onclick="checkAnswer()">Проверить</button>
            <p id="result"></p>
        </div>

        <script>
            function checkAnswer() {{
                var userAnswer = document.getElementById("answer").value;
                var correctAnswer = {black_cards} / {all_cards};
                userAnswer = parseFloat(userAnswer);
                if (Math.abs(userAnswer - correctAnswer) < 0.01) {{
                    document.getElementById("result").innerHTML = "Правильно";
                }} else {{
                    document.getElementById("result").innerHTML = "Неправильно. Попробуйте еще раз!";
                }}
            }}
        </script>
    """
    return render_template('lesson.html', title=title, lesson_title=lesson_title,
                           lesson_content=Markup(lesson_content))


@app.route('/course/lesson4')
def lesson4():
    title = "Lesson 4"
    lesson_title = "Урок 4: Алгебра событий"
    lesson_content = """
        <p>Когда мы считаем вероятности, нас может устраивать более чем один результат событий. Или другая ситуация — нам может быть важно, чтобы два события выполнялись вместе. В таких случаях на помощь приходит алгебра событий. Разбираемся, какие действия она позволяет совершать.</p>
        <h3>Сложение (объединение) событий</h3>
        <p>Сумма двух событий A + B — это сложное событие, которое произойдёт, если случится или событие A, или событие B, или оба одновременно.</p>
        <p>Допустим, мы хотим вычислить вероятность выпадения на кубике стороны с числами 2 или 4. Обозначим событие «выпадение стороны 2» как A, а событие «выпадение стороны 4» как B. Так как у кубика всего шесть граней, вероятность выпадения каждой из этих сторон равна 1/6.</p>
        <h3>Умножение (пересечение) событий</h3>
        <p>Произведение событий A и B — это событие A × B, которое произойдёт, если случится и событие A, и событие B.</p>
        <p>Допустим, мы бросаем монетку два раза и хотим понять, каков шанс, что оба раза выпадет решка. Напомним, что вероятность выпадения решки — 1/2.</p>
        <p>Обозначаем события: A — решка выпадает первый раз, B — решка выпадает второй раз.</p>
        <p>Получаем, что шанс выпадения решки два раза подряд — 25%.</p>
        <h3>Задание</h3>
        <p>На экзамене по геометрии школьнику достаётся один вопрос из списка экзаменационных вопросов. Вероятность того, что это вопрос на тему «Ромб», равна 0,1. Вероятность того, чт
о это вопрос на тему «Описанная окружность», равна 0,15. Вопросов, относящихся одновременно к этим двум темам, нет. Найдите вероятность того, что на экзамене школьнику достанется вопрос по одной из этих двух тем.</p>
        <div>
            <label for="answer">Введите вероятность:</label>
            <input type="text" id="answer" name="answer">
            <button onclick="checkAnswer()">Проверить</button>
            <p id="result"></p>
        </div>

        <script>
            function checkAnswer() {
                var userAnswer = document.getElementById("answer").value;
                var correctAnswer = 0.005;
                userAnswer = parseFloat(userAnswer);
                if (userAnswer === correctAnswer) {
                    document.getElementById("result").innerHTML = "Правильно";
                } else {
                    document.getElementById("result").innerHTML = "Неправильно. Попробуйте еще раз!";
                }
            }
        </script>
    """
    return render_template('lesson.html', title=title, lesson_title=lesson_title, lesson_content=Markup(lesson_content))


@app.route('/course/lesson5')
def lesson5():
    root1 = random.randint(1, 200)
    root2 = random.randint(1, 200)

    title = "Иррациональные числа"
    lesson_title = "Урок 5: Иррациональные числа"
    lesson_content = f"""
        <p>Иррациональные числа не поддаются привычным математическим действиям. Чтобы правильно работать с этим подмножеством чисел в 6 классе требуется знание нескольких правил и законов. Именно об этих правилах и законах и пойдет речь сегодня.</p>
        <p>Все действительные числа делятся на рациональные и иррациональные.</p>
        <p>К рациональным относятся:</p>
        <ul>
            <li>Натуральные числа, от 1 и до бесконечности. Дробные числа сюда не входят.</li>
            <li>Дробные числа с любым знаком.</li>
            <li>Целые числа: положительные, отрицательные целые числа и ноль.</li>
        </ul>
        <p>К иррациональным числа относятся любые значения со знаком радикала. Подмножество иррациональных чисел имеет обозначение J.</p>
        <p><strong>Знак радикала</strong></p>
        <p>Что такое знак радикала? Это знак корня. Корень может быть любой степени, важен сам факт наличия радикала. Отдельно отметим, что корень, который можно вычислить нельзя считать иррациональным числом. Отличительным признаком иррационального числа является невозможность точного подсчета его значения.</p>
        <p>Это значит, что если вбить значение корня в калькулятор, то получившееся значение будет бесконечно.</p>
        <p>В точных математических расчетах иррациональное число считается вычисленным, если можно точно узнать любое количество знаков после запятой. Количество вычисленных иррационал
ьных чисел на сегодняшний момент минимально. Число пи так же является иррациональным и не вычисленным до конца. В школьных примерах можно оставлять действия с корнем на самый конец выч
ислений, а потом считать на калькуляторе приближенное значение. Округление до 0,01 считается приемлемы для учебных вычислений. Можно и вовсе просто оставить пример с не вычисленными корнями, особенно это касается задач на упрощение примеров.</p>
        <h3>Задание</h3>
        <p>Сравните значения корней √{root1} и √{root2}. Введите в поле ниже, какой из корней больше:</p>
        <div>
            <input type="text" id="answer" name="answer">
            <button onclick="checkAnswer()">Проверить</button>
            <p id="result"></p>
        </div>

        <script>
            function checkAnswer() {{
                var userAnswer = document.getElementById("answer").value;
                var correctAnswer = Math.sqrt({max(root1, root2)});
                if (userAnswer.trim().toLowerCase() === "√{max(root1, root2)}") {{
                    document.getElementById("result").innerHTML = "Правильно! √{max(root1, root2)} больше, чем √{min(root1, root2)}.";
                }} else {{
                    document.getElementById("result").innerHTML = "Неправильно. Попробуйте еще раз!";
                }}
            }}
        </script>
    """
    return render_template('lesson.html', title=title, lesson_title=lesson_title, lesson_content=Markup(lesson_content))


@app.route('/course/lesson6')
def lesson6():
    title = "Абсолютная погрешность"
    lesson_title = "Урок 6: Абсолютная погрешность"

    measured_weight = round(random.uniform(1, 10), 1)
    true_weight = round(measured_weight + random.uniform(-0.5, 0.5), 1)

    absolute_error = abs(true_weight - measured_weight)

    lesson_content = f"""
        <p>Абсолютной погрешностью числа называют разницу между этим числом и его точным значением.</p>
        <p>Рассмотрим пример: в школе учится 374 ученика. Если округлить это число до 400, то абсолютная погрешность измерения равна 400-374=26.</p>
        <p>Для подсчета абсолютной погрешности необходимо из большего числа вычитать меньшее.</p>
        <p>Существует формула абсолютной погрешности. Обозначим точное число буквой А, а буквой а – приближение к точному числу. Приближенное число – это число, которое незначительно отличается от точного и обычно заменяет его в вычислениях. Тогда формула будет выглядеть следующим образом:</p>
        <p>Δа = А - а.</p>
        <p>На практике абсолютной погрешности недостаточно для точной оценки измерения. Редко когда можно точно знать значение измеряемой величины, чтобы рассчитать абсолютную погрешно
сть. Измеряя книгу в 20 см длиной и допустив погрешность в 1 см, можно считать измерение с большой ошибкой. Но если погрешность в 1 см была допущена при измерении стены в 20 метров, это измерение можно считать максимально точным. Поэтому в практике более важное значение имеет определение относительной погрешности измерения.</p>

        <h3>Задание:</h3>
        <p>При измерении массы пакета продуктов на весах, точные веса которых неизвестны, вес пакета был определен как {measured_weight} кг. Если точный вес пакета составляет {true_weight} кг, найдите абсолютную погрешность этого измерения.</p>
        <div>
            <label for="answer">Введите ваш ответ:</label>
            <input type="text" id="answer" name="answer">
            <button onclick="checkAnswer()">Проверить</button>
            <p id="result"></p>
        </div>

        <script>
            function checkAnswer() {{
                var userAnswer = document.getElementById("answer").value;
                var correctAnswer = {absolute_error};
                userAnswer = parseFloat(userAnswer);
                if (Math.abs(userAnswer - correctAnswer) < 0.01) {{
                    document.getElementById("result").innerHTML = "Правильно";
                }} else {{
                    document.getElementById("result").innerHTML = "Неправильно. Попробуйте еще раз!";
                }}
            }}
        </script>
    """

    return render_template('lesson.html', title=title, lesson_title=lesson_title,
                           lesson_content=Markup(lesson_content))


@app.route('/course/lesson7')
def lesson7():
    title = "Относительная погрешность"
    lesson_title = "Урок 7: Относительная погрешность"

    absolute_error = random.randint(1, 5)
    exact_length = random.randint(170, 190)
    relative_error = round((absolute_error / exact_length) * 100, 2)

    lesson_content = f"""
        <style>
            .round-button {{
                border-radius: 20px;
            }}
        </style>
        <p>Относительной погрешностью называют отношение абсолютной погрешности числа к самому этому числу. Чтобы рассчитать относительную погрешность в примере с учениками, разделим 26 на 374.</p>
        <p>Получим число 0,0695, переведем в проценты и получим 7 %. Относительную погрешность обозначают процентами, потому что это безразмерная величина. Относительная погрешность – 
это точная оценка ошибки измерений. Если взять абсолютную погрешность в 1 см при измерении длины отрезков 10 см и 10 м, то относительные погрешности будут соответственно равны 10 % и 0,1 %. Для отрезка длиной в 10 см погрешность в 1 см очень велика, это ошибка в 10 %. А для десятиметрового отрезка 1 см не имеет значения, всего 0,1 %.</p>
        <p>Различают систематические и случайные погрешности. Систематической называют ту погрешность, которая остается неизменной при повторных измерениях. Случайная погрешность возникает в результате воздействия на процесс измерения внешних факторов и может изменять свое значение.</p>
        <p>Правила подсчета погрешностей:</p>
        <ul>
            <li>при сложении и вычитании чисел необходимо складывать их абсолютные погрешности;</li>
            <li>при делении и умножении чисел требуется сложить относительные погрешности;</li>
            <li>при возведении в степень относительную погрешность умножают на показатель степени.</li>
        </ul>
        <p>Приближенные и точные числа записываются при помощи десятичных дробей. Берется только среднее значение, поскольку точное может быть бесконечно длинным. Чтобы понять, как зап
исывать эти числа, необходимо узнать о верных и сомнительных цифрах. Верными называются такие цифры, разряд которых превосходит абсолютную погрешность числа. Если же разряд цифры меньш
е абсолютной погрешности, она называется сомнительной. Например, для дроби 3,6714 с погрешностью 0,002 верными будут цифры 3,6,7, а сомнительными – 1 и 4. В записи приближенного числа оставляют только верные цифры. Дробь в этом случае будет выглядеть таким образом – 3,67.</p>
        <p>При измерении длины стола была получена абсолютная погрешность в {absolute_error} см.
        Если точная длина стола составляет {exact_length} см, найдите относительную погрешность этого измерения.</p>
        <div>
            <label for="answer">Введите ваш ответ:</label>
            <input type="text" id="answer" name="answer">
            <button onclick="checkAnswer({relative_error})">Проверить</button>
            <p id="result"></p>
        </div>

        <script>
            function checkAnswer(correctAnswer) {{
                var userAnswer = document.getElementById("answer").value;
                userAnswer = parseFloat(userAnswer);
                if (Math.abs(userAnswer - correctAnswer) < 0.01) {{
                    document.getElementById("result").innerHTML = "Правильно";
                }} else {{
                    document.getElementById("result").innerHTML = "Неправильно. Попробуйте еще раз!";
                }}
            }}
        </script>
    """

    return render_template('lesson.html', title=title, lesson_title=lesson_title, lesson_content=Markup(lesson_content))



if __name__ == '__main__':
    create_table()
    app.run('127.0.0.1', 8080)
