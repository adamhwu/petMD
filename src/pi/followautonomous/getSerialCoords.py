import serial

# Adjust this to your ESP32's serial port (check with `ls /dev/tty*`)
SERIAL_PORT = '/dev/ttyUSB0'
BAUD_RATE = 9600

def is_valid_char(c):
    return c.isdigit() or c == ','

def main():
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)

    while True:
        raw_data = ser.read_until(b'U')  # read until 'U' terminator
        raw_str = raw_data.decode(errors='ignore').strip()

        buffer = raw_str.replace('U', '')  # Remove the delimiter
        cleanout = ''.join(c for c in buffer if is_valid_char(c))

        if cleanout.count(',') != 2:
            print("[!] Failure - bad format:", cleanout)
            continue

        try:
            x_str, y_str, dist_str = cleanout.split(',')
            x = int(x_str)
            y = int(y_str)
            distance = int(dist_str)

            print(f"[✓] Success: x={x}, y={y}, distance={distance}")
            # ➜ You can now pass these to motor control, vision, etc.
        except ValueError:
            print("[!] Parse error:", cleanout)

if __name__ == "__main__":
    main()
