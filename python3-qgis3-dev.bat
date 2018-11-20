@echo off
call C:\OSGeo4W64\bin\o4w_env.bat
call C:\OSGeo4W64\bin\qt5_env.bat
call C:\OSGeo4W64\bin\py3_env.bat
@echo off
path C:\OSGeo4W64\apps\qgis\bin;%PATH%
set QGIS_PREFIX_PATH=%OSGEO4W_ROOT:\=/%/apps/qgis
set GDAL_FILENAME_IS_UTF8=YES
rem Set VSI cache to be used as buffer, see #6448
set VSI_CACHE=TRUE
set VSI_CACHE_SIZE=1000000
set QT_PLUGIN_PATH=C:\OSGeo4W64\apps\qgis\qtplugins;C:\OSGeo4W64\apps\qt5\plugins
set PYTHONPATH=C:\OSGeo4W64\apps\qgis\python;%PYTHONPATH%
start /d "C:\Program Files\JetBrains\PyCharm Community Edition 2018.2.2\bin\" pycharm64.exe
