def read_secret_bin(path):
    with open(path, "rb") as f:
        binaries = f.read()

    bits = list()

    for bit in binaries:
        b = bin(bit)
        b = b.replace("0b", "")
        b = b.zfill(8)
        bits.append(b)

    return "".join(
        [
            bin(bit).replace("0b", "").zfill(8) for bit in binaries
        ]
    )

if __name__ == "__main__":
    path = "./secret.py"
    print(read_secret_bin(path))
