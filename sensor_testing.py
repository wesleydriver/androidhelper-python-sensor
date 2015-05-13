import sys
import types
import time
from math import log
import androidhelper as android

droid = android.Android()

def event_loop():
  for i in range(10):
    e = droid.eventPoll(1)
    if e.result is not None:
      return True
    time.sleep(2)
  return False

def test_gps():
  droid.startLocating()
  try:
    return event_loop()
  finally:
    droid.stopLocating()

def test_speak():
  result = droid.ttsSpeak('Hello, Wesley!')
  return result.error is None

def test_geocode():
  result = droid.geocode(0.0, 0.0, 1)
  return result.error is None

def test_vibrate():
  result = droid.vibrate()
  return result.error is None

def test_lightSensor():
  dt = 1000 #1000ms between sensings
  endTime = 3000 #sample for 2000ms
  timeSensed=0
  droid.startSensingTimed(4,dt) 
  while timeSensed <= endTime:
    result = droid.sensorsGetLight()
    value = result.result
    print int(2*log(value + 2.5))
    time.sleep(dt/1000.0)
    timeSensed+=dt
  droid.stopSensing()
  return result.error is None

def test_sensorsReadAccelerometer():
  dt = 1000 #1000ms between sensings
  endTime = 3000 #sample for 2000ms
  timeSensed=0
  droid.startSensingTimed(2,dt) 
  while timeSensed <= endTime:
    result = droid.sensorsReadAccelerometer()
    print result.result
    time.sleep(dt/1000.0)
    timeSensed+=dt
  droid.stopSensing()
  return result.error is None

def test_Location():
  droid.startLocating(30,5)
  time.sleep(1)
  result = droid.readLocation()
  droid.stopLocating()
  print result.result
  return result.error is None

def test_camer():
  cur_time = str(time.clock())
  path = '/sdcard/Download/%s.jpg'%cur_time
  result = droid.cameraCapturePicture(path)
  return result.error is None


if __name__ == '__main__':
  for name, value in globals().items():
    if name.startswith('test_') and isinstance(value, types.FunctionType):
      print 'Running %s...' % name,
      sys.stdout.flush()
      if value():
        print ' PASS'
      else:
        print ' FAIL'
