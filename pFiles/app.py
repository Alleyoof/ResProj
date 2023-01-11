from flask import Flask, render_template
app = Flask(__name__) # name for the Flask app (refer to output)
# running the server
googleClientId = '998511586381-jir9hao48i7ua4ukmkd3ln8bo4k6n4g8.apps.googleusercontent.com'
googleSecret = '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'
@app.route("/", methods=['GET', 'POST', 'PUT']) 
def login(): 
    return render_template('loginPage.html')

@app.route("/home", methods=['GET', 'POST', 'PUT']) # decorator
def home(): 
    return "!"
if __name__ == "__main__":
    app.run(debug = True)