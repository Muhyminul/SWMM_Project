from cx_Freeze import setup, Executable

setup(

   name="ArcGIS_TO_SWMM_Convertor",

   version="1.0",

   description="These tool will convert the gis shape file to SWMM input file",

   executables=[Executable("QGIS.py")],

)