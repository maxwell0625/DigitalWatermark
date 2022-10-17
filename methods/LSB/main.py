import os
import sys

sys.path.append(os.path.realpath("."))

from utils import read_image, read_secret
from methods.parent import Method


class LSB_Method(Method):

    def encrypt(carrier_path, secret_path):
        img, shape = read_image.read_img_by_cv2(carrier_path)
        info = read_secret.read_secret_bin(secret_path)
        
        cnt = 0
        l = len(info)

        for h in range(0, shape[1]):
            for w in range(0, shape[0]):
                pix = img[w, h]

                if cnt >= l:
                    break

                pix = pix - pix % 2 + int(info[cnt])
                cnt += 1

                img[w, h] = pix
        
        return img
    
    def decrypt(length, img, result_path) -> str:
        shape = img.shape

        cnt = 0
        bits = ""
        for h in range(0, shape[1]):
            for w in range(0, shape[0]):

                pix = img[w, h]

                bits += str(pix % 2)
                cnt += 1

                if cnt == length:
                    break
            
            if cnt == length:
                break

        with open(result_path, "wb") as f:
            for i in range(0, len(bits), 8):
                ascii_code = int(bits[i:i+8], 2)
                ascii_code = chr(ascii_code)

                b = bytes(ascii_code, encoding="utf-8")
                f.write(b)

        return bits
