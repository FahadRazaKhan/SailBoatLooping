'''
@author: Fahad Raza
Data: Nov. 10, 2017
Project: CUHK(SZ) Hybrid Sailboat
Embedded Controller: Raspberry Pi Zero W

Description:

         This program is for performing continous Autonomous loops (Open-loop) of a
         Hybrid Sailboat. It also measures and stores the Current Sensor values in
         XLSX file. Looping and Current measuring functions run on two different threads
         simultaneously. 



'''


import socket
from ina219 import INA219
from ina219 import DeviceRangeError
import xlsxwriter
from collections import deque
import sys
import time
import pigpio
import threading
import RPi.GPIO as GPIO
import os
os.system('sudo pigpiod')
time.sleep(1)




#-------Autonomous Looping--------------------

def looping():
    
    while True:
        
        
    
        ReceivedData = 'Y' #str(data.decode('utf-8'))
    
        if ReceivedData.upper() == "C": # if User sends 'C' cancel the looping
            break
        else:
            pi.set_servo_pulsewidth(ESC1, 1150)
            pi.set_servo_pulsewidth(ESC2, 1150)
            time.sleep(4)

            pi.set_servo_pulsewidth(ESC1, 0)
            pi.set_servo_pulsewidth(ESC2, 0)
            time.sleep(3)

            pi.set_servo_pulsewidth(ESC1,1150)
            pi.set_servo_pulsewidth(ESC2,0)
            time.sleep(3)

            pi.set_servo_pulsewidth(ESC1,0)
            pi.set_servo_pulsewidth(ESC2,0)
            time.sleep(4)

            pi.set_servo_pulsewidth(ESC1,1150)
            pi.set_servo_pulsewidth(ESC2,1150)
            time.sleep(4)

            pi.set_servo_pulsewidth(ESC1,0)
            pi.set_servo_pulsewidth(ESC2,0)
            time.sleep(3)

            pi.set_servo_pulsewidth(ESC1,0)
            pi.set_servo_pulsewidth(ESC2,1150)
            time.sleep(2)

            pi.set_servo_pulsewidth(ESC1,0)
            pi.set_servo_pulsewidth(ESC2,0)
            time.sleep(3)

            pi.set_servo_pulsewidth(ESC1,1150)
            pi.set_servo_pulsewidth(ESC2,1150)
            time.sleep(4)

            pi.set_servo_pulsewidth(ESC1,0)
            pi.set_servo_pulsewidth(ESC2,0)

            break



    pi.set_servo_pulsewidth(ESC1,0)
    pi.set_servo_pulsewidth(ESC2,0)
    time.sleep(0.4)
    pi.stop()
    time.sleep(0.5)
    global flag 
    flag = True # Updating flag value
    message = 'Motors Stopped, and Looping Finished'
    messageBytes = message.encode('utf-8')
    conn.sendall(messageBytes) #Send Message
    time.sleep(0.5)

    conn.close()
    time.sleep(1)
    print('Connection closed!')
    

#------------------------------------------------


''' Current Sensor Reading and Data Recording'''

    
    
def Sensor():

    try:
						        
    					
        print('Starting Current Sensor')
        print('Collecting Sensor Values...')
        start = time.time() # Start Time
        row = 1 # Starting Row (0 indexed)
        col = 0 # Starting Column (0 indexed) 

        DataPoints = deque(maxlen=None) # Creating Array of datatype deque to store values




        while True:
            #print('Flag is ',flag)

            if flag: # Break when flag = True
                break
        
            

            ina = INA219(Shunt_OHMS) # Auto Gain
            ina.configure()
            print('Bus Voltage: %.3f V' % ina.voltage())

            try:
                print('Bus Current: %.3f mA' % ina.current())
                print('Power: %.3f mW' % ina.power())
                currentvalue = round(ina.current()) # Rounding off values to nearest integer
                voltagevalue = float('{0:.1f}'.format(ina.voltage())) # Floating point up to one decimal point
                powervalue = round(ina.power())
                timevalue = float('{0:.1f}'.format(time.time()-start)) # Elapsed time in Seconds with 1 decimal point floating number 

                DataPoints.append([timevalue, currentvalue, voltagevalue, powervalue]) # Updating DataPoints Array

            except DeviceRangeError:
                print('Device Range Error')

            time.sleep(0.5) # Reading value after half second
            



        n = len(DataPoints) # Total number of rows
        print('Total number of rows: ',n)

        print('Writing Data into Worksheet')
        
        for Time, value1, value2, value3 in (DataPoints): # Writing Data in XLSX file
            
            worksheet.write(row, col, Time)
            worksheet.write(row, col+1, value1)
            worksheet.write(row, col+2, value2)
            worksheet.write(row, col+3, value3)
            row += 1

        chart1 = workbook.add_chart({'type': 'line'}) # adding chart of type 'Line' for Current values
        chart2 = workbook.add_chart({'type': 'line'}) # Chart for Voltage
        chart3 = workbook.add_chart({'type': 'line'}) # Chart for Power

        
    
        chart1.add_series({'name':['Sheet1',0,1],
                           'categories': ['Sheet1', 1,0,n,0],
                           'values': ['Sheet1', 1,1,n,1]
                           })
        chart2.add_series({'name':['Sheet1',0,2],
                           'categories': ['Sheet1', 1,0,n,0],
                           'values': ['Sheet1', 1,2,n,2]
                           })
        chart3.add_series({'name':['Sheet1',0,3],
                           'categories': ['Sheet1', 1,0,n,0],
                           'values': ['Sheet1', 1,3,n,3]
                           })
    
        chart1.set_title({'name': 'Current Chart'}) # Setting Title name
        chart1.set_x_axis({'name': 'Elapsed Time (s)'}) # Setting X-Axis name
        chart1.set_y_axis({'name': 'Value'}) # Setting Y-Axis name

        chart2.set_title({'name': 'Voltage Chart'})
        chart2.set_x_axis({'name': 'Elapsed Time (s)'})
        chart2.set_y_axis({'name': 'Value'})

        chart3.set_title({'name': 'Power Chart'})
        chart3.set_x_axis({'name': 'Elapsed Time (s)'})
        chart3.set_y_axis({'name': 'Value'})


        chart1.set_style(8) # Setting Chart Color
        chart2.set_style(5)
        chart2.set_style(9)

        worksheet.insert_chart('D2', chart1, {'x_offset': 25, 'y_offset': 10}) # Inserting Charts in the Worksheet
        worksheet.insert_chart('D2', chart2, {'x_offset': 25, 'y_offset': 10}) # //
        worksheet.insert_chart('D5', chart3, {'x_offset': 25, 'y_offset': 10}) # //


    except:

        print('An Error Occured during sensor reading, Please try again!')


    workbook.close() # Closing Workbook 
    time.sleep(1)
    print('Sensor Reading Stopped')
    

