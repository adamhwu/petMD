# testmotors.py
from motors import init, move, stop, cleanup
import time

def test_motors():
    print("[🟢] Testing motors...")

    try:
        init()  # ✅ Make sure GPIO and PWM are set up

        print("➡️ Moving forward")
        move(90, 80)
        time.sleep(2)

        

    except Exception as e:
        print(f"[❌] Error occurred: {e}")

    finally:
        print("[✅] Cleanup complete")
        cleanup()

if __name__ == "__main__":
    test_motors()

