import streamlit as st                  # create web apps
import pandas as pd                   # data manipulation 
import numpy as np
import pickle
from sklearn.preprocessing import StandardScaler, LabelEncoder
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

uri = "mongodb+srv://vishal:vishal1234@cluster0.ypqfx7x.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(uri, server_api=ServerApi("1"))
db = client["student"]
collection = db["student_pred"]


def load_model():                                   #  for pysical file
    with open("stud_per_app/student_lr_final_model.pkl", 'rb') as file:
        model,scaler,le=pickle.load(file)
    return model,scaler,le

def preprocesssing_input_data(data,scaler,le):
    data['Extracurricular Activities']= le.transform([data['Extracurricular Activities']])[0]
    df = pd.DataFrame([data])
    df_transformed = scaler.transform(df)
    return df_transformed

def predict(data):
    model,scaler,le = load_model()
    processed_data = preprocesssing_input_data(data,scaler,le)
    prediction = model.predict(processed_data)
    return prediction

def main():
    st.title("Student Performance Prediction App")
    st.write("Enter your data to get a prediction for your performance:")

    Hours_Studied = st.number_input("Hours Studied", min_value = 1, max_value = 10, value = 5)
    Previous_Score = st.number_input("Previous Score", min_value = 40, max_value = 100, value = 70)
    Extra = st.selectbox("Extra Curricular Activities", ["Yes", "No"])
    Sleeping_hour = st.number_input("Sleeping hours", min_value = 4, max_value = 10, value = 7)
    Number_of_quetion_paper_solved = st.number_input("Number of quetion paper solved", min_value = 0, max_value = 10, value = 5)

    if st.button("predict_your_score"):
        user_data = {
            'Hours Studied': Hours_Studied,
            'Previous Scores': Previous_Score,
            'Extracurricular Activities': Extra,
            'Sleep Hours': Sleeping_hour,
            'Sample Question Papers Practiced': Number_of_quetion_paper_solved
        }
        prediction = predict(user_data)
        st.success(f"your prediction result is {prediction}")
        user_data['prediction'] = round(float(prediction[0]),2 )               # add one more key
        user_data = {key: int(value) if isinstance(value, np.integer) else float(value) if isinstance(value, np.floating) else value for key,value in user_data.items()}
        collection.insert_one(user_data)

        



if __name__ == '__main__':
    main()


   



   # for run>>   cd ".\FSDS\stud_per_app\"
   # ls
   # streamlit run stud_per.py