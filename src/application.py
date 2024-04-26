import argparse
import socket


def parse_arguments():
    parser = argparse.ArgumentParser(description='DRTP File Transfer Application')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-s', '--server', action='store_true', help='Run as the server')
    group.add_argument('-c', '--client', action='store_true', help='Run as the client')
    parser.add_argument('-i', '--ip', type=str, help='IP address of the server (for client) or binding (for server)',
                        required=True)
    parser.add_argument('-p', '--port', type=int, help='Port to use', required=True)
    parser.add_argument('-f', '--file', type=str,
                        help='File to send (for client) or location to save file (for server)', required=False)

    return parser.parse_args()


def run_server(ip, port, file_path='received_file'):
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
