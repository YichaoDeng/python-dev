class Empty:
    __slots__ = ['roots', 'attr', 'default']

    def __init__(self, root=None, attr="", default=None):
        self.root = root  # noqa
        self.attr = attr
        self.default = default

    def __getattr__(self, item):
        return self.__class__(self, item)

    def __setattr__(self, key, value):
        pass

    def __bool__(self):
        return False

    def __repr__(self):
        return f"<Empty: {self.attr or 'empty'}>"

    def __call__(self, *args, **kwargs):
        return self.default


empty = Empty()
