import os
import re
import warnings

import psutil

warnings.filterwarnings("ignore")

IP_REGEX = re.compile(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}')


def get_host_ip(prefix='', refresh=False, index=0):
    """
    获取本机 IP
    :param prefix:
    :param refresh:
    :param index:
    :return:
    """
    try:
        cache_key = f'HOST_IP_WITH_{prefix or "any"}_FOR_{index}'
        if not os.environ.get(cache_key) or refresh:
            ips = []
            for adapter, snics in psutil.net_if_addrs().items():
                for snic in snics:
                    if not snic.family.name.startswith('AF_INET'):
                        continue
                    ip = snic.address.strip()

                    if prefix and ip.startswith(prefix):
                        ips.append(ip)
                    elif ip != '127.0.0.1' and IP_REGEX.match(ip):
                        ips.append(ip)
            else:
                os.environ[cache_key] = ips[index]

        return os.environ[cache_key].strip()
    except:  # noqa
        return ""


print(get_host_ip(prefix='127.0'))
