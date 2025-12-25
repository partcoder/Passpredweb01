// script.js - Handles the prediction logic using pre-trained models

// Pre-trained model parameters for each subject
const models = {
    maths: {
        weights: [5.48607179, 0.11094018, 2.19845888],
        bias: 1.1982828051807244,
        means: [3.18664, 3.98, 54.347],
        scales: [1.59892974, 1.98836616, 26.71697197]
    },
    science: {
        weights: [4.84260576, 0.10082359, 3.13512602],
        bias: -1.6638160894763305,
        means: [5.18072, 3.977, 55.623],
        scales: [2.70750588, 2.01605332, 25.85387536]
    },
    english: {
        weights: [2.5081715, 0.11443409, 1.61310246],
        bias: -0.9714287693261199,
        means: [2.0562, 4.016, 55.095],
        scales: [1.1504459, 2.01785629, 26.56256718]
    }
};

// Sigmoid function
function sigmoid(z) {
    return 1 / (1 + Math.exp(-z));
}

// Scale features using pre-computed means and scales
function scaleFeatures(features, means, scales) {
    return features.map((x, i) => (x - means[i]) / scales[i]);
}

// Predict function
function predictPass(subject, studyHours, daysBefore, attendance) {
    const model = models[subject];
    if (!model) {
        throw new Error('Invalid subject');
    }

    // Scale the input features
    const scaledFeatures = scaleFeatures([studyHours, daysBefore, attendance], model.means, model.scales);

    // Compute z = weights * scaledFeatures + bias
    const z = scaledFeatures.reduce((sum, x, i) => sum + x * model.weights[i], 0) + model.bias;

    // Sigmoid and threshold
    const probability = sigmoid(z);
    return probability >= 0.5 ? 'Yes' : 'No';
}

// Handle form submission
document.getElementById('predictionForm').addEventListener('submit', function(event) {
    event.preventDefault();

    const subject = document.getElementById('subject').value;
    const studyHours = parseFloat(document.getElementById('study_hours').value);
    const daysBefore = parseFloat(document.getElementById('days_before_exam').value);
    const attendance = parseFloat(document.getElementById('attendance_percentage').value);

    const loading = document.getElementById('loading');
    const resultDiv = document.getElementById('result');

    loading.style.display = 'block';
    resultDiv.textContent = '';

    try {
        const result = predictPass(subject, studyHours, daysBefore, attendance);
        resultDiv.textContent = `Will the student pass? ${result}`;
    } catch (error) {
        resultDiv.textContent = `Error: ${error.message}`;
    } finally {
        loading.style.display = 'none';
    }
});