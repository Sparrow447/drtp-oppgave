import argparse
import logging
import socket

# Configure logging to write to drtp.log, set the logging level to INFO, and specify the log format.
logging.basicConfig(filename='drtp.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Set the buffer size for UDP packets
BUFFER_SIZE = 1024


def parse_arguments():
    """
    Parse command-line arguments to configure the DRTP file transfer application.

    The function supports arguments for running in server or client mode, the IP address for
    binding or connection, the port number to use, and optionally, the file to send or receive.

    Returns:
        Namespace: An object containing the parsed command-line arguments.
    """
    # Argument parser setup
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
    Runs the server which listens for incoming UDP packets and writes them to a file.
    It provides feedback via logging and handles shutdowns and socket errors gracefully.
    """
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        server_socket.bind((ip, port))
        logging.info(f"Server listening on {ip}:{port}")

        with open(file_path, 'wb') as file_to_write:
            while True:
                try:
                    chunk, client_address = server_socket.recvfrom(BUFFER_SIZE)
                    logging.info(f"Received data from {client_address}")
                    file_to_write.write(chunk)
                    file_to_write.flush()
                    server_socket.sendto(b'ACK', client_address)
                except socket.error as e:
                    logging.error(f"Socket error: {e}")
                    break  # Exit the loop on socket error
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
    finally:
        server_socket.close()
        logging.info("Server socket closed.")


def run_client(server_ip, server_port, file_path):
    """
    Sends a file to the server using UDP packets.
    It waits for an acknowledgment from the server before sending the next packet.
    """
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    try:
        with open(file_path, 'rb') as file_to_send:
            chunk = file_to_send.read(BUFFER_SIZE)
            while chunk:
                try:
                    client_socket.sendto(chunk, (server_ip, server_port))
                    ack, _ = client_socket.recvfrom(BUFFER_SIZE)
                    logging.info(f"Acknowledgment received from server: {ack.decode()}")
                    chunk = file_to_send.read(BUFFER_SIZE)
                except socket.timeout:
                    logging.warning("No acknowledgment received, resending last packet.")
                    continue  # Resend the last packet
    except FileNotFoundError:
        logging.error(f"The file {file_path} does not exist.")
    except Exception as e:
        logging.error(f"An error occurred: {e}")
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
        logging.info("Running as server...")
        print("Running as server...")
        run_server(args.ip, args.port, args.file if args.file else 'received_file')
    elif args.client:
        logging.info("Running as client...")
        print("Running as client...")
        if not args.file:
            logging.error("Error: Please provide a file to send using the -f option.")
            print("Error: Please provide a file to send using the -f option.")
            return
        run_client(args.ip, args.port, args.file)


if __name__ == '__main__':
    main()
