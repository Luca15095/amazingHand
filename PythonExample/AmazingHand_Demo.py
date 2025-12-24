import time
import numpy as np

# --- ÄNDERUNG 1: Deinen Wrapper laden ---
# from rustypot import Scs0009PyController <-- WEG
from toArduino import ArduinoController  # <-- NEU

#Side
Side = 2 # 1=> Right Hand // 2=> Left Hand

#Speed
# HINWEIS: Diese Werte haben aktuell keinen Einfluss, da dein Arduino
# die Geschwindigkeit über die Glättung (Smoothing) selbst regelt.
MaxSpeed = 7
CloseSpeed = 3

#Fingers middle poses
# HIER kannst du Fein-Tuning betreiben.
# Wenn ein Finger bei "0" Grad (also 90 am Servo) etwas schief steht,
# trage hier z.B. 5 oder -5 ein.
MiddlePos = [0, 0, 0, 0, 0, 0, 0, 0] 

# --- ÄNDERUNG 2: Controller starten ---
# c = Scs0009PyController(...) <-- WEG
c = ArduinoController()      # <-- NEU


def main():
    print("Starte Hand-Steuerung... (STRG+C zum Beenden)")
    
    # Das wird vom Wrapper ignoriert, stört aber nicht
    c.write_torque_enable(1, 1) 
    
    t0 = time.time()

    try:
        while True:
            t = time.time() - t0

            print("Geste: OpenHand")
            OpenHand()
            time.sleep(1)

            print("Geste: CloseHand")
            CloseHand()
            time.sleep(2)

            print("Geste: OpenHand_Progressive")
            OpenHand_Progressive()
            time.sleep(2)

            print("Geste: SpreadHand")
            SpreadHand()
            time.sleep(0.6)
            
            print("Geste: ClenchHand")
            ClenchHand()
            time.sleep(0.6)

            OpenHand()
            time.sleep(0.2)

            print("Geste: Zeigefinger")
            Index_Pointing()
            time.sleep(0.4)
            Nonono()
            time.sleep(0.5)
            
            OpenHand()
            time.sleep(0.3)

            '''print("Geste: Perfect")
            Perfect()
            time.sleep(0.8)'''

            OpenHand()
            time.sleep(0.4)

            print("Geste: Victory & Scissors")
            Victory()
            time.sleep(1)
            Scissors()
            time.sleep(0.5)

            OpenHand()
            time.sleep(0.4)

            print("Geste: Pinched")
            Pinched()
            time.sleep(1)

            '''print("Geste: Mittelfinger")
            Fuck()
            time.sleep(0.8)'''

    except KeyboardInterrupt:
        print("\nProgramm beendet.")
        c.close() # WICHTIG: Port schließen



def OpenHand():
    Move_Index (-35,35, MaxSpeed)
    Move_Middle (-35,35, MaxSpeed)
    Move_Ring (-35,35, MaxSpeed)
    Move_Thumb (-35,35, MaxSpeed)

def CloseHand():
    Move_Index (90,-90, CloseSpeed)
    Move_Middle (90,-90, CloseSpeed)
    Move_Ring (90,-90, CloseSpeed)
    Move_Thumb (90,-90, CloseSpeed+1)

def OpenHand_Progressive():
    Move_Index (-35,35, MaxSpeed-2)
    time.sleep(0.2)
    Move_Middle (-35,35, MaxSpeed-2)
    time.sleep(0.2)
    Move_Ring (-35,35, MaxSpeed-2)
    time.sleep(0.2)
    Move_Thumb (-35,35, MaxSpeed-2)

def SpreadHand():
    if (Side==1): # Right Hand
        Move_Index (4, 90, MaxSpeed)
        Move_Middle (-32, 32, MaxSpeed)
        Move_Ring (-90, -4, MaxSpeed)
        Move_Thumb (-90, -4, MaxSpeed)  
  
    if (Side==2): # Left Hand
        Move_Index (-60, 0, MaxSpeed)
        Move_Middle (-35, 35, MaxSpeed)
        Move_Ring (-4, 90, MaxSpeed)
        Move_Thumb (-4, 90, MaxSpeed)  
  
def ClenchHand():
    if (Side==1): # Right Hand
        Move_Index (-60, 0, MaxSpeed)
        Move_Middle (-35, 35, MaxSpeed)
        Move_Ring (0, 70, MaxSpeed)
        Move_Thumb (-4, 90, MaxSpeed)  
  
    if (Side==2): # Left Hand
        Move_Index (0, 60, MaxSpeed)
        Move_Middle (-35, 35, MaxSpeed)
        Move_Ring (-70, 0, MaxSpeed)
        Move_Thumb (-90, -4, MaxSpeed)
  
def Index_Pointing():
    Move_Index (-40, 40, MaxSpeed)
    Move_Middle (90, -90, MaxSpeed)
    Move_Ring (90, -90, MaxSpeed)
    Move_Thumb (90, -90, MaxSpeed)
  
def Nonono():
  Index_Pointing()
  for i in range(3) :
        time.sleep(0.2)
        Move_Index (-10, 80, MaxSpeed)
        time.sleep(0.2)
        Move_Index (-80, 10, MaxSpeed)
  
  Move_Index (-35, 35, MaxSpeed)
  time.sleep(0.4)
  
