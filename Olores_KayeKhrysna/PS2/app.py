from flask import Flask, render_template, request, redirect, jsonify
import json

app = Flask(__name__)

def save_to_json(data):
    try:
        with open('data.json', 'r') as file:
            existing_data = json.load(file)
    except FileNotFoundError:
        existing_data = []

    existing_data.append(data)

    with open('data.json', 'w') as file:
        json.dump(existing_data, file, indent=4)

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

    save_to_json(user_data)

    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
