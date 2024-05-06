import serial
from struct import pack, unpack
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import itertools

# Se configura el puerto y el BAUD_Rate
PORT = 'COM3'  # Esto depende del sistema operativo
BAUD_RATE = 115200  # Debe coincidir con la configuracion de la ESP32

# Se abre la conexion serial
ser = serial.Serial(PORT, BAUD_RATE, timeout = 1)

# Funciones
def send_message(message):
    """ Funcion para enviar un mensaje a la ESP32 """
    ser.write(message)

def receive_response():
    """ Funcion para recibir un mensaje de la ESP32 """
    response = ser.readline()
    return response

def receive_data():
    """ Funcion que recibe tres floats (fff) de la ESP32 
    y los imprime en consola """
    data = receive_response()
    print(f"Data = {data}")
    data = unpack("fff", data)
    print(f'Received: {data}')
    return data

def send_end_message():
    """ Funcion para enviar un mensaje de finalizacion a la ESP32 """
    end_message = pack('4s', 'END\0'.encode())
    ser.write(end_message)

# Se inicializa el gráfico
fig, axs = plt.subplots(2, 2)
xlist, accx, accy, accz = [], [], [], []
RMSx, RMSy, RMSz = [], [], []
FFTx, FFTy, FFTz = [], [], []
xlistpeaks, Peaksx, Peaksy, Peaksz = [], [], [], []

ln, = axs[0, 0].plot([], [], 'ro')
ln2, = axs[0, 1].plot([], [], 'ro')
ln3, = axs[1, 0].plot([], [], 'ro')
ln4, = axs[1, 1].plot([], [], 'ro')

index = 0

def i_gen():
    for cnt in itertools.count():
        yield cnt

def init():
    axs[0, 0].set_title('Aceleración')
    axs[0, 0].set_ylim(-20, 20)
    axs[0, 1].set_title('RMS')
    axs[0, 1].set_ylim(-10, 10)
    axs[1, 1].set_title('FFT')
    axs[1, 1].set_title('Peaks')
    axs[1, 1].set_ylim(-30, 30)

def update(i, xlist, accx, accy, accz, RMSx, RMSy, RMSz, FFTx, FFTy, FFTz, xlistpeaks, Peaksx, Peaksy, Peaksz):
    global index
    # Read the sensor data
    if ser.in_waiting > 0:
        try:
            response = ser.readline()
            print("DATOS")
            print(response)

            dataRows = response.decode().strip("; \r\n").split("; ")

            accDatax, accDatay, accDataz = dataRows[:3]
            new_accx = [float(x) for x in accDatax.split(", ")]
            new_accy = [float(y) for y in accDatay.split(", ")]
            new_accz = [float(z) for z in accDataz.split(", ")]

            RMSDatax, RMSDatay, RMSDataz = dataRows[3:6]
            newRMSx = [float(x) for x in RMSDatax.split(", ")]
            newRMSy = [float(y) for y in RMSDatay.split(", ")]
            newRMSz = [float(z) for z in RMSDataz.split(", ")]
            
            FFTDatax, FFTDatay, FFTDataz = dataRows[6:9]
            newFFTx = [float(x) for x in FFTDatax.split(", ")]
            newFFTy = [float(y) for y in FFTDatay.split(", ")]
            newFFTz = [float(z) for z in FFTDataz.split(", ")]

            PeaksDatax, PeaksDatay, PeaksDataz = dataRows[9:12]
            newPeaksx = [float(x) for x in PeaksDatax.split(", ")]
            newPeaksy = [float(y) for y in PeaksDatay.split(", ")]
            newPeaksz = [float(z) for z in PeaksDataz.split(", ")]

            # Add the data to the lists
            xlist += list(range(index*500, ((index+1)*500)))
            accx += new_accx
            accy += new_accy
            accz += new_accz

            RMSx += newRMSx
            RMSy += newRMSy
            RMSz += newRMSz

            FFTx += newFFTx
            FFTy += newFFTy
            FFTz += newFFTz

            xlistpeaks += list(range(index*5, (index+1)*5))
            Peaksx += newPeaksx
            Peaksy += newPeaksy
            Peaksz += newPeaksz
            
            # Limit lists to 2000 items
            xlist = xlist[-2000:]
            accx = accx[-2000:]
            accy = accy[-2000:]
            accz = accz[-2000:]
            
            RMSx = RMSx[-2000:]
            RMSy = RMSy[-2000:]
            RMSz = RMSz[-2000:]

            FFTx = FFTx[-2000:]
            FFTy = FFTy[-2000:]
            FFTz = FFTz[-2000:]

            xlistpeaks = xlistpeaks[-50:]
            Peaksx = Peaksx[-50:]
            Peaksy = Peaksy[-50:]
            Peaksz = Peaksz[-50:]

            # Draw data
            axs[0, 0].clear()
            axs[0, 0].set_title('Aceleración')
            axs[0, 0].set_ylim(-20, 20)
            axs[0, 0].plot(xlist, accx, color="blue", label = "Eje x")
            axs[0, 0].plot(xlist, accy, color="red", label = "Eje y")
            axs[0, 0].plot(xlist, accz, color="green", label = "Eje z")
            axs[0, 0].legend()

            axs[0, 1].clear()
            axs[0, 1].set_title('RMS')
            axs[0, 1].set_ylim(-10, 10)
            axs[0, 1].plot(xlist, RMSx, color="blue", label = "Eje x")
            axs[0, 1].plot(xlist, RMSy, color="red", label = "Eje y")
            axs[0, 1].plot(xlist, RMSz, color="green", label = "Eje z")
            axs[0, 1].legend()

            axs[1, 0].clear()
            axs[1, 0].set_title('FFT')
            #axs[1, 0].set_ylim(-10, 10)
            axs[1, 0].plot(xlist, FFTx, color="blue", label = "Eje x")
            axs[1, 0].plot(xlist, FFTy, color="red", label = "Eje y")
            axs[1, 0].plot(xlist, FFTz, color="green", label = "Eje z")
            axs[1, 0].legend()

            axs[1, 1].clear()
            axs[1, 1].set_title('Peaks')
            axs[1, 1].set_ylim(-30, 30)
            axs[1, 1].plot(xlistpeaks, Peaksx, color="blue", label = "Eje x")
            axs[1, 1].plot(xlistpeaks, Peaksy, color="red", label = "Eje y")
            axs[1, 1].plot(xlistpeaks, Peaksz, color="green", label = "Eje z")
            axs[1, 1].legend()

            index += 1

        except KeyboardInterrupt:
            print('Finalizando comunicacion')
            
        """ except:
            print('Error en leer mensaje') """


# # Se lee data por la conexion serial
# counter = 0
while True:
    if ser.in_waiting > 0:
        response = ser.readline()
        parsed = str(response.decode()).replace("\r", "").replace("\n", "")
        if parsed == "BEGIN":
            send_message("OK\0".encode())
            print("Conexión establecida")
            break
        else:
            print("PARSED",parsed)


# while True:
#     print(ser.in_waiting)
#     if ser.in_waiting > 0:
#         try:
#             response = ser.readline()
#             print("DATOS")
#             print(response)
#         except KeyboardInterrupt:
#             print('Finalizando comunicacion')
#             break
#         except:
#             print('Error en leer mensaje')
#             continue

anim = FuncAnimation(fig, update, i_gen, init_func=init, save_count=200, fargs=(xlist, accx, accy, accz, RMSx, RMSy, RMSz, FFTx, FFTy, FFTz, xlistpeaks, Peaksx, Peaksy, Peaksz))
plt.show()
