import serial
import time
import schedule
import math



if __name__ == "__main__":

    while True:
        arduino = serial.Serial('/dev/cu.usbmodem1301', 115200)
        #print(arduino)
        arduino_data = arduino.readline()
        

        #decoded_values = str(arduino_data[0:len(arduino_data)].decode("utf-8"))
        try:
            decoded_values = arduino_data.decode("utf-8")
            #print(decoded_values)
            list_values = decoded_values.split()
            distance = float(list_values[0])
            actual_pitch = math.radians(float(list_values[1]))
            actual_roll = math.radians(float(list_values[2]))
            actual_yaw = math.radians(float(list_values[3]))

            yaw = actual_roll
            pitch = actual_pitch

            print("p: {} r: {} y: {}".format(pitch, actual_roll, yaw))

            x = distance * math.sin(yaw) * math.cos(pitch)
            y = distance * math.sin(pitch)
            z = distance * math.cos(yaw) * math.cos(pitch)

            print("{} {} {}".format(x, y, z))

        except:
            print("decode exception XD")
        
