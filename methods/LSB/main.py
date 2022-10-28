import os
import sys
from tabnanny import check

sys.path.append(os.path.realpath("."))

import random

from utils import read_image, read_secret, convert_1d_2_2d
from methods.parent import Method


class LSB_Method(Method):

    def encrypt(self, carrier_path, secret_path, **args):
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
    
    def decrypt(self, length, img, result_path, **args) -> str:
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

        return self.back_process(result_path, bits)


class LSB_RandomInterval(Method):

    def encrypt(self, carrier_path, secret_path, **args):
        img, shape = read_image.read_img_by_cv2(carrier_path)
        info = read_secret.read_secret_bin(secret_path)
        random.seed(2)
        
        cnt = 0
        l = len(info)
        step_max = int(shape[0] * shape[1] / l)

        if args["interval_step"] > step_max:
            raise Exception("步长设置过大")
        
        random_seq = [0] * l
        for i in range(0, l):
            random_seq[i] = int(random.random() * args["interval_step"] + 1)
        
        q = 1
        for cnt in range(l):
            w, h = convert_1d_2_2d.convert(q, shape[0])
            pix = img[w, h]
            pix = pix - pix % 2 + int(info[cnt])
            q = q + random_seq[cnt]
            img[w, h] = pix
        
        return img

    def decrypt(self, length, img, result_path, **args) -> str:
        random.seed(2)
        shape = img.shape

        cnt = 0
        bits = ""

        random_seq = [0] * length
        for i in range(0, length):
            random_seq[i] = int(random.random() * args["interval_step"] + 1)
        
        q = 1
        for cnt in range(length):
            w, h = convert_1d_2_2d.convert(q, img.shape[0])
            pix = img[w, h]
            bits += str(pix % 2)
            q += random_seq[cnt]
        
        return self.back_process(result_path, bits)


class LSB_RegionalCheck(Method):

    def encrypt(self, carrier_path, secret_path, **args):
        img, shape = read_image.read_img_by_cv2(carrier_path)
        info = read_secret.read_secret_bin(secret_path)
        # random.seed(2)

        check_size = args["check_size"]

        cnt = 0
        l = len(info)

        q = 1
        size_max = int(shape[0] * shape[1] / l)
        if shape[0] * shape[1] < check_size * l:
            raise Exception("Check size设置过大")

        pixels = list()
        for p in range(1, l + 1):
            for i in range(1, check_size + 1):
                w, h = convert_1d_2_2d.convert((p - 1) * check_size + i, shape[0])
                pixels.append(img[w, h])
            
            temp = 0
            for i, v in enumerate(pixels):
                temp += v % 2
            pixels = list()
            temp %= 2

            if temp != int(info[p - 1]):
                q = int(random.random() * check_size) + 1
                w, h = convert_1d_2_2d.convert((p - 1) * check_size + q, shape[0])
                pix = img[w, h]
                img[w, h] = pix - 1
        
        return img
    
    def decrypt(self, length, img, result_path, **args) -> str:
        check_size = args["check_size"]
        random.seed(2)
        shape = img.shape

        cnt = 0
        bits = ""

        pixels = list()
        for p in range(1, length + 1):
            for i in range(1, check_size + 1):
                w, h = convert_1d_2_2d.convert((p - 1) * check_size + i, img.shape[0])
                pixels.append(img[w, h])
            
            temp = 0
            for i, v in enumerate(pixels):
                temp += v % 2
            pixels = list()
            temp %= 2
            bits += str(temp)

        return self.back_process(result_path, bits)