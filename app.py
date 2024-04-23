import streamlit as st
import requests
import boto3
from io import BytesIO

def upload_to_s3(presigned_url, file_buffer):
    """ Uploads an image to S3 using a pre-signed URL """
    response = requests.put(presigned_url, data=file_buffer)
    return response.status_code == 200

# Streamlit user interface
st.title('Upload Image to S3 wahoo')

# File uploader widget
uploaded_file = st.file_uploader("Choose an image...", type=['jpg'])

if uploaded_file is not None:
    # Display the uploaded image
    st.image(uploaded_file, caption='Uploaded Image', use_column_width=True)

    # Button to upload to S3
    if st.button('Upload to S3'):
        # Prepare the JSON payload with the file name
        file_name = uploaded_file.name.rsplit('.', 1)[0]
        payload = {'file_name': file_name}

        # Make HTTP POST request to your API Gateway to get the presigned URL
        try:
            api_url = "https://lt2mw7lpi2.execute-api.us-east-2.amazonaws.com/default/s3presignkey_yolov8"  # Update this with your API Gateway URL
            headers = {"Content-Type": "application/json"}
            response = requests.post(api_url, json=payload, headers=headers)
            response.raise_for_status()
            presigned_url = response.json().get('url')
            
            # Upload image to S3 using the presigned URL
            file_buffer = BytesIO(uploaded_file.getvalue())
            success = upload_to_s3(presigned_url, file_buffer)
            
            if success:
                st.success('Image successfully uploaded to S3.')
            else:
                st.error('Failed to upload image to S3.')
        except requests.RequestException as e:
            st.error(f'Failed to get presigned URL: {e}')