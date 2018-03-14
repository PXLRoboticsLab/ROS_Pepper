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

                # draw rectangle and center on image
                # uncomment for original detection
                # img2 = cv2.polylines(img2, [np.int32(dst)], True, 255, 3, cv2.LINE_AA)
                # uncomment for rectangle draw
                # img2 = self.draw_rectangle(img2, [np.int32(dst)])
                # uncomment for rotate image
                img2 = self.rotate_image(img2, [np.int32(dst)])

                self.successfull += 1
                cv2.imwrite(args.out_path + image_path_list[i], img2)

            else:
                print "Not enough matches are found - %d/%d" % (len(good),MIN_MATCH_COUNT)
                # matchesMask = None

    # solution 1: just make a rectangle over the detected rectangle
    def draw_rectangle(self, img, points):
        # Calculate rectangle and center
        corners = self.calculate_rectangle_opposite_corners(points)
        center = self.calculate_center(corners)

        img = cv2.rectangle(img, corners[0], corners[1], 255, 3)
        img = cv2.circle(img, center, 0, 255, 10)
        return img

    def calculate_rectangle_opposite_corners(self, points):
        left = right = points[0][0][0][0]
        top = bottom = points[0][0][0][1]
        for i in range(4):
            newX = points[0][i][0][0]
            newY = points[0][i][0][1]
            print([newX, newY])
            if newX < left:
                left = newX
            elif newX > right:
                right = newX
            if newY < top:
                top = newY
            elif newY > bottom:
                bottom = newY
        corners = [(left, top), (right, bottom)]
        return corners

    def calculate_center(self, points):
        x = (points[0][0] + points[1][0])/2
        y = (points[0][1] + points[1][1])/2
        point = (x, y)
        return point

    # solution 2: rotate the image
    def rotate_image(self, img, points):
        print("POINTS COMING IN:")
        print(points)
        angle = self.calculate_rotation(points)
        corners = self.calculate_rectangle_opposite_corners(points)
        center = self.calculate_center(corners)
        print("-------------------ANGLE: " + str(angle))
        print("-------------------CENTER: " + str(center))

        # Uncomment for angle in radians
        angle *= 180/np.pi

        shape = img.shape[:2]

        matrix = cv2.getRotationMatrix2D(center, angle, 1)
        img = cv2.warpAffine(img, matrix, shape)

        return img

    def calculate_rotation(self, points):
        # calculate middle of rectangle
        corners = self.calculate_rectangle_opposite_corners(points)
        p1 = self.calculate_center(corners)

        # calculate middle of point3 en 4
        print("PRINTING POINTS 3 AND 4 "+ str(points[0][2][0]) + str(points[0][3][0]) )
        point3 = points[0][2][0]
        point4 = points[0][3][0]
        p2 = self.calculate_center([point3, point4])

        # calculate distance between p1 and p2 in our case equal to distance between p1 and p3
        s3 = s2 = self.calculate_distance(p1, p2)

        # define p3
        p3 = ((p1[0] + s2), p1[1])

        # calculate distance between p2 and p3
        s1 = self.calculate_distance(p2, p3)

        # calculate angle
        angle = self.calculate_angle(s1, s2, s3)

        return angle




    def calculate_distance(self, point1, point2):
        # calculate the power of (x1-x2)^2 and (y1-y2)^2
        arg = np.power([(point1[0] - point2[0]), (point1[1] - point2[1])], 2)
        distance = np.sqrt(arg[0] + arg[1])
        return distance

    def calculate_angle(self, side1, side2, side3):
        # calculate arccos((b^2+c^2-a^2)/(2*b*c))
        power = np.power([side1, side2, side3], 2 )
        x = power[1] + power[2] - power[0]
        y = 2 * side2 * side3
        angle = np.arccos(x/y)
        return angle







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