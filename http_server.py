import socket
import threading
import datetime
from http_request_anatomical import HttpAnatomical

# Define constants for the server
HOST = 'localhost'
PORT = 8000
MAX_CLIENTS = 5

# Create a dictionary to hold all connected clients and their usernames
connected_clients = {}
username_to_socket = {}
usernames_set = set()

# Create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to a specific address and port
server_socket.bind((HOST, PORT))

# Listen for incoming connections
server_socket.listen(MAX_CLIENTS)


# Function to handle incoming client connections
def handle_client_send(client_socket, client_address):
    request = client_socket.recv(1024).decode()
    http_anatomical = HttpAnatomical(request)
    param = http_anatomical.get_query_param()
    if not param:
        age_results = """<h1>Welcome in My Fridge
        <h3>How to use:</h3>http://localhost:8000/YYYY-MM-DD
        <h3>Example:</h3>http://localhost:8000/2001-12-21
        <h4>created by:</h4>Hkraaat
        """
    else:
        try:
            d = datetime.date.fromisoformat(param)
            age_in_seconds = (datetime.date.today() - d).total_seconds()
            age_in_minutes = age_in_seconds / 60
            age_in_hours = age_in_minutes / 60
            age_in_days = age_in_hours / 24
            age_results = f"""
    <h1>Results</h1>
    <h3>Age in Seconds</h3> = {age_in_seconds}
    <h3>Age in Minutes</h3> = {age_in_minutes}
    <h3>Age in Hours</h3> = {age_in_hours}
    <h3>Age in Days</h3> = {age_in_days}
    """
        except ValueError:
            age_results = "Invalid Date Format!. The valid date format is YYYY-MM-DD."
    
   
    body  = f"""<html><body>{age_results}</body></html>"""
    body_length = len(body)
    headers = f"""HTTP/1.1 200 OK
Content-Type: text/html charset=UTF-8
content-length: {body_length}

"""
    """GET / HTTP/1.1
    """
    response = headers + body
    client_socket.send(response.encode())
    # print(response.encode())
    # client_socket.close()
    client_socket.close()

# Function to handle client requests for the list of connected clients
def list_clients(client_socket):
    client_list = ""
    for c in connected_clients.values():
        client_list += c + "\n"
    if client_list == "":
        client_socket.send(client_list.encode())


# Main loop to handle incoming connections
while True:
    # Accept incoming connections
    client_socket, client_address = server_socket.accept()

    # Create a new thread to handle client requests for the list of connected clients
    list_thread = threading.Thread(target=list_clients, args=(client_socket,))
    list_thread.start()

    # Create a new thread to handle the client connection
    client_thread_send = threading.Thread(
        target=handle_client_send, args=(client_socket, client_address))
    client_thread_send.start()
    