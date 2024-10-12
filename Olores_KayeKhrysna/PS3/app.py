from flask import Flask, render_template, request
import mysql.connector
import os

app = Flask(__name__)

app.secret_key = os.urandom(24)  

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'adet'
}

def save_to_mysql(user_data):
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        query = """
        INSERT INTO adet_user (first_name, middle_name, last_name, contact_number, email, address) 
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        data = (
            user_data['First Name'],
            user_data['Middle Name'],
            user_data['Last Name'],
            user_data['Contact Number'],
            user_data['Email Address'],
            user_data['Address']
        )

        cursor.execute(query, data)
        conn.commit()

    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

@app.route('/')
def registration_form():
    return render_template('registration.html')

@app.route('/register', methods=['POST'])
def register():
    
    first_name = request.form['first_name']
    middle_name = request.form['middle_name']
    last_name = request.form['last_name']
    contact_number = request.form['contact_number']
    email = request.form['email']
    address = request.form['address']

    user_data = {
        'First Name': first_name,
        'Middle Name': middle_name,
        'Last Name': last_name,
        'Contact Number': contact_number,
        'Email Address': email,
        'Address': address
    }

    save_to_mysql(user_data)

    return render_template('success.html') 

if __name__ == '__main__':
    app.run(debug=True)
