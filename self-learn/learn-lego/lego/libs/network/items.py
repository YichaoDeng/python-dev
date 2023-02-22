from lego.utils import universal


class Dtype:
    __slots__ = ['data', 'index', 'name', 'dtype']

    def __init__(self, data, name=None, index=None, dtype=None, layout=None):
        if isinstance(data, Dtype):
            self.data = data.data
            self.index = data.index or index
            self.name = data.name or name
        else:
            self.index = index
            self.data = data
            self.name = name

        if dtype:
            self.data = dtype(self.data)

        self.dtype = type(data)
        self.data = universal.process_dict_objects(self.data, layout=layout)


class Item(dict):
    def __init__(self):
        super().__init__()
