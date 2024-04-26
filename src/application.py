import argparse
import socket


def parse_arguments():
    """
    Parse command-line arguments to configure the DRTP file transfer application.

    The function supports arguments for running in server or client mode, the IP address for
    binding or connection, the port number to use, and optionally, the file to send or receive.

    Returns:
        Namespace: An object containing the parsed command-line arguments.
    """
    parser = argparse.ArgumentParser(description='DRTP File Transfer Application')
    group = parser.add_mutually_exclusive_group(required=True)

    # Server mode argument
    group.add_argument('-s', '--server', action='store_true', help='Run as the server')

    # Client mode argument
    group.add_argument('-c', '--client', action='store_true', help='Run as the client')

    # IP address argument
    parser.add_argument('-i', '--ip', type=str, required=True,
                        help='IP address of the server (for client) or binding (for server)')

    # Port number argument
    parser.add_argument('-p', '--port', type=int, required=True, help='Port to use')

    # File path argument
    parser.add_argument('-f', '--file', type=str,
                        help='File to send (for client) or location to save file (for server)', required=False)

    return parser.parse_args()


def run_server(ip, port, file_path='received_file'):
    """
    Start a DRTP server that listens for incoming data and writes it to a file.

    Args:
        ip (str): IP address to bind the server to.
        port (int): Port number for the server to listen on.
        file_path (str): The path where the received file will be saved. Defaults to 'received_file'.

    The server listens indefinitely until a KeyboardInterrupt is issued. Each received chunk of data
    is written to the file and an acknowledgment is sent back to the client.
    """
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind((ip, port))
    print(f"Server listening on {ip}:{port}")

    with open(file_path, 'wb') as file_to_write:
        try:
            while True:
                chunk, client_address = server_socket.recvfrom(1024)
                print(f"Received data from {client_address}")
                file_to_write.write(chunk)
                file_to_write.flush()
                server_socket.sendto(b'ACK', client_address)
        except KeyboardInterrupt:
            print("Server is shutting down.")
        finally:
            server_socket.close()


def run_client(server_ip, server_port, file_path):
    """
    Start a DRTP client to send a file to a server over UDP.

    Args:
        server_ip (str): IP address of the server to send data to.
        server_port (int): Port number of the server to connect to.
        file_path (str): Path of the file to send.

    The client reads the file in chunks and sends each chunk to the server, waiting for an
    acknowledgment before sending the next chunk. If the file does not exist or an error occurs,
    an appropriate message is printed.
    """
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    try:
        with open(file_path, 'rb') as file_to_send:
            chunk = file_to_send.read(1024)
            while chunk:
                client_socket.sendto(chunk, (server_ip, server_port))
                ack, _ = client_socket.recvfrom(1024)
                print(f"Acknowledgment received from server: {ack.decode()}")
                chunk = file_to_send.read(1024)
    except FileNotFoundError:
        print(f"The file {file_path} does not exist.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        client_socket.close()


def main():
    """
    The main function of the DRTP File Transfer Application.

    Based on the parsed command-line arguments, the function determines whether to
    run the application in server or client mode and proceeds with the respective function calls.
    """
    args = parse_arguments()

    if args.server:
        print("Running as server...")
        run_server(args.ip, args.port, args.file if args.file else 'received_file')
    elif args.client:
        print("Running as client...")
        if not args.file:
            print("Error: Please provide a file to send using the -f option.")
            return
        run_client(args.ip, args.port, args.file)


if __name__ == '__main__':
    main()
