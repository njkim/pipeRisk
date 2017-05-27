# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# City_Park.py
# Created on: 2017-05-25 09:29:14.00000
#   (generated by ArcGIS/ModelBuilder)
# Usage: City_Park <WT_Pipe_main_surf> 
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
WT_Pipe_main_surf_Layer1 = "WT_Pipe_main_surf_Layer1"
WT_Pipe_main_surf_Layer1__2_ = WT_Pipe_main_surf_Layer1
FC_FacAllSite_V = "\\\\watis\\public\\InternsSpring2017\\Spring2017_WT_GeoDb.mdb\\Public Works\\FC_FacAllSite_V"
FC_FacAllSite_V_Select = "\\\\watis\\public\\InternsSpring2017\\Spring2017_WT_GeoDb.mdb\\FC_FacAllSite_V_Select"
WT_Pipe_main_surf_test = FC_FacAllSite_V_Select
WT_Pipe_main_surf_test__5_ = FC_FacAllSite_V_Select
WT_Pipe_main_surf_test__2_ = FC_FacAllSite_V_Select
WT_Pipe_main_surf_test__7_ = WT_Pipe_main_surf_Layer1__2_
WT_Pipe_main_surf_test__6_ = WT_Pipe_main_surf_test
WT_Pipe_main_surf_test__3_ = WT_Pipe_main_surf_test__5_
WT_Pipe_main_surf_test__8_ = WT_Pipe_main_surf_test__2_
WT_Pipe_main_surf_test__10_ = "\\\\watis\\public\\InternsSpring2017\\Spring2017_WT_GeoDb.mdb\\Spring2017_WT\\WT_Pipe_main_surf_test"

# Process: Calculate Field
arcpy.CalculateField_management(WT_Pipe_main_surf, "Risk_Park", "1", "PYTHON", "")

# Process: Make Feature Layer
arcpy.MakeFeatureLayer_management(WT_Pipe_main_surf__2_, WT_Pipe_main_surf_Layer1, "", "", "OBJECTID OBJECTID VISIBLE NONE;GID GID VISIBLE NONE;LAYER LAYER VISIBLE NONE;PIPEID PIPEID VISIBLE NONE;MATERIAL MATERIAL VISIBLE NONE;MaterialDesc MaterialDesc VISIBLE NONE;DIAMETER DIAMETER VISIBLE NONE;MEASUREDLE MEASUREDLE VISIBLE NONE;ACTUALLENG ACTUALLENG VISIBLE NONE;INSTALLATI INSTALLATI VISIBLE NONE;DRAWINGNO DRAWINGNO VISIBLE NONE;SOURCE SOURCE VISIBLE NONE;PressureZo PressureZo VISIBLE NONE;RiskCondition RiskCondition VISIBLE NONE;RiskFactor RiskFactor VISIBLE NONE;RiskIndex RiskIndex VISIBLE NONE;Shape Shape VISIBLE NONE;Z_Min Z_Min VISIBLE NONE;Z_Max Z_Max VISIBLE NONE;Z_Mean Z_Mean VISIBLE NONE;SLength SLength VISIBLE NONE;Min_Slope Min_Slope VISIBLE NONE;Max_Slope Max_Slope VISIBLE NONE;Avg_Slope Avg_Slope VISIBLE NONE;Shape_Length Shape_Length VISIBLE NONE;Risk_Pipe Risk_Pipe VISIBLE NONE;Risk_TruckRoute Risk_TruckRoute VISIBLE NONE;Risk_School Risk_School VISIBLE NONE;Risk_Business Risk_Business VISIBLE NONE;Risk_Facility Risk_Facility VISIBLE NONE;Risk_Park Risk_Park VISIBLE NONE;Risk_PumpStation Risk_PumpStation VISIBLE NONE;Risk_Creek Risk_Creek VISIBLE NONE;Risk_Diameter Risk_Diameter VISIBLE NONE;Likelihood Likelihood VISIBLE NONE;Consequence Consequence VISIBLE NONE;Risk_Index Risk_Index VISIBLE NONE")

# Process: Select
arcpy.Select_analysis(FC_FacAllSite_V, FC_FacAllSite_V_Select, "[TYPE] = 'Park'")

# Process: Select Layer By Location
arcpy.SelectLayerByLocation_management(WT_Pipe_main_surf_Layer1, "WITHIN_A_DISTANCE", FC_FacAllSite_V_Select, "1000 Feet", "NEW_SELECTION", "NOT_INVERT")

# Process: Calculate Field (2)
arcpy.CalculateField_management(WT_Pipe_main_surf_Layer1__2_, "Risk_Park", "2", "PYTHON", "")

# Process: Select Layer By Location (2)
arcpy.SelectLayerByLocation_management(WT_Pipe_main_surf_test__7_, "WITHIN_A_DISTANCE", FC_FacAllSite_V_Select, "500 Feet", "NEW_SELECTION", "NOT_INVERT")

# Process: Calculate Field (3)
arcpy.CalculateField_management(WT_Pipe_main_surf_test, "Risk_Park", "3", "PYTHON", "")

# Process: Select Layer By Location (3)
arcpy.SelectLayerByLocation_management(WT_Pipe_main_surf_test__6_, "WITHIN_A_DISTANCE", FC_FacAllSite_V_Select, "100 Feet", "NEW_SELECTION", "NOT_INVERT")

# Process: Calculate Field (4)
arcpy.CalculateField_management(WT_Pipe_main_surf_test__5_, "Risk_Park", "4", "PYTHON", "")

# Process: Select Layer By Location (4)
arcpy.SelectLayerByLocation_management(WT_Pipe_main_surf_test__3_, "INTERSECT", FC_FacAllSite_V_Select, "0 Feet", "NEW_SELECTION", "NOT_INVERT")

# Process: Calculate Field (5)
arcpy.CalculateField_management(WT_Pipe_main_surf_test__2_, "Risk_Park", "5", "PYTHON", "")

