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

``sudo apt-get install python-pyaudio python3-pyaudio sox libatlas-base-dev libpcre3-dev portaudio19-dev``

#### 3.1.2 Get snowboygoogle tar 

``git clone https://github.com/PXLRoboticsLab/ROS_Pepper``

#### 3.1.3 Extract to desired workplace

Navigate to the cloned folder and extract the tar file

```
cd <pathofsnowboyassistant>
tar xvf snowboyassistant.tar.gz
```

#### 3.1.4 Install Python dependencies

Install the necessary Python requirements

``pip install -r requirements.txt``

#### 3.1.5 Check Google Assistant config data

```
cd ~/.config
ls
```

Confirm that both **googlesamples-assistant** and **google-oauthlib-tool** directories are present and not empty.
If they do not exist, please follow the Google Assistant Python SDK tutorial mentioned above!

####  3.1.6 Test audio and microphone

speaker

``speaker-test -t wav -c 6``
 
microphone

```
arecord -d 5 /tmp/test.wav
aplay /tmp/test.wav
```

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

#### 3.2.1 Install PulseAudio dependencies

``sudo apt install pavucontrol``

#### 3.2.2 Install Python dependencies

``pip install sounddevice``

#### 3.2.3 Add loopback module 

Create a loopback kernel module 

``sudo modprobe snd-aloop``

Confirm the new device with 

``python -m sounddevice``

#### 3.2.4 Add module permanently 

Add "snd-aloop" to /etc/modules so that the kernel module can load at boot time.
If you wish to unload the module, just remove the "snd-aloop" and restart.

``nano /etc/modules``

#### 3.2.5 Create a device for the loopback module

In order to use the loopback device, edit the .asoundrc file (if not present create new). 

``nano ~/.asoundrc``

Add the following code 

```
pcm.loop {

    type plug
    
    slave.pcm "hw:Loopback,1,0"
    
}
```
Confirm that the loopback device has been created with 

``python -m sounddevice``

You should see a device named "loop", remember or write down its index number (something between 0-10 usually). 

#### 3.2.6 Choose the loopback device as playback device

Open PulseAudio control panel with 

``pavucontrol``

Go to the "Playback" tab, you should see an "audio_play" device. Select "Loopback Analog Stereo" in the dropdown menu next to the symbol. All the sound that is retrieved by the topic and played back, is now redirected to the loopback device. Remember the index number that you needed to write down earlier? By providing this number to the snowboyassistant, you basically tell the assistant to listen to the loopback device which plays the audio coming from the remote host (via a topic). 

#### 3.2.7 Test demo 

You can now start the Pepper (or any other remote device of preference) and wait for the "audio/audio" topic to appear. Start the playback node on the local host with

`` roslaunch pepper_audio audio.launch ``

Run the demo again and provide the index number earlier as a parameter

``python demo.py <indexnumber>``


## 4. Troubleshooting

Help, my ALSA config is screwed! Calm down and:

```

sudo rm /lib/modules/`uname -r`/kernel/sound

sudo cp -a ~/backup/sound /lib/modules/`uname -r`/kernel/

sudo alsa force-reload

```
