# aa-cam

## Purpose

To record audio and video simultaniously using Python, and to automatically set optimal aperture settings by using p-iris control.  

Right now, this code is written for a specific purpose & hardware (Raspberry Pi Zero), but can easily be written for other uses.

## Pre-Requisite

1. Set ssh port to an obscure uncommon port.
2. Install on the rpi: `pip install image` or `pip install Pillow` and `python3 -m pip install sounddevice`
3. Set-up microphone gains: `alsamixer`
4. Install VNC Viewer to set-up focus: Download [here](https://www.realvnc.com/en/connect/download/viewer/)
5. SSH into the rpi and run `startx`.   
    - _If the desktop doesn't boot then try to run `vncserver` to create a virtual desktop. Destroy virtual desktop by running `vncserver -kill :{display-number}`. Open VNC Viewer and change RealVNC settings on the rpi. Click `RealVNC > Options > Troubleshooting > Enable direct capture mode`_
8. Run `raspistill -f -t 0` to view a camera preview and adjust focus, field of view and zoom

## Usage

```
python3 set_exposure.py {desired exposure 0 - 255 : int}
python3 picam.py {record_time seconds} {audio boolean}
```

## Remote Control

```
pip install paramiko
pip install scp
```
See `aa_lab > util.py` package for code:  
```
my_ssh_client = SSHClientSCP(host_ip='{ip address}', psswd='{password}')
SSHClientSCP.RAW_MEDIA_DIR = '{absolute path}'
my_ssh_client.set_picam(120)
my_ssh.client.record_picam(30, True)
my_ssh_client.get_rawmedia()
```
