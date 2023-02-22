from typing import Optional, Mapping, Any, Union, Callable, Dict

import requests
import ujson

from lego.libs import empty


class Header(dict):

    def __init__(
            self,
            data=None,
            _dtype: Callable = None,
            _ktype: Callable = None,
            **kwargs
    ):
        self.dtype = _dtype or (lambda x: x)
        self.ktype = _ktype or str
        self.comps = [
            lambda x: str(x).lower(),
            lambda x: str(x).upper(),
            lambda x: str(x).title(),
        ]
        if data is None:
            data = {}
        super().__init__({**data, **kwargs})

    def __setitem__(self, key, value):
        key: str = self.ktype(key)
        keys = self.keys()

        for comp in self.comps:
            nkey = comp(key)
            if nkey in keys:
                return super().__getitem__(nkey)
        else:
            return super().__getitem__(key)

    def __delitem__(self, key):
        key: str = self.ktype(key)
        keys = self.keys()

        for comp in self.comps:
            nkey = comp(keys)
            if nkey in keys:
                return super().__delitem__(nkey)
        else:
            return super().__delitem__(key)

    def __eq__(self, other):
        if isinstance(other, (Mapping, dict)):
            other = self.__class__(other, dtype=self.dtype, ktype=self.ktype)
        else:
            return NotImplemented
        # Compare insensitively
        return self.items() == other.items()

    def __contains__(self, __o: object) -> bool:
        key: str = self.ktype(__o)
        keys = self.keys()

        for comp in self.comps:
            nkey = comp(key)
            if nkey in keys:
                return True
        else:
            return False

    def setdefault(self, __key, __default):  # noqa
        key: str = self.ktype(__key)
        keys = self.keys()

        for comp in self.comps:
            nkey = comp(key)
            if nkey in keys:
                return super().setdefault(nkey, self.dtype(__default))
        else:
            return super().setdefault(key, self.dtype(__default))


class Request:

    def __init__(
            self,
            url: str = None,
            method: str = "get",
            params: Optional[Mapping[str, str]] = None,
            data: Any = None,
            json: Any = None,
            headers: Union[Mapping[str, str]] = None,
            cookies: Union[Mapping[str, str]] = None,
            files=None,
            auth=None,
            timeout: int = ...,
            allow_redicrects: bool = True,
            auto_referer: bool = True,
            proxies: Optional[Mapping[str, str]] = None,
            stream: Union[bool] = None,
            verify: Union[bool] = False,
            cert=None,
            callback: Callable = empty,
            spider=empty,
            httpversion=None,
            sslversion=None,
            extra: dict = None,
            **kwargs
    ):
        self.url = url
        self.method = method.upper()
        self.params = params or {}
        self.data = data
        self.json = json
        self.__headers = Header(headers, _dtype=str)
        self.cookies = cookies
        self.files = files
        self.auth = auth
        self.timeout = timeout
        self.allow_redirects = allow_redicrects
        self.auto_referer = auto_referer
        self.proxies: Dict[str, str] = proxies
        self.stream = stream
        self.verify = verify
        self.cert = cert
        self.retry = 0
        self.httpversion = httpversion
        self.sslversion = sslversion
        self.max_retry = 5
        self.res_min_size = None
        self.pass_code = kwargs.pop("pass_code", ...)
        self.spider = spider
        self.callback: Callable = callback
        self._seeds = Item()
        self.storage = True
        self.extra = extra or {}

        for k, v in kwargs.items():
            setattr(self, k, v)

    headers: Header = property(
        fget=lambda self: self._headers,
        fset=lambda self, v: setattr(self, "_headers", Header(v, _dtype=str)),
        fdel=lambda self: setattr(self, "_headers", Header({}, _dtype=str)),
        doc="请求头"
    )

    @property
    def seeds(self) -> Item:
        return self._seeds

    @seeds.setter
    def seeds(self, v):
        self._seeds = Item(v)

    @seeds.deleter
    def seeds(self):
        self._seeds = Item()

    @property
    def request(self):
        """
        获取 PreparedRequest 对象
        :return:
        """
        p = requests.PreparedRequest()
        p.prepare(
            method=self.method.upper(),
            url=self.url,
            headers=self.headers,
            files=self.files,
            data=self.data or {},
            json=self.json,
            params=self.params or {},
            auth=self.auth,
            cookies=self.cookies
        )
        return p

    @property
    def curl(self):
        """
        request object to curl cmd
        :return:
        """
        req = self.request
        args = [
            'curl',
            '-X %s' % req.method
        ]
        for k, v in sorted(req.headers.items()):
            args.append('-H ' + ujson.dumps('{}: {}'.format(k, v), escape_forward_slashes=False))

        if req.body:
            body = req.body.decode() if isinstance(req.body, bytes) else req.body
            args.append('-d ' + ujson.dumps(body, escape_forward_slashes=False))

        args.append(ujson.dumps(req.url, escape_forward_slashes=False))

        return ' '.join(args)