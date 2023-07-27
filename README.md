# Excel文件合并程序

## 文件结构

- 打包
	- `pyinstaller.exe -F -w app.py --add-data "script;script" --add-data "template;template"`
- excel_util
    - app.py
    - config.yaml
    - script
    - template


## BUG记录

- System.TypeLoadException: 未能从程序集"mscorlib, Version=4.0.0.0, Culture=neutral PublicKeyToken=xxxxxxxxxxx"中加载类型"System.ValueTuple`3"
	- 解决方法： 下载`.NET4.7.2`必须是4.7.2


- cannot call null pointer pointer from cdata 'int(*)(void*, int)'
	- 解决方法：在报错的电脑上重装pythonnet
	- `python -m pip uninstall pythonnet`
	- `python -m pip install pythonnet`

- pyinstaller打包时报错unable to create process
	- 解决方法：重装pyinstaller
	- `python -m pip install --force-reinstall pyinstaller`

- 运行app.exe报错Invalid file descriptor to ICU data received
	- 使用cefpython3(chrome，cef)报错
	- pyinstaller打包时没有将cefpython3的库完整的打包
	- 解决方法：https://github.com/pangao1990/PPX/issues/5
	- 打包时不用-F，将site-packages中的cefpython3全部粘贴到打包后的cefpython3中


## 核心代码

`webview.start(gui='cef')` 另外安装cefpython3：为了让win7使用chrome而不是ie