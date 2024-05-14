# Proyecto de Microcontroladores con ESP32 y Sensor Inercial BOSCH BMI270

## Descripción

Este proyecto consiste en la integración de un microcontrolador ESP32 con un sensor inercial BOSCH BMI270.

Se establece una comunicación serial I2C entre el ESP32 y el sensor BMI270 para controlar su configuración y obtener mediciones. Estas mediciones se transmiten a un computador a través de una conexión serial UART, donde serán mostradas.

## Características del Sensor Inercial (IMU) BMI270

El sensor BMI270 tiene diferentes modos de poder que deben ser implementados:

- **Modo de bajo rendimiento**
- **Modo de medio rendimiento**
- **Modo de alto rendimiento**
- **Modo de suspensión**

Adicionalmente, es necesario poder cambiar la configuración de sensibilidad y la frecuencia de muestreo (ODR) tanto para el giroscopio como para el acelerómetro del sensor.

## Modo de Uso

=========== [Modo de uso] ===========
p1 : Suspend Power Mode
p2 : Lower Power Mode
p3 : Normal Power Mode
p4 : Performance Power Mode
s1 : Cambio a rango +/-2g
s2 : Cambio a rango +/-4g
s3 : Cambio a rango +/-8g
s4 : Cambio a rango +/-16g
a1 : Cambio frecuencia de muestreo 200Hz
a2 : Cambio frecuencia de muestreo 400Hz
a3 : Cambio frecuencia de muestreo 800Hz
a4 : Cambio frecuencia de muestreo 1600Hz
===================================

## Recursos

- [Datasheet del BMI270](https://www.bosch-sensortec.com/products/motion-sensors/imus/bmi270/)
- [Documentación ESP-IDF](https://docs.espressif.com/projects/esp-idf/en/latest/esp32/)

## Video Demostración

Para una demostración visual del proyecto, ver el siguiente video: [Video Demostración](https://youtu.be/ibvGQPzwFDM?si=VdsOHDcw-h0leEQ3)
