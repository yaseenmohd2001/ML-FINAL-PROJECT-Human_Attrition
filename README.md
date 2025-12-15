# Human Attrition Prediction System (Python | ML | Streamlit)

## Overview

This project implements an AI-powered system to predict employee attrition. Using machine learning models trained on HR datasets, it provides insights into which employees are at risk of leaving, helping organizations make data-driven retention decisions.

The system features an interactive Streamlit app for real-time predictions and analytics, along with a modular pipeline for data preprocessing, model training, and evaluation.

## Key Features

- Predicts employee attrition using supervised ML models
- Interactive Streamlit web application
- Supports both single predictions and batch analysis
- Modular pipeline with data preprocessing, feature engineering, and modeling
- Visual analytics for insights into attrition patterns
- Model evaluation and performance reporting
- Reproducible and well-documented workflow

## Tech Stack

**Programming Language:** Python

**Core Libraries:**
- pandas, numpy (Data manipulation)
- scikit-learn (Machine learning)
- matplotlib, seaborn (Visualization)
- streamlit (Interactive web app)

**Version Control:** Git, GitHub

## Project Structure

```
ML-FINAL-PROJECT-Human_Attrition/
│
├── data/                       # Input datasets (CSV) and processed data
├── src/                        # Source code modules
│   ├── preprocessing.py        # Data cleaning and feature engineering
│   ├── modeling.py             # ML model training and evaluation
│   ├── prediction.py           # Functions for making predictions
│   └── utils.py                # Helper functions
│
├── app3.py                     # Streamlit app for interactive predictions
├── requirements.txt            # Project dependencies
├── README.md                   # Project documentation
└── trained_models/             # Saved ML models
```

## ML Pipeline Workflow

### Data Preprocessing
- Clean and normalize HR datasets
- Encode categorical features
- Handle missing values
- Feature scaling

### Modeling
- Train multiple ML models (e.g., Random Forest, Logistic Regression)
- Evaluate performance using metrics like accuracy, precision, recall, and F1-score
- Select the best-performing model

### Prediction & Visualization
- Predict employee attrition on new data
- Visualize key patterns and risk factors in the Streamlit app
- Provide actionable insights to HR teams

## How to Run the Project

### 1. Clone the Repository
```bash
git clone https://github.com/yaseenmohd2001/ML-FINAL-PROJECT-Human_Attrition.git
cd ML-FINAL-PROJECT-Human_Attrition
```

### 2. Create a Virtual Environment (Optional but Recommended)
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the Streamlit App
```bash
streamlit run app3.py
```

## Output

- Interactive predictions for individual employees or batch datasets
- Visualizations of attrition trends, correlations, and feature importance
- Saved ML models for reuse and deployment

## Logging and Error Handling

- Errors during preprocessing or prediction are captured in logs
- Ensures robust performance even with new or missing data
- Streamlit app provides user-friendly messages for incorrect inputs

## Project Outcome

- Developed an AI system to predict employee attrition
- Built an interactive, user-friendly dashboard for HR insights
- Trained and evaluated ML models with reproducible results
- Enabled data-driven decision-making to reduce turnover

## Future Improvements

- Integrate more advanced ML/Deep Learning models for higher accuracy
- Include real-time database integration for live employee data
- Deploy as a web service using Docker, AWS Lambda, or EC2
- Add employee retention recommendations based on model insights

## Author

**Thaha Muhammed Yaseen**

GitHub: https://github.com/yaseenmohd2001

## License

This project is for educational and portfolio purposes.
