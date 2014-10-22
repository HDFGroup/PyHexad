@ECHO OFF

cd unit

python h5getInfoTest.py
python h5showTreeTest.py
python h5showListTest.py

del /f/q *~ *.h5 *.pyc 

cd ..
echo "Done!"
 





