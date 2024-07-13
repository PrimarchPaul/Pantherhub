from flask import Flask, request, redirect, url_for, render_template, session, jsonify
from flask_socketio import SocketIO, emit
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from pyzipcode import ZipCodeDatabase
# from waitress import serve
from datetime import datetime
import re
import os
import mysql.connector


app = Flask(__name__, template_folder=os.path.join(os.getcwd(), "templates"))
secret_key = os.urandom(24)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['SECRET_KEY'] = secret_key
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg'}
zcdb = ZipCodeDatabase()


# checks if the file given is allowed within the list

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


try:

    db_config = {
        'host': 'localhost',
        'user': 'root',
        'password': 'password',
        'database': 'pantherhub',
        'auth_plugin': 'mysql_native_password'
    }
except mysql.connector.Error as e:
    print(f"Error connecting to MySQL: {e}")


# -----------------------------------------------------------------------------------------------------------------------
# home function
# -----------------------------------------------------------------------------------------------------------------------

@app.route("/home/", methods=["GET", "POST"])
def home():
    return render_template("index.html")


# -----------------------------------------------------------------------------------------------------------------------
# Login function
# -----------------------------------------------------------------------------------------------------------------------

@app.route("/login/", methods=["GET", "POST"])
def login_page():
    if request.method == "POST":

        # connect to mysql database

        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # Correctly executing the query with a parameter
        cursor.execute("SELECT userPassword FROM userLogin WHERE userName = %s", (request.form["username"],))
        # Fetching the result
        password_from_db = cursor.fetchone()  # Use fetchone to get the first result

        # Close cursor and connection
        cursor.close()
        conn.close()
        login_password = request.form["password"]

        # Check if we got a result and if the password matches
        if check_password_hash(password_from_db[0], login_password):
            session['user'] = request.form["username"]
            return redirect(url_for("browse"))
        else:
            # Pass an error message to the render_template function
            return render_template("login.html", error="Username or Password did not match")

    # If it's a GET request or if no form has been submitted yet, just show the login page
    return render_template("login.html")


# -----------------------------------------------------------------------------------------------------------------------
# Browse function
# -----------------------------------------------------------------------------------------------------------------------

@app.route("/browse/", methods=["GET", "POST"])
def browse():
    if 'user' in session:
        # establish connection to db

        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)

        # get the userID of the current session user
        username = session['user']

        # find the profiles that have not been seen by the current session user using the session username

        cursor.execute(""" SELECT ua.*
                                    FROM useraccount ua
                                    WHERE ua.username != %s
                                    AND NOT EXISTS (
                                        SELECT 1
                                        FROM userMatch um
                                        WHERE um.userName = ua.userName AND um.username = %s
                                    )
                                    ORDER BY RAND()
                                    LIMIT 1;
                                    ;""", (username, username))
        profile = cursor.fetchone()
        print(profile)
        print(username)

        # fetch the potential match's PFP located in a different table and set it to dictionary

        cursor.execute("""SELECT PhotoDirectory FROM userPhoto WHERE userName = %s""", (profile["userName"],))

        profilePhoto = cursor.fetchone()

        if profilePhoto:
            profile['userPFP'] = (f'/static/uploads/{profilePhoto.get("PhotoDirectory")}')
        else:
            profile['userPFP'] = '/static/images/test.png'

        current_date = datetime.now()
        user_dob_split = profile['userDOB'].split('-')
        user_dob = datetime(int(user_dob_split[0]), int(user_dob_split[1]), int(user_dob_split[2]))
        userAge = int((current_date - user_dob).days / 365.25)
        profile['userAge'] = str(userAge)
        profile['userZip'] = zcdb[int(profile['userZip'])].city


        if profile:
            return render_template('browse.html', profile=profile)
        else:
            return "No more profiles to show."

    return redirect(url_for('login_page'))


