import hashlib
import secrets


def hash_password(password):
    # Generate a random 16-byte salt
    salt = secrets.token_hex(16)

    # Combine password and salt, then create SHA-256 hash
    hashed_password = hashlib.sha256(
        (password + salt).encode()
    ).hexdigest()

    return {
        "salt": salt,
        "hash": hashed_password
    }


if __name__ == "__main__":
    password = input("Enter a password: ")

    result = hash_password(password)

    print("\nPassword hash created successfully!")
    print(f"Salt: {result['salt']}")
    print(f"Hash: {result['hash']}")