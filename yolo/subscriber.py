#! /usr/bin/env python
from darkflow.net.build import TFNet
import os
import cv2
import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import time
import sys
import argparse


class subscribe_pepper:
    def __init__(self, args):
        subscriberName = "yolo" + str(os.getpid())
        topicName = args.source
        # if args.source == 'w':
        #     topicName = "/usb_cam/image_raw"
        # elif args.source == 'p':
        #     topicName = "/pepper_robot/naoqi_driver/camera/front/image_raw"

        self.subscriber = rospy.Subscriber(topicName, Image, self.callback)

        options = {"model": "cfg/yolo-voc.cfg", "load": "bin/yolo-voc.weights", "threshold": 0.25, "gpu": 0.9}

        self.tfnet = TFNet(options)

    def callback(self, image_message):
        bridge = CvBridge()
        # imgcv = cv2.imread("./sample_img/" + img_name)

        image = bridge.imgmsg_to_cv2(image_message, desired_encoding="passthrough")

        result = self.tfnet.return_predict(image)

        imgcv = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        for index in range(len(result)):
            topleft = (result[index]['topleft']['x'], result[index]['topleft']['y'])
            topleftText = (result[index]['topleft']['x'], result[index]['topleft']['y'] - 25)
            bottomright = (result[index]['bottomright']['x'], result[index]['bottomright']['y'])
            text = result[index]['label']
            cv2.rectangle(imgcv, topleft, bottomright, (255, 0, 0), 2)
            cv2.putText(imgcv, text, topleftText, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 255)

        cv2.imshow("vision", imgcv)
        k = cv2.waitKey(1)  # 0==wait forever
        # file = open("log.txt", "a")
        #
        # file.write(str(result))
        # file.write("\n\n")
        #
        # file.close()


def main(args):
    sp = subscribe_pepper(args)
    rospy.init_node('subscribe_pepper', anonymous=False)

    try:
        rospy.spin()
    except KeyboardInterrupt:
        print "Shutting down ROS Image feature detector module"
    cv2.destroyAllWindows()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('--source', type=str,
                        help='Specify what you want to use. Give the topic name of the device.',
                        default='/usb_cam/image_raw')
    args = parser.parse_args()
    main(args)
