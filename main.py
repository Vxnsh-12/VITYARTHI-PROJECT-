import cv2
import numpy as np
import time
import winsound
import os
import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import subprocess # To open folders


NOD_THRESHOLD = 40  
SAFETY_SCORE_MAX = 100
PENALTY_RATE = 2   
RECOVERY_RATE = 1  
DARKNESS_LIMIT = 60 



def save_evidence(frame, score):
    """Saves photo and log WITHOUT connecting to internet"""
    if not os.path.exists('evidence'):
        os.makedirs('evidence')
        
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"evidence/INCIDENT_{timestamp}.jpg"
    
    print(">>> SAVING BLACK BOX DATA (LOCAL)...") 
    
    cv2.imwrite(filename, frame)
    
    # Log without GPS data
    with open("evidence/flight_recorder_log.txt", "a") as f:
        f.write(f"ALERT: {datetime.now()} | Score: {score} | Location: OFFLINE_MODE | Proof: {filename}\n")
    
    return filename

def draw_hud_box(img, x, y, w, h, color, alpha=0.4):
    """Draws a see-through glass panel"""
    overlay = img.copy()
    cv2.rectangle(overlay, (x, y), (x + w, y + h), color, -1)
    cv2.addWeighted(overlay, alpha, img, 1 - alpha, 0, img)

def draw_static_dashboard(frame, width, height, current_score):
    """Draws the UI elements that should ALWAYS be visible"""
    # 1. Top Bar
    draw_hud_box(frame, 0, 0, width, 60, (20, 20, 20), 0.8)
    cv2.line(frame, (0, 62), (width, 62), (0, 255, 0), 2)
    cv2.putText(frame, "SLEEPGUARD OFFLINE v2.0", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    
    # 2. Bottom Bar
    draw_hud_box(frame, 0, height-50, width, 50, (20, 20, 20), 0.8)
    cv2.line(frame, (0, height-52), (width, height-52), (0, 255, 0), 2)
    cv2.putText(frame, "SYSTEM STATUS: LOCAL MONITORING ACTIVE", (20, height-15), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (200, 200, 200), 1)

    # 3. Health Bar Background
    draw_hud_box(frame, 20, height//2 - 100, 40, 200, (0, 0, 0), 0.6)
    cv2.rectangle(frame, (20, height//2 - 100), (60, height//2 + 100), (255, 255, 255), 2)
    
    # Filled Bar Logic
    bar_h = int((current_score / SAFETY_SCORE_MAX) * 200)
    bar_color = (0, 255, 0) # Green
    if current_score < 50: bar_color = (0, 165, 255) # Orange
    if current_score < 20: bar_color = (0, 0, 255) # Red
    
    start_y = height//2 + 100
    cv2.rectangle(frame, (25, start_y - bar_h), (55, start_y), bar_color, -1)
    cv2.putText(frame, "HP", (25, start_y + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)

def start_monitoring():
   
    
    if not os.path.exists('haarcascade_frontalface_default.xml'):
        messagebox.showerror("Error", "Missing XML file! Please download 'haarcascade_frontalface_default.xml'")
        return

    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    cap = cv2.VideoCapture(0)
    cap.set(3, 1280)
    cap.set(4, 720)

    baseline_y = 0
    is_calibrated = False
    calibration_frames = 0
    current_score = SAFETY_SCORE_MAX
    evidence_cooldown = 0 
    
    print("--- CAMERA STARTED ---")

    while True:
        ret, frame = cap.read()
        if not ret: break

        h, w, _ = frame.shape
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # --- DRAW UI ---
        draw_static_dashboard(frame, w, h, current_score)
        
        # Night Vision Check
        if np.mean(gray) < DARKNESS_LIMIT:
            cv2.putText(frame, "⚠️ LOW LIGHT", (w-200, h-20), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

        faces = face_cascade.detectMultiScale(gray, 1.1, 5)

        if len(faces) > 0:
            (x, y, f_w, f_h) = faces[0]
            center_y = y + (f_h // 2)
            
            cv2.rectangle(frame, (x, y), (x+f_w, y+f_h), (0, 255, 255), 1)
            cv2.line(frame, (x, center_y), (x+f_w, center_y), (0, 255, 255), 1)

            if not is_calibrated:
                calibration_frames += 1
                progress = int((calibration_frames / 50) * 100)
                cv2.putText(frame, f"CALIBRATING {progress}%", (w//2 - 100, h//2), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)
                if calibration_frames >= 50:
                    baseline_y = center_y
                    is_calibrated = True
                    winsound.Beep(1000, 150)
            else:
                displacement = center_y - baseline_y
                
                # Logic
                if displacement > NOD_THRESHOLD:
                    current_score -= PENALTY_RATE
                    cv2.putText(frame, "HEAD DROPPING!", (w//2 - 100, h//2), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                else:
                    current_score += RECOVERY_RATE
                
                current_score = max(0, min(SAFETY_SCORE_MAX, current_score))

                if current_score == 0:
                    draw_hud_box(frame, 0, 0, w, h, (0, 0, 255), 0.3)
                    cv2.putText(frame, "DRIVER ASLEEP!", (w//2 - 200, h//2), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 5)
                    winsound.Beep(3000, 100)
                    
                    if evidence_cooldown == 0:
                        cv2.putText(frame, "SAVING LOGS...", (w//2 - 80, h//2 + 60), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
                        cv2.imshow('SleepGuard Monitor', frame)
                        cv2.waitKey(1)
                        save_evidence(frame, current_score)
                        evidence_cooldown = 100 
                
                if evidence_cooldown > 0: evidence_cooldown -= 1

        else:
            cv2.putText(frame, "SEARCHING FOR DRIVER...", (w//2 - 200, h//2), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)

        cv2.imshow('SleepGuard Monitor', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


    if not os.path.exists('evidence'):
        os.makedirs('evidence')
    os.startfile('evidence')

def create_gui():
    root = tk.Tk()
    root.title("SleepGuard Command Center")
    root.geometry("400x500")
    root.configure(bg="#101010")

    tk.Label(root, text="SLEEPGUARD", font=("Impact", 30), fg="#00ff00", bg="#101010").pack(pady=(50, 5))
    tk.Label(root, text="OFFLINE DRIVER MONITORING", font=("Arial", 10, "bold"), fg="#888888", bg="#101010").pack(pady=(0, 50))

    btn_config = {"font": ("Arial", 11, "bold"), "width": 30, "height": 2, "bd": 0, "cursor": "hand2"}
    
    tk.Button(root, text="▶ INITIALIZE CAMERA", bg="#00cc00", fg="white", command=start_monitoring, **btn_config).pack(pady=10)
    tk.Button(root, text="📂 OPEN LOCAL LOGS", bg="#0088cc", fg="white", command=open_folder, **btn_config).pack(pady=10)
    tk.Button(root, text="✖ SHUTDOWN", bg="#cc0000", fg="white", command=root.destroy, **btn_config).pack(pady=10)

    tk.Label(root, text="System Ready | Local Mode", font=("Arial", 8), fg="gray", bg="#101010").pack(side="bottom", pady=20)

    root.mainloop()



    create_gui()

