from flask import Flask, render_template, request, flash, redirect, url_for, json
import requests

app = Flask(__name__)

app.config['SECRET_KEY'] = 'sam'

def is_human(captcha_response):
    """ Validating reCAPTCHA response from Google server.
        Returns True if captcha test passed for the submitted form, else returns False.
    """
    secret = "6LdZaDMqAAAAADsvPKFM-kCmJ-a3lXDla17HFZ9q"
    payload = {'response': captcha_response, 'secret': secret}
    response = requests.post("https://www.google.com/recaptcha/api/siteverify", data=payload)
    response_text = json.loads(response.text)
    return response_text['success']

@app.route("/", methods=["GET", "POST"])
def contact():
    sitekey = "6LdZaDMqAAAAABz79h8nh8g0Qy93YRXioVc6l17m"
    
    if request.method == "POST":
        name = request.form.get('name')
        email = request.form.get('email')
        msg = request.form.get('message')
        captcha_response = request.form.get('g-recaptcha-response')
        
        if name is None or email is None or captcha_response is None:
            flash("Please fill out all fields and complete the reCAPTCHA.", "warning")
            return redirect(url_for('contact'))
        
        if is_human(captcha_response):
            status = f"Details submitted successfully. Name: {name}, Email: {email}, Message: {msg}"
            flash(status, "success")
        else:
            flash("Sorry! Please check 'I'm not a robot'.", "danger")
        
        return redirect(url_for('contact'))
    
    return render_template("contact.html", sitekey=sitekey)

if __name__ == '__main__':
    app.run(debug=True)
