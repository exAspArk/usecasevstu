# -*- mode: python -*-
# coding: UTF-8
# первые 2 параметра магия os.path.join(HOMEPATH,'support\\_mountzlib.py'), os.path.join(CONFIGDIR,'support\\useUnicode.py')
# 3 путь до скрипта главного, их может быть несколько
# 4 это просто где лежит программа для сборки в exe
# 5 снова магия
a = Analysis([os.path.join(HOMEPATH,'support\\_mountzlib.py'), 
			 os.path.join(CONFIGDIR,'support\\useUnicode.py'), 'D:\\Programming\\Project\\usecasevstu\\usecase_python\\usecase_python.py'],
             pathex=['C:\\Soft\\pyinstaller'],
             excludes = ['_ssl','bz2','win32ui'],
  )
# это тоже магия трогать не нужно
def not_system(arr):
    name,path,type = arr
    return not path.startswith(r'C:\WINDOWS\system32') or name.lower().startswith('py')
a.binaries = filter(not_system,a.binaries)
# это тоже магия трогать не нужно
def not_qt4_plugin(arr):
    name,path,type = arr
    return not name.startswith('qt4_plugins')
a.datas = filter(not_qt4_plugin,a.binaries)

# это тоже магия трогать не нужно
pyz = PYZ(a.pure)
# тут правим просто куда будет скидываться сборка
# путь до иконки
# и файл для версии программа 
exe = EXE(pyz,
          a.scripts,
		  a.binaries,
          a.zipfiles,
          a.datas,
          exclude_binaries=1,
          name=os.path.join('D:\\Programming\\Project\\usecasevstu\\build', 'UseCase.exe'),
          debug=False,
          strip=False,
          upx=False,
          console=False,
		  icon=r'D:\\Programming\\Project\\usecasevstu\\usecase_python\\images\\icon.ico',
          version=r'D:\\Programming\\Project\\usecasevstu\\version_info.py',		  
		  )
# тут где будет лежать запускающий файл программы
coll = COLLECT( exe,
               [
			   ],
               name=r'D:\\Programming\\Project\\usecasevstu\\bin')
