from flask import Flask, render_template, request
import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        try:
            full_name = request.form.get('full_name')
            phone_number = request.form.get('phone_number')
            email = request.form.get('email')
            service_needed = request.form.get('service_needed')
            project_details = request.form.get('project_details')

            # Create email message
            message = MIMEMultipart()
            message['Subject'] = 'New Project Request'
            message['From'] = 'gowthamgowda414@gmail.com'
            message['To'] = 'gowthamgowda414@gmail.com'
            
            body = f"""
            New Project Request Details:
            
            Full Name: {full_name}
            Phone Number: {phone_number}
            Email: {email}
            Service Needed: {service_needed}
            Project Details: {project_details}
            """
            
            message.attach(MIMEText(body, 'plain'))

            # Send email
            password = os.environ.get('password')
            with smtplib.SMTP('smtp.gmail.com', 587) as server:
                server.starttls()
                server.login('gowthamgowda414@gmail.com', password) # type: ignore
                server.send_message(message)
            
            return render_template('contact.html', message='Your message has been sent successfully')
        
        except Exception as e:
            print(f"Error sending email: {e}")
            return render_template('contact.html', message='Sorry, there was an error sending your message. Please try again.')
    
    else:
        return render_template('contact.html')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/portfolio')
def portfolio():
    # Get all images from static/images folder
    image_folder = 'static/images'
    images = []
    
    if os.path.exists(image_folder):
        images = [f for f in os.listdir(image_folder) 
                 if f.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.webp'))]
    
    return render_template('portfolio.html', images=images)

@app.route('/ideas')
def ideas():
    return render_template('ideas.html')

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=False)
