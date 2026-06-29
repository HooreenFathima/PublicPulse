from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
import joblib

app = Flask(__name__)

# ---------------- DATABASE CONNECTION ----------------
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="public_pulse"
)

cursor = db.cursor(dictionary=True, buffered=True)

# ---------------- LOAD MODEL ----------------
model = joblib.load('sentiment_model (1).pkl')
vectorizer = joblib.load('vectorizer (2).pkl')

# ---------------- ADMIN LOGIN DATA ----------------
admins = {"admin": "admin"}


# ---------------- HOME ----------------
@app.route('/')
def index():
    return render_template('index.html')


# ---------------- LOGIN PAGE ----------------
@app.route('/login')
def login():
    return render_template('login_choice.html')


# ---------------- USER REGISTER ----------------
@app.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == 'POST':

        username = request.form.get('username')
        email = request.form.get('email')
        mobile = request.form.get('mobile')
        password = request.form.get('password')

        query = """
        INSERT INTO users (username,email,mobile,password,status)
        VALUES (%s,%s,%s,%s,%s)
        """

        values = (username, email, mobile, password, 'Pending')

        cursor.execute(query, values)
        db.commit()

        return redirect(url_for('user_login'))

    return render_template('register.html')


# ---------------- USER LOGIN ----------------
@app.route('/user_login', methods=['GET', 'POST'])
def user_login():

    if request.method == 'POST':

        username = request.form.get('username')
        password = request.form.get('password')

        query = "SELECT * FROM users WHERE username=%s AND password=%s"
        cursor.execute(query, (username, password))

        user = cursor.fetchone()

        if user:
            if user['status'] == "Approved":
                return redirect(url_for('user_dashboard'))
            else:
                return "Waiting for Admin Approval"

        return "Invalid Username or Password"

    return render_template('user_login.html')


# ---------------- USER DASHBOARD ----------------
@app.route('/user_dashboard')
def user_dashboard():
    return render_template('user_dashboard.html')


# ---------------- PREDICTION PAGE ----------------
@app.route('/prediction')
def prediction():
    return render_template('prediction.html')


# ---------------- ML PREDICT ----------------
@app.route("/predict", methods=["POST"])
def predict():

    text = request.form.get("scheme")

    if not text:
        return "Please enter some text"

    text_vector = vectorizer.transform([text])

    # Prediction
    prediction = model.predict(text_vector)[0]

    # Confidence
    probs = model.predict_proba(text_vector)[0]
    confidence = max(probs) * 100

    return render_template(
        "result.html",
        result=prediction,
        confidence=round(confidence, 2)
    )

# ---------------- ADMIN LOGIN ----------------
@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():

    if request.method == 'POST':

        username = request.form.get('username')
        password = request.form.get('password')

        if username in admins and admins[username] == password:
            return redirect(url_for('admin_dashboard'))

        return "Invalid Admin Login"

    return render_template('admin_login.html')


# ---------------- ADMIN DASHBOARD ----------------
@app.route('/admin_dashboard')
def admin_dashboard():
    return render_template('admin_dashboard.html')


# ---------------- AUTHORIZE USERS ----------------
@app.route('/authorize_users')
def authorize_users():

    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()

    return render_template("authorize_users.html", users=users)


# ---------------- APPROVE USER ----------------
@app.route('/approve_user/<int:id>', methods=['POST'])
def approve_user(id):

    cursor.execute("UPDATE users SET status='Approved' WHERE id=%s", (id,))
    db.commit()

    return redirect(url_for('authorize_users'))


# ---------------- REJECT USER ----------------
@app.route('/reject_user/<int:id>', methods=['POST'])
def reject_user(id):

    cursor.execute("UPDATE users SET status='Rejected' WHERE id=%s", (id,))
    db.commit()

    return redirect(url_for('authorize_users'))


# ---------------- DELETE USER ----------------
@app.route('/delete_user/<int:id>', methods=['POST'])
def delete_user(id):

    cursor.execute("DELETE FROM users WHERE id=%s", (id,))
    db.commit()

    return redirect(url_for('authorize_users'))


# ---------------- VIEW GRAPHS ----------------
@app.route('/view_graphs')
def view_graphs():
    import pandas as pd
    from matplotlib import pyplot as plt
    import io
    df = pd.read_excel("telangana_public_pulse.xlsx")

    # Count sentiments
    sentiment_counts = df['sentiment'].value_counts()

    # Create plot
    plt.figure()
    sentiment_counts.plot(kind='bar')
    plt.xlabel("Sentiment Type")
    plt.ylabel("Count")
    plt.title("Sentiment Distribution")
    plt.tight_layout()  
    plt.savefig("static/css/datasetoverview.jpg")
  
    return render_template('view_graphs.html')


# ---------------- RUN APP ----------------
if __name__ == "__main__":
    app.run(debug=True)