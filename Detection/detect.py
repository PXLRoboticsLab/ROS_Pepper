#!/usr/bin/env python
import numpy as np
import cv2
import argparse
import os
from matplotlib import pyplot as plt

MIN_MATCH_COUNT = 10
valid_image_extensions = [".jpg", ".jpeg", ".png", ".tif", ".tiff"]
image_path_list = []


class detect:
    def __init__(self, args):
        self.successfull = 0
        self.sift = cv2.xfeatures2d.SIFT_create()

        FLANN_INDEX_KDTREE = 0
        index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
        search_params = dict(checks=50)

        self.flann = cv2.FlannBasedMatcher(index_params, search_params)

        for file in os.listdir(args.in_path):
            extension = os.path.splitext(file)[1]
            if extension.lower() not in valid_image_extensions:
                continue
            image_path_list.append(file)
        self.search(args)


    def search(self, args):
        # load query image
        img1 = cv2.imread(args.find, 0)

        # repeat for the number specified in args
        for i in range(args.number):
            # load image
            print(args.in_path + image_path_list[i])
            img2 = cv2.imread(args.in_path + image_path_list[i], 0)

            # find the keypoints and descriptors with SIFT
            kp1 = self.sift.detect(img1,None)
            kp2 = self.sift.detect(img2,None)
            des1 = self.sift.compute(img1, kp1)
            des2 = self.sift.compute(img2, kp2)

            matches = self.flann.knnMatch(des1[1], des2[1], k=2)

            # store all the good matches as per Lowe's ratio test.
            good = []
            for m,n in matches:
                if m.distance < 0.7*n.distance:
                    good.append(m)

            if len(good)>MIN_MATCH_COUNT:
                src_pts = np.float32([ kp1[m.queryIdx].pt for m in good ]).reshape(-1,1,2)
                dst_pts = np.float32([ kp2[m.trainIdx].pt for m in good ]).reshape(-1,1,2)

                M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC,5.0)
                # matchesMask = mask.ravel().tolist()

                h,w = img1.shape
                pts = np.float32([ [0,0],[0,h-1],[w-1,h-1],[w-1,0] ]).reshape(-1,1,2)
                dst = cv2.perspectiveTransform(pts,M)

                img2 = cv2.polylines(img2,[np.int32(dst)],True, 255 ,3, cv2.LINE_AA)
                print([np.int32(dst)][0][0][0][0])
                print([np.int32(dst)])
                self.successfull += 1
                cv2.imwrite(args.out_path + image_path_list[i], img2)

            else:
                print "Not enough matches are found - %d/%d" % (len(good),MIN_MATCH_COUNT)
                # matchesMask = None

    def calculate_rectangle_points(self, corners):
        
        for i in range(4):
            left = corners[0][0][0][0] + corners[0][0][0][0]


def main(args):
    sp = detect(args)
    cv2.destroyAllWindows()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('--find', type=str,
                        help='Give the path to the image you want to find. Default is this /img/train.jpg.',
                        default='img/train.jpg')
    parser.add_argument('--in_path', type=str,
                        help='Specify the path to the directory with images.',
                        default='img/')
    parser.add_argument('--number', type=int,
                        help='Specify how many images you want to check. 1.jpg-X.jpg',
                        default='10')
    parser.add_argument('--out_path', type=str,
                        help='Specify the path to the directory with images.',
                        default='out/')
    args = parser.parse_args()
    main(args)