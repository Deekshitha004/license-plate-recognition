import streamlit as st
from PIL import Image
import pytesseract
import cv2
import numpy as np
import base64

st.set_page_config(layout="wide")

# Set Tesseract OCR path
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Define states dictionary
states = {
    "AN": "Andaman and Nicobar Islands", "AP": "Andhra Pradesh", "AR": "Arunachal Pradesh", "AS": "Assam",
    "BH": "Bharat", "BR": "Bihar", "CH": "Chandigarh", "CG": "Chhattisgarh",
    "DD": "Dadra and Nagar Haveli and Daman and Diu", "DL": "Delhi", "GA": "Goa", "GJ": "Gujarat",
    "HR": "Haryana", "HP": "Himachal Pradesh", "JK": "Jammu and Kashmir", "JH": "Jharkhand",
    "KA": "Karnataka", "KL": "Kerala", "LD": "Lakshadweep", "MP": "Madhya Pradesh", "MH": "Maharashtra",
    "MN": "Manipur", "ML": "Meghalaya", "MZ": "Mizoram", "NL": "Nagaland",
    "OD": "Odisha", "PY": "Puducherry", "PB": "Punjab", "RJ": "Rajasthan",
    "SK": "Sikkim", "TN": "Tamil Nadu", "TS": "Telangana", "TR": "Tripura",
    "UP": "Uttar Pradesh", "UK": "Uttarakhand", "WB": "West Bengal"
}

# Read and encode the image file
with open(r"C:\Users\deekshu\Pictures\py projects\streamlit-dll\car pics\car bg.jpg", "rb") as image_file:
    encoded_image = base64.b64encode(image_file.read()).decode()

def main():
    st.title("License Plate Recognition App")

    st.sidebar.markdown(
        f"""
        <style>
        [data-testid="stSidebar"] > div:first-child {{
            
            background: url(data:image/png;base64,{encoded_image});
            background-size: cover;
            height: 100vh;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.sidebar.header("Navigation")
    page = st.sidebar.radio("Go to", ["Home", "License Plate Recognition"])

    if page == "Home":
        st.markdown(
            """
            <style>
            .box-with-shadow {
                background-color: lightgrey;
                width: auto;
                height: auto;
                text: verdana;
                color: white;
                font-size: 40px;
                border: 5px solid black;
                padding: 50px;
                margin: 20px;
            }
            </style>
            """,
            unsafe_allow_html=True
        )
        st.markdown('<div class="box-with-shadow"> License Plate Recognition</div>', unsafe_allow_html=True)

    elif page == "License Plate Recognition":
        st.subheader("Upload Image")
        uploaded_file = st.file_uploader("Choose a file", type=['png', 'jpeg', 'jpg'])

        if uploaded_file is not None:
            image = Image.open(uploaded_file)
            st.image(image, caption='Uploaded Image', use_column_width=True)

            if st.button("Process Image"):
                # Process image and perform license plate recognition
                process_image(image)

def process_image(image):
    gray_plates = None
    st.markdown("----")
    img_array = np.array(image)  # Convert PIL Image to NumPy array
    text = pytesseract.image_to_string(img_array)

    gray = cv2.cvtColor(img_array, cv2.COLOR_BGR2GRAY)
    cascade = cv2.CascadeClassifier('haarcascade_russian_plate_number (1).xml')
    plates = cascade.detectMultiScale(gray, 1.2, 5)

    for (x, y, w, h) in plates:
        cv2.rectangle(img_array, (x, y), (x + w, y + h), (0, 255, 0), 2)
        
        gray_plates = gray[y:y + h, x:x + w]
       
        color_plates = img_array[y:y + h, x:x + w]
        

        try:
            text1 = pytesseract.image_to_string(gray_plates)

            if text1:
                state_code = text1[0:2]
                print("State Code:", state_code)

                try:
                    state_name = states[state_code]
                    print("State Name:", state_name)
                    st.success("Car belongs to " + state_name)
                except KeyError:
                    st.error("Car is not recognized")
            else:
                st.warning("No text detected on the license plate.")

        except Exception as e:
            st.error(f"An error occurred: {e}")

    st.divider()
    if gray_plates is not None:
        st.image([color_plates], caption='Detected License Plate', use_column_width=True)

if __name__ == "__main__":
    main()
