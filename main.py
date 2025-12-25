import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler



def train_and_get_model(filename):
    df = pd.read_csv(filename)
    X = df[['study_hours', 'days_before_exam', 'attendance_percentage']]
    y = df['pass']

    # Scale features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # Train model
    model = LogisticRegression(max_iter=1000)
    model.fit(X_scaled, y)

    return model, scaler

def main():
    subjects = ['maths', 'science', 'english']
    models = {}
    scalers = {}

    for subj in subjects:
        filename = f'{subj}.csv'
        model, scaler = train_and_get_model(filename)
        models[subj] = model
        scalers[subj] = scaler

        print(f"{subj.upper()} Model:")
        print(f"  Weights: {model.coef_[0]}")
        print(f"  Bias: {model.intercept_[0]}")
        print(f"  Scaler means: {scaler.mean_}")
        print(f"  Scaler scales: {scaler.scale_}")
        print()

    # Now for prediction
    subject = input("Choose subject (maths/science/english): ").strip().lower()
    if subject not in models:
        print("Invalid subject.")
        return

    model = models[subject]
    scaler = scalers[subject]

    # Take input from user
    study_hours = float(input("Enter study hours: "))
    days_before_exam = float(input("Enter days before exam: "))
    attendance_percentage = float(input("Enter attendance percentage: "))

    new_student = np.array([[study_hours, days_before_exam, attendance_percentage]])
    new_student_scaled = scaler.transform(new_student)
    prediction = model.predict(new_student_scaled)
    print("Will the student pass?", "Yes" if prediction[0] == 1 else "No")

if __name__ == "__main__":
    main()
