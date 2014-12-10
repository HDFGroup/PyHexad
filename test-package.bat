set HOME=C:\home
cd C:\Users\Gerd\git\PyHexad
C:\Python27\python.exe setup.py bdist_egg upload -r https://testpypi.python.org/pypi --identity="Gerd Heber" --sign --quiet 
C:\Python27\python.exe setup.py bdist_wininst --target-version=2.7 register upload -r https://testpypi.python.org/pypi --identity="Gerd Heber" --sign --quiet
C:\Python27\python.exe setup.py sdist upload -r https://testpypi.python.org/pypi --identity="Gerd Heber" --sign
pause
