
import os
import requests
import streamlit as st

st.set_page_config(page_title="SuperKart Sales Forecast", page_icon="🛒")

st.title("SuperKart Sales Forecast")
st.write("Enter product and store information to forecast product-store sales.")

BACKEND_URL = os.getenv("BACKEND_URL", "http://superkart-backend:7860")
PREDICT_URL = f"{BACKEND_URL}/v1/predict"

product_weight = st.number_input("Product Weight", min_value=0.0, value=12.66)
product_sugar_content = st.selectbox(
    "Product Sugar Content", ["Low Sugar", "Regular", "No Sugar"]
)
product_allocated_area = st.number_input(
    "Product Allocated Area", min_value=0.0, value=0.027, format="%.4f"
)
product_mrp = st.number_input("Product MRP", min_value=0.0, value=117.08)

store_size = st.selectbox("Store Size", ["Small", "Medium", "High"])
store_location = st.selectbox(
    "Store Location City Type", ["Tier 1", "Tier 2", "Tier 3"]
)
store_type = st.selectbox(
    "Store Type",
    ["Departmental Store", "Food Mart", "Supermarket Type1", "Supermarket Type2"],
)

product_id_char = st.selectbox("Product ID Prefix", ["FD", "NC", "DR"])
store_age_years = st.number_input(
    "Store Age (Years)", min_value=0, value=16, step=1
)
product_type_category = st.selectbox(
    "Product Type Category", ["Perishables", "Non Perishables"]
)

if st.button("Predict Sales"):
    payload = {
        "Product_Weight": product_weight,
        "Product_Sugar_Content": product_sugar_content,
        "Product_Allocated_Area": product_allocated_area,
        "Product_MRP": product_mrp,
        "Store_Size": store_size,
        "Store_Location_City_Type": store_location,
        "Store_Type": store_type,
        "Product_Id_char": product_id_char,
        "Store_Age_Years": store_age_years,
        "Product_Type_Category": product_type_category,
    }

    try:
        response = requests.post(PREDICT_URL, json=payload, timeout=30)

        if response.ok:
            prediction = response.json()["prediction"]
            st.success(f"Predicted Sales: {prediction:,.2f}")
        else:
            st.error(f"Prediction failed: {response.text}")
    except requests.RequestException as exc:
        st.error(f"Could not connect to the backend: {exc}")
