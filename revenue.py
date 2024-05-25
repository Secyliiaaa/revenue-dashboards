import joblib
import numpy as np
import streamlit as st

# Load the trained model
model = joblib.load('best_decision_tree_model.pkl')

# Streamlit UI
st.title('Revenue Growth Prediction')

# Input features
features_input = st.text_input('Input features (comma separated):')
features = [float(x) for x in features_input.split(',')] if features_input else []

if st.button('Predict'):
    if features:
        prediction = model.predict([features])
        st.write(f'Prediction: {prediction[0]}')
    else:
        st.write('Please input features')