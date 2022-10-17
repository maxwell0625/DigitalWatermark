from cgitb import handler
from methods.LSB.main import LSB_Method
from methods.parent import Handler


if __name__ == "__main__":
    carrier_path = "./carrier.jpg"
    secret_path = "./secret.py"
    result_path = "./encrypted.jpg"

    handler = Handler(carrier_path, secret_path, result_path)

    print("*" * 5 + "LSB算法" + "*" * 5)
    handler.method = LSB_Method
    handler.run()
