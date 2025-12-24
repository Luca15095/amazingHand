import serial
import serial.tools.list_ports
import time
import numpy as np

class ArduinoController:
    print("ArduinoController wird initialisiert...")
    
    def __init__(self):
        # --- 1. Automatische Port-Suche ---
        ports = list(serial.tools.list_ports.comports())
        arduino_port = None
        for p in ports:
            if "usbmodem" in p.device or "USB Serial" in p.description:
                arduino_port = p.device
                break
        
        if not arduino_port:
            print("WARNUNG: Kein Arduino gefunden! (Simulation Mode)")
            self.ser = None
        else:
            print(f"Arduino verbunden an: {arduino_port}")
            self.ser = serial.Serial(arduino_port, 115200)
            time.sleep(2) # Warten auf Arduino Reset

        # --- ÄNDERUNG: Dictionary für 8 Servos ---
        # Wir speichern die Werte nicht mehr einzeln, sondern in einer Liste/Map.
        # IDs 1 bis 8 starten alle auf 90 Grad.
        self.servo_positions = {
            1: 90, 2: 90, 3: 90, 4: 90,
            5: 90, 6: 90, 7: 90, 8: 90
        }

    # --- Fake-Methoden ---
    def write_torque_enable(self, id, val):
        pass 

    def write_goal_speed(self, id, val):
        pass 

    # --- Die WICHTIGE Methode: Radiant -> Arduino String ---
    def write_goal_position(self, id, radians, same_sign):
        # 1. Radiant in Grad umrechnen
        degree = np.rad2deg(radians)
        
        # 2. Offset anwenden (0 rad = 90 Grad Servo-Mitte)
        if same_sign : 
            servo_angle = 90 - degree
        else: 
            servo_angle = 90 + degree
            
        
        # 3. Begrenzen auf 0-180
        #servo_angle = servo_angle * 1.1
        servo_angle = int(max(0, min(180, servo_angle)))

        # 4. Wert speichern (Dynamisch für jede ID von 1-8)
        # Wir stellen sicher, dass 'id' eine ganze Zahl ist
        id = int(id)
        
        if id in self.servo_positions:
            self.servo_positions[id] = servo_angle
        else:
            print(f"WARNUNG: ID {id} liegt nicht im Bereich 1-8 und wird ignoriert.")
            return

        # 5. Nachricht an Arduino senden
        self.send_to_arduino()

    def send_to_arduino(self):
        if self.ser and self.ser.is_open:
            # --- ÄNDERUNG: String dynamisch bauen ---
            # Baut einen String: "M1:90 M2:90 ... M8:90"
            msg_parts = []
            for i in range(1, 9): # Loop von 1 bis 8
                msg_parts.append(f"M{i}:{self.servo_positions[i]}")
            
            # Zusammenfügen mit Leerzeichen und Zeilenumbruch am Ende
            msg = " ".join(msg_parts) + "\n"
            
            self.ser.write(msg.encode())
            
            # Optional: Debugging aktivieren, um zu sehen was rausgeht
            # print(f"Sende: {msg.strip()}") 

    def close(self):
        if self.ser:
            self.ser.close()