"""Smoke checks for the local Docker Compose test environment."""
import allure
import pytest

pytestmark = [pytest.mark.docker, allure.feature('Docker Compose environment')]

LONG_RUNNING = ['postgres', 'redis', 'kafka', 'web', 'grpc', 'worker']
WITH_HEALTHCHECK = ['postgres', 'redis', 'kafka', 'web', 'grpc']
ONE_SHOT = ['kafka-storage-init', 'init', 'topic-init']


@allure.title('Долгоживущие сервисы запущены')
@pytest.mark.parametrize('service', LONG_RUNNING)
def test_service_is_running(compose, service):
    assert compose.services()[service]['State'] == 'running'


@allure.title('Healthcheck: сервис не просто запущен, а готов принимать запросы')
@pytest.mark.parametrize('service', WITH_HEALTHCHECK)
def test_service_is_healthy(compose, service):
    assert compose.services()[service]['Health'] == 'healthy'


@allure.title('Init-задачи отработали один раз и завершились с кодом 0')
@pytest.mark.parametrize('service', ONE_SHOT)
def test_one_shot_jobs_exited_successfully(compose, service):
    container = compose.services()[service]

    assert (container['State'], container['ExitCode']) == ('exited', 0)


@allure.title('Порты опубликованы только на 127.0.0.1')
@pytest.mark.parametrize(('service', 'container_port', 'host'), [
    ('web', '8000', '127.0.0.1:8010'),
    ('grpc', '50051', '127.0.0.1:50051'),
    ('postgres', '5432', '127.0.0.1:55432'),
])
def test_published_ports(compose, service, container_port, host):
    assert compose.run('port', service, container_port).strip() == host


@allure.title('depends_on: web стартует только после успешного init')
def test_web_waits_for_init(compose):
    depends = compose.config()['services']['web']['depends_on']

    assert depends['init']['condition'] == 'service_completed_successfully'


@allure.title('Одна сборка — несколько сервисов: web, grpc и worker из одного образа')
def test_one_image_many_commands(compose):
    services = compose.config()['services']

    assert services['web']['image'] == services['grpc']['image'] == services['worker']['image']
    assert services['worker']['command'] == ['python', '-m', 'shop.worker']


@allure.title('Volume: данные PostgreSQL переживают пересоздание контейнера')
def test_postgres_data_volume(compose):
    volumes = compose.config()['services']['postgres']['volumes']

    assert any(volume['target'] == '/var/lib/postgresql/data' and volume['type'] == 'volume' for volume in volumes)


@allure.title('exec: команда внутри контейнера — psql и redis-cli')
def test_exec_into_containers(compose):
    assert compose.exec('postgres', 'psql', '-U', 'qa', '-d', 'qa_shop', '-tAc', 'SELECT 1') == '1'
    assert compose.exec('redis', 'redis-cli', 'PING') == 'PONG'


@allure.title('Сеть compose: контейнеры обращаются друг к другу по имени сервиса')
def test_service_dns_inside_network(compose):
    code = "import socket; print(socket.gethostbyname('postgres'))"

    address = compose.exec('web', 'python', '-c', code)

    assert address.count('.') == 3


@allure.title('Логи: worker работает и не упал с ошибкой')
def test_worker_logs_have_no_traceback(compose):
    assert 'Traceback' not in compose.logs('worker', tail=300)