# -----------------------------------------------------------------------------------------------------------------------
# Interest function
# -----------------------------------------------------------------------------------------------------------------------


@app.route('/interest/<profile_id>/<action>', methods=['POST'])
def interest(profile_id, action):
    user_id = session.get('user')  # Ensure you have the user's ID or username in the session
    if not user_id:
        return jsonify({'error': 'User not logged in'}), 403

        # Convert action into a boolean value
    is_interested = action == 'interested'

    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)

        print("session username is ", user_id)

        cursor.execute("SELECT * FROM userMatch WHERE username = %s AND user1name = %s", (user_id, profile_id))
        existing_record = cursor.fetchone()

        if not existing_record:
            insert_sql = "INSERT INTO userMatch (username, user1name, userInterest) VALUES (%s, %s, %s)"
            cursor.execute(insert_sql, (user_id, profile_id, is_interested))
            conn.commit()
        else:
            print("Record already exists, not inserting again.")

        search = True
        while search:
            cursor.execute(""" SELECT ua.*
                                               FROM useraccount ua
                                               WHERE ua.username != %s
                                               AND NOT EXISTS (
                                                   SELECT 1
                                                   FROM userMatch um
                                                   WHERE um.userName = ua.userName AND um.username = %s
                                               )
                                               ORDER BY RAND()
                                               LIMIT 1;
                                               ;""", (user_id, user_id))

            profile = cursor.fetchone()
            user1name = profile['userName']

            if not profile:
                return jsonify({'success': True, 'message': 'No more profiles to show.'})

            seen_user_sql = "SELECT * from userMatch WHERE username = %s and user1name = %s"
            cursor.execute(seen_user_sql, (user_id, user1name))
            seen_user = cursor.fetchone()

            if seen_user:
                continue

            search = False

        # fetch the potential match's PFP located in a different table and set it to dictionary

        cursor.execute("""SELECT PhotoDirectory FROM userPhoto WHERE userName = %s""", (profile["userName"],))

        profilePhoto = cursor.fetchone()

        if profilePhoto:
            profile['userPFP'] = (f'/static/uploads/{profilePhoto.get("PhotoDirectory")}')
        else:
            profile['userPFP'] = '/static/images/test.png'

        current_date = datetime.now()
        user_dob_split = profile['userDOB'].split('-')
        user_dob = datetime(int(user_dob_split[0]), int(user_dob_split[1]), int(user_dob_split[2]))
        userAge = int((current_date - user_dob).days / 365.25)
        profile['userAge'] = str(userAge)
        profile['userZip'] = zcdb[int(profile['userZip'])].city

        return jsonify({'success': True, 'newProfile': profile})

    except mysql.connector.Error as err:
        print("Error: ", err)
        conn.rollback()
        return jsonify({'error': 'Database operation failed'}), 500
    finally:
        cursor.close()
        conn.close()


# -----------------------------------------------------------------------------------------------------------------------
# redirect function
# -----------------------------------------------------------------------------------------------------------------------


@app.route('/redirect/<action>', methods=['POST'])
def redirection(action):
    # Based on the action, decide the redirection URL
    redirect_url = '/home'
    if action == 'change_email':
        redirect_url = '/changeemail'
    elif action == 'to_settings':
        redirect_url = '/settings/'
    elif action == 'to_browse':
        redirect_url = '/browse/'
    if action == 'edit_profile':
        redirect_url = '/editprofile'
    elif action == "to_browse":
        redirect_url = '/browse/'
    elif action == "delete_account":
        redirect_url = '/deleteaccount'
    elif action == "login":
        redirect_url = '/login'
    elif action == "create_account":
        redirect_url = '/signup'
    elif action == "profile":
        redirect_url = '/profile'
    elif action == "home":
        redirect_url = '/home'
    elif action == "logout":
        session.clear()
        print("session data cleared")
        redirect_url = '/home'
    elif action == "to_messaging":
        redirect_url = '/messages'


        # Return a JSON response with the redirection URL
    return jsonify({"redirect": True, "redirectUrl": redirect_url})

    # Return a JSON response with the redirection URL



