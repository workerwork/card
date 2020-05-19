# card

## 安装环境

### 安装python3.6

在 https://www.python.org/downloads/release/python-368/ 选择对应的版本下载安装

### 安装pyscard

执行　python -m pip install pyscard

### 安装pyqt5

1) 在cmd命令中输入 python -m pip install --upgrade pip 来升级pip
2) 在cmd命令中输入 pip install pyqt5 -i https://pypi.douban.com/simple 安装pyqt5
3) 在cmd命令中输入 pip install pyqt5-tools -i https://pypi.douban.com/simple 安装pyqt5-tools

### 在python的pyqt5包安装路径找到designer打开

如果遇到msvcp140.dll找不到的错误:

检查是否安装：Microsoft Visual C++ 2015 Redistributable(x64)

检查是否安装：Microsoft Visual C++ 2015 Redistributable(x86)

官方下载链接：https://www.microsoft.com/zh-cn/download/details.aspx?id=48145

## 使用IDE编辑code

## 打包exe文件

### 安装pyinstaller

执行 python -m pip install pyinstaller

### 打包

执行 pyinstaller.exe -F KSUsimCard.py 生成KSUsimCard.exe

执行 pyinstaller.exe -F YTUsimCard.py 生成YTUsimCard.exe
