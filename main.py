# importa o client do adafruit
from Adafruit_IO import MQTTClient
import time
import sys

# importa gpio para realizar os acionamentos
import RPi.GPIO as GPIO 


# Seu username criado no adafruit IO
# Chave gerada para o username no adafruit IO
USER_ADAFRUIT = 'ADAFRUIT_USER_NAME' #'TEU_USER_NAME'
USER_ADAFRUIT_KEY = 'aio_ADAFRUIT_KEY'


# ---- FEED predentido, por exemplo LAMPADA-1
IO_FEED1 = 'LAMPADA-1'
IO_FEED2 = 'LAMPADA-2'
IO_FEED3 = 'LAMPADA-3'
# Username dono do feed - geralmente o mesmo de cima
IO_FEED_USERNAME = USER_ADAFRUIT

# configuracoes de GPIO
GPIO.setmode(GPIO.BCM)  # Indica que utilizaremos o endereçamento dos GPIOS que aparecem no PINOUT e nao o numero do PINO
GPIO.setup(2, GPIO.OUT) # quero que meu pino GPIO02 seja output

##################### vou criar metodos pra usar o mqtt client e ficar ouvindo um topico
def connected(client):
    # quando conctado, ele subscreve num topico
    client.subscribe(IO_FEED1, IO_FEED_USERNAME)
    client.subscribe(IO_FEED2, IO_FEED_USERNAME)
    client.subscribe(IO_FEED3, IO_FEED_USERNAME)

def disconnected(client):
    print('conexao fechou. fecha o programa')
    sys.exit(1)

def message(client, feed_id, payload):
    # quando recebe a informacao do topico
    # Aprensentamos na sysout os dados recebidos
    print('Feed {0} novo valor recebido: {1}'.format(feed_id, payload))

    if feed_id == IO_FEED1:
    # Aciona ou nao a GPIO
        GPIO.output(2, payload == 'Ligado') # Quando usamos Ligado x Desligado no botao configurado no dashboard do adafruit, caso contrario, usar ON/OFF
    if feed_id == IO_FEED2:
    # Aciona ou nao a GPIO
        GPIO.output(3, payload == 'Ligado') # Quando usamos Ligado x Desligado no botao configurado no dashboard do adafruit, caso contrario, usar ON/OFF

    if feed_id == IO_FEED3:
    # Aciona ou nao a GPIO
        GPIO.output(4, payload == 'Ligado') # Quando usamos Ligado x Desligado no botao configurado no dashboard do adafruit, caso contrario, usar ON/OFF

#-------------------- Area de instancias
# Cria instancia mqtt.
client = MQTTClient(USER_ADAFRUIT, USER_ADAFRUIT_KEY)

# seta os metodos de callback para cair nos metodos criados anteriormente, 
# a partir de cada evento.
client.on_connect       =   connected
client.on_disconnect    =   disconnected
client.on_message       =   message

# tenta conectar
client.connect()

# abre uma thread pra ficar ouvindo o topico em background
client.loop_background()

# Segura o script ligado, apenas ouvindo
while True:
     time.sleep(10)
     print ('Estado do GPIO -> ' + str(GPIO.input(2)))





