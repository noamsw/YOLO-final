import os
import shutil
import json
import argparse
# this script unifies the batches into one large batch, renaming the images
# and updating the annotations. It also consolidates the many categories into 
# larger super categories
# variables

# data_folder = "/home/noamwolf/taco/TACO/data"
# annotations_file = "/home/noamwolf/taco/TACO/data/annotations.json"
# output_folder = "/home/noamwolf/taco/united_data"
log_folder = "/home/noamwolf/taco/TACO/log"


glass = ["Glass bottle", "Broken glass", "Glass jar","Glass cup", ]
plastic_and_metal = [
                    "Clear plastic bottle","Other plastic bottle", 
                    "Disposable plastic cup","Other plastic cup",
                    "Plastic lid","Spread tub", "Other plastic container",
                    "Aerosol", "Drink can", "Food Can", 
                    "Metal lid",]
other_plastic = [
            "Plastic bottle cap","Six pack rings", 
            "Polypropylene bag", "Tupperware", "Disposable food container",
            "Plastic glooves", "Plastic utensils", 
            "Plastic straw", "Other plastic", "Plastic film","Single-use carrier bag",
            "Garbage bag",]

        
cigarette = ["Cigarette",]
non_recyclable = [
            "Aluminium blister pack", "Carded blister pack",
            "Meal carton", "Pizza box",
            "Paper cup", "Foam cup",
            "Wrapping paper",
            "Magazine paper", 
            "Plastified paper bag",
            "Other plastic wrapper", "Foam food container",
            "Rope & strings", "Shoe", "Squeezable tube",
            "Styrofoam piece", "Drink carton", "Crisp packet",]

other = ["Battery", "Unlabeled litter", "Aluminium foil", 
            "Metal bottle cap",  "Pop tab", "Scrap metal", "Food waste",]

paper = [
            "Corrugated carton", "Egg carton", "Toilet tube",
            "Other carton", "Normal paper", "Paper bag",
            "Tissues", "Paper straw",]


# functions
def open_log_file(log_file_path):
    if not os.path.exists(log_file_path):
        with open(log_file_path, 'w') as file:
            file.write("Log File:\n")
            print(f'file {log_file_path} created')

def log_to_file(message, log_file_path=log_folder):
    with open(log_file_path, 'a') as file:
        file.write(message + "\n")


# rename the file names in annotations to match the new names
# consolidate the 60 categories into 7       
def taco_label_to_new_label(label):
    categories = {"glass":0, "plastic_and_metal":1, "other_plastic":2, "cigarette":3, "non_recyclable":4,
        "paper":5, "other":6}
    if (label in glass):
        label = "glass"
    elif (label in plastic_and_metal):
        label = "plastic_and_metal"
    elif(label in other_plastic):
        label = "other_plastic"
    elif (label in cigarette):
        label = "cigarette"
    elif(label in non_recyclable):
        label = "non_recyclable"
    elif(label in paper):
        label = "paper"
    else:
        # print(label, "is non-taco label")
        label = "other"
    id = categories[label]
    return id, label





def move_and_rename_images(source_folder):
    images_folder = os.path.join(source_folder, "images")
    os.makedirs(images_folder, exist_ok=True)

    count = 0
    name_mapping = {}
    for batch_folder in os.listdir(source_folder):
        batch_path = os.path.join(source_folder, batch_folder)
        if os.path.isdir(batch_path) and batch_folder.startswith("batch_"):
            for filename in os.listdir(batch_path):
                if filename.lower().endswith((".jpg", ".jpeg", ".JPG")):
                    new_filename = f"{count:06}.jpg"
                    source_filepath = os.path.join(batch_path, filename)
                    target_filepath = os.path.join(images_folder, new_filename)
                    shutil.move(source_filepath, target_filepath)
                    full_filename = os.path.join(batch_folder, filename)
                    name_mapping[full_filename] = new_filename
                    count += 1
                else:
                    print(f'Ignoring non-image file: {filename}')

    return name_mapping
