from flask import Flask
import cv2
# from ultralytics import YOLO
from azure.storage.blob import BlobServiceClient #, BlobClient, ContainerClient
# from azure.identity import DefaultAzureCredential

app = Flask(__name__)

@app.route("/")
def hello():

    # cap = cv2.VideoCapture('https://mozaikface.blob.core.windows.net/video/KakaoTalk_20231221_131436011.mp4')
    cap = cv2.VideoCapture('https://mozaikface.blob.core.windows.net/video/KakaoTalk_20240203_202132549.mp4')
    
    if not cap.isOpened():
        return "Cannot open"
        
    # # load a pretrained YOLOv8n model
    # model = YOLO("yolov8n.pt", "v8")
    
    ret, frame = cap.read()
    H, W, _ = frame.shape
    # localmp4 = 'KakaoTalk_20231221_131436011_out.mp4'
    localmp4 = 'KakaoTalk_20240203_202132549_out.mp4'
    # out = cv2.VideoWriter(localmp4, cv2.VideoWriter_fourcc(*'mp4v'), int(cap.get(cv2.CAP_PROP_FPS)), (W, H))
    out = cv2.VideoWriter(localmp4, cv2.VideoWriter_fourcc('m', 'p', '4', 'v'), int(cap.get(cv2.CAP_PROP_FPS)), (W, H))

    threshold = 0.5
    while ret:
        # results = model(frame)[0]

        # for result in results.boxes.data.tolist():
        #     x1, y1, x2, y2, score, class_id = result

        # if score > threshold:
        #     cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 4)
        #     cv2.putText(frame, results.names[int(class_id)].upper(), (int(x1), int(y1 - 10)),
        #                 cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 255, 0), 3, cv2.LINE_AA)

        out.write(frame)
        ret, frame = cap.read()
    
    cap.release()
    out.release()
    # cv2.destroyAllWindows()
    
    # Create the BlobServiceClient object
    blob_service_client = BlobServiceClient.from_connection_string('DefaultEndpointsProtocol=https;AccountName=mozaikface;AccountKey=Qt8tdH03hw3WpPmG10NOo2cU5sCwqeth1brj6XOURH4WWeW5Mp8qdOCiW+v+tFccPMpuR0Zh2qgo+AStvG7wdg==;EndpointSuffix=core.windows.net') # (account_url, credential=default_credential)
    # container_client = blob_service_client.create_container('video')
    blob_client = blob_service_client.get_blob_client(container='video', blob=localmp4)
    with open(file=localmp4, mode="rb") as data:
        blob_client.upload_blob(data)

    return "Hello, World!3"


    # account_url = "https://mozaikface.blob.core.windows.net/"
    # # connect_str = os.getenv('AZURE_STORAGE_CONNECTION_STRING')
    # # default_credential = DefaultAzureCredential()
