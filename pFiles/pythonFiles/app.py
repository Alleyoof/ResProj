from flask import Flask
app = Flask(__name__) # name for the Flask app (refer to output)
# running the server
@app.route("/", methods=['GET', 'POST', 'PUT']) # decorator
def home(): 
    return "Hello world!"
if __name__ == "__main__":
    app.run(debug = True)