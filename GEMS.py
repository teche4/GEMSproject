import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.OUT)
GPIO.setup(12, GPIO.OUT)
GPIO.setup(15, GPIO.OUT)
GPIO.setup(16, GPIO.OUT)
GPIO.setup(21, GPIO.OUT)
GPIO.setup(22, GPIO.OUT)
GPIO.setup(23, GPIO.OUT)
GPIO.setup(24, GPIO.OUT)
GPIO.setup(26, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) #pressure sensor

b1c = GPIO.PWM(11, 1000)
b1ac = GPIO.PWM(15, 1000) #bot motors clock and anti clock pins in l293d

b2c = GPIO.PWM(12, 1000)
b2ac = GPIO.PWM(16, 1000)

a1u = GPIO.PWM(21, 1000)
a1d = GPIO.PWM(23, 1000)

a2o = GPIO.PWM(22, 1000)
a2c = GPIO.PWM(24, 1000)



class motion:
    def __str__(self):
        return ("This function is used to control GEMS bot motion") #print the function for info

    def bot(self, bot_motion, pwm1, rel_angle):
        self.speed = 100-pwm1 #convert active high to active low pwm
        if(bot_motion == "f"):#forward
            b1c.start(self.speed)
            b2c.start(self.speed)
            b1ac.start(100)
            b2ac.start(100)

        elif(bot_motion == "b"):#backward
            b1ac.start(self.speed)
            b2ac.start(self.speed)
            b1c.start(100)
            b2c.start(100)

        elif(bot_motion == "r"): #right relative angle decreases rad of curve
            speed2 = 100 - (rel_angle/90)*self.speed
            b1c.start(self.speed)
            b2ac.start(speed2)
            b1ac.start(100)
            b2c.start(100)
            
            
        elif(bot_motion == "l"): #left
            speed2 = 100 - (rel_angle/90)*self.speed
            b2c.start(self.speed)
            b1ac.start(speed2)
            b2ac.start(100)
            b1c.start(100)

        return()


    def arm(self, arm_motion, pwm1): #one for arm movement
        self.speed = 100-pwm1
        if(arm_motion == "u"):  #up motion
            a1u.start(self.speed)
            a1d.start(100)
            a2o.start(100)
            a2c.start(100)

        elif(arm_motion == "d"): #down motion
            a1d.start(self.speed)
            a1u.start(100)
            a2o.start(100)
            a2c.start(100)

        elif(arm_motion == "o"): #open
            a1d.start(100)
            a1u.start(100)
            a2o.start(self.speed)
            a2c.start(100)

        elif(arm_motion == "sdo"):#simultaneous down and open
            a1d.start(self.speed)
            a1u.start(100)
            a2o.start(self.speed)
            a2c.start(100)

        elif(arm_motion == "suo"): #simultaneous up and open
            a1d.start(100)
            a1u.start(self.speed)
            a2o.start(self.speed)
            a2c.start(100)

        elif(GPIO.input(26)==GPIO.LOW): #if pressure sensor val is 0
            if(arm_motion == "c"): #close
                a1d.start(100)
                a1u.start(100)
                a2o.start(100)
                a2c.start(self.speed)

            elif(arm_motion == "sdc"): #simultaneous down and close
                a1d.start(self.speed)
                a1u.start(100)
                a2o.start(100)
                a2c.start(self.speed)

            elif(arm_motion == "suc"): #simultaneous up and close
                a1d.start(100)
                a1u.start(aelf.speed)
                a2o.start(100)
                a2c.start(self.speed)

        return ()

            

print("Prog Start")
gems_motion = motion() #creating instance
gems_motion.bot("f",50, 0) #give rel_angle 0 for f, b
time.sleep(15)
gems_motion.bot("r",50, 9)
time.sleep(15)
gems_motion.arm("u",55)
time.sleep(15)
gems_motion.arm("sdc", 45)
print("Prog Ending")

b1c.stop()
b1ac.stop()

b2c.stop()
b2ac.stop()

a1d.stop()
a1u.stop()
a2o.stop()
a2c.stop()#stop the PWM


GPIO.cleanup()#reset all IO

    
