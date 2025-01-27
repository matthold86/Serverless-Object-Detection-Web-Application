# AWS-Sagemaker-Object-Detection

This project focuses on ML Model deployment using AWS Serverless Resources! Provided an off-the-shelf YOLOV8 object detection model, we deploy a fully serviced web application for uploading an image and viewing the resultant object-detected processed image with bounding boxes and classifications directly on the web application interface. Image processesing and model inference are broken into isolated microservices and managed through API gateways and lambda functions. The lambda functions are organized into a broader AWS Step Function for handling parallel workflows. An instance of the YOLOV8 model is deployed through AWS Sagemaker and the image metadata is stored in an AWS S3 bucket. For more information on each microservice check out the Primary Microservice repository links at the bottom of this ReadMe. A demonstration of the application output is shown in the video below as well.


![object-detection-web-application](https://github.com/matthold86/Serverless-Object-Detection-Web-Application/assets/114833075/78ba2acb-68b0-459f-8e8c-931dab4d3aef)


Step Function Architecture:
![image](https://github.com/matthold86/Serverless-Object-Detection-Web-Application/assets/114833075/17bb2e4c-f4b8-44ec-a14d-bf1fc28e93f1)

Link to Primary Microservices:

- **Image Preprocessing**: https://github.com/matthold86/image_preprocessing_lambda

- **Model Inference**: https://github.com/matthold86/AWS-sagemaker-inference-lambda

- **Image Postprocessing**: https://github.com/matthold86/image-postprocessing-lambda


