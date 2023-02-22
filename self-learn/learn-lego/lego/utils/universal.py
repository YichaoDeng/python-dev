import ast
import functools
import getpass
import importlib
import inspect
import os
import re

from typing import Union

import ujson


def host(public, private, condition=('ubuntu', 'root')):
    """
    根据条件自动选择私有 ip 或 公有 ip
    :param public:
    :param private:
    :param condition:
    :return:
    """
    if not callable(condition):
        res = getpass.getuser() in condition
    else:
        res = condition()

    return private if res else public


def process_dict_objects(obj: dict, layout=None, excludes=(), mapping: dict = None, fields: Union[list, dict] = None):
    """
    加工字典对象
    :param obj:
    :param layout:
    :param excludes:
    :param mapping:
    :param fields:
    :return:
    """

    def fmt_factory(_factory):
        @functools.wraps(_factory)
        def inner(_item):
            if not _factory:
                return _item
            try:
                return result(
                    func=_factory,
                    args=[_item],
                    kwargs={
                        **obj,
                        "__item__": obj
                    },
                    strict=True
                )
            except Exception:  # noqa
                if not _item:
                    return None
                else:
                    return _item

        return inner


def result(
        func,
        args: Union[list, tuple] = None,
        kwargs: dict = None,
        strict: bool = True,
        debug: bool = True,
        to_generater: bool = False,
        to_gen_kwargs: dict = None
):
    """
    运行一个函数并获取结构，可以自动修复参数错误，移除无效参数，补充缺失参数
    :param func: 需要调用的函数引用或相对位置
    :param args: 函数的位置参数
    :param kwargs: 函数的关键字参数
                - _fix_return: 是否自动修正返回值
                - _strict: 是否抛出异常
    :param strict:
    :param debug:
    :param to_generater:
    :param to_gen_kwargs:
    :return:
    """
    if not func:
        return func
    args = (args and [*args]) or []
    kwargs = (kwargs and {**kwargs}) or {}
    try:
        func = load_object(func)
    except Exception as e:
        if isinstance(func, str) and not args and not kwargs:
            return func
        else:
            raise e
    _result = None


def json_or_eval(text, jsonp=False, errors="strict", _step=0, **kwargs) -> Union[dict, list, str]:
    def literal_eval():
        return ast.literal_eval(text)

    def json_decode():
        return ujson.loads(text)

    def use_jsonp():
        real_text = re.search('\S+?\((?P<obj>[\s\S]*)\)', text).group('obj')  # noqa
        return json_or_eval(real_text, jsonp=True, _step=_step + 1, **kwargs)

    if not isinstance(text, str):
        return text

    funcs = [json_decode, literal_eval]
    jsonp and _step == 0 and funcs.append(use_jsonp)
    for func in funcs:
        try:
            return func()
        except:
            pass
    else:
        if errors != 'ignore':
            raise ValueError(f'illegal json string: `{text}`')
        else:
            return text


def string2argv(_string: str):
    if not isinstance(_string, str): return _string  # noqa

    options = {}
    if not _string: return options  # noqa

    try:
        options = json_or_eval(_string)
        assert isinstance(options, dict)
        return options
    except:  # noqa
        _string = parse.unquote(_string)
        return {
            j[0].strip(): guess(j[1].strip()) for i in _string.strip().split("&") if i for j in [i.split("=", 1)] if
            "=" in i
        }


def load_object(path, reload=False, frompath=False, strict=True, __env__=None):
    """
    加载给定绝对路径的对象，并返回它
    对象可以是类、函数、变量或实例的导入路径，
    例如 'lego.core.downloader.AioHttpDownloader'
    如果 'path' 不是字符串，而是可调用对象，
    例如类或函数，则按原样返回
    :param path: 模块的路径
    :param reload: 是否重载模块
    :param frompath: 从绝对路径中加载
    :param strict:
    :param __env__:
    :return:
    """

    __env__ = __env__ or {**globals(), **locals()}

    def _load(o):
        try:
            return eval(o, __env__)
        except:  # noqa
            try:
                _ret = importlib.import_module(o)
                reload and inspect.ismodule(_ret) and importlib.reload(_ret)
                return _ret

            except Exception as e:
                if strict:
                    raise ValueError(f"加载对象失败：{raw}")
                else:
                    return e

    if not isinstance(path, str):
        return path

    if frompath:
        base_dir = os.getcwd()
        if path.__contains__(base_dir):
            sons = path.replace(base_dir, "").split(".")[0].replace("/", ".")
        else:
            i = 0
            for i, s in enumerate(path):
                try:
                    assert base_dir[i] == s
                except AssertionError:
                    sons = path[i:].split(".")[0].replace("/", ".")
                    break
            else:
                sons = os.path.basename(path.split(".")[0])

        spec2 = importlib.util.spec_from_file_location(sons, path)  # noqa
        odm = importlib.util.module_from_spec(spec2)  # noqa
        spec2.loader.exec_module(odm)
        return odm
    else:
        if not re.search(r'[a-zA-Z.]+', path):
            return path

        raw = path
        # 获取调用参数
        if path.__contains__('?'):
            path, para = path.split('?', 1)
            args, kwargs = [], string2argv(para)
