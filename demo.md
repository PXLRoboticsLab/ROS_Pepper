# Imagescraper ([github: rushilsrivastava](https://github.com/rushilsrivastava/image-scrapers))
This project is used to download all the images of a certain object. You can search on both google and bing. In theory you should be able to download a 1.000 images of a chosen search. But this varies depending on the item. 

# SIFT ([github: NielsDebrier](https://github.com/NielsDebrier/SIFT-Detection-and-Rotation))
We will use SIFT to filter a first time through the images. Because the scrapper will download everything with Snickers this means also images related to Snickers but that aren't Snickers.
With this we can also rotate the image and do other things. This maybe improved later on but for the moment it is very usefull for a first filter.

# YOLO_Mark ([github: AlexeyAB](https://github.com/AlexeyAB/Yolo_mark))
This is a very handy tool made by AlexeyAB specially for YOLO. You can label al you images manually with this tool and it will make all the annotations and files like yolo needs them. It is really as simple as copy and pasting after you are done with labeling.

# Training your own model with darknet ([YOLO pjreddie](https://pjreddie.com/darknet/yolo/)) 
the command(if you use the default values):

`$ ./darknet detector train data/obj.data yolo-obj.cfg darknet19_448.conv.23`

In obj.data you will find all the information that YOLO needs like the number of classes, where the train.txt and valid.txt file is located as well as the obj.names file and path to where he needs to put the checkpoints.

yolo-obj.cfg is the config file. You need to change the filter and class value depending on how many classes you use. Filter is (classes + 5) * 5 so in our case 30 as we only have 1 class. And then change the value of classes to 1.

darknet19_448.conv.23 is the pretrained file for darknet. This way you only train the last layers.

When you are done with training we can test with:

`$ ./darknet detector recall data/obj.data  yolo-obj.cfg backup/yolo-obj_40000.weights`

This will you give more information about a certain checkpoint. With this you will also look for the best checkpoint because it will get worse if you keep training.

To run YOLO with your just trained model on the webcam:

`$ ./darknet detector demo data/obj.data yolo-obj.cfg backup/yolo-obj_final.weights`

To run on an image:

`$ ./darknet detector test data/obj.data yolo-obj.cfg backup/yolo-obj_final.weights sample/20180307_171325.jpg`

# Testing the weights with darkflow ([github: thtrieu](https://github.com/thtrieu/darkflow))
You can also run the just trained files on darkflow.
For this to work you need to change the offset from 16 to 20 in the loader.py.
Go to darkflow/darkflow/utils/loader.py and search for self.offset = 16 and change the 16 to 20.
Now you should be able to run:

`$ ./flow --model cfg/yolo-obj.cfg --load bin/yolo-obj_final.weights --demo camera --gpu 0.9`

To run on images instead of the webcam you need to remove the '--demo camera' and use '--imgdir /path'.
For more information run: `$ ./flow --h`


**side note:** After running on darknet and darkflow we noticed that yolo detects object from further away. A quick test showed that darknet detected the snicker on a cellphone from 68.5cm away while darkflow detected it at 58.3cm which is 10cm closer. Also it seems that darknet runs on a quite stable 30fps as to darkflow with 18fps. We will be testing this further in the next days.

# Ros connection darkflow
A connection to ROS can be made with darkflow. There is a file subscriber.py that we need to run for this.
To run with ROS do:

`$ roscore`

In a new terminal run:

`$ rosrun usb_cam usb_cam_node`

or this command if you want to use the camera of pepper.

`$ roslaunch pepper_bringup pepper_full.launch nao_ip:=<pepper ip> roscore_ip:=<ip computer> network_interface:=<network interface>`

For this to work you need to install the ros packages for usb_cam.
There is also a small bug that is solved by quickly running and stopping roslaunch of the same package: `$ roslaunch usb_cam usb_cam_node`
When these two are running you can now navigate to the darkflow folder and start the subscriber.

`$ ./subscriber.py`

Or for pepper you need to know the rostopic. If you know it for example /pepper_robot/naoqi_driver/camera/front/image_raw then you can run:

`$ ./subscriber.py --source /pepper_robot/naoqi_driver/camera/front/image_raw`

# Detectron ([github: facebookresearch](https://github.com/facebookresearch/Detectron))
Detectron gave a lot of troubles concerning the installation. So we changed from a regular installation to dockerfiles.
To start the dockercontainer do the following.

Check if the docker container is running: `$ sudo docker ps -a` \
If not then do the following: `$ sudo docker start <id>` \
The id is the one you saw by executing the previous command so copy and paste. 
Check if the docker is started: `$ sudo docker ps` \
If it is you can now enter the docker container with:

`$ sudo docker exec -it <id> /bin/bash`

Now you are in the docker environment. Now we can test detectron. If we want to run detectron on images:

>python2 tools/infer_simple.py \\ \
    --cfg configs/12_2017_baselines/e2e_mask_rcnn_R-101-FPN_2x.yaml \\ \
    --output-dir /host/detectron-visualizations \\ \
    --image-ext jpg \\ \
    --wts https://s3-us-west-2.amazonaws.com/detectron/35861858/12_2017_baselines/e2e_mask_rcnn_R-101-FPN_2x.yaml.02_32_51.SgT4y1cO/output/train/coco_2014_train:coco_2014_valminusminival/generalized_rcnn/model_final.pkl \\ \
    demo

To explain the command:
--cfg will point to the config file with which you run detectron. \
--output-dir points to the folder we want to put our output. In our case we want this to be /host as this is a shared folder so that you can view this outside the docker with the gui. \
--image-ext here you will state the extensions of the images. \
--wts will point to the weights file used. \ 
demo is the path of the folder where your images are. In this case in demo. \
If we run this command we will se the detected images apear in /host/detectron-visualizations in pdf format.