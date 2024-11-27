
from flask import Flask, render_template, request, redirect, url_for
import cx_Oracle

# Create Flask app
app = Flask(__name__)

# Oracle DB connection details
DB_USER = 'stbl_user'
DB_PASSWORD = 'stbl_password'
DB_DSN = '140.245.114.177:1521/cdb1'

# Function to get Oracle DB connection
def get_db_connection():
    connection = cx_Oracle.connect(DB_USER, DB_PASSWORD, DB_DSN)
    return connection

# Home route that displays the table data
@app.route('/')
def index():
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM STBL_TABLE')
    data = cursor.fetchall()
    cursor.close()
    connection.close()
    return render_template('index.html', data=data)

# Add new record route
@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        join_date = request.form['join_date']

        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute('''
            INSERT INTO STBL_TABLE (NAME, AGE, JOIN_DATE)
            VALUES (:name, :age, TO_DATE(:join_date, 'YYYY-MM-DD'))
        ''', {'name': name, 'age': age, 'join_date': join_date})
        connection.commit()
        cursor.close()
        connection.close()

        return redirect(url_for('index'))

    return render_template('add.html')

# Edit record route
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    connection = get_db_connection()
    cursor = connection.cursor()
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        join_date = request.form['join_date']

        cursor.execute('''
            UPDATE STBL_TABLE
            SET NAME = :name, AGE = :age, JOIN_DATE = TO_DATE(:join_date, 'YYYY-MM-DD')
            WHERE ID = :id
        ''', {'name': name, 'age': age, 'join_date': join_date, 'id': id})
        connection.commit()
        cursor.close()
        connection.close()

        return redirect(url_for('index'))

    cursor.execute('SELECT * FROM STBL_TABLE WHERE ID = :id', {'id': id})
    data = cursor.fetchone()
    cursor.close()
    connection.close()

    return render_template('edit.html', data=data)

# Delete record route
@app.route('/delete/<int:id>')
def delete(id):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute('DELETE FROM STBL_TABLE WHERE ID = :id', {'id': id})
    connection.commit()
    cursor.close()
    connection.close()

    return redirect(url_for('index'))

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
