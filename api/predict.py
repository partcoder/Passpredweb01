import pandas as pd
from sklearn.linear_model import LogisticRegression

def handler(request):
    if request.method != 'POST':
        return {'statusCode': 405, 'body': 'Method Not Allowed'}

    # Get form data
    data = request.form
    subject = data.get('subject')
    study_hours = float(data.get('study_hours', 0))
    days_before = float(data.get('days_before_exam', 0))
    attendance = float(data.get('attendance_percentage', 0))

    # Map subject to filename
    if subject == "maths":
        filename = 'maths.csv'
    elif subject == "science":
        filename = 'science.csv'
    elif subject == "english":
        filename = 'english.csv'
    else:
        result = "Invalid subject"
        html = generate_html(result, subject, study_hours, days_before, attendance)
        return {'statusCode': 200, 'headers': {'Content-Type': 'text/html'}, 'body': html}

    # Load data and train model
    df = pd.read_csv(filename)
    X = df[['study_hours', 'days_before_exam', 'attendance_percentage']]
    y = df['pass']

    # Train model
    model = LogisticRegression(max_iter=1000)
    model.fit(X, y)

    # Predict
    new_student = pd.DataFrame(
        [[study_hours, days_before, attendance]],
        columns=['study_hours', 'days_before_exam', 'attendance_percentage']
    )
    prediction = model.predict(new_student)
    result = "Yes" if prediction[0] == 1 else "No"

    html = generate_html(result, subject, study_hours, days_before, attendance)
    return {'statusCode': 200, 'headers': {'Content-Type': 'text/html'}, 'body': html}

def generate_html(result, subject, study_hours, days_before, attendance):
    return f"""
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