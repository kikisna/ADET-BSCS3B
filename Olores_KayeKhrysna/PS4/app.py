from flask import Flask, render_template, request, redirect, url_for, session, flash
import mysql.connector
import hashlib

app = Flask(__name__)
app.secret_key = 'ADET' 

db_config = {
    'host': 'localhost',
    'user': 'root',  
    'password': '',  
    'database': 'adet'
}

@app.route('/', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        
        registration_data = {
            'first_name': request.form.get('first_name'),
            'middle_name': request.form.get('middle_name'),
            'last_name': request.form.get('last_name'),
            'contact_number': request.form.get('contact_number'),  
            'email': request.form.get('email'),
            'address': request.form.get('address'),
            'password': hashlib.sha256(request.form.get('password').encode()).hexdigest()  
        }

        try:
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor()

            
            cursor.execute("SELECT email FROM adet_user WHERE email = %s", (registration_data['email'],))
            if cursor.fetchone():
                flash("This email is already registered. Please use another email.", "error")
                return redirect(url_for('register'))

            
            sql = """
            INSERT INTO adet_user (first_name, middle_name, last_name, contact_number, email, address, password)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(sql, (
                registration_data['first_name'],
                registration_data['middle_name'],
                registration_data['last_name'],
                registration_data['contact_number'],  
                registration_data['email'],
                registration_data['address'],
                registration_data['password']
            ))
            conn.commit()
            cursor.close()
            conn.close()

            flash("Registered successfully!", "success")
            return redirect(url_for('success'))

        except mysql.connector.Error as err:
            flash(f"Error: {err}", "error")
            return redirect(url_for('register'))

    return render_template('registration.html')

@app.route('/success')
def success():
    return render_template('success.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = hashlib.sha256(request.form.get('password').encode()).hexdigest()  

        try:
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM adet_user WHERE email = %s AND password = %s", (email, password))
            user = cursor.fetchone()
            cursor.close()
            conn.close()

            if user:
                session['email'] = email  
                return redirect(url_for('dashboard'))
            else:
                flash("Invalid credentials. Please try again.", "danger")
                return redirect(url_for('login'))
        except mysql.connector.Error as err:
            flash(f"Error: {err}", "danger")
            return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'email' not in session:
        return redirect(url_for('login'))

    user_email = session['email']
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT first_name, middle_name, last_name, contact_number, email, address FROM adet_user WHERE email = %s", (user_email,))
        user = cursor.fetchone()
        cursor.close()
        conn.close()
    except mysql.connector.Error as err:
        return f"Error: {err}"

    return render_template('dashboard.html', user=user)

@app.route('/logout')
def logout():
    session.pop('email', None)  
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
