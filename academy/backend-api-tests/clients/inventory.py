import sys

import allure
import grpc

from clients.settings import ROOT

# Стабы сгенерированы из shop/proto/inventory.proto командой grpc_tools.protoc.
sys.path.insert(0, str(ROOT))
from shop.proto import inventory_pb2, inventory_pb2_grpc  # noqa: E402


class InventoryClient:
    """gRPC-клиент сервиса Inventory. Токен передаётся в metadata, как HTTP-заголовок."""

    def __init__(self, target: str):
        self.channel = grpc.insecure_channel(target)
        self.stub = inventory_pb2_grpc.InventoryStub(self.channel)

    def close(self) -> None:
        self.channel.close()

    def get_stock(self, product_id: int, token: str | None = None, timeout: float = 5):
        metadata = [('authorization', f'Bearer {token}')] if token else []
        with allure.step(f'gRPC Inventory.GetStock(product_id={product_id})'):
            return self.stub.GetStock(inventory_pb2.StockRequest(product_id=product_id),
                                      metadata=metadata, timeout=timeout)
