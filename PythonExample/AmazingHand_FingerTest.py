import time
import numpy as np

# --- ÄNDERUNG 1: Deinen eigenen Controller importieren ---
# from rustypot import Scs0009PyController  <-- LÖSCHEN
from toArduino import ArduinoController   # <-- EINFÜGEN

ID_1 = 3
ID_2 = 4
MiddlePos_1 = 2 
MiddlePos_2 = 0 

# --- ÄNDERUNG 2: Deinen Controller initialisieren ---
# c = Scs0009PyController(...) <-- LÖSCHEN
c = ArduinoController()      # <-- EINFÜGEN (Parameter braucht er nicht mehr)


def main():
    print("Start Kalibrierung... (STRG+C zum Beenden)")
    
    # Der Befehl funktioniert jetzt, macht aber nichts (ist okay)
    c.write_torque_enable(1, 1) 
    
    try:
        while True:
            print("Finger schließen...")
            CloseFinger()
            time.sleep(3)

            print("Finger öffnen...")
            OpenFinger()
            time.sleep(1)

    except KeyboardInterrupt:
        print("Beendet.")
        c.close() # Port sauber schließen

def CloseFinger ():
    # Die Speed-Befehle werden ignoriert (macht der Arduino)
    c.write_goal_speed(ID_1, 6) 
    c.write_goal_speed(ID_2, 6) 
    
    # Hier rechnet das Skript: 0 + 90 = 90 Grad -> Radiant
    Pos_1 = np.deg2rad(MiddlePos_1+90)
    # Hier: 0 - 90 = -90 Grad -> Radiant
    Pos_2 = np.deg2rad(MiddlePos_2-90)
    
    # Dein Controller rechnet das zurück in Servo-Werte:
    # Pos_1 (1.57 rad) -> wird zu 180 Grad am Servo
    # Pos_2 (-1.57 rad) -> wird zu 0 Grad am Servo
    c.write_goal_position(ID_1, Pos_1)
    c.write_goal_position(ID_2, Pos_2)
    
    time.sleep(0.01)


def OpenFinger():
    c.write_goal_speed(ID_1, 6) 
    c.write_goal_speed(ID_2, 6) 
    
    # Öffnen ist nur +/- 30 Grad
    Pos_1 = np.deg2rad(MiddlePos_1-30)
    Pos_2 = np.deg2rad(MiddlePos_2+30)
    
    c.write_goal_position(ID_1, Pos_1)
    c.write_goal_position(ID_2, Pos_2)
    time.sleep(0.01)

if __name__ == '__main__':
    main()