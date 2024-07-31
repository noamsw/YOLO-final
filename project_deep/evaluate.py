import model_utils as utils
from ultralytics import YOLO
import argparse



def main():
    parser = argparse.ArgumentParser(description='evaluate model on a test set')
    parser.add_argument('weights', type=str, help='Path to the file containing the weights')
    parser.add_argument('testpath', type=str, help='Path to the data.yaml folder in the dataset used for validation')

    args = parser.parse_args()

    weightspath = args.weights
    testpath = args.testpath

    model = YOLO(weightspath)
    metrics = utils.validate_model(model, testpath)

    mAP = metrics.box.map    # map50-95
    mAP50 = metrics.box.map50  # map50
    mAP75 = metrics.box.map75  # map75
    mAPlist = metrics.box.maps   # a list 

    print(f"mAP50-95: {mAP}")
    print(f"mAP50: {mAP50}")
    print(f"mAP75: {mAP75}")
    print(f"mAPlist: {mAPlist}")

if __name__ == "__main__":
    main()   



