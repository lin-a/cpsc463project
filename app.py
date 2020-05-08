from flask import Flask, redirect, render_template, request, flash, url_for, session
from flask_mysqldb import MySQL
import yaml

# Init
app = Flask(__name__)

# Configure db. DO NOT TOUCH
# change in db.yaml instead
db = yaml.load(open('db.yaml'))
app.config['SECRET_KEY'] = db['secret_key']
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']

mysql = MySQL(app)


# dealers
# 0 dealer_id
# 1 dealer_name
# 2 dealer_space
# 3 dealer_password
#
# cars
# 0 cars_id
# 1 car_model
# 2 cars_variant
# 3 dealer_dealer_id


# login
@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        username = request.form['username']
        password = request.form['password']
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM dealers WHERE dealer_name=(%s)", (username,))
        dealer = cur.fetchone()
        cur.close()
        if dealer is not None and len(dealer) > 0:
            if password == dealer[3]:  # 3 is dealer_password
                session['name'] = username
                session['id'] = dealer[0]
                return redirect('home')
            else:
                flash('Wrong login password', 'danger')
                return render_template('login.html')
        else:
            flash('Wrong login name', 'danger')
            return render_template('login.html')


@app.route('/logout')
def logout():
    session.clear()
    return redirect('login')


# register
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        username = request.form['username']
        password = request.form['password']
        space = request.form['space']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO dealers(dealer_name, dealer_password, dealer_space) VALUES(%s, %s, %s)",
                    (username, password, space))
        mysql.connection.commit()
        # get user id and put in session
        cur.close()
        return redirect(url_for('login'))


# main page for displaying table
# change to /user/<uid>
@app.route('/home')
def home():
    cur = mysql.connection.cursor()
    # cur.execute("SELECT cars_id, car_model, car_variant FROM dealers, cars WHERE dealers.id=cars.id")
    cur.execute("""SELECT cars_id, car_model, cars_variant
    FROM cars WHERE dealer_dealer_id = %s""", (session['id'],))
    data = cur.fetchall()
    cur.close()
    return render_template('index.html', cars=data)


# for ordering cars. INSERT
# check SELECT COUNT(*) FROM cars
# match the count to space #, if over, then reject
@app.route('/insert', methods=['POST'])
def insert():
    if request.method == "POST":
        model = request.form['model']
        variant = request.form['variant']
        cur = mysql.connection.cursor()
        cur.execute("SELECT dealer_space FROM dealers WHERE dealer_id = %s", (session['id'],))
        space = cur.fetchone()  # this max parking space
        cur.execute("SELECT COUNT(*) FROM cars WHERE dealer_dealer_id = %s", (session['id'],))
        count = cur.fetchone()  # number of cars the dealer has
        if count[0] < space[0]:  # if count is less than space, ex. 9 < 10, then it can still put in 1 more
            cur.execute("""INSERT INTO cars(car_model, cars_variant, dealer_dealer_id) VALUES(%s, %s, %s)""",
                        (model, variant, session['id']))
            mysql.connection.commit()
            flash('Data inserted successfully', 'success')
        else:
            flash('Insert failed. Out of parking space', 'danger')
        cur.close()
        return redirect(url_for('home'))


# edit car info(optional). UPDATE
# this isn't used because it doesn't make sense to
# edit car from a model/variant to another
# the app is for ordering NEW car
@app.route('/update', methods=['POST', 'GET'])
def update():
    if request.method == 'POST':
        cid = request.form['id']
        model = request.form['model']
        variant = request.form['variant']
        cur = mysql.connection.cursor()
        cur.execute("""
               UPDATE cars
               SET car_model=%s, cars_variant=%s
               WHERE cars_id=%s
            """, (model, variant, cid))
        mysql.connection.commit()
        flash('Data updated successfully', 'success')
        cur.close()
        return redirect(url_for('home'))


# remove car maybe use for sold car. DELETE
@app.route('/delete/<string:cid>', methods=['GET'])
def delete(cid):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM cars WHERE cars_id=%s", (cid,))
    mysql.connection.commit()
    flash('Data deleted successfully', 'success')
    cur.close()
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)
