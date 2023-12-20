import tkinter as tk
from tkinter import scrolledtext
import socket
import threading
from datetime import datetime
import random
from colorama import Fore, init

init()

host = '127.0.0.1'
port = 55555
separator_token = "<SEP>"

# Choosing Nickname
username = input("Enter your username: ")

colors = [Fore.RED, Fore.BLUE, Fore.YELLOW, Fore.CYAN, Fore.GREEN]
userclr = random.choice(colors)

# Set up the tkinter window
root = tk.Tk()
root.title("Chatroom")

# Create a scrolled text widget for the chat messages
chat_text = scrolledtext.ScrolledText(root, wrap=tk.WORD)
chat_text.grid(row=0, column=0, padx=10, pady=10, columnspan=2)

# Create an entry widget for typing messages
entry_message = tk.Entry(root, width=25)
entry_message.grid(row=1, column=0, padx=10, pady=10)

# Function to send a message when Enter key is pressed
def send_message(event=None):
    message = entry_message.get()
    if message:
        entry_message.delete(0, tk.END)
        client.send(f"{username}: {message}".encode('ascii'))

# Bind the Enter key to the send_message function
root.bind('<Return>', send_message)

# Button to send messages
send_button = tk.Button(root, text="Send", command=send_message)
send_button.grid(row=1, column=1, padx=10, pady=10)

# Function to update the chat window with received messages
def update_chat_window(message, is_user=False):
    # Get the current time
    now = datetime.now().strftime('%I:%M:%S %p')
    
    if is_user:
        # If the message is from the user, display on the right side
        formatted_message = f"{now} {message}"
        chat_text.tag_configure("right", justify='right')
        chat_text.insert(tk.END, formatted_message + '\n', "right")
    else:
        # If the message is from others, display on the left side
        formatted_message = f"{now} {message}"
        chat_text.tag_configure("left", justify='left')
        chat_text.insert(tk.END, formatted_message + '\n', "left")

    chat_text.yview(tk.END)  # Scroll to the bottom

# Function to receive messages from the server
def receive():
    while True:
        try:
            message = client.recv(1024).decode('ascii')
            if message == 'getName':
                client.send(username.encode('ascii'))
            else:
                # Check if the message is from the current user
                is_user_message = username in message
                update_chat_window(message, is_user=is_user_message)
        except:
            # Close Connection When Error
            print('error')
            client.close()
            break

# Connect to the server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((host, port))

# Start the receive thread
receive_thread = threading.Thread(target=receive)
receive_thread.start()

# Start the Tkinter main loop
root.mainloop()
