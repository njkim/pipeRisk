# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# Pipe_Risk.py
# Created on: 2017-05-25 09:32:36.00000
#   (generated by ArcGIS/ModelBuilder)
# Usage: Pipe_Risk <WT_Pipe_main_surf> 
# Description: 
# ---------------------------------------------------------------------------

# Import arcpy module
import arcpy

# Script arguments
WT_Pipe_main_surf = arcpy.GetParameterAsText(0)
if WT_Pipe_main_surf == '#' or not WT_Pipe_main_surf:
    WT_Pipe_main_surf = "\\\\watis\\public\\InternsSpring2017\\Spring2017_WT_GeoDb.mdb\\Spring2017_WT\\WT_Pipe_main_surf" # provide a default value if unspecified

# Local variables:
WT_Pipe_main_surf_test = WT_Pipe_main_surf

# Process: Calculate Field
arcpy.CalculateField_management(WT_Pipe_main_surf, "Risk_Pipe", "likelihood( !DIAMETER! , !MATERIAL! , !INSTALLATI! , !Z_Max! )", "PYTHON", "def likelihood(a,b,c,d):\\n# a = diamter, b = material, c = age, d = elevation\\n\\n    if a == None or b == None or c == None or a == 0 or b == \"\" or c == \"\" or b == \"UNK\":\\n       return None\\n    else:\\n        e = 0\\n\\n# diamter\\n    if a <= 10:\\n        e = e + 5\\n    elif a > 10 and a <=20:\\n        e = e + 4\\n    else:\\n        e = e + 3\\n\\n# material\\n    if b[0:1] == \"S\" or b==\"CIP\":\\n        e = e + 5\\n    elif b[0:2] == \"DI\":\\n        e = e + 4\\n    elif b == \"ACP\" or b == \"CIP\":\\n        e = e + 3\\n    elif b == \"RCP\":\\n        e = e + 2\\n    else:\\n        e = e + 1\\n\\n# age\\n    if c[0:3] == \"195\" or c[0:3] == \"196\":\\n        e = e + 4\\n    elif c[0:3] == \"197\" or c[0:3] == \"198\":\\n        e = e + 3\\n    elif c[0:3] == \"199\" or c[0:3] == \"200\":\\n        e = e + 2\\n    else:\\n        e = e + 1\\n\\n# elevation\\n    if d >= 100:\\n        e = e + 5\\n    else:\\n        e = e + 1\\n\\n    return e")
