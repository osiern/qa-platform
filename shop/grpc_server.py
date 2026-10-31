from concurrent import futures
import grpc
from sqlalchemy import select
from shop.db import Session, Product, User
from shop.security import session_user
from shop.proto import inventory_pb2 as messages
from shop.proto import inventory_pb2_grpc as services


class Inventory(services.InventoryServicer):
    def GetStock(self, request, context):
        auth = dict(context.invocation_metadata()).get('authorization', '')
        uid = session_user(auth[7:]) if auth.startswith('Bearer ') else None
        with Session() as db:
            if not uid or not db.get(User, uid):
                context.abort(grpc.StatusCode.UNAUTHENTICATED, 'Требуется вход')
            if request.product_id <= 0:
                context.abort(grpc.StatusCode.INVALID_ARGUMENT, 'product_id должен быть положительным')
            p = db.get(Product, request.product_id)
            if not p or not p.active:
                context.abort(grpc.StatusCode.NOT_FOUND, 'Товар не найден')
            return messages.StockReply(product_id=p.id, available=p.stock)


def main():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=8))
    services.add_InventoryServicer_to_server(Inventory(), server)
    server.add_insecure_port('0.0.0.0:50051')  # только изолированный учебный стенд
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    main()
