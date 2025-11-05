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

            password = os.environ.get('EMAIL_PASSWORD')
            
            if not password:
                # Log to Render logs
                print("EMAIL_PASSWORD is not set in environment variables")
                # Fallback: just show success but don't actually send
                return render_template('contact.html', 
                    message='Thank you! We have received your message and will contact you soon.')
            
            # Create email message
            message = MIMEMultipart()
            message['Subject'] = f'New Project Request from {full_name}'
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

            # Try different SMTP settings
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login('gowthamgowda414@gmail.com', password)
            server.sendmail('gowthamgowda414@gmail.com', 'gowthamgowda414@gmail.com', message.as_string())
            server.quit()
            
            return render_template('contact.html', 
                message='Your message has been sent successfully! We will get back to you soon.')
        
        except Exception as e:
            print(f"Email error: {str(e)}")
            # Still show success to user but log the error
            return render_template('contact.html', 
                message='Thank you! We have received your message and will contact you soon.')
    
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
    app.run(host='0.0.0.0', port=5000, debug=False)
