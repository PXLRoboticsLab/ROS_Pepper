# Install guide Google Assistant and Snowboy on Ubuntu 16.04 (for Pepper)

## 1. Summary

This guide is normally meant for the Pepper robot. Luckily, it works on any Ubuntu device 16.04 or higher. 
It is based on the *pushtotalk* module of the Google Assistant SDK and includes **Snowboy** for a custom hotword detection. 
If you want to record and playback on a local machine only, you can skip step X.X.  This guide assumes you have completed a 
full tutorial of Google Assistant or at least have the required directories under ~/.config available. If any issues are 
encountered, make sure to read the **troubleshoot** section. 

## 2. Requirements
- ROS Kinetic (test on other versions, at own risk!) 
- Python >= 2.7.12
- ``export PYTHONPATH=/opt/ros/kinetic/lib/python2.7/dist-package``
-  (Put line above in ~/.bashrc)
- Pip ``sudo apt-get install python-pip``
- Completed https://developers.google.com/assistant/sdk/guides/library/python/ tutorial (step 6) and tested **hotword** or **pushtotalk** modules

## 3. Installing snowboygoogle 

### 3.1 Using local machine as audio input and output

#### 3.1.1 Install a few dependencies 
``sudo apt-get install python-pyaudio python3-pyaudio sox libatlas-base-dev libpcre3-dev``

#### 3.1.2 Get snowboygoogle tar 

#### 3.1.3 Extract to desired workplace

#### 3.1.4 Install Python dependencies
Navigate to the directory of the extracted tar

```cd <pathofsnowboyassistant>```

Install the necessary Python requirements

```pip install -r requirements.txt```

#### 3.1.5 Check Google Assistant config data
``cd ~/.config``

``ls``

Confirm that both **googlesamples-assistant** and **google-oauthlib-tool** directories are present and not empty 

####  3.1.6 Test audio and microphone
speaker

``speaker-test -t wav -c 6``
 
microphone

``arecord -d 5 /tmp/test.wav``

``aplay /tmp/test.wav``

adjust settings if needed

``alsamixer``

#### 3.1.7 Test demo
Run the demo with 

``python demo.py``

Activate the assistant with the word "Pepper" and if you hear a sound, the assistant is listening. 
Confirm the demo is working correctly by analyzing the logs on the command line.

#### 3.1.8 Change trained voice

If you want to change the hotword or replace it with a better model (with your own voice for example), use https://snowboy.kitt.ai/dashboard
Replace the .pmdl file in the directory afterwards with the newly trained .pmdl file. 

### 3.2 Using the Pepper as audio input and output (to be continued) 
