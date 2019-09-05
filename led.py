import ifcfg
import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

LED = 12
BUT = 16
short = 0.25
long = 1.0

GPIO.setup(LED, GPIO.OUT)
GPIO.setup(BUT, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.output(LED, GPIO.LOW)

def flash(secs):
  GPIO.output(LED, GPIO.HIGH)
  time.sleep(secs)
  GPIO.output(LED, GPIO.LOW)
  time.sleep(short)

def blink(num):
  if num > 10:
    print "error: num greater than 10"
    return
  if num == 0:
    flash(1.0)
    return
  while num > 0:
    flash(0.25)
    num -= 1
  return

def pause(secs):
  time.sleep(secs)

def output(msg):
  for l in msg:
    if l == '.':
      pause(long)
      continue
    if l == ' ':
      pause(2*long)
      continue
    l = int(l)
    if l == 0:
      flash(long)
      continue
    if int(l) in [1,2,3,4,5,6,7,8,9]:
      blink(l)
    pause(long)

def button():
  val = bool(GPIO.input(BUT))
  return not val

def ips():
  ips = []
  for name, interface in ifcfg.interfaces().items():
    for ip in interface['inet4']:
      if name == 'lo':
        continue
      ips.append(ip)
  string = ' '.join(ips)
  return string

def pressed():
  output(ips())

# main loop
while True:
  if button():
    time.sleep(long)
    pressed()
  else:
    time.sleep(0.1)