###
# def move_and_rename_images(source_folder):


#     # Create a new folder named "images" within the base folder
#     images_folder = os.path.join(source_folder, "images")
#     # print(images_folder)
#     os.makedirs(images_folder, exist_ok=True)
#     # print(f'source folder {source_folder}')
#     count = 0
#     name_mapping = {}
#     for batch_folder in os.listdir(source_folder):
#         batch_path = os.path.join(source_folder, batch_folder)
#         if os.path.isdir(batch_path):
#             for filename in os.listdir(batch_path):
#                 if filename.endswith(".jpg") or filename.endswith(".JPG"):
#                     new_filename = f"{count:06}.jpg"
#                     source_filepath = os.path.join(batch_path, filename)
#                     target_filepath = os.path.join(source_folder, 'images', new_filename)
#                     # print(f'source file: {source_filepath}, target file: {target_filepath}')
#                     shutil.move(source_filepath, target_filepath)
#                     full_filename = os.path.join(batch_folder, filename)
#                     name_mapping[full_filename] = new_filename
#                     # log_message = f'{full_filename}: {new_filename}'
#                     # log_to_file(log_message)
#                     count += 1
#                 else:
#                     print(f'weird file: {filename}')
#     # print(f'count {count}')
#     return name_mapping


# def create_labels_mapping(annotations_file):
#     with open(annotations_file) as f:
#         annotations = json.load(f)
#     labels_mapping = {}
#     for cat in annotations['categories']:
#         old_label = cat['name']
#         label_id, new_label = taco_label_to_new_label(old_label)
#         cat['name'] = new_label
#         cat['id'] = label_id
#         cat['supercategory'] = new_label
#         if old_label not in labels_mapping:
#             labels_mapping[old_label] = new_label
#     return labels_mapping



def update_annotations_file(annotations_file, name_mapping):
    with open(annotations_file) as f:
        annotations = json.load(f)
    # update file name in annotations
    for image in annotations['images']:
        old_file_name = image['file_name']
        # log_to_file(f'attempting to search key:{old_file_name}')
        if old_file_name in name_mapping:
            new_image_name = name_mapping[old_file_name]
            if new_image_name:
                image["file_name"] = new_image_name
        else:
            print("houston we have a problem")
            print(f'{old_file_name} is not a key in namemappings')

    # update the categories, and create a labels mapping
    cat_ids_mapping = {}
    filtered_categories_list = []
    new_ids_list = set()
    for cat in annotations['categories']:
        old_label = cat['name']
        old_id = cat['id']
        new_category_id, new_label = taco_label_to_new_label(old_label)
        cat_ids_mapping[old_id] = new_category_id
        if new_category_id not in new_ids_list:
            new_ids_list.add(new_category_id)
            filtered_categories_list.append(cat)
        cat['name'] = new_label
        cat['id'] = new_category_id
        cat['supercategory'] = new_label
    # print(filtered_categories_list)
    annotations['categories'] = filtered_categories_list

    # update the annotations to new category ids
    for ann in annotations['annotations']:
        old_category_id = ann['category_id']
        new_category_id = cat_ids_mapping[old_category_id]
        ann['category_id'] = new_category_id

    with open(annotations_file, 'w') as f:
        json.dump(annotations, f, indent=4)


def main():
    parser = argparse.ArgumentParser(description='Process TACO data and annotations')
    parser.add_argument('DataDir', type=str, help='Path to the Data folder that contains batches of images and annotations')
    args = parser.parse_args()

    DataDir = args.DataDir
    name_mapping = move_and_rename_images(DataDir)
    annotations_file = os.path.join(DataDir, "annotations.json")
    # print(annotations_file)
    update_annotations_file(annotations_file, name_mapping)

if __name__ == "__main__":
    main()

# if __name__ == "__main__":
#     # open_log_file(log_folder)
#     name_mapping = move_and_rename_images(data_folder, output_folder)
#     update_annotations_file(annotations_file, output_folder, name_mapping)
