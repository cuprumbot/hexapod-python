# hexapod-python

## Preparando la Raspberry Pi

Instala Raspbian usando [Imager](https://www.raspberrypi.com/software/)

Es posible que la Raspi no quede lista para usarse mediante SSH, entonces se necesitará comenzar con pantalla y teclado.

## Habilita SSH

Tras instalar Raspbian entramos a la Raspi y configuramos la red que vamos a usar. 

Luego ejecutamos `sudo raspi-config` y buscamos `Interfacing Options`. Vamos a la opción de `SSH` y lo habilitamos.

## Instalando librerías

Comenzamos instalando y configurando las librerías para I2C.

`sudo apt install python3-smbus`

`sudo apt install i2c-tools`

[Configurar I2C](https://learn.adafruit.com/adafruits-raspberry-pi-lesson-4-gpio-setup/configuring-i2c)

Después instalamos la librería de Adafruit (circuitpython)

[Instalar librería](https://learn.adafruit.com/circuitpython-on-raspberrypi-linux/installing-circuitpython-on-raspberry-pi)

## Controlando el hexapod desde el teléfono

Ver PDF adjunto con instrucciones detalladas para hacer SSH hacia la Raspi desde nuestro teléfono.