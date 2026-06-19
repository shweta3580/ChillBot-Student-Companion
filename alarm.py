import time
import threading
import winsound  # For Windows alarm sound

def ring_alarm():
    """Plays an alarm sound when the alarm goes off."""
    print("⏰ Alarm ringing! Time's up! ⏰")
    for _ in range(5):  # Repeat sound 5 times
        winsound.Beep(1000, 500)  # Windows beep sound (1000 Hz, 500 ms)
        time.sleep(1)

def set_alarm(alarm_time):
    """Waits until the alarm time and then rings the alarm."""
    while True:
        current_time = time.strftime("%H:%M")
        if current_time == alarm_time:
            ring_alarm()
            break
        time.sleep(30)  # Check time every 30 seconds

# Example: Set an alarm for 14:30
alarm_time = input("Enter alarm time (HH:MM): ")  
print("Alarm set for:", alarm_time)  
threading.Thread(target=set_alarm, args=(alarm_time,)).start()