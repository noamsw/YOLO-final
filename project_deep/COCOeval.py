from pycocotools.coco import COCO
from pycocotools.cocoeval import COCOeval
import argparse
import json



def evaluate(Ground, Pred):
    #load annotation files
    cocoGt = COCO(Ground)
    cocoDt = cocoGt.loadRes(Pred)

    # running evaluation
    cocoEval = COCOeval(cocoGt,cocoDt, 'bbox')
    cocoEval.evaluate()
    cocoEval.accumulate()
    cocoEval.summarize()

def main():
    parser = argparse.ArgumentParser(description='Preform COCO eval')
    parser.add_argument('Ground', type=str, help='Path to Ground Truth file')
    parser.add_argument('Pred', type=str, help='Path to predictions file')

    args = parser.parse_args()

    Ground = args.Ground
    Pred = args.Pred

    evaluate(Ground, Pred)

if __name__ == "__main__":
    main()