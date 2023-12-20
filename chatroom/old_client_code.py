import socket
import random
import pytz
import threading
from datetime import datetime
from colorama import Fore, init, Back

init()

host = '127.0.0.1'
port = 55555

separator_token = "<SEP>"

# Choosing Nickname
username = input("Enter your username: ")

colors = [Fore.RED, Fore.BLUE, Fore.YELLOW, Fore.CYAN, Fore.GREEN ]
userclr = random.choice(colors)

# Set the timezone to IST (UTC+5:30)
ist = pytz.timezone('Asia/Kolkata')

# Connecting To Server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((host, port))

# Listening to Server and Sending Nickname      
def receive():
    while True:
        try:
            # Get the current time in Kolkata
            now = datetime.now(ist)

            # Format the time string in 12-hour format
            current_time = now.strftime('%Y-%m-%d %I:%M:%S %p')

            # Receive Message From Server If 'User' Send Nickname
            message = client.recv(1024).decode('ascii')
            # new = f"{userclr}[{date_now}] {username}{separator_token}{message}{Fore.RESET}"
            new = f"{userclr}[{current_time}] {Fore.RESET}"
            
            if message == 'getName':
                client.send(username.encode('ascii'))
            else:
                # Print the message only if it's not from the current user
                if username not in message:
                    print(new + message)
        except:
            # Close Connection When Error
            print('error')
            client.close()
            break


# Sending Messages To Server        
def write():
    while True:
        message = '{}: {}'.format(username, input(''))
        client.send(message.encode('ascii'))

# Starting Threads For Listening And Writing        
receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()