from flask import Flask, render_template, request, redirect
import psycopg2

app = Flask(__name__)
conn = psycopg2.connect(database="service_db",
                        user="dbadmin",
                        password="pass",
                        host="localhost",
                        port="5433")
cursor = conn.cursor()


@app.route('/login/', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        cursor.execute(f"SELECT * FROM service.users WHERE login='{str(username)}'")
        records = list(cursor.fetchall())
        if not records:
            return render_template('login.html', req='We havent that login in our DB. Please click a registration button')
        elif records[0][3] == password:
            return render_template('account.html', req=records[0])
        else:
            return render_template('login.html', req='Wrong password')

    return render_template('login.html')

@app.route('/registration/', methods=['POST', 'GET'])
def registration():
    if request.method == 'POST':
        name = request.form.get('name')
        login = request.form.get('login')
        password = request.form.get('password')

        cursor.execute(f"SELECT * FROM service.users WHERE login='{str(login)}'")
        records = list(cursor.fetchall())
        if records:
            return render_template('registration.html', already='That login already exits in DB')
        else:
            cursor.execute('INSERT INTO service.users (full_name, login, password) VALUES (%s, %s, %s);',
                           (str(name), str(login), str(password)))
            conn.commit()
            return redirect('/login/')
    return render_template('registration.html')