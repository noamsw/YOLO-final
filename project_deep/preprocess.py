import os
import argparse
import json
import shutil


def move_and_rename_images(source_folder, test_anns):
    train_images_folder = os.path.join(source_folder, "train_images")
    os.makedirs(train_images_folder, exist_ok=True)
    test_images_folder = os.path.join(source_folder, "test_images")
    os.makedirs(test_images_folder, exist_ok=True)

    try:
        with open(test_anns, 'r') as file:
            
            content = file.read()
            for batch_folder in os.listdir(source_folder):
                batch_path = os.path.join(source_folder, batch_folder)
                if os.path.isdir(batch_path) and batch_folder.startswith("batch_"):
                    for filename in os.listdir(batch_path):
                        if filename.lower().endswith((".jpg", ".jpeg", ".JPG")):
                            new_filename = f"{batch_folder}_{filename}"

                            if new_filename in content:
                                source_filepath = os.path.join(batch_path, filename)
                                target_filepath = os.path.join(test_images_folder, new_filename)
                                shutil.move(source_filepath, target_filepath)

                            else:
                                source_filepath = os.path.join(batch_path, filename)
                                target_filepath = os.path.join(train_images_folder, new_filename)
                                shutil.move(source_filepath, target_filepath)
                        else:
                            print(f'Ignoring non-image file: {filename}')
    except FileNotFoundError:
            print("File not found.")





# update annotation files
def update_annotations_file(annotations_file):
    with open(annotations_file) as f:
        annotations = json.load(f)
    # update file name in annotations
    for image in annotations['images']:
        old_file_name = image['file_name']
        batch, num = old_file_name.split('/')
        image["file_name"] = f'{batch}_{num}'
    
    with open(annotations_file, 'w') as f:
        json.dump(annotations, f, indent=4)


def main():
    parser = argparse.ArgumentParser(description='Process TACO data and annotations')
    parser.add_argument('DataDir', type=str, help='Path to the Data folder that contains batches of images and annotations (test plus train)')
    args = parser.parse_args()


    DataDir = args.DataDir
    train_anns = 'annotations_train.json'
    train_anns = os.path.join(DataDir, train_anns)
    test_anns = 'annotations_test.json'
    test_anns = os.path.join(DataDir, test_anns)


    update_annotations_file(train_anns)
    update_annotations_file(test_anns)
    move_and_rename_images(DataDir, test_anns)

if __name__ == "__main__":
    main()