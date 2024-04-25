import streamlit as st
import requests
import boto3
from io import BytesIO
import time

status_dict = {
    "preprocessing": "Image Preprocessing",
    "inference": "Performing Inference",
    "postprocessing": "Image Postprocessing",
    "complete": "Detection Complete"
}

def upload_to_s3(presigned_url, file_buffer):
    """ Uploads an image to S3 using a pre-signed URL """
    response = requests.put(presigned_url, data=file_buffer)
    return response.status_code == 200

def check_status(image_id):
    """ Polls the status endpoint to check the processing status """
    payload = {'image_id': image_id}
    statuscheck_api = "https://4md0ddt1p1.execute-api.us-east-2.amazonaws.com/default/yolov8-statuscheck"
    headers = {"Content-Type": "application/json"}
    time.sleep(3)
    # Create a placeholder for the status text
    status_text = st.empty()
    with st.spinner(''):
        while True:
            response = requests.post(statuscheck_api, json=payload, headers=headers)
            if response.status_code == 200:
                status_data = response.json()
                status = status_data['status']
                display_text = status_dict.get(status, "Processing...")
                status_text.text(f'{display_text}')
                if status_data['status'] == 'complete':
                    s3 = status_data['S3_object_key']
                    return s3
                
            elif response.status_code == 404:
                st.error("Job not found.")
                break
            time.sleep(5)  # Delay for 5 seconds before checking again

# Streamlit user interface
st.title('Serverless Object Detection Web Application')

# File uploader widget
uploaded_file = st.file_uploader("Choose an image...", type=['jpg'])

# UI Design
# st.set_page_config(page_title='Image Processing App', page_icon=":camera:", layout='wide')
# st.title('Serverless Object Detection Web Application')

# col1, col2 = st.columns(2)
# with col1:
#     uploaded_file = st.file_uploader("Choose an image...", type=['jpg'])
# if uploaded_file is not None:
#     with col2:
#         st.image(uploaded_file, caption='Uploaded Image', use_column_width=True)

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
            api_url = "https://lt2mw7lpi2.execute-api.us-east-2.amazonaws.com/default/s3presignkey_yolov8"
            headers = {"Content-Type": "application/json"}
            response = requests.post(api_url, json=payload, headers=headers)
            response.raise_for_status()
            result = response.json()
            presigned_url = result.get('url')
            image_id = result.get('image_id')
            
            # Upload image to S3 using the presigned URL
            file_buffer = BytesIO(uploaded_file.getvalue())
            if upload_to_s3(presigned_url, file_buffer):
                st.success('Image successfully uploaded to S3. Processing...')
                # Start polling for status
                final_image_S3key = check_status(image_id)
                st.image(f"{final_image_S3key}", caption='Processed Image')
            else:
                st.error('Failed to upload image to S3.')
        except requests.RequestException as e:
            st.error(f'Failed to communicate with the server: {e}')





# import streamlit as st
# import requests
# import time
# from io import BytesIO

# def upload_to_s3(presigned_url, file_buffer):
#     """ Uploads an image to S3 using a pre-signed URL """
#     response = requests.put(presigned_url, data=file_buffer)
#     return response.status_code == 200

# def check_status(job_id):
#     """ Polls the status endpoint to check the processing status """
#     status_url = f"https://yourstatusapi.com/status/{job_id}"  # Update with your actual status check URL
#     while True:
#         response = requests.get(status_url)
#         if response.status_code == 200:
#             status_data = response.json()
#             if status_data['status'] == 'completed':
#                 return status_data['object_key']
#         time.sleep(5)  # Delay for 5 seconds before checking again

# # Streamlit user interface
# st.title('Upload and Process Image')

# # File uploader widget
# uploaded_file = st.file_uploader("Choose an image...", type=['jpg'])

# if uploaded_file is not None:
#     # Display the uploaded image
#     st.image(uploaded_file, caption='Uploaded Image', use_column_width=True)

#     # Button to upload to S3 and start processing
#     if st.button('Upload and Process'):
#         # Prepare the JSON payload with the file name
#         file_name = uploaded_file.name.rsplit('.', 1)[0]
#         payload = {'file_name': file_name}

#         # Make HTTP POST request to get the presigned URL and initiate processing
#         api_url = "https://lt2mw7lpi2.execute-api.us-east-2.amazonaws.com/default/s3presignkey_yolov8"  # Update this with your API Gateway URL for presigned URLs
#         try:
#             response = requests.post(api_url, json=payload)
#             response.raise_for_status()
#             result = response.json()
#             presigned_url = result.get('url')
#             job_id = result.get('job_id')  # Assume the API also returns a job ID for status checks

#             # Upload image to S3 using the presigned URL
#             file_buffer = BytesIO(uploaded_file.getvalue())
#             if upload_to_s3(presigned_url, file_buffer):
#                 st.success('Image successfully uploaded to S3. Processing...')
#                 # Start polling for status
#                 final_image_key = check_status(job_id)
#                 st.image(f"https://yourbucket.s3.amazonaws.com/{final_image_key}", caption='Processed Image')
#             else:
#                 st.error('Failed to upload image to S3.')
#         except requests.RequestException as e:
#             st.error(f'Failed to communicate with the server: {e}')
