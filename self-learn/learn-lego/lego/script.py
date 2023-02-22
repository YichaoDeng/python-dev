import os
import sys
import inspect
import secrets

from lego.libs.network import Request

from lego.utils.ip import get_host_ip
from lego.utils.universal import host


class Scripter:

    @staticmethod
    def _to_file(text, path, mode='w'):
        with open(path, mode, encoding='utf-8') as f:
            f.write(text)

    @classmethod
    def start_project(cls, base_dir=None):
        """开始项目: args: 项目名称[可选]"""
        base_dir = base_dir or input("项目名称: ")
        base_dir = base_dir or os.path.dirname(inspect.stack()[1].filename)

        not os.path.exists(base_dir) and os.makedirs(base_dir)

        with open(os.path.join(os.path.dirname(__file__), 'templates', 'setting.tmp'), encoding='utf-8') as t:
            setting_tpl_text = t.read().format(SECRECT_KEY=secrets.token_hex(32))

        with open(os.path.join(os.path.dirname(__file__), 'templates', 'main.tmp'), encoding='utf-8') as t:
            main_tpl_text = t.read()

        os.makedirs(os.path.join(base_dir, 'apps'), exist_ok=True)
        os.makedirs(os.path.join(base_dir, 'files'), exist_ok=True)

        cls._to_file(
            text='"""APP相关的文件统一存放地址',
            path=os.path.join(base_dir, 'apps', '__init__.py')
        )
        cls._to_file(
            text=setting_tpl_text,
            path=os.path.join(base_dir, 'settings.py')
        )
        cls._to_file(
            text=main_tpl_text,
            path=os.path.join(base_dir, 'frameless_app.py')
        )

    @classmethod
    def update(cls, package_name: str):
        """更新框架"""
        host_ip = host(public="1.14.197.109", private="10.0.0.184",
                       condtion=lambda: str(get_host_ip()).startswith("10.0"))
        cmd = f'pip install --upgrade {package_name} -i http://{host_ip}:8081/repository/pypi-group/simple --upgrade --trusted-host {host_ip}'
        os.system(cmd)

    @classmethod
    def fetch(cls, url):
        """进入 URL， 进入调试 SHELL 界面"""
        try:
            import IPython  # noqa
        except ImportError:
            raise ImportError("该功能依赖 ipython, 尝试使用 pip install ipython 后体验完整特性 ")

        request = Request(url=url)
        response = request.to_response()
