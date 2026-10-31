"""Inventory gRPC contract, authorization and error behavior."""
import allure
import grpc
import pytest

pytestmark = [pytest.mark.grpc, allure.feature('gRPC inventory')]


@allure.title('OK: GetStock возвращает тот же остаток, что лежит в PostgreSQL')
def test_get_stock_matches_database(inventory, user, make_product, db):
    product = make_product(stock=7)

    reply = inventory.get_stock(product['id'], token=user.token)

    assert (reply.product_id, reply.available) == (product['id'], 7)
    assert reply.available == db.scalar('SELECT stock FROM products WHERE id=%s', (product['id'],))


@allure.title('gRPC видит списание остатка после заказа через HTTP')
def test_stock_decreases_after_order(inventory, user, make_product):
    product = make_product(stock=5)
    user.put_cart(product['id'], 2)
    user.create_order('Самара, Учебная улица, 10')

    assert inventory.get_stock(product['id'], token=user.token).available == 3


@allure.title('Ошибки: код статуса — часть контракта, как HTTP-код')
@pytest.mark.parametrize(
    ('product_id', 'with_token', 'code'),
    [
        pytest.param(1, False, grpc.StatusCode.UNAUTHENTICATED, id='без токена'),
        pytest.param(0, True, grpc.StatusCode.INVALID_ARGUMENT, id='id = 0'),
        pytest.param(-5, True, grpc.StatusCode.INVALID_ARGUMENT, id='отрицательный id'),
        pytest.param(999999999, True, grpc.StatusCode.NOT_FOUND, id='нет товара'),
    ],
)
def test_error_codes(inventory, user, product_id, with_token, code):
    with pytest.raises(grpc.RpcError) as error:
        inventory.get_stock(product_id, token=user.token if with_token else None)

    assert error.value.code() == code


@allure.title('Сообщение ошибки передаётся в details')
def test_error_details(inventory, user):
    with pytest.raises(grpc.RpcError) as error:
        inventory.get_stock(0, token=user.token)

    assert error.value.details() == 'product_id должен быть положительным'


@allure.title('Протухший токен: после logout gRPC тоже отказывает — сессия общая в Redis')
def test_logout_invalidates_grpc(inventory, user, product):
    token = user.token
    user.logout()

    with pytest.raises(grpc.RpcError) as error:
        inventory.get_stock(product['id'], token=token)

    assert error.value.code() == grpc.StatusCode.UNAUTHENTICATED


@allure.title('Deadline: клиент сам ограничивает время ожидания ответа')
def test_deadline_exceeded():
    # Микросекундный timeout на живом сервере нестабилен: прогретый канал иногда успевает.
    # Детерминированно: сервер не отвечает (порт закрыт), wait_for_ready ждёт до deadline.
    from shop.proto import inventory_pb2, inventory_pb2_grpc

    with grpc.insecure_channel('127.0.0.1:1') as channel:
        stub = inventory_pb2_grpc.InventoryStub(channel)
        with pytest.raises(grpc.RpcError) as error:
            stub.GetStock(inventory_pb2.StockRequest(product_id=1), timeout=0.5, wait_for_ready=True)

    assert error.value.code() == grpc.StatusCode.DEADLINE_EXCEEDED


@allure.title('Без wait_for_ready недоступный сервер — сразу UNAVAILABLE, а не ожидание')
def test_unavailable_without_wait():
    from shop.proto import inventory_pb2, inventory_pb2_grpc

    with grpc.insecure_channel('127.0.0.1:1') as channel:
        stub = inventory_pb2_grpc.InventoryStub(channel)
        with pytest.raises(grpc.RpcError) as error:
            stub.GetStock(inventory_pb2.StockRequest(product_id=1), timeout=5)

    assert error.value.code() == grpc.StatusCode.UNAVAILABLE


@allure.title('Protobuf: незаданное поле равно значению по умолчанию, а не None')
def test_protobuf_defaults():
    from shop.proto import inventory_pb2

    request = inventory_pb2.StockRequest()

    assert request.product_id == 0
    assert request.SerializeToString() == b''
    assert inventory_pb2.StockRequest.FromString(inventory_pb2.StockRequest(product_id=150).SerializeToString()).product_id == 150