#------------------------------------------------

# ESC Calibration Function

def ESC_Calibration():
    
    print('Starting ESC Calibration')
    message = 'Starting ESC Calibration...'
    messageBytes = message.encode('utf-8') # Encoding message
    conn.sendall(messageBytes) # Sending Data

    pi.set_servo_pulsewidth(ESC1,1000) # Min. Throttle
    pi.set_servo_pulsewidth(ESC2,1000) # Min. Throttle
    time.sleep(2)

    pi.set_servo_pulsewidth(ESC1,2000) # Max. Throttle
    pi.set_servo_pulsewidth(ESC2,2000) # Max. Throttle
    time.sleep(2)

    pi.set_servo_pulsewidth(ESC1,1100) # Slightly open throttle
    pi.set_servo_pulsewidth(ESC2,1100) # Slightly open throttle
    time.sleep(1)

    pi.set_servo_pulsewidth(ESC1,0)
    pi.set_servo_pulsewidth(ESC2,0)

    time.sleep(1)
    print('E.S.C Calibrated')
    message = 'E.S.C Calibrated successfully'
    messageBytes = message.encode('utf-8')
    conn.sendall(messageBytes) # Sending message
    time.sleep(1)
    

#------------------------------------------------------




def main():


    global flag
    flag = False # Initialising flag

    #-----------ESC Calibration----------------------



    

    if ReceivedData.upper() == "Y": # If User send Y then Start Calibration
    
        ESC_Calibration()

    # Starting threads for parallel processing

    
        t1 = threading.Thread(target= looping)
        t2 = threading.Thread(target= Sensor)
    

        t1.start() # start thread 1
    
        t2.start() # start thread 2

    
        t1.join() # wait for the t1 thread to complete
        t2.join() # wait for the t2 thread to complete
    

    else:
        pi.set_servo_pulsewidth(ESC1,0)
        pi.set_servo_pulsewidth(ESC2,0)
        print('Program Aborted!')
        message = 'Program Aborted!'
        messageBytes = message.encode('utf-8')
        conn.sendall(messageBytes) # Sending message
        time.sleep(0.5)

        conn.close()
        time.sleep(1)
        print('Connection closed!')
        


    #---------------------------------------------



    
    	
    







#-----------TCP Connectivity-----------------
    ''' Establishing a TCP connection with client '''

    
TCP_IP = ''
TCP_PORT = 50007
BUFFER_SIZE = 1024
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print('Server socket is created')
try:
    s.bind((TCP_IP, TCP_PORT))
except:
    print('Error: No binding could be done')
    sys.exit()

s.listen(0)
print('Socket is now listening')

conn,addr = s.accept()
print('Connection address:', addr)

message = 'Command Received!'
messageBytes = message.encode('utf-8')

data = conn.recv(BUFFER_SIZE)  # Receiving Data       
ReceivedData = str(data.decode('utf-8')) # Decoding Data
print('Data Received : ', ReceivedData)

conn.sendall(messageBytes) #Sending Data back to Client for confirmation
time.sleep(1)
#--------------------------------------------------


# Data Recording


workbook = xlsxwriter.Workbook('SensorValues01.xlsx',{'constant_memory': True})  # Creating XLSX File for Data Keeping 
worksheet = workbook.add_worksheet() # Generating worksheet

bold = workbook.add_format({'bold':True}) # Formating for Bold text

worksheet.write('A1', 'Time', bold) # Writing Column Titles
worksheet.write('B1', 'Current (mA)', bold)
worksheet.write('C1', 'Voltage (v)', bold)
worksheet.write('D1', 'Power (mW)', bold)





Shunt_OHMS = 0.1 # For this sensor it is 0.1 ohm
#Max_Expected_Amps = 0.2 # must be close to expected value in Amps


#----------------------------------------------------------


# ------ESC Configuration-----------

ESC1 = 23 # GPIO Pin for ESC1
ESC2 = 27 # GPIO Pin for ESC2

pi = pigpio.pi()

#-----------------------------------


main() # Calling main function




        
    


