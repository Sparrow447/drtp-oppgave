import subprocess
import hashlib
import os
import time


def calculate_md5(filename, block_size=256 * 128):
    """Calculate the MD5 checksum of a file."""
    md5 = hashlib.md5()
    try:
        with open(filename, 'rb') as f:
            for block in iter(lambda: f.read(block_size), b''):
                md5.update(block)
    except FileNotFoundError:
        print(f"File not found: {filename}")
        return None
    return md5.hexdigest()


def run_test(server_cmd, client_cmd, file_to_send, received_file_path):
    """Run the server and client to test the file transfer and validate the file content."""
    # Start the server as a subprocess
    server_process = subprocess.Popen(server_cmd, shell=True)
    time.sleep(1)  # Give the server some time to start

    # Start the client as a subprocess
    client_process = subprocess.Popen(client_cmd, shell=True)
    client_process.wait()  # Wait for the client to finish the file transfer

    # Verify the file was received correctly
    original_checksum = calculate_md5(file_to_send)
    received_checksum = calculate_md5(received_file_path)
    test_passed = original_checksum == received_checksum

    # Output the test result
    if test_passed:
        print(f"Test passed: {file_to_send} was sent and received correctly.")
    else:
        print(f"Test failed: The received file did not match the sent file.")

    # Terminate the server process
    server_process.terminate()

    return test_passed


# Define the server and client commands
server_command = 'python application.py -s -i 127.0.0.1 -p 8080'
client_command = 'python application.py -c -f testfile.txt -i 127.0.0.1 -p 8080'

# Define the path to the test file and the expected received file path
test_file_path = 'testfile.txt'
received_file_path = 'received_file'

# Ensure the received file is cleared before running the test
if os.path.exists(received_file_path):
    os.remove(received_file_path)

# Run the test
if __name__ == '__main__':
    test_success = run_test(server_command, client_command, test_file_path, received_file_path)
    # Optionally, add more tests or assertions here
