import pickle
import numpy as np
from flask import Flask, request, render_template_string

app = Flask(__name__)

# Load the trained Logistic Regression model
model_path = 'loan.pkl'
with open(model_path, 'rb') as f:
    model = pickle.load(f)

# HTML Template with Embedded Tailwind CSS Layout
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Loan Eligibility Prediction Portal</title>
    <!-- Tailwind CSS CDN for modern styling -->
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <style>
        body { font-family: 'Inter', sans-serif; }
    </style>
</head>
<body class="bg-gradient-to-br from-slate-900 via-indigo-950 to-slate-900 text-slate-100 min-h-screen py-10 px-4">
    <div class="max-w-4xl mx-auto">
        <!-- Header -->
        <div class="text-center mb-10">
            <span class="bg-indigo-500/10 text-indigo-400 text-xs font-semibold px-3 py-1 rounded-full uppercase tracking-wider border border-indigo-500/20">AI-Powered Financial Services</span>
            <h1 class="text-4xl font-extrabold text-white mt-3 tracking-tight">Loan Eligibility Predictor</h1>
            <p class="text-slate-400 mt-2 text-sm sm:text-base">Provide applicant details below to instantly evaluate loan approval status.</p>
        </div>

        <!-- Main Card Container -->
        <div class="bg-slate-900/80 backdrop-blur-xl border border-slate-800 rounded-2xl shadow-2xl overflow-hidden p-6 sm:p-10">
            
            {% if prediction_text %}
            <!-- Result Banner -->
            <div class="mb-8 p-5 rounded-xl border text-center transition-all duration-300 {% if is_approved %} bg-emerald-950/40 border-emerald-500/40 text-emerald-300 {% else %} bg-rose-950/40 border-rose-500/40 text-rose-300 {% endif %}">
                <h3 class="text-lg font-semibold uppercase tracking-wider mb-1">Evaluation Result</h3>
                <p class="text-2xl font-bold">{{ prediction_text }}</p>
            </div>
            {% endif %}

            <!-- Input Form -->
            <form action="/predict" method="POST" class="grid grid-cols-1 sm:grid-cols-2 gap-6">
                
                <!-- Gender -->
                <div>
                    <label class="block text-sm font-medium text-slate-300 mb-2">Gender</label>
                    <select name="Gender" required class="w-full bg-slate-800 border border-slate-700 rounded-lg px-4 py-2.5 text-white focus:outline-none focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 transition">
                        <option value="1">Male</option>
                        <option value="0">Female</option>
                    </select>
                </div>

                <!-- Married -->
                <div>
                    <label class="block text-sm font-medium text-slate-300 mb-2">Marital Status</label>
                    <select name="Married" required class="w-full bg-slate-800 border border-slate-700 rounded-lg px-4 py-2.5 text-white focus:outline-none focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 transition">
                        <option value="1">Yes (Married)</option>
                        <option value="0">No (Unmarried)</option>
                    </select>
                </div>

                <!-- Dependents -->
                <div>
                    <label class="block text-sm font-medium text-slate-300 mb-2">Dependents</label>
                    <select name="Dependents" required class="w-full bg-slate-800 border border-slate-700 rounded-lg px-4 py-2.5 text-white focus:outline-none focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 transition">
                        <option value="0">0</option>
                        <option value="1">1</option>
                        <option value="2">2</option>
                        <option value="3">3+</option>
                    </select>
                </div>

                <!-- Education -->
                <div>
                    <label class="block text-sm font-medium text-slate-300 mb-2">Education</label>
                    <select name="Education" required class="w-full bg-slate-800 border border-slate-700 rounded-lg px-4 py-2.5 text-white focus:outline-none focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 transition">
                        <option value="1">Graduate</option>
                        <option value="0">Not Graduate</option>
                    </select>
                </div>

                <!-- Self Employed -->
                <div>
                    <label class="block text-sm font-medium text-slate-300 mb-2">Self Employed</label>
                    <select name="Self_Employed" required class="w-full bg-slate-800 border border-slate-700 rounded-lg px-4 py-2.5 text-white focus:outline-none focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 transition">
                        <option value="0">No</option>
                        <option value="1">Yes</option>
                    </select>
                </div>

                <!-- Applicant Income -->
                <div>
                    <label class="block text-sm font-medium text-slate-300 mb-2">Applicant Income ($)</label>
                    <input type="number" name="ApplicantIncome" placeholder="e.g. 5000" required class="w-full bg-slate-800 border border-slate-700 rounded-lg px-4 py-2.5 text-white focus:outline-none focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 transition">
                </div>

                <!-- Coapplicant Income -->
                <div>
                    <label class="block text-sm font-medium text-slate-300 mb-2">Coapplicant Income ($)</label>
                    <input type="number" step="any" name="CoapplicantIncome" placeholder="e.g. 1500" required class="w-full bg-slate-800 border border-slate-700 rounded-lg px-4 py-2.5 text-white focus:outline-none focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 transition">
                </div>

                <!-- Loan Amount -->
                <div>
                    <label class="block text-sm font-medium text-slate-300 mb-2">Loan Amount (in thousands)</label>
                    <input type="number" step="any" name="LoanAmount" placeholder="e.g. 120" required class="w-full bg-slate-800 border border-slate-700 rounded-lg px-4 py-2.5 text-white focus:outline-none focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 transition">
                </div>

                <!-- Loan Amount Term -->
                <div>
                    <label class="block text-sm font-medium text-slate-300 mb-2">Loan Term (in months)</label>
                    <input type="number" name="Loan_Amount_Term" placeholder="e.g. 360" required class="w-full bg-slate-800 border border-slate-700 rounded-lg px-4 py-2.5 text-white focus:outline-none focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 transition">
                </div>

                <!-- Credit History -->
                <div>
                    <label class="block text-sm font-medium text-slate-300 mb-2">Credit History Meets Guidelines</label>
                    <select name="Credit_History" required class="w-full bg-slate-800 border border-slate-700 rounded-lg px-4 py-2.5 text-white focus:outline-none focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 transition">
                        <option value="1">Yes (1.0)</option>
                        <option value="0">No (0.0)</option>
                    </select>
                </div>

                <!-- Property Area -->
                <div class="sm:col-span-2">
                    <label class="block text-sm font-medium text-slate-300 mb-2">Property Area</label>
                    <select name="Property_Area" required class="w-full bg-slate-800 border border-slate-700 rounded-lg px-4 py-2.5 text-white focus:outline-none focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 transition">
                        <option value="2">Urban</option>
                        <option value="1">Semiurban</option>
                        <option value="0">Rural</option>
                    </select>
                </div>

                <!-- Submit Button -->
                <div class="sm:col-span-2 mt-4">
                    <button type="submit" class="w-full bg-gradient-to-r from-indigo-600 to-violet-600 hover:from-indigo-500 hover:to-violet-500 text-white font-semibold py-3.5 px-6 rounded-lg shadow-lg shadow-indigo-600/30 transition-all duration-200 transform hover:-translate-y-0.5">
                        Predict Loan Eligibility
                    </button>
                </div>

            </form>
        </div>

        <!-- Footer -->
        <div class="text-center mt-8 text-xs text-slate-500">
            Flask Deployment • Logistic Regression Model
        </div>
    </div>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Extract features matching model.feature_names_in_ order:
        # 1. Gender, 2. Married, 3. Dependents, 4. Education, 5. Self_Employed,
        # 6. ApplicantIncome, 7. CoapplicantIncome, 8. LoanAmount, 
        # 9. Loan_Amount_Term, 10. Credit_History, 11. Property_Area
        features = [
            float(request.form['Gender']),
            float(request.form['Married']),
            float(request.form['Dependents']),
            float(request.form['Education']),
            float(request.form['Self_Employed']),
            float(request.form['ApplicantIncome']),
            float(request.form['CoapplicantIncome']),
            float(request.form['LoanAmount']),
            float(request.form['Loan_Amount_Term']),
            float(request.form['Credit_History']),
            float(request.form['Property_Area'])
        ]
        
        final_features = np.array([features])
        prediction = model.predict(final_features)
        
        output = prediction[0]
        is_approved = (output == 1 or output == 'Y' or output == True)
        
        prediction_text = "Congratulations! Your Loan is Approved." if is_approved else "Sorry, your Loan Application is Rejected."
            
        return render_template_string(
            HTML_TEMPLATE, 
            prediction_text=prediction_text, 
            is_approved=is_approved
        )
    except Exception as e:
        return render_template_string(
            HTML_TEMPLATE, 
            prediction_text=f"Error in processing: {str(e)}", 
            is_approved=False
        )

if __name__ == '__main__':
    app.run(debug=True)
