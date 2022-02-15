from time import sleep
from gpiozero import LED, Buzzer, Servo

alarm = Buzzer(12)
fan = LED(15)
light = LED(17)
servo = Servo(19)

while  True: 
    alarm.on()
    fan.on()
    light.on()

    sleep(2)

    alarm.off()
    fan.off()
    light.off()

    servo.min()
    servo.max()
    sleep(5)
    servo.min()


 #servo motor with degrees
#from gpiozero import AngularServo
#servo = AngularServo(19, initial_angle=0, min_pulse_width=0.0006, max_pulse_width=0.0023)
#servo.angle = 45
#sleep(2)
#servo.angle = 0
#sleep(2)
#servo.angle = -45
#sleep(2)
