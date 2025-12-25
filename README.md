# Student Pass Prediction Web App

A static web application that predicts whether a student will pass an exam based on study hours, days before exam, and attendance percentage for Maths, Science, and English subjects.

## Features

- Clean, modern UI with glassmorphism design
- Input validation
- Instant predictions using pre-trained logistic regression models
- Responsive design

## How to Use

1. Select the subject (Maths, Science, or English)
2. Enter the study hours (decimal number)
3. Enter the number of days before the exam
4. Enter the attendance percentage (0-100)
5. Click "Predict" to see the result

## Hosting on GitHub Pages

1. Create a new repository on GitHub
2. Upload all files: `index.html`, `script.js`, `css/style.css`, and optionally the CSV files
3. Go to repository Settings > Pages
4. Set source to "Deploy from a branch"
5. Select "main" branch and "/ (root)" folder
6. Save and wait for deployment

The app will be available at `https://yourusername.github.io/repositoryname/`

## Local Development

Open `index.html` in a web browser to run the app locally.

## Model Training

The models were trained using scikit-learn on the provided CSV datasets. The trained parameters are hardcoded in `script.js` for fast predictions.