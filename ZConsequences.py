# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# Consequences.py
# Created on: 2017-05-25 09:30:59.00000
#   (generated by ArcGIS/ModelBuilder)
# Usage: Consequences <WT_Pipe_main_surf> 
# Description: 
# ---------------------------------------------------------------------------

# Import arcpy module
import arcpy

# Script arguments
WT_Pipe_main_surf = arcpy.GetParameterAsText(0)
if WT_Pipe_main_surf == '#' or not WT_Pipe_main_surf:
    WT_Pipe_main_surf = "\\\\watis\\public\\InternsSpring2017\\Spring2017_WT_GeoDb.mdb\\Spring2017_WT\\WT_Pipe_main_surf" # provide a default value if unspecified

# Local variables:
WT_Pipe_main_surf__2_ = WT_Pipe_main_surf
WT_Pipe_main_surf_test = WT_Pipe_main_surf__2_
WT_Pipe_main_surf_test__6_ = WT_Pipe_main_surf_test

# Process: Calculate Field
arcpy.CalculateField_management(WT_Pipe_main_surf, "Consequence", "(!Risk_Facility! *4 + !Risk_PumpStation! *5 + !Risk_Park! *2 + !Risk_School! *4 + !Risk_Business! *4 + !Risk_Creek! *5 + !Risk_Diameter! *5)*10./145", "PYTHON", "")

# Process: Calculate Field (2)
arcpy.CalculateField_management(WT_Pipe_main_surf__2_, "Likelihood", "PipeRisk(!Risk_Pipe!, !Risk_TruckRoute!)", "PYTHON", "def PipeRisk(a,b):\\n# a: pipe risk (20), b: truck route (5)\\n    if a == None:\\n        return None\\n    else:\\n        return (a+b)/2.5")

# Process: Calculate Field (3)
arcpy.CalculateField_management(WT_Pipe_main_surf_test, "Risk_Index", "RiskIndex( !Consequence!, !Likelihood! )", "PYTHON", "def RiskIndex(a,b):\\n    if a == None or b == None:\\n        return None\\n    else:\\n        return (a*b)")

