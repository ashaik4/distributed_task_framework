import click
import requests
import json
import socketio 
import time


sio = socketio.Client()

@click.command()
# @click.option('--name', prompt='Your name', help='The person to greet.')
# @click.option('--age', prompt='Your age', help='Your current age.')
@click.option('--n', prompt='Nth Fibonacci', help='The nth fibonacci number to generate.')
def send_request(n):
    url = 'http://localhost:5001/api/fibonacci'
    payload = {
        'n': n
    }

    headers = {'content-type': 'application/json'}

    response = requests.post(url, data=json.dumps(payload), headers=headers)

    if response.status_code == 200:
        click.echo('Data sent successfully!')
        sio.emit('socketio Data sent successfully!')
        click.echo('Server response: {}'.format(response.json()))
    else:
        click.echo('Failed to send data. Server responded with status code: {}'.format(response.status_code))

@sio.event
def connect():
    print('Connected to server')

@sio.event
def disconnect():
    print('Disconnected from server')

@sio.event
def log(data):
    print('Log: ', data)

if __name__ == '__main__':
    connected = False 
    while not connected:
        try:
            sio.connect('http://localhost:5001')
            connected = True
            send_request()
            sio.wait()
        except Exception as e:
            print("Failed to establish initial connnection to server:", type(e).__name__)
            time.sleep(2)
    #sio.connect('http://localhost:5001')
    
