import os
import argparse
import json
import shutil
from pycocotools.coco import COCO





def update_img_and_label_names(source_folder):
    test_images_folder = os.path.join(source_folder, "images")
    test_labels_folder = os.path.join(source_folder, "labels")
    annotaionspath = os.path.join(source_folder, "_annotations.coco.json")


    coco = COCO(annotaionspath)

    img_id_mapping = {}
    for img_id in coco.getImgIds():
        img_info = coco.loadImgs(img_id)[0]
        img_id_mapping[img_info['file_name']] = img_id


    imgfilelist = []
    labelfilelist = []
    
    for full_img_name in os.listdir(test_images_folder):
        # label_name = (full_label_name.split(".rf")[0])
        imgfilelist.append(full_img_name)


    for full_label_name in os.listdir(test_labels_folder):
        # label_name = (full_label_name.split(".rf")[0])
        labelfilelist.append(full_label_name)


    for full_img_name in imgfilelist:
        # img_name = (full_img_name.split(".rf")[0])
        # img_name = img_name.lower().split('_jpg')[0]
        # img_name = img_name + '.jpg'
        img_id = img_id_mapping[full_img_name]
        new_name =   str(img_id) + ".jpg"
        oldimgpath = os.path.join(test_images_folder, full_img_name)
        newimgpath = os.path.join(test_images_folder, new_name)
        os.rename(oldimgpath, newimgpath)


    for full_label_name in labelfilelist:
        label_name = (full_label_name.split(".txt")[0])
        # label_name = label_name.lower().split('_jpg')[0]
        # label_name = label_name + '.jpg'
        label_name = label_name + '.jpg'
        img_id = img_id_mapping[label_name]
        new_name =   str(img_id) + ".txt"
        oldlabelpath = os.path.join(test_labels_folder, full_label_name)
        newlabelpath = os.path.join(test_labels_folder, new_name)
        os.rename(oldlabelpath, newlabelpath)



def main():
    parser = argparse.ArgumentParser(description='Process test set and labels for coco eval')
    parser.add_argument('DataDir', type=str, help='Path to the Data folder that contains test images,labels and annotations in COCO format')

    args = parser.parse_args()

    DataDir = args.DataDir


    update_img_and_label_names(DataDir)

if __name__ == "__main__":
    main()   