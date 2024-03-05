from flask import Flask, request,redirect,url_for, render_template

app = Flask(__name__)

@app.route("/home")
def home():
    return render_template("home.html")

@app.route("/signup/")
def acctCreate():
    return render_template("create_account.html")
@app.route("/signupdata/", methods=['POST','GET'])
def signupdata():
    if request.method == 'POST':
        form_data = request.form
        return render_template("signupdata.html", form_data=form_data)
    if(request.method == 'GET'):
        return redirect(url_for('acctCreate'))

#@app.route("/<name>")
#def userName(name):
#    return f"hello {name }!"

@app.route("/admin/")
def admin():
    return redirect(url_for("userName", name = "Admin"))

#@app.route('/imgUpload', methods=['POST'])
#def uploadImage():  # put application's code here
#   if 'file' not in request.files:
#        return "Please Upload an image"
#    file = request.files['file']
#        # Process the uploaded file here
#    return 'File uploaded successfully'


if __name__ == '__main__':
    app.run(debug= True)
