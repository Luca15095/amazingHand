import time
import numpy as np
import pyarrow as pa
from dora import Node
from toArduino import ArduinoController

# Initialisierung des Controllers
c = ArduinoController()
MiddlePos = [0, 0, 0, 0, 0, 0, 0, 0]
MaxSpeed = 7
TuneFactor = 1.3

def main():
    # Dora Node initialisieren
    node = Node()
    print("Hardware-Node gestartet, warte auf Simulationsdaten...")

    try:
        # Wir nutzen die exakt gleiche Struktur wie in der Simulation
        for event in node:
            event_type = event["type"]
            
            if event_type == "INPUT":
                event_id = event["id"]
                if event_id == "mj_joints_pos":
                    # Das sind die 8 Radianten-Werte aus der Simulation
                    motor_pos_rad = event["value"].to_numpy()

                    # 2. Umrechnung: Radiant -> Grad
                    # Da deine Move_X Funktionen intern np.deg2rad(Angle) rechnen,
                    # müssen wir hier erst in Grad umrechnen.
                    angles_deg = np.rad2deg(motor_pos_rad)

                    # 3. Hardware ansteuern
                    # Index 0,1 -> Index Finger
                    move_index(motor_pos_rad[0], motor_pos_rad[1], MaxSpeed)
                    # Index 2,3 -> Middle Finger
                    move_middle(motor_pos_rad[2], motor_pos_rad[3], MaxSpeed)
                    # Index 4,5 -> Ring Finger
                    move_ring(motor_pos_rad[4], motor_pos_rad[5], MaxSpeed)
                    # Index 6,7 -> Thumb
                    move_thumb(motor_pos_rad[6], motor_pos_rad[7], MaxSpeed)

            elif event["type"] == "STOP":
                break

    except KeyboardInterrupt:
        pass
    finally:
        print("Schließe Verbindung zum Arduino...")
        c.close()

# Hilfsfunktionen (basierend auf deinem Skript)
def move_index(a1, a2, speed):
    c.write_goal_speed(1, speed)
    c.write_goal_speed(2, speed)
    a1Tuned = a1 * TuneFactor
    same_sign = (a1 * a2) > 0
    c.write_goal_position(1, MiddlePos[0] + a1, same_sign)
    c.write_goal_position(2, MiddlePos[1] + a2, same_sign)

def move_middle(a1, a2, speed):
    c.write_goal_speed(3, speed)
    c.write_goal_speed(4, speed)
    same_sign = (a1 * a2) > 0
    c.write_goal_position(3, MiddlePos[2] + a1, same_sign)
    c.write_goal_position(4, MiddlePos[3] + a2, same_sign)

def move_ring(a1, a2, speed):
    c.write_goal_speed(5, speed)
    c.write_goal_speed(6, speed)
    same_sign = (a1 * a2) > 0
    c.write_goal_position(5, MiddlePos[4] + a1, same_sign)
    c.write_goal_position(6, MiddlePos[5] + a2, same_sign)

def move_thumb(a1, a2, speed):
    c.write_goal_speed(7, speed)
    c.write_goal_speed(8, speed)
    same_sign = (a1 * a2) > 0
    c.write_goal_position(7, MiddlePos[6] + a1, same_sign)
    c.write_goal_position(8, MiddlePos[7] + a2, same_sign)

if __name__ == '__main__':
    main()