# -----------------------------------------------------------------------------------------------------------------------
# Messages function
# -----------------------------------------------------------------------------------------------------------------------


@app.route("/messages/")
def messages():
    return render_template("messaging.html")


# -----------------------------------------------------------------------------------------------------------------------
#settings function
# -----------------------------------------------------------------------------------------------------------------------


@app.route("/settings/", methods=["GET", "POST"])
def settings():
    if "user" in session:
        return render_template("settings.html")
    else:
        return render_template("login.html")


# -----------------------------------------------------------------------------------------------------------------------
# Delete account function
# -----------------------------------------------------------------------------------------------------------------------


@app.route('/deleteaccount/', methods=['GET', 'POST'])
def delete_account():
    if 'user' not in session:
        return redirect(url_for('login_page'))

    if request.method == 'POST':
        userinfo = request.form
        username = userinfo['username']
        user_password = userinfo['password']
        user_confirmpass = userinfo['confirmpass']
        errors = {}

        try:
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor()

            user_info_sql = "SELECT userPassword FROM userLogin WHERE userName = %s"

            cursor.execute(user_info_sql, (username,))
            user_info = cursor.fetchone()

            if user_info is None:
                errors["username_err"] = "This user does not exist"
                return render_template("change_email.html", errors=errors)

            if user_info[0] != user_password:
                errors["email_err"] = "Password does not match user's current password"
                return render_template("change_email.html", errors=errors)

            if user_info[0] == user_password and user_confirmpass != user_info[0]:
                errors["confirmpass_err"] = "Passwords do not match"
                return render_template("change_email.html", errors=errors)

            delete_account = "DELETE FROM userAccount WHERE username = %s"
            cursor.execute(delete_account, (username,))
            conn.commit()
            session.clear()
            return render_template("login.html", delete_success=True)

        except mysql.connector.Error as e:
            print("error:", e)
            errors["server_err"] = "There is an issue with the server right now, come try another time"
            conn.rollback()
            return render_template("change_email.html", errors=errors)
        finally:
            cursor.close()
            conn.close()

    return render_template("delete_account.html")


# -----------------------------------------------------------------------------------------------------------------------
# new account function
# -----------------------------------------------------------------------------------------------------------------------


