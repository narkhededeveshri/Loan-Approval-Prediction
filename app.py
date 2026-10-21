import pickle
import numpy as np
import pandas as pd
from flask import Flask, request, render_template_string

app = Flask(__name__)

# Load the trained model from loan.pkl
with open('loan.pkl', 'rb') as f:
    model = pickle.load(f)

# Modern, responsive HTML template with embedded Bootstrap 5 styling
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Loan Eligibility Prediction Portal</title>
    <!-- Bootstrap 5 CSS CDN -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <!-- FontAwesome Icons -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        body {
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            min-height: 100vh;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            padding-bottom: 50px;
        }
        .navbar-brand {
            font-weight: 700;
            letter-spacing: 0.5px;
        }
        .card {
            border: none;
            border-radius: 1rem;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.08);
        }
        .card-header {
            background: linear-gradient(135deg, #0d6efd 0%, #0a58ca 100%);
            color: white;
            border-radius: 1rem 1rem 0 0 !important;
            padding: 1.5rem;
        }
        .form-label {
            font-weight: 600;
            color: #333;
            font-size: 0.9rem;
        }
        .form-control, .form-select {
            border-radius: 0.5rem;
            padding: 0.75rem;
            border: 1px solid #ced4da;
            transition: all 0.3s;
        }
        .form-control:focus, .form-select:focus {
            border-color: #0d6efd;
            box-shadow: 0 0 0 0.25rem rgba(13, 110, 253, 0.15);
        }
        .btn-primary {
            background: linear-gradient(135deg, #0d6efd 0%, #0a58ca 100%);
            border: none;
            border-radius: 0.5rem;
            padding: 0.75rem;
            font-weight: 600;
            letter-spacing: 0.5px;
            transition: all 0.3s;
        }
        .btn-primary:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(13, 110, 253, 0.3);
        }
        .result-card {
            border-radius: 1rem;
            padding: 2rem;
            text-align: center;
            margin-top: 2rem;
            animation: fadeIn 0.5s ease-in-out;
        }
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
    </style>
</head>
<body>

    <!-- Navbar -->
    <nav class="navbar navbar-dark bg-dark shadow-sm mb-4">
        <div class="container">
            <a class="navbar-brand" href="#">
                <i class="fas fa-university me-2 text-primary"></i> SmartLoan Predictor
            </a>
        </div>
    </nav>

    <!-- Main Container -->
    <div class="container">
        <div class="row justify-content-center">
            <div class="col-lg-9">
                <div class="card shadow-lg">
                    <div class="card-header text-center">
                        <h2><i class="fas fa-file-invoice-dollar me-2"></i>Loan Eligibility Form</h2>
                        <p class="mb-0 text-white-50">Fill out the applicant information below to check loan approval status.</p>
                    </div>
                    <div class="card-body p-4 p-md-5">
                        
                        <form method="POST" action="/">
                            <div class="row g-3">
                                <!-- Gender -->
                                <div class="col-md-4">
                                    <label class="form-label"><i class="fas fa-venus-mars me-1 text-primary"></i> Gender</label>
                                    <select class="form-select" name="Gender" required>
                                        <option value="1" {% if data and data.Gender == '1' %}selected{% endif %}>Male</option>
                                        <option value="0" {% if data and data.Gender == '0' %}selected{% endif %}>Female</option>
                                    </select>
                                </div>

                                <!-- Married -->
                                <div class="col-md-4">
                                    <label class="form-label"><i class="fas fa-ring me-1 text-primary"></i> Married</label>
                                    <select class="form-select" name="Married" required>
                                        <option value="1" {% if data and data.Married == '1' %}selected{% endif %}>Yes</option>
                                        <option value="0" {% if data and data.Married == '0' %}selected{% endif %}>No</option>
                                    </select>
                                </div>

                                <!-- Dependents -->
                                <div class="col-md-4">
                                    <label class="form-label"><i class="fas fa-users me-1 text-primary"></i> Dependents</label>
                                    <select class="form-select" name="Dependents" required>
                                        <option value="0" {% if data and data.Dependents == '0' %}selected{% endif %}>0</option>
                                        <option value="1" {% if data and data.Dependents == '1' %}selected{% endif %}>1</option>
                                        <option value="2" {% if data and data.Dependents == '2' %}selected{% endif %}>2</option>
                                        <option value="3" {% if data and data.Dependents == '3' %}selected{% endif %}>3+</option>
                                    </select>
                                </div>

                                <!-- Education -->
                                <div class="col-md-6">
                                    <label class="form-label"><i class="fas fa-graduation-cap me-1 text-primary"></i> Education</label>
                                    <select class="form-select" name="Education" required>
                                        <option value="1" {% if data and data.Education == '1' %}selected{% endif %}>Graduate</option>
                                        <option value="0" {% if data and data.Education == '0' %}selected{% endif %}>Not Graduate</option>
                                    </select>
                                </div>

                                <!-- Self Employed -->
                                <div class="col-md-6">
                                    <label class="form-label"><i class="fas fa-briefcase me-1 text-primary"></i> Self Employed</label>
                                    <select class="form-select" name="Self_Employed" required>
                                        <option value="0" {% if data and data.Self_Employed == '0' %}selected{% endif %}>No</option>
                                        <option value="1" {% if data and data.Self_Employed == '1' %}selected{% endif %}>Yes</option>
                                    </select>
                                </div>

                                <!-- Applicant Income -->
                                <div class="col-md-6">
                                    <label class="form-label"><i class="fas fa-wallet me-1 text-primary"></i> Applicant Income</label>
                                    <input type="number" step="any" class="form-control" name="ApplicantIncome" placeholder="e.g. 5000" value="{{ data.ApplicantIncome if data else '' }}" required>
                                </div>

                                <!-- Coapplicant Income -->
                                <div class="col-md-6">
                                    <label class="form-label"><i class="fas fa-hand-holding-usd me-1 text-primary"></i> Coapplicant Income</label>
                                    <input type="number" step="any" class="form-control" name="CoapplicantIncome" placeholder="e.g. 1500" value="{{ data.CoapplicantIncome if data else '' }}" required>
                                </div>

                                <!-- Loan Amount -->
                                <div class="col-md-6">
                                    <label class="form-label"><i class="fas fa-dollar-sign me-1 text-primary"></i> Loan Amount (in thousands)</label>
                                    <input type="number" step="any" class="form-control" name="LoanAmount" placeholder="e.g. 128" value="{{ data.LoanAmount if data else '' }}" required>
                                </div>

                                <!-- Loan Amount Term -->
                                <div class="col-md-6">
                                    <label class="form-label"><i class="fas fa-calendar-alt me-1 text-primary"></i> Loan Term (in months)</label>
                                    <input type="number" class="form-control" name="Loan_Amount_Term" placeholder="e.g. 360" value="{{ data.Loan_Amount_Term if data else '' }}" required>
                                </div>

                                <!-- Credit History -->
                                <div class="col-md-6">
                                    <label class="form-label"><i class="fas fa-history me-1 text-primary"></i> Credit History</label>
                                    <select class="form-select" name="Credit_History" required>
                                        <option value="1" {% if data and data.Credit_History == '1' %}selected{% endif %}>1.0 (Good History)</option>
                                        <option value="0" {% if data and data.Credit_History == '0' %}selected{% endif %}>0.0 (Bad History)</option>
                                    </select>
                                </div>

                                <!-- Property Area -->
                                <div class="col-md-6">
                                    <label class="form-label"><i class="fas fa-map-marker-alt me-1 text-primary"></i> Property Area</label>
                                    <select class="form-select" name="Property_Area" required>
                                        <option value="2" {% if data and data.Property_Area == '2' %}selected{% endif %}>Urban</option>
                                        <option value="1" {% if data and data.Property_Area == '1' %}selected{% endif %}>Semiurban</option>
                                        <option value="0" {% if data and data.Property_Area == '0' %}selected{% endif %}>Rural</option>
                                    </select>
                                </div>

                                <!-- Submit Button -->
                                <div class="col-12 mt-4">
                                    <button type="submit" class="btn btn-primary w-100 py-3 shadow">
                                        <i class="fas fa-check-circle me-2"></i> Predict Loan Eligibility
                                    </button>
                                </div>
                            </div>
                        </form>

                        <!-- Prediction Result Card -->
                        {% if prediction_text %}
                        <div class="result-card shadow-sm {% if is_approved %}bg-success-subtle text-success-emphasis border border-success{% else %}bg-danger-subtle text-danger-emphasis border border-danger{% endif %}">
                            <h4>
                                {% if is_approved %}
                                <i class="fas fa-circle-check fa-lg me-2 text-success"></i> Congratulations!
                                {% else %}
                                <i class="fas fa-circle-xmark fa-lg me-2 text-danger"></i> Application Status
                                {% endif %}
                            </h4>
                            <p class="fs-5 mb-0 mt-2 fw-semibold">{{ prediction_text }}</p>
                        </div>
                        {% endif %}

                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- Bootstrap JS Bundle CDN -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def home():
    prediction_text = None
    is_approved = False
    data = None

    if request.method == "POST":
        try:
            data = request.form

            # Map and cast form input values to float/int matching training setup
            gender = float(data["Gender"])
            married = float(data["Married"])
            dependents = float(data["Dependents"])
            education = float(data["Education"])
            self_employed = float(data["Self_Employed"])
            applicant_income = float(data["ApplicantIncome"])
            coapplicant_income = float(data["CoapplicantIncome"])
            loan_amount = float(data["LoanAmount"])
            loan_amount_term = float(data["Loan_Amount_Term"])
            credit_history = float(data["Credit_History"])
            property_area = float(data["Property_Area"])

            # Construct DataFrame matching the exact features expected by the model
            input_df = pd.DataFrame([[
                gender, married, dependents, education, self_employed,
                applicant_income, coapplicant_income, loan_amount,
                loan_amount_term, credit_history, property_area
            ]], columns=[
                "Gender", "Married", "Dependents", "Education", "Self_Employed",
                "ApplicantIncome", "CoapplicantIncome", "LoanAmount",
                "Loan_Amount_Term", "Credit_History", "Property_Area"
            ])

            # Run prediction
            prediction = model.predict(input_df)[0]

            # Interpret model output (1/Y for Approved, 0/N for Rejected)
            if prediction == 1 or prediction == 'Y':
                prediction_text = "Your Loan Application is Approved! You meet the eligibility criteria."
                is_approved = True
            else:
                prediction_text = "Sorry, your Loan Application is Rejected based on the
