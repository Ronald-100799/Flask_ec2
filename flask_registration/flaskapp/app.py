from flask import Flask, render_template, request, redirect, url_for, flash
from flaskext.mysql import MySQL
import pymysql

app = Flask(__name__)
app.secret_key = "Cairocoders-Ednalan"
  
mysql = MySQL()
import aws_credentials as rds  
# MySQL configurations
conn = pymysql.connect(
        host= rds.host, #endpoint link
        port = rds.port, # 3306
        user = rds.user, # admin
        password = rds.password, #adminadmin
        db = rds.db, #test
        
        )
@app.route('/')
def Index():
    return render_template('home2.html')

@app.route('/Index1')
def Index1():
    # conn = mysql.connect()
    cur = conn.cursor(pymysql.cursors.DictCursor)
    cur.execute('SELECT * FROM registration')
    data = cur.fetchall()
  
    cur.close()
    return render_template('reg.html', registration = data)

@app.route('/Index2')
def Index2():
   # conn = mysql.connect()
    cur = conn.cursor(pymysql.cursors.DictCursor)
    cur.execute('SELECT * FROM registration')
    data = cur.fetchall()
  
    cur.close()
    return render_template('index.html',registration = data)

@app.route('/add_registration', methods=['POST'])
def add_registration():
    #conn = mysql.connect()
    cur = conn.cursor(pymysql.cursors.DictCursor)
    if request.method == 'POST':
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        #age = request.form['age']
        email = request.form['email']
        gender = request.form['optradio']
        address = request.form['address']
        date = request.form['date']
        sem = request.form['sem']
        rolno = request.form['rolno']
        phone = request.form['phone']
        course = request.form['course']
        cur.execute("INSERT INTO registration (firstname,lastname,date,gender,rolno,email,address,phone,course,sem) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", (firstname,lastname,date,gender,rolno,email,address,phone,course,sem))
        conn.commit()
        flash('Information Added successfully')
        return redirect(url_for('Index1'))
 
@app.route('/edit/<id>', methods = ['POST', 'GET'])
def get_registration(id):
    #conn = mysql.connect()
    cur = conn.cursor(pymysql.cursors.DictCursor)
  
    cur.execute('SELECT * FROM registration WHERE id = %s', (id))
    data = cur.fetchall()
    cur.close()
    print(data[0])
    return render_template('edit.html', registration = data[0])
 
@app.route('/update/<id>', methods=['POST'])
def update_registration(id):
    if request.method == 'POST':
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        #age = request.form['age']
        email = request.form['email']
        gender = request.form['optradio']
        address = request.form['address']
        date = request.form['date']
        sem = request.form['sem']
        rolno = request.form['rolno']
        phone = request.form['phone']
        course = request.form['course']
        #conn = mysql.connect()
        cur = conn.cursor(pymysql.cursors.DictCursor)
        cur.execute("""
            UPDATE registration
            SET firstname = %s,
                lastname = %s,
                date = %s,
                gender = %s,
                rolno = %s,
                email = %s,
                address = %s,
                phone = %s,
                course = %s,
                sem = %s
            WHERE id = %s
        """, (firstname,lastname,date,gender,rolno,email,address,phone,course,sem,id))
        flash('Info Updated Successfully')
        conn.commit()
        return redirect(url_for('Index2'))
 
@app.route('/delete/<string:id>', methods = ['POST','GET'])
def delete_registration(id):
    #conn = mysql.connect()
    cur = conn.cursor(pymysql.cursors.DictCursor)
  
    cur.execute('DELETE FROM registration WHERE id = {0}'.format(id))
    conn.commit()
    flash('Info Removed Successfully')
    return redirect(url_for('Index2'))
 
# starting the app
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True)