@app.route("/signup/", methods=["GET", "POST"])
def new_account():
    if request.method == "POST":
        new_user_info = request.form
        print(new_user_info)

        '''Open connection to database
            since we cannot physically add information into database, 
            object cursor is used to locate and update information in database
         '''

        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        errors = {}

        # error form checking
        # password checking if it does not match or does not meet requirements

        requirement_pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$'

        if new_user_info["password"] != new_user_info["confirm_password"]:
            errors["confirm_err"] = "Passwords do not Match"

        if not re.match(requirement_pattern, new_user_info["password"]):
            errors["requirement_err"] = ("Password does not meet requirement. "
                                         "Must be 8 characters long, contain at least one lowercase and uppercase letter"
                                         ", one number, one of these symbols @$!%*?&")

        # username not taken verification

        cursor.execute("SELECT userName FROM userAccount WHERE userName = %s", (new_user_info["username"],))
        db_user_name = cursor.fetchone()

        if db_user_name and db_user_name[0] == new_user_info["username"]:
            errors["username_err"] = "Username is already taken"

        # email not taken verification

        cursor.execute("SELECT userEmail FROM userAccount WHERE userEmail = %s", (new_user_info["email"],))
        db_user_email = cursor.fetchone()

        print("email from db", db_user_email)

        if db_user_email and db_user_email[0] == new_user_info["email"]:
            errors["email_err"] = "Email is already taken"

        # age verification

        today = datetime.today()
        user_dob = request.form["dob"]
        user_dob_obj = datetime.strptime(user_dob, "%Y-%m-%d")
        user_age = today.year - user_dob_obj.year
        if (today.month, today.day) < (user_dob_obj.month, user_dob_obj.day):
            user_age -= 1

        if user_age < 18:
            errors["age_err"] = "You must be 18 years or older to sign up for Pantherhub"

        # if any errors occur, re-render template with errors given

        if errors:
            return render_template("account_creation.html", errors=errors)

        '''get html form data'''

        username = new_user_info["username"]
        password = generate_password_hash(new_user_info["password"])
        email = new_user_info["email"]
        userFname = new_user_info["firstname"]
        userLname = new_user_info["lastname"]
        userPID = new_user_info["Panther ID"]
        userphone = new_user_info["phonenumber"]
        userDOB = new_user_info["dob"]
        userGender = new_user_info["gender"]
        userPreference = new_user_info["sexual_preference"]
        userZip = new_user_info["zip_code"]
        userState = new_user_info["State"]

        try:

            cursor.execute("INSERT INTO useraccount (userName, userEmail, userFName,"
                           "userLName,userPID,userPhoneNumber,userDOB,userGender,userPreference,userZIP,userState) "
                           "VALUES (%s, %s,%s, %s, %s,%s,%s, %s,%s,%s,%s)",
                           (username, email, userFname, userLname, userPID, userphone, userDOB, userGender,
                            userPreference,
                            userZip, userState))
            conn.commit()
            cursor.execute("INSERT INTO userLogin (userName, userEmail, userPassword) VALUES (%s, %s, %s)",
                           (username, email, password))
            conn.commit()
        except mysql.connector.Error as err:
            print("Error: ", err)
            conn.rollback()
            errors["signup_err"] = (
                "There has been an issue with signing up. Please contact your administrator and try "
                "again at a different time.")
            return render_template("account_creation.html", errors=errors)
        finally:
            cursor.close()
            conn.close()
            session["user"] = username
        return redirect(url_for("browse"))

    return render_template("account_creation.html")


# -----------------------------------------------------------------------------------------------------------------------
# Profile function
# -----------------------------------------------------------------------------------------------------------------------


@app.route("/profile/")
def profile():


    if 'user' not in session:
        return redirect(url_for("login_page"))

    profile = None
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)

    try:

        sql = "SELECT * FROM useraccount WHERE userName = %s"
        cursor.execute(sql, (session['user'],))
        profile = cursor.fetchone()
        current_date = datetime.now()
        user_dob_split = profile['userDOB'].split('-')
        user_dob = datetime(int(user_dob_split[0]), int(user_dob_split[1]), int(user_dob_split[2]))
        userAge = int((current_date - user_dob).days / 365.25)
        profile['userAge'] = str(userAge)
        profile['userZip'] = zcdb[int(profile['userZip'])].city

        cursor.execute("""SELECT PhotoDirectory FROM userPhoto WHERE userName = %s""", (profile["userName"],))
        profilePhoto = cursor.fetchone()

        if profilePhoto:
            profile['userPFP'] = f'/static/uploads/{profilePhoto.get("PhotoDirectory")}'
        else:
            profile['userPFP'] = f'/static/images/test.png'
        print(profile)


    except mysql.connector.Error as err:
        print("Error: ", err)
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

    if profile:
        return render_template("profile.html", profile=profile)
    else:

        return "No profile found or an error occurred"


# -----------------------------------------------------------------------------------------------------------------------
# Edit Profile function
# -----------------------------------------------------------------------------------------------------------------------


