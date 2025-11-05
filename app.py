from flask import Flask, render_template, request
import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)


@app.route('/contact')
def contact():
    success = request.args.get('success')
    message = "Your message has been sent successfully! We'll get back to you soon." if success else None
    return render_template('contact.html', message=message)

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
