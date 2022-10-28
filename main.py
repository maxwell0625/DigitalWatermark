from cgitb import handler
from methods.LSB.main import LSB_Method, LSB_RandomInterval, LSB_RegionalCheck
from methods.parent import Handler


if __name__ == "__main__":
    carrier_path = "./carrier.jpg"
    secret_path = "./secret.py"
    result_path = "./encrypted.jpg"

    handler = Handler(carrier_path, secret_path, result_path)

    print("*" * 5 + "LSB算法" + "*" * 5)
    handler.method = LSB_Method
    psnr, ssim, hamming = handler.run()
    print(f"PSNR: {psnr} SSIM: {ssim} HAMMING: {hamming}")

    print("*" * 5 + "LSB 随机间隔 算法" + "*" * 5)
    psnr_max = 0
    ssim_max = 0
    hamming_min = 100
    for i in range(1, 15):
        try:
            handler.method = LSB_RandomInterval
            psnr, ssim, hamming = handler.run(interval_step=i)
            if psnr > psnr_max and ssim > ssim_max and hamming <= hamming_min:
                psnr_max = psnr
                ssim_max = ssim
                hamming_min = hamming
            # print(f"PSNR: {psnr} SSIM: {ssim} HAMMING: {hamming}")
        except:
            break
    print(f"PSNR: {psnr_max} SSIM: {ssim_max} HAMMING: {hamming_min}")

    print("*" * 5 + "LSB 区域校验位 算法" + "*" * 5)
    handler.method = LSB_RegionalCheck
    psnr_max = 0
    ssim_max = 0
    hamming_min = 100
    for i in range(1, 24):
        try:
            handler.method = LSB_RandomInterval
            psnr, ssim, hamming = handler.run(check_size=i)
            if psnr > psnr_max and ssim > ssim_max and hamming <= hamming_min:
                psnr_max = psnr
                ssim_max = ssim
                hamming_min = hamming
            # print(f"PSNR: {psnr} SSIM: {ssim} HAMMING: {hamming}")
        except:
            break
    print(f"PSNR: {psnr_max} SSIM: {ssim_max} HAMMING: {hamming_min}")
