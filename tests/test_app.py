from app import hash_password


def test_hash_password_returns_salt_and_hash():
    result = hash_password("mypassword")

    assert "salt" in result
    assert "hash" in result


def test_hash_is_sha256_length():
    result = hash_password("mypassword")

    # SHA-256 hexadecimal hash is 64 characters
    assert len(result["hash"]) == 64


def test_same_password_creates_different_hashes():
    result1 = hash_password("mypassword")
    result2 = hash_password("mypassword")

    # Random salt should make hashes different
    assert result1["hash"] != result2["hash"]


def test_salts_are_different():
    result1 = hash_password("mypassword")
    result2 = hash_password("mypassword")

    assert result1["salt"] != result2["salt"]