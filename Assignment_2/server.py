import ssl, socket
import random
import hashlib


# ==== Client ====
# Coing Tossing / Die Rolling
roll = random.randint(1,6)
rnd_bits = ssl.RAND_bytes((256 - roll.bit_length()) // 8)

c = str(roll) + str(rnd_bits)
commitment = hashlib.sha256(c.encode()).digest()


# Start Client
def start_client():
    hostname = 'localhost'

    context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    context.verify_mode = ssl.CERT_REQUIRED
    context.load_verify_locations('./certs/ca_cert.pem')

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0) as sock:
        sock.connect((hostname, 8443))
        with context.wrap_socket(sock, server_hostname=hostname) as ssock:
            print(ssock.version())





# ==== Start Server ====
def start_server():
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain('./certs/ca_cert.pem', './certs/ca_key.key')

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0) as sock:
        sock.bind(('localhost', 8443))
        sock.listen(5)
        with context.wrap_socket(sock, server_side=True) as ssock:
            conn, addr = ssock.accept()


if __name__ == "__main__":
    try:
        start_server()
    except Exception as e:
        start_client()
