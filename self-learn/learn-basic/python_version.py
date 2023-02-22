import sys
import os


def main():
    """
    检查运行的环境
    """
    r"""
    当前 Python 解释器路径：
    /opt/homebrew/Caskroom/miniconda/base/envs/Lego/bin/python
    """
    print('当前 Python 解释器路径：')
    print(sys.executable)
    print()

    r"""
    当前 Python 解释器目录：
    /opt/homebrew/Caskroom/miniconda/base/envs/Lego/bin
    """
    print('当前 Python 解释器目录：')
    print(os.path.dirname(sys.executable))


if __name__ == '__main__':
    main()
