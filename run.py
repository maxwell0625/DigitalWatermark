import grpc
import time
from concurrent import futures
from server import server_pb2_grpc


ONE_DAY_IN_SECONDS = 60 * 60 * 24
HOST = "localhost"
PORT = "9999"


class DigitalWatermark(server_pb2_grpc.DigitalWatermarkServicer):
    
    def Encrypt(self, request, context):
        return super().Encrypt(request, context)

    def Decrypt(self, request, context):
        return super().Decrypt(request, context)

def run_server():
    grpcServer = grpc.server(futures.ThreadPoolExecutor(max_workers=4))
    server_pb2_grpc.add_DigitalWatermarkServicer_to_server(DigitalWatermark(), grpcServer)
    grpcServer.add_insecure_port(HOST + ":" + PORT)
    grpcServer.start()
    print("Start server successfully")
    try:
        while True:
            time.sleep(ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        grpcServer.stop(0)

if __name__ == "__main__":
    run_server()
