# 📄 PRODUCT REQUIREMENT DOCUMENT (PRD)

## Navi Mumbai Real Estate Price Predictor

**Version:** 2.0 – Detailed Engineering PRD
**Product Type:** Full-Stack Machine Learning Web Application
**Prepared For:** Academic / Portfolio / Workshop Implementation

---

# 1. Executive Summary

The **Navi Mumbai Real Estate Price Predictor** is a web-based Machine Learning system designed to estimate residential property prices using structured property inputs. The application combines a **Next.js frontend**, a **Python backend API**, and a **Scikit-Learn Linear Regression model** to deliver fast and interpretable price predictions.

The product aims to simulate a real-world ML deployment workflow where users interact with a modern UI while the backend performs data preprocessing, prediction logic, and business analysis.

---

# 2. Vision & Goals

## Product Vision

To create a beginner-friendly yet professionally structured ML web application that demonstrates how real estate pricing models can be deployed as an interactive web service.

## Primary Goals

* Deliver accurate property price predictions.
* Provide a responsive and intuitive UI.
* Demonstrate a complete ML lifecycle: dataset → training → deployment → prediction.
* Build a reusable architecture where additional models can be integrated later.

## Success Metrics

* Prediction response time under 3 seconds.
* API success rate above 95%.
* Fully responsive UI across devices.
* Model prediction consistency with training dataset patterns.

---

# 3. Problem Statement

Property prices in Navi Mumbai vary significantly depending on multiple features such as location, size, property age, and amenities. Manual estimation methods are inconsistent and time-consuming.

This application will:

* Automate price estimation using ML.
* Provide users with instant price insights.
* Demonstrate data-driven decision-making.

---

# 4. Stakeholders

* Students and Developers learning ML deployment
* Home Buyers & Sellers
* Real Estate Agents
* Workshop Mentors / Evaluators

---

# 5. Target Users & Personas

## Persona 1 — Home Buyer

Needs a quick estimate before visiting properties.

## Persona 2 — Property Seller

Wants to compare price with market trends.

## Persona 3 — Student Developer

Wants to understand how ML integrates with frontend systems.

---

# 6. Product Scope

## In Scope

* Residential property prediction
* Navi Mumbai locations only
* Linear Regression model
* Next.js frontend interface
* REST API backend
* Price comparison logic

## Out of Scope

* Authentication or user accounts
* Property listing marketplace
* Real-time market scraping
* Financial or legal verification

---

# 7. Functional Requirements

## 7.1 User Inputs

Users must be able to provide:

* Location (Dropdown)
* Area in Square Feet
* BHK Configuration
* Number of Bathrooms
* Property Age
* Parking Availability

## 7.2 System Processing

* Validate user inputs
* Convert categorical features into encoded values
* Send structured data to backend
* Run ML prediction pipeline
* Calculate derived metrics

## 7.3 System Outputs

The system must display:

* Predicted Price (INR)
* Price per Sq.Ft
* Market Comparison Status:

  * Below Market
  * Average
  * Above Market

---

# 8. Non-Functional Requirements

## Performance

* Prediction time < 3 seconds
* Lightweight backend processing

## Usability

* Beginner-friendly interface
* Minimal form complexity
* Clear error messages

## Reliability

* API should handle invalid inputs gracefully
* Model loaded once during startup

## Maintainability

* Modular backend architecture
* Reusable ML model pipeline

---

# 9. Technical Architecture

## High-Level Architecture

Frontend (Next.js)
↓ HTTP Request
Backend API (Python FastAPI/Flask)
↓
ML Prediction Engine (Scikit-Learn)

## Design Principles

* Separation of concerns
* API-first architecture
* Reusable ML modules
* Clean folder structure

---

# 10. Machine Learning Requirements

## Dataset Structure

Dataset must include:

* location
* area
* bhk
* bathrooms
* age
* parking
* price

## Data Processing Pipeline

1. Load CSV file using Pandas.
2. Handle missing values.
3. Encode location using OneHotEncoding or get_dummies.
4. Normalize numeric features if required.
5. Split dataset for training/testing.

## Model Training

* Algorithm: Linear Regression
* Train model offline via `train_model.py`
* Save trained model as `model.pkl`.

## Prediction Pipeline

* Load model at server startup.
* Convert incoming JSON to dataframe.
* Apply identical preprocessing.
* Return prediction result.

---

# 11. Backend Requirements

## API Endpoint

POST /predict/real-estate

### Request Example

{
location,
area,
bhk,
bathrooms,
age,
parking
}

### Response Example

{
predicted_price,
price_per_sqft,
market_status
}

## Backend Responsibilities

* Input validation
* Model loading
* Prediction execution
* Business logic calculation

## Folder Structure

backend/
└── app/
├── main.py
├── schemas.py
├── model/
│     ├── train_model.py
│     ├── predictor.py
│     └── model.pkl

---

# 12. Frontend Requirements

## UI Components

* Dropdown for location
* Numeric input fields
* Toggle for parking
* Predict button
* Result display card

## UX Features

* Loading spinner during prediction
* Error handling alerts
* Responsive layout
* Clean Tailwind styling

## Frontend Responsibilities

* Collect user input
* Send API request
* Display results dynamically

---

# 13. User Flow

1. User opens web application.
2. User enters property details.
3. User clicks “Predict Price”.
4. Frontend sends POST request to backend.
5. Backend processes model prediction.
6. Result displayed instantly.

---

# 14. Business Logic Rules

## Price per Sq.Ft Calculation

price_per_sqft = predicted_price / area

## Market Comparison Logic

* If predicted price < dataset average → Below Market
* If close to average → Average
* If higher → Above Market

---

# 15. Deployment Requirements

* Frontend deployed on Vercel
* Backend deployed on Render
* Environment variables for API URLs

---

# 16. Testing Requirements

## Backend Testing

* Valid JSON requests
* Missing field handling
* Model loading verification

## Frontend Testing

* Form validation
* API response rendering
* Mobile responsiveness

---

# 17. Risks & Constraints

* Small dataset may limit accuracy.
* Feature mismatch between training and prediction may cause errors.
* Incorrect encoding can break predictions.
* Deployment free-tier limits.

---

# 18. Future Enhancements

* Rental price prediction module
* Interactive price heatmap
* Dynamic model selection
* EMI calculator integration
* Multi-city expansion

---

# 19. Project Timeline

Phase 1: Dataset Preparation & Model Training
Phase 2: Backend API Development
Phase 3: Frontend Integration
Phase 4: Testing & Deployment

---

# 20. Acceptance Criteria

* Users can submit property details successfully.
* Backend returns valid price prediction.
* Frontend displays all outputs clearly.
* Application runs without runtime errors.

---
