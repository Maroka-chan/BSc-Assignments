import socket, ssl

hostname = 'localhost'

context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
context.verify_mode = ssl.CERT_REQUIRED
context.load_verify_locations('./certs/ca_cert.pem')

with socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0) as sock:
    sock.connect((hostname, 8443))
    with context.wrap_socket(sock, server_hostname=hostname) as ssock:
        print(ssock.version())