@app.route("/editprofile/", methods=["GET", "POST"])
def editprofile():

    if 'user' not in session:
        return redirect(url_for("login_page"))

    if request.method == "POST":

        # Accessing file differently from other form data
        profile_img = request.files['img']
        error = {}


        # get request form and establish valid columns to prevent SQL injection

        user_edit_info = request.form

        valid_columns = ['userFName', 'userLName', 'userPreference', 'userPhoneNumber', 'userZip', 'userPID', "userBio",
                         "userState", "userGender"]

        # Connect to your database
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        try:
            for key in user_edit_info:
                if key in valid_columns and user_edit_info[key] != '':
                    sql = "UPDATE useraccount set {} = %s WHERE userName = %s".format(key)
                    cursor.execute(sql, (user_edit_info[key], session['user']))

            conn.commit()
            if profile_img and profile_img.filename:

                timestamp = datetime.now()
                correct_file = profile_img.filename.split(".")
                if correct_file[1] not in ALLOWED_EXTENSIONS:
                    error['file_incorrect'] = "Invalid File, accepted are", ALLOWED_EXTENSIONS
                    return render_template('edit_profile.html', error = error)

                print(correct_file)
                print("before secure", profile_img.filename)
                filename = secure_filename(profile_img.filename)
                print("after secure", filename)
                path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                profile_img.save(path)

                existingpfp_sql = "SELECT * FROM userPhoto WHERE userName = %s"
                cursor.execute(existingpfp_sql, (session['user'],))
                existingpfp = cursor.fetchone()

                if existingpfp:
                    update = "UPDATE userPhoto set PhotoDirectory = %s, uploadDate = %s WHERE userName = %s"
                    cursor.execute(update,(filename, timestamp, session['user']))
                else:
                    insert = "INSERT INTO userPhoto (userName, PhotoDirectory, uploadDate) VALUES (%s, %s, %s)"
                    cursor.execute(insert, (session['user'], filename, timestamp))

                conn.commit()

                return render_template("edit_profile.html", edit_success=True)

        except mysql.connector.Error as err:
            print("Error: ", err)
            conn.rollback()
        finally:
            cursor.close()
            conn.close()

    return render_template("edit_profile.html")


# -----------------------------------------------------------------------------------------------------------------------
# Change Email
# -----------------------------------------------------------------------------------------------------------------------


@app.route("/changeemail/", methods=["GET", "POST"])
def change_email():
    if 'user' not in session:
        return redirect(url_for('login_page'))

    if request.method == 'POST':
        userinfo = request.form
        username = userinfo['username']
        user_old_email = userinfo['oldemail']
        user_new_email = userinfo['newemail']
        errors = {}

        try:
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor()

            user_info_sql = "SELECT userEmail FROM userAccount WHERE userName = %s"
            new_email_sql = "SELECT userEmail FROM userAccount WHERE userEmail = %s"
            cursor.execute(user_info_sql, (username,))
            user_info = cursor.fetchone()
            cursor.execute(new_email_sql, (user_new_email,))
            new_email_existed = cursor.fetchone()

            if user_info is None:
                errors["username_err"] = "This user does not exist"
                return render_template("change_email.html", errors=errors)

            if user_info[0] != user_old_email:
                errors["email_err"] = "Email does not match user's current email"
                return render_template("change_email.html", errors=errors)

            if new_email_existed and new_email_existed[0] == user_new_email:
                errors["email1_err"] = "Email already registered"
                return render_template("change_email.html", errors=errors)

            update_account_email = "UPDATE userAccount SET userEmail = %s WHERE userEmail = %s"
            update_login_email = "UPDATE userlogin set userEmail = %s WHERE userEmail = %s"

            cursor.execute(update_login_email, (user_new_email, user_old_email))
            cursor.execute(update_account_email, (user_new_email, user_old_email))
            conn.commit()

            return render_template("edit_profile.html", email_success=True)

        except mysql.connector.Error as e:
            print("error:", e)
            errors["server_err"] = "There is an issue with the server right now, come try another time"
            conn.rollback()
            return render_template("change_email.html", errors=errors)
        finally:
            cursor.close()
            conn.close()

    return render_template("change_email.html")


if __name__ == '__main__':
    app.run(debug=True)
