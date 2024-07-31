import model_utils as utils
import argparse
import argparse


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='train a yolov8x model')
    parser.add_argument('Datapath', type=str, help='Path to the Data.yaml file of the roboflow download')

    args = parser.parse_args()

    # dataset = utils.download_data(apikey="tbgnNS8bCW5iRz1lVg3O", workspace="deep-learning-q1acw",
                #    project="trash-detection-new-categories", version=1, model="yolov8")
    datapathyaml = args.Datapath
    model = utils.initialize_and_train_model(datapathyaml=datapathyaml)
    val_results = utils.validate_model(model, datapathyaml)
    print(val_results)

