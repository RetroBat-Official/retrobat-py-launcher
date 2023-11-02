# -*- coding: utf-8 -*-
import os, subprocess, configparser

app_path = os.path.dirname(os.path.normpath(__file__))
print(r'Working Dir: ' + app_path)

## Read config file

ini = configparser.ConfigParser()
iniFile = os.path.join(app_path, 'retrobat.ini')
ini.read(iniFile)
#ini.sections()

## Remove double quote from value to compare

def check_value(Section, Param, Value):
    if (ini[Section][Param]).startswith('"', 0) & (ini[Section][Param]).endswith('"', -1): 
        _result = (ini[Section][Param]).strip('"')
        if _result == Value:
            return True

def strip(Value):
    if (Value).startswith('"', 0) & (Value).endswith('"', -1):
        return (Value).strip('"')

## Set video file

if check_value('SplashScreen', 'FilePath', 'default'):
    video_path = os.path.join(app_path, 'emulationstation', '.emulationstation', 'video')
else:
    video_path = ini['SplashScreen']['FilePath']

print(r'Video path: ' + video_path)

video_file = strip(ini['SplashScreen']['FileName'])
print(r'Video file: ' + video_file)

## Append arguments to command array

commandArray = list()

if not ini['EmulationStation'].getboolean('Fullscreen'): 
    commandArray.append('--resolution' + ' ' + ini['EmulationStation']['WindowXSize'] + ' ' + ini['EmulationStation']['WindowYSize'] + ' ' + '--windowed')

if ini['EmulationStation'].getboolean('ForceFullscreenRes') & ini['EmulationStation'].getboolean('Fullscreen'):
    commandArray.append('--resolution' + ' ' + ini['EmulationStation']['WindowXSize'] + ' ' + ini['EmulationStation']['WindowYSize'])

if ini['EmulationStation'].getboolean('GameListOnly'): 
    commandArray.append('--gamelist-only')

if ini['EmulationStation'].getboolean('NoExitMenu'): 
    commandArray.append('--no-exit')

if int(ini['EmulationStation']['InterfaceMode']) >> 0:
    if int(ini['EmulationStation']['InterfaceMode']) == 1:
        commandArray.append('--force-kiosk')
    if int(ini['EmulationStation']['InterfaceMode']) == 2:
        commandArray.append('--force-kid')

if int(ini['EmulationStation']['MonitorIndex']) >> 0: 
    commandArray.append('--monitor' + ' ' + ini['EmulationStation']['MonitorIndex'])

withSpace = ' '
arguments = withSpace.join(commandArray)

## Functions

video = os.path.join(video_path, video_file)

def get_video_duration(video):
    import cv2
    video = cv2.VideoCapture(video)
    duration = video.get(cv2.CAP_PROP_POS_MSEC)
    frame_count = video.get(cv2.CAP_PROP_FRAME_COUNT)
    print(duration, frame_count)
    return duration, frame_count

## Process start

get_video_duration(video)
print(video)

## Start video intro

if ini['SplashScreen'].getboolean('EnableIntro'):
    subprocess.run(os.path.join(app_path, 'emulationstation', 'emulationstation.exe') + ' ' + '--video' + ' ' + video)

## Start EmulationStation

print(os.path.join(app_path, 'emulationstation', 'emulationstation.exe') + ' ' + arguments)
subprocess.run(os.path.join(app_path, 'emulationstation', 'emulationstation.exe') + ' ' + arguments)