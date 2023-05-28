import socket
import threading
from datetime import datetime
from http_request_anatomical import HttpAnatomical

# Define constants for the server
HOST = 'localhost'
PORT = 8000
MAX_CLIENTS = 5

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
        age_results = """
<!DOCTYPE html>
<html>

<head>
    <title>Welcome to our page</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 20px;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            background-color: #f5f5f5;
        }

        .container {
            text-align: center;
            max-width: 500px;
            padding: 40px;
            background-color: #fff;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            border-radius: 4px;
        }

        h1 {
            color: #333;
            margin-bottom: 20px;
        }

        h3 {
            color: #333;
            margin-top: 30px;
            margin-bottom: 10px;
        }

        h4 {
            color: #333;
            margin-top: 10px;
        }

        a {
            color: #0066cc;
            text-decoration: none;
        }

        a:hover {
            text-decoration: underline;
        }
    </style>
</head>

<body>
    <div class="container">
        <h1>Welcome to our page</h1>
        <h3>How to use:</h3>
        <p>http://localhost:8000/YYYY-MM-DD</p>
        <h3>Example:</h3>
        <p>For example, you can visit:</p>
        <pre><a href="http://localhost:8000/2001-12-21">http://localhost:8000/2001-12-21</a></pre>
        <h3>Created by:</h3>
        <p>Hkraaat</p>
    </div>
</body>

</html>
        """
    else:
        try:
            start_time = datetime.fromisoformat(param)
            current_time = datetime.now()
            age_in_seconds = (current_time - start_time).total_seconds()
            age_in_minutes = age_in_seconds / 60
            age_in_hours = age_in_minutes / 60
            age_in_days = age_in_hours / 24
            age_in_years = age_in_days / 360
            age_results = f"""  
    <!DOCTYPE html>
<html>
<head>
    <style>
        body {{
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            background-color: #f1f1f1;
        }}

        .container {{
            text-align: center;
            padding: 20px;
            background-color: #fff;
            border-radius: 5px;
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
        }}

        h1 {{
            color: #333;
            font-size: 24px;
            margin-bottom: 10px;
        }}

        h3 {{
            color: #777;
            font-size: 18px;
            margin-top: 10px;
        }}

        p {{
            margin: 0;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>Results</h1>
        <h3>Age in Seconds</h3>
        <p>{age_in_seconds}</p>
        <h3>Age in Minutes</h3>
        <p>{age_in_minutes}</p>
        <h3>Age in Hours</h3>
        <p>{age_in_hours}</p>
        <h3>Age in Days</h3>
        <p>{age_in_days}</p>
        <h3>Age in Years</h3>
        <p>{age_in_years}</p>
    </div>
</body>
</html>

    """
        except ValueError:
            age_results = "Invalid Date Format!. The valid date format is YYYY-MM-DD."
    
   
    body  = f"""<html><body>{age_results}</body></html>"""
    body_length = len(body)
    headers = f"""HTTP/1.1 200 OK
Content-Type: text/html charset=UTF-8
content-length: {body_length}

"""
    response = headers + body
    client_socket.send(response.encode())
    print(response.encode())
    client_socket.close()



# Main loop to handle incoming connections
while True:
    # Accept incoming connections
    client_socket, client_address = server_socket.accept()

    # Create a new thread to handle the client connection
    client_thread_send = threading.Thread(
        target=handle_client_send, args=(client_socket, client_address))
    client_thread_send.start()
