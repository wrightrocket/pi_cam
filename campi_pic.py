''' WrightRocket Camera for Raspberry Pi
    By Keith Wright
    Created May 14, 2018
'''
import os
import sys
from datetime import datetime
from time import sleep
from picamera import PiCamera
from sense_hat import SenseHat

def moment():
    return str(datetime.now().isoformat()[:-7])

def zoom_info():
    return 'x'.join((str(x) for x in camera.zoom))
        

def info(verbose=True):
    '''camera_num=0, stereo_mode='none', stereo_decimate=False, resolution=None, framerate=None, sensor_mode=0, led_pin=None, clock_mode='reset', framerate_range=None
    '''
    return '\n'.join((str(x) for x in ('Camera settings:',
    'sharpness', camera.sharpness,
    'contrast', camera.contrast,
    'brightness', camera.brightness,
    'saturation', camera.saturation,
    'iso', camera.iso,
    'video_stabilization', camera.video_stabilization,
    'exposure_compensation', camera.exposure_compensation,
    'exposure_mode', camera.exposure_mode,
    'meter_mode', camera.meter_mode,
    'awb_mode', camera.awb_mode,
    'image_effect', camera.image_effect,
    'color_effects', camera.color_effects,
    'rotation', camera.rotation, 
    'hflip', camera.hflip,
    'zoom', zoom_info())))

def snap(filename=None, secs=2):
    global stop_preview
    if not filename:
        filename = '.'.join([DIR_CAPTURES + str(moment()), 'jpg'])
    if not secs or secs < 2:
        secs = 2 
    print('Snap', filename)
    camera.start_preview()
    camera.annotate_text = moment()
    sleep(secs)
    camera.capture(filename)
    camera.stop_preview()
    print('Snap complete', info(), sep='\n')
    
def capture(filename=None, secs=3):
    global stop_preview
    if not filename:
        filename = '.'.join([str(DIR_CAPTURES + moment()),'jpg'])
    if secs < 2:
        secs = 2 
    print('Capturing', filename)
    # camera.start_preview()
    camera.annotate_text = moment()
    #sleep(secs)
    camera.capture(filename)
    stop_preview = True
    print('Capture complete', info(), sep='\n')
    
def preview(secs=10):
    print('Previewing', info(), 'for', secs, 'seconds')
    camera.start_preview()
    sec = 0
    while not stop_preview and sec < secs:
        sleep(secs)
        camera.stop_preview()

def effects():
    camera.start_preview()
    print('Displaying effects')
    for effect in sorted(camera.IMAGE_EFFECTS):
        camera.image_effect = effect
        print(effect)
        sleep(3)
        filename = '.'.join([str(moment()), effect, 'jpg'])
        camera.annotate_text = "%s" % filename
        camera.capture(filename)
    camera.stop_preview()

def set_rotation():
    '''  Update the camera rotation

    Depending on the Sense HAT orientation '''
    acceleration = sense.get_accelerometer_raw()

    x = acceleration['x']
    y = acceleration['y']
    z = acceleration['z']

    x=round(x, 0)
    y=round(y, 0)
    z=round(z, 0)

    if x  == -1:
      camera.rotation = 180
    elif y == 1:
      camera.rotation = 90
    elif y == -1:
      camera.rotation =270
    else:
      camera.rotation =0

def acc_capture():
    xt = 0
    yt = 0
    zt = 0
    count = 0
    while True:
        acceleration = sense.get_accelerometer_raw()

        x = acceleration['x']
        y = acceleration['y']
        z = acceleration['z']

        digits = 3
        delta = pow(10, - digits) * 5
        print('factor', delta)
        x=round(x, digits)
        y=round(y, digits)
        z=round(z, digits)
        xt += x
        yt += y
        zt += z
        count += 1
        xa = round(xt / count, digits)
        ya = round(yt / count, digits)
        za = round(zt / count, digits)
        print("xa={0}, ya={1}, za={2}".format(xa, ya, za))
        print("x={0}, y={1}, za{2}".format(x, y, z))
        if (abs(z - za) > delta) or (abs(y - ya) > delta) or (abs(x - xa) > delta):
            snap()
            
def capture_dir(dir_name=None, mode=777):
    global DIR_CAPTURES
    if not dir_name:
        dir_name = DIR_CAPTURES
    elif not dir_name.endswith(os.sep):
        dir_name = dir_name + os.sep
        print('Using {0} directory for captures'.format(dir_name))
    if os.path.exists(dir_name) and not os.path.isdir(dir_name):
        print('{0} unvavailable to use, using current directory for captures'.format(dir_name))
        dir_name = '.' + os.sep
    elif os.path.exists(dir_name) and os.path.isdir(dir_name):
        print('Using {0} directory for captures'.format(dir_name))
    else:
        try:
            os.mkdir(dir_name)
        except OSError:
            print (sys.exc_info)
        else:
            print('Successfully created {0} directory for captures'.format(dir_name))
    DIR_CAPTURES = dir_name 
            
        
DIR_CAPTURES = 'captures'
capture_dir(DIR_CAPTURES)
stop_preview = False
sense = SenseHat()
camera = PiCamera()
set_rotation()
sense.stick.direction_any = capture
# preview()
# capture()
# effects()
acc_capture()
