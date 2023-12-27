from flask import Flask, render_template, request, send_from_directory
import random
import string
import re
import os
app = Flask(__name__)



def generate_custom_password(length, num_alphabets, num_uppercase, num_lowercase, num_digits, num_special, user_input_word):
    # Ensure the sum of individual criteria does not exceed the total length
    if num_alphabets + num_digits + num_special > length:
        return "Invalid input: Sum of alphabets, digits, and special characters exceeds the total length."

    # Initialize a list to store characters
    password_chars = []

    # Check conditions for the user input word
    if user_input_word:
        # Count the number of uppercase, lowercase, digits, and special characters in the user input word
        word_uppercase = sum(1 for char in user_input_word if char.isupper())
        word_lowercase = sum(1 for char in user_input_word if char.islower())
        word_digits = sum(1 for char in user_input_word if char.isdigit())
        word_special = sum(1 for char in user_input_word if char in '!@#$%^&*()_+{}|<>?')

        # Add the user input word to the password
        password_chars += list(user_input_word)

        # Concatenate uppercase letters after the word
        password_chars += random.sample(string.ascii_uppercase, min(num_uppercase - word_uppercase, length - len(password_chars)))

        # Concatenate lowercase letters after the word
        password_chars += random.sample(string.ascii_lowercase, min(num_lowercase - word_lowercase, length - len(password_chars)))

        # Concatenate digits after the word
        password_chars += random.sample(string.digits, min(num_digits - word_digits, length - len(password_chars)))

        # Concatenate special characters after the word
        password_chars += random.sample('!@#$%^&*()_+{}|<>?', min(num_special - word_special, length - len(password_chars)))

    else:
        # Concatenate uppercase letters
        password_chars += random.sample(string.ascii_uppercase, min(num_uppercase, length - len(password_chars)))

        # Concatenate lowercase letters
        password_chars += random.sample(string.ascii_lowercase, min(num_lowercase, length - len(password_chars)))

        # Concatenate digits
        password_chars += random.sample(string.digits, min(num_digits, length - len(password_chars)))

        # Concatenate special characters
        password_chars += random.sample('!@#$%^&*()_+{}|<>?', min(num_special, length - len(password_chars)))

    # Shuffle the characters to create a random password
    # random.shuffle(password_chars)

    # Join the characters to form the password
    password = ''.join(password_chars)

    return password


def check_password_strength(password):
    # Minimum length requirement
    if len(password) < 8:
        return "Weak: Password should be at least 12 characters long."

    # Check for uppercase letters
    if not re.search("[A-Z]", password):
        return "Weak: Password should contain at least one uppercase letter."

    # Check for lowercase letters
    if not re.search("[a-z]", password):
        return "Weak: Password should contain at least one lowercase letter."

    # Check for numbers
    if not re.search("[0-9]", password):
        return "Weak: Password should contain at least one digit."

    # Check for special characters from the predefined set
    if not re.search("[!@#$%^&*()_+{}|<>?]", password):
        return "Weak: Password should contain at least one special character."

    # If the password passes all checks
    return "Strong: Password meets the criteria."

@app.route('/')
def home():
    return render_template('home.html')


@app.route('/contact_us')
def contact_us():
    return render_template('contact_us.html')

@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        message = request.form.get('message')

        # Writing user input to a text file
        with open('user_inputs.txt', 'a') as file:
            file.write(f"Name: {name}\nEmail: {email}\nPhone: {phone}\nMessage: {message}\n\n")

        return render_template('contact_us.html', name=name)

@app.route('/about_us')
def about_us():

    profile_image_path = os.path.join(os.getcwd(),"..","static","mitul.jpg")
    profile_image_path = os.path.join(os.getcwd(),"..","static","shashank.jpg")
    profile_image_path = os.path.join(os.getcwd(),"..","static","mitali.jpg")
    profile_image_path = os.path.join(os.getcwd(),"..","static","kriti.jpg")
    return render_template('about_us.html', profile_image_path=profile_image_path)

@app.route('/image/<filename>')
def get_image(filename):
    images_directory = os.path.join(os.getcwd(), 'static')  
    return send_from_directory(images_directory, filename)

@app.route('/static/<path:filename>')
def static_files(filename):
    print("static hit")
    return send_from_directory('static', filename)

@app.route('/password_tool')
def tools():
    return render_template('password_tool.html', generated_password=None, strength_result=None)

@app.route('/generate_password', methods=['POST'])
def generate_password():
    length = int(request.form['length'])
    num_alphabets=int(request.form['num_alphabets'])
    num_uppercase = int(request.form['num_uppercase'])
    num_lowercase = int(request.form['num_lowercase'])
    num_digits = int(request.form['num_digits'])
    num_special = int(request.form['num_special'])
    user_input_word = request.form['user_input_word']

    generated_password = generate_custom_password(length, num_alphabets, num_uppercase, num_lowercase, num_digits, num_special, user_input_word)

    return render_template('password_tool.html', generated_password=generated_password, strength_result=None)

@app.route('/check_password_strength', methods=['POST'])
def check_password_strength_route():
    user_password = request.form['password']
    strength_result = check_password_strength(user_password)
    return render_template('password_tool.html', generated_password=None, strength_result=strength_result)

def get_user_input(remaining_lengths):
    user_input = {}
    
    for category, remaining_length in remaining_lengths.items():
        user_input[category] = int(request.form[category])

    user_input['word'] = request.form['user_input_word']

    return user_input

if __name__ == '__main__':
    app.run(debug=True)
