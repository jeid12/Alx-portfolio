from flask import Flask, render_template, request, redirect, flash
from flask_mail import Mail, Message

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for flashing messages

# Configuration for Flask-Mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'niyokwizerajd123@gmail.com'
app.config['MAIL_PASSWORD'] = 'propane123'

mail = Mail(app)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        fname = request.form['fname']
        lname = request.form['lname']
        email = request.form['email']
        message = request.form['message']
        
        name = f"{fname} {lname}"
        
        # Compose the email
        msg = Message('Contact Form Submission',
                      sender='niyokwizerajd123@gmail.com',
                      recipients=['recipient@example.com'])
        msg.body = f"""
        From: {name} <{email}>
        
        Message:
        {message}
        """
        
        try:
            mail.send(msg)
            flash('Message sent successfully!', 'success')
        except Exception as e:
            flash(f'An error occurred: {e}', 'danger')
        
        return redirect('/contact')
    
    return render_template('contact.html')
@app.route('/send_email', methods=['POST'])
def send_email():
    fname = request.form['fname']
    lname = request.form['lname']
    email = request.form['email']
    message = request.form['message']
    
    msg = Message(subject='Contact Form Submission',
                  sender='niyokwizerajd123@gmail.com',
                  recipients=['niyokwizerajd123@gmail.com', 'tobiadesiyan007@gmail.com'])  # Enter your recipient email addresses
    
    msg.body = f'First Name: {fname}\nLast Name: {lname}\nEmail: {email}\nMessage: {message}'

    mail.send(msg)
    
    return 'Message sent successfully!'

if __name__ == '__main__':
    app.run(debug=True)
