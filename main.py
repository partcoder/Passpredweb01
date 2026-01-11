import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from flask import Flask, request, send_file, send_from_directory

app = Flask(__name__)

@app.route('/')
def index():
    return send_file('index.html')

@app.route('/css/<path:filename>')
def css_files(filename):
    return send_from_directory('css', filename)

@app.route('/predict', methods=['POST'])
def predict():
    subject = request.form['subject']
    study_hours = float(request.form['study_hours'])
    days_before = float(request.form['days_before_exam'])
    attendance = float(request.form['attendance_percentage'])

    # Map subject to filename
    if subject == "maths":
        filename = 'maths.csv'
    elif subject == "science":
        filename = 'science.csv'
    elif subject == "english":
        filename = 'english.csv'
    else:
        result = "Please Enter Subject"
        # Return HTML with error
        html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Pass Prediction</title>
    <link rel="stylesheet" href="/css/style.css">
</head>
<body>
    <div class="container">
        <h1>Student Pass Prediction</h1>
        <form action="/predict" method="post">
            <label for="subject">Choose Subject:</label>
            <select name="subject" required>
                <option value="">Select Subject</option>
                <option value="maths">Maths</option>
                <option value="science">Science</option>
                <option value="english">English</option>
            </select>
            <label for="study_hours">Study Hours:</label>
            <input type="number" name="study_hours" step="0.1" min="0" required>
            <label for="days_before_exam">Days Before Exam:</label>
            <input type="number" name="days_before_exam" min="0" required>
            <label for="attendance_percentage">Attendance Percentage:</label>
            <input type="number" name="attendance_percentage" step="0.1" min="0" max="100" required>
            <button type="submit">Predict</button>
        </form>
        <div class="result">{result}</div>
    </div>
</body>
</html>
"""
        return html

    # Load data and train model
    df = pd.read_csv(filename)
    X = df[['study_hours', 'days_before_exam', 'attendance_percentage']]
    y = df['pass']

    # Train model
    model = LogisticRegression(max_iter=1000)
    model.fit(X, y)  # No scaling in the original, so keep simple

    # Predict
    new_student = pd.DataFrame(
        [[study_hours, days_before, attendance]],
        columns=['study_hours', 'days_before_exam', 'attendance_percentage']
    )
    prediction = model.predict(new_student)
    result = "Yes" if prediction[0] == 1 else "No"

    # Return HTML with result
    html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Pass Prediction</title>
    <link rel="stylesheet" href="/css/style.css">
</head>
<body>
    <div class="container">
        <h1>Student Pass Prediction</h1>
        <form action="/predict" method="post">
            <label for="subject">Choose Subject:</label>
            <select name="subject" required>
                <option value="">Select Subject</option>
                <option value="maths" {"selected" if subject == "maths" else ""}>Maths</option>
                <option value="science" {"selected" if subject == "science" else ""}>Science</option>
                <option value="english" {"selected" if subject == "english" else ""}>English</option>
            </select>
            <label for="study_hours">Study Hours:</label>
            <input type="number" name="study_hours" step="0.1" min="0" value="{study_hours}" required>
            <label for="days_before_exam">Days Before Exam:</label>
            <input type="number" name="days_before_exam" min="0" value="{days_before}" required>
            <label for="attendance_percentage">Attendance Percentage:</label>
            <input type="number" name="attendance_percentage" step="0.1" min="0" max="100" value="{attendance}" required>
            <button type="submit">Predict</button>
        </form>
        <div class="result">Will the student pass? {result}</div>
    </div>
</body>
</html>
"""
    return html

if __name__ == "__main__":
    app.run(debug=True)
