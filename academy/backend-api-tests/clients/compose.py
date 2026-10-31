import json
import subprocess

import allure

from clients.settings import ROOT


class Compose:
    """docker compose учебного стенда через scripts/dc.sh: тот же профиль, что при ручном запуске."""

    def run(self, *args: str, timeout: float = 60) -> str:
        with allure.step('docker compose ' + ' '.join(args)):
            result = subprocess.run(['sh', 'scripts/dc.sh', *args], cwd=ROOT, capture_output=True,
                                    text=True, timeout=timeout)
            allure.attach(result.stdout[-5000:] + result.stderr[-2000:], name='output',
                          attachment_type=allure.attachment_type.TEXT)
        assert result.returncode == 0, result.stderr
        return result.stdout

    def services(self) -> dict[str, dict]:
        """Контейнеры по имени сервиса, включая завершившиеся init-задачи."""
        lines = self.run('ps', '--all', '--format', 'json').splitlines()
        return {row['Service']: row for row in map(json.loads, filter(None, lines))}

    def config(self) -> dict:
        return json.loads(self.run('config', '--format', 'json'))

    def exec(self, service: str, *command: str) -> str:
        return self.run('exec', '-T', service, *command).strip()

    def logs(self, service: str, tail: int = 200) -> str:
        return self.run('logs', '--no-color', '--tail', str(tail), service)
