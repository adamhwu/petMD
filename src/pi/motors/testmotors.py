# pi/motors/motor_test.py

from motor import move, stop, cleanup
import time

def test_motors():
    print("[🟢] Testing motors...")

    try:
        print("➡️ Moving forward")
        move(50, 50)
        time.sleep(2)

        print("⬅️ Moving backward")
        move(-50, -50)
        time.sleep(2)

        print("↪️ Turning right")
        move(50, 20)
        time.sleep(2)

        print("↩️ Turning left")
        move(20, 50)
        time.sleep(2)

        print("🛑 Stopping")
        stop()
        time.sleep(1)

    finally:
        print("[✅] Cleanup complete")
        cleanup()

if __name__ == "__main__":
    test_motors()
