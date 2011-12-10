# -*- mode: python -*-
# coding: UTF-8
# ������ 2 ��������� ����� os.path.join(HOMEPATH,'support\\_mountzlib.py'), os.path.join(CONFIGDIR,'support\\useUnicode.py')
# 3 ���� �� ������� ��������, �� ����� ���� ���������
# 4 ��� ������ ��� ����� ��������� ��� ������ � exe
# 5 ����� �����
a = Analysis([os.path.join(HOMEPATH,'support\\_mountzlib.py'), 
			 os.path.join(CONFIGDIR,'support\\useUnicode.py'), 'D:\\Programming\\Project\\usecasevstu\\usecase_python\\usecase_python.py'],
             pathex=['C:\\Soft\\pyinstaller'],
             excludes = ['_ssl','bz2','win32ui'],
  )
# ��� ���� ����� ������� �� �����
def not_system(arr):
    name,path,type = arr
    return not path.startswith(r'C:\WINDOWS\system32') or name.lower().startswith('py')
a.binaries = filter(not_system,a.binaries)
# ��� ���� ����� ������� �� �����
def not_qt4_plugin(arr):
    name,path,type = arr
    return not name.startswith('qt4_plugins')
a.datas = filter(not_qt4_plugin,a.binaries)

# ��� ���� ����� ������� �� �����
pyz = PYZ(a.pure)
# ��� ������ ������ ���� ����� ����������� ������
# ���� �� ������
# � ���� ��� ������ ��������� 
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
# ��� ��� ����� ������ ����������� ���� ���������
coll = COLLECT( exe,
               [
			   ],
               name=r'D:\\Programming\\Project\\usecasevstu\\bin')
