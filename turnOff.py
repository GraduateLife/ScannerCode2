
import fGenControl
import motorWrapper
fGenControl.turnFgenOff()

motorWrapper.MotorStartup(500)
motorWrapper.setXspeed(500)
motorWrapper.moveX(0)
motorWrapper.moveY(0)

