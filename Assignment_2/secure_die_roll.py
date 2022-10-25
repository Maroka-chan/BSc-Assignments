import ssl, socket
import hashlib
import secrets

hostname = 'localhost'
roll_bit_count = 3
commitment_length = 256
rnd_bit_count = commitment_length - roll_bit_count

# ==== Start Client ==== (Bob)
def start_client():
    # Coing Tossing / Die Rolling
    roll = secrets.randbits(roll_bit_count)
    rnd_bits = ssl.RAND_bytes(rnd_bit_count // 8)
    c = bytes(roll) + rnd_bits
    commitment = hashlib.sha256(c).digest()

    print("This is Bob.")

    context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    context.verify_mode = ssl.CERT_REQUIRED
    context.load_verify_locations('./certs/ca_cert.pem')

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0) as sock:
        with context.wrap_socket(sock, server_hostname=hostname) as ssock:
            ssock.connect((hostname, 8443))
            ssock.send(commitment)
            print(f"[Sent] Commitment: {commitment}")
            
            aliceRoll = int.from_bytes(ssock.recv(roll_bit_count), 'little')
            print(f"[Received] Alice's roll: {aliceRoll}")

            ssock.send(roll.to_bytes(1, 'little'))
            print(f"[Sent] Roll: {roll}")
            ssock.send(rnd_bits)
            print(f"[Sent] Random bits: {rnd_bits}")

            print(f"Final roll: {((roll ^ aliceRoll)%6)+1}")



# ==== Start Server ==== (Alice)
def start_server():
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain('./certs/ca_cert.pem', './certs/ca_key.key')
    

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0) as sock:
        with context.wrap_socket(sock, server_side=True) as ssock:
            ssock.bind((hostname, 8443))
            ssock.listen(5)

            print("This is Alice.")

            conn, _ = ssock.accept()
            bobCommitment = conn.recv(commitment_length)
            print(f"[Received] Bobs's commitment: {bobCommitment}")
            
            roll = secrets.randbits(roll_bit_count)
            conn.send(roll.to_bytes(1, 'little'))
            print(f"[Sent] Roll: {roll}")

            bobRoll = int.from_bytes(conn.recv(roll_bit_count), 'little')
            print(f"[Received] Bobs's roll: {bobRoll}")
            bob_rnd_bits = conn.recv(rnd_bit_count)
            print(f"[Received] Bobs's random bits: {bob_rnd_bits}")
            
            c = bytes(bobRoll) + bob_rnd_bits
            commitment = hashlib.sha256(c).digest()
            print(f"Alice's hash using Bob's roll and random bits: {bobCommitment}")

            if bobCommitment != commitment:
                print("The hashes do not match. Bob Cheated! :(");
                exit(0)

            print("The hashes match :)")

            print(f"Final roll: {((roll ^ bobRoll)%6)+1}")


if __name__ == "__main__":
    try:
        start_server()
    except Exception as e:
        start_client()

