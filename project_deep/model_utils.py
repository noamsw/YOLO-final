from roboflow import Roboflow
from ultralytics import YOLO
def download_data(apikey="tbgnNS8bCW5iRz1lVg3O", workspace="deep-learning-q1acw",
                   project="trash-detection-new-categories", version=2, model="coco"):

    # Initialize the Roboflow object with your API key
    rf = Roboflow(api_key=apikey, )
    # Retrieve your current workspace and project name
    project = rf.workspace(workspace).project(project)
    # download the dataset
    dataset = project.version(version).download(model)
    return dataset

#training 
def initialize_and_train_model(datapathyaml, yolomodel='yolov8x'):
# yolov8x-p2.yaml
    model = YOLO(yolomodel).load('yolov8x.pt')
    # Use the model
    # datapathyaml = str(dataset.location) +  "/data.yaml"
    model.train(data=datapathyaml, epochs=150, imgsz=640, batch=-1)  # train the model
    # model.train(data=datapathyaml, epochs=150, imgsz=640, patience=25, batch=-1, dropout=0.3, weight_decay=0.005,
    #             lrf=0.0001, lr0=0.01, cls=1.0, label_smoothing=0.1)  # train the model
    # metrics = model.val()  # evaluate model performance on the validation set
    # results = model("https://ultralytics.com/images/bus.jpg")  # predict on an image
    # path = model.export(format="onnx")  # export the model to ONNX format
    return model

def validate_model(model, testdatapathyaml):
    # datapathyaml = str(dataset.location) +  "/data.yaml"
    val_results = model.val(data=testdatapathyaml, save_json=True)
    return val_results

def predict(model, source):
    prediction = model.predict(source=source, save=True, save_json=True)
    return prediction