def Perfect():
  if (Side==1): #Right Hand
        Move_Index (50, -50, MaxSpeed)
        Move_Middle (0, -0, MaxSpeed)
        Move_Ring (-20, 20, MaxSpeed)
        Move_Thumb (65, 12, MaxSpeed)

  
  if (Side==2): #Left Hand
        Move_Index (50, -50, MaxSpeed)
        Move_Middle (0, -0, MaxSpeed)
        Move_Ring (-20, 20, MaxSpeed)
        Move_Thumb (-12, -65, MaxSpeed)
  
def Victory():
  if (Side==1): #Right Hand 
        Move_Index (-15, 65, MaxSpeed)
        Move_Middle (-65, 15, MaxSpeed)
        Move_Ring (90, -90, MaxSpeed)
        Move_Thumb (90, -90, MaxSpeed)

  
  if (Side==2): #Left Hand
        Move_Index (-65, 15, MaxSpeed)
        Move_Middle (-15, 65, MaxSpeed)
        Move_Ring (90, -90, MaxSpeed)
        Move_Thumb (90, -90, MaxSpeed)
  
def Pinched():
  if (Side==1): #Right Hand
        Move_Index (90, -90, MaxSpeed)
        Move_Middle (90, -90, MaxSpeed)
        Move_Ring (90, -90, MaxSpeed)
        Move_Thumb (0, -75, MaxSpeed)

  if (Side==2): #Left Hand
        Move_Index (90, -90, MaxSpeed)
        Move_Middle (90, -90, MaxSpeed)
        Move_Ring (90, -90, MaxSpeed)
        Move_Thumb (75, 5, MaxSpeed)

def Scissors():
  Victory();
  if (Side==1): #Right Hand
        for i in range(3):  
            time.sleep(0.2)
            Move_Index (-50, 20, MaxSpeed)
            Move_Middle (-20, 50, MaxSpeed)
            
            time.sleep(0.2)
            Move_Index (-15, 65, MaxSpeed)
            Move_Middle (-65, 15, MaxSpeed)
    

  if (Side==2): #Left Hand
        for i in range(3):
            time.sleep(0.2)
            Move_Index (-20, 50, MaxSpeed)
            Move_Middle (-50, 20, MaxSpeed)
            
            time.sleep(0.2)
            Move_Index (-65, 15, MaxSpeed)
            Move_Middle (-15, 65, MaxSpeed)

def Fuck():

  if (Side==1): #Right Hand
        Move_Index (90, -90, MaxSpeed)
        Move_Middle (-35, 35, MaxSpeed)
        Move_Ring (90, -90, MaxSpeed)
        Move_Thumb (0, -75, MaxSpeed)

  if (Side==2): #Left Hand
        Move_Index (90, -90, MaxSpeed)
        Move_Middle (-35, 35, MaxSpeed)
        Move_Ring (90, -90, MaxSpeed)
        Move_Thumb (75, 0, MaxSpeed)
  
def Move_Index (Angle_1,Angle_2,Speed):
    
    c.write_goal_speed(1, Speed)
    time.sleep(0.0002)
    c.write_goal_speed(2, Speed)
    time.sleep(0.0002)
    Pos_1 = np.deg2rad(MiddlePos[0]+Angle_1)
    Pos_2 = np.deg2rad(MiddlePos[1]+Angle_2)
    c.write_goal_position(1, Pos_1)
    c.write_goal_position(2, Pos_2)
    time.sleep(0.005)

def Move_Middle(Angle_1,Angle_2,Speed):    
    c.write_goal_speed(3, Speed)
    time.sleep(0.0002)
    c.write_goal_speed(4, Speed)
    time.sleep(0.0002)
    Pos_1 = np.deg2rad(MiddlePos[2]+Angle_1)
    Pos_2 = np.deg2rad(MiddlePos[3]+Angle_2)
    c.write_goal_position(3, Pos_1)
    c.write_goal_position(4, Pos_2)
    time.sleep(0.005)

def Move_Ring(Angle_1,Angle_2,Speed):    
    c.write_goal_speed(5, Speed)
    time.sleep(0.0002)
    c.write_goal_speed(6, Speed)
    time.sleep(0.0002)
    Pos_1 = np.deg2rad(MiddlePos[4]+Angle_1)
    Pos_2 = np.deg2rad(MiddlePos[5]+Angle_2)
    c.write_goal_position(5, Pos_1)
    c.write_goal_position(6, Pos_2)
    time.sleep(0.005)

def Move_Thumb(Angle_1,Angle_2,Speed):    
    c.write_goal_speed(7, Speed)
    time.sleep(0.0002)
    c.write_goal_speed(8, Speed)
    time.sleep(0.0002)
    Pos_1 = np.deg2rad(MiddlePos[6]+Angle_1)
    Pos_2 = np.deg2rad(MiddlePos[7]+Angle_2)
    c.write_goal_position(7, Pos_1)
    c.write_goal_position(8, Pos_2)
    time.sleep(0.005)


if __name__ == '__main__':
    main()



