# PayWise

PayWise is a modern web-based platform for smart payment optimization. It provides users with seamless authentication, intuitive financial dashboards, budgeting tools, spending insights, and a personalized rewards system.

---

## Features

- Full-stack login, signup, and forgot password system with OTP verification
- Captcha validation using random math expressions (+, -)
- Responsive, glassmorphic user interface for authentication and dashboard
- Dynamic dashboard with:
  - Budget planner and tracker
  - Spending analytics with charts
  - User profile management
  - Rewards and referral system
- Dark mode support with local state persistence
- Clean modular separation of frontend and backend (Supabase or Python Flask)

---

## 1. Setup

### 1.1. Clone and Open Project

git clone https://github.com/Rashi1575/PayWise.git
cd PayWise

### 1.2. Creating a virtual environment and activating it

```bash
python -m venv <virtual_env_name>
<virtual_env_name>/Scripts/Activate
```
### 1.3. installing requirements
```bash
pip install -r requirements.txt
```
---

## 2. Project Structure

```
PayWise/

```

---

## 3. Frontend Usage

### 3.1. Run Locally (HTML + JS only)

Open terminal:
cd frontend 
python -m http.server 3000

And in another terminal:
cd backend
python app.py

Use this link to open the website:
http://localhost:3000/#


### 3.2. Navigation Flow

- On signup, user receives OTP via backend
- On login, user solves Captcha
- Successful login/signup redirects to `dashb/dashb.html`
- Logout from dashboard redirects back to login

---

## 4. Backend Setup (Optional)

If using Flask:

```bash
cd server
pip install flask
python app.py
```

Ensure CORS is handled and the endpoints match the frontend fetch calls:
- `/login`
- `/signup`
- `/send-otp`
- `/verify-otp`
- `/forgot-password`
- `/get-email`

If using Supabase, configure the REST API URL and key in `app.js`.

---

## 5. Machine Learning Models

### 5.1 Expense Category Classifier

This model categorizes expense descriptions into predefined categories like Food, Healthcare, Transportation, etc.

*Pipeline:*

- *Text Preprocessing:*
  - Lowercasing
  - Removal of punctuation, digits
  - Stopword removal (nltk)
  - Lemmatization (WordNetLemmatizer)

- *Vectorization:*
  - TF-IDF (TfidfVectorizer) with bigrams (ngram_range=(1, 2))
  - max_features = 1500

- *Classifier:*
  - LogisticRegression(max_iter=1000)

- *Training:*
  - Train/Test Split: 80/20 using train_test_split
  - Input data: expensessssss_data_indian_household.csv

- *Prediction:*
  - predict_expense(text) processes and classifies input strings.

---

## 5.2 Fraud Detection System

This model predicts and flags potentially fraudulent credit card transactions based on structured transaction data.

*Pipeline:*

- *Model:*
  - RandomForestClassifier(n_estimators=100, random_state=42)

- *Training Data:*
  - CSV dataset: creditcard.csv
  - Target column: Class renamed to is_fraud

- *Evaluation:*
  - Evaluated with classification_report on an 80/20 stratified split

- *Artifacts:*
  - Saved model: fraud_model.pkl
  - Saved features: fraud_model_features.pkl

- *Additional Rule-Based Checks:*
  - check_unusual_amount(user_id, amount) — flags abnormally high transactions
  - check_velocity(user_id) — detects burst of rapid transactions
  - check_geolocation_inconsistency(user_id, ip) — flags IP location jumps
  - check_ip_risk_score(ip) — uses IPQualityScore API to detect risk
  - is_card_valid(card_number, expiry_date, cvv) — validates card format and expiry
  - check_ml_anomaly(transaction_dict) — runs Random Forest prediction

## 6. Dashboard Features

- User greeting and profile section
- Make payment buttons (UPI, Net Banking)
- Budget tracker with input fields
- Expense insights via pie and bar charts (Chart.js)
- Rewards section with referral codes
- Dark mode toggle

---

## 7. Data Persistence



---

## 8. Troubleshooting

- Page not updating: Clear browser cache (`Ctrl + Shift + R`)
- OTP not working: Ensure email is passed to backend during verification
- Dashboard not loading: Check if redirection URL is correct
- Changes not reflecting: Verify script caching, restart Live Server

---

## 9. Credits

- Dashboard UI and logic by: CodeBlooded
- API backend: Flask or Supabase (configurable)
- Charts via: [Chart.js](https://www.chartjs.org)
- Fonts: Segoe UI

---

## 10. License

MIT License
