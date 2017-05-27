import arcpy

print("preparing data...")
arcpy.env.overwriteOutput = True
arcpy.env.workspace = "in_memory"

path = "C:\\Temp\\Spring2017_WT_GeoDb.mdb"
# path = "\\\\watis\\public\\InternsSpring2017\\Spring2017_WT_GeoDb.mdb"

pipe = path + "\\Spring2017_WT\\WT_Pipe_main_surf"
BS_School = path + "\\City Bench\\BS_School"
NF_Creeks = path + "\\Natural Features\\NF_Creeks"
TR_TrkRte = path + "\\Transportation\\TR_TrkRte"
PL_MidtBndy = path + "\\Planning\\PL_MidtBndy"
PL_TSA = path + "\\Planning\\PL_TSA"
FC_FacAllSite_V = path + "\\Public Works\\FC_FacAllSite_V"

PL_Business = "PL_Business"
FC_FacAllSite_V_Facility = "FC_FacAllSite_V_Facility"
FC_FacAllSite_V_Park = "FC_FacAllSite_V_Park"
FC_FacAllSite_V_PumpStation = "FC_FacAllSite_V_PumpStation"
pipe_layer = "pipe_layer"

arcpy.Union_analysis([PL_MidtBndy, PL_TSA], PL_Business, "ALL", "", "GAPS")
arcpy.Select_analysis(FC_FacAllSite_V, FC_FacAllSite_V_Facility, "[TYPE] = 'Facility'")
arcpy.Select_analysis(FC_FacAllSite_V, FC_FacAllSite_V_Park, "[TYPE] = 'Park'")
arcpy.Select_analysis(FC_FacAllSite_V, FC_FacAllSite_V_PumpStation, "[TYPE] = 'Pump Station'")

print("creating pipe_layer...")
arcpy.MakeFeatureLayer_management(pipe, pipe_layer)

# adding fields
print("adding fields...")
arcpy.AddField_management(pipe_layer, "Risk_Pipe", "SHORT", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
arcpy.AddField_management(pipe_layer, "Risk_TruckRoute", "SHORT", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
arcpy.AddField_management(pipe_layer, "Risk_School", "SHORT", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
arcpy.AddField_management(pipe_layer, "Risk_Business", "SHORT", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
arcpy.AddField_management(pipe_layer, "Risk_Facility", "SHORT", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
arcpy.AddField_management(pipe_layer, "Risk_Park", "SHORT", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
arcpy.AddField_management(pipe_layer, "Risk_PumpStation", "SHORT", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
arcpy.AddField_management(pipe_layer, "Risk_Creek", "SHORT", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
arcpy.AddField_management(pipe_layer, "Risk_Diameter", "SHORT", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
arcpy.AddField_management(pipe_layer, "Likelihood", "FLOAT", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
arcpy.AddField_management(pipe_layer, "Consequence", "FLOAT", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
arcpy.AddField_management(pipe_layer, "Risk_Index", "SHORT", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")

""" spatial analysis to calculate the risk factor according to the distance from a certain area
"""
def distance(district_name, field_name):
    # a is a district name as a variable name, b is a field name as a string
    print("calculating " + field_name + "...")
    arcpy.CalculateField_management(pipe_layer, field_name, "1", "PYTHON", "")
    arcpy.SelectLayerByLocation_management(pipe_layer, "WITHIN_A_DISTANCE", district_name, "1000 Feet", "NEW_SELECTION", "NOT_INVERT")
    arcpy.CalculateField_management(pipe_layer, field_name, "2", "PYTHON", "")
    arcpy.SelectLayerByLocation_management(pipe_layer, "WITHIN_A_DISTANCE", district_name, "500 Feet", "NEW_SELECTION", "NOT_INVERT")
    arcpy.CalculateField_management(pipe_layer, field_name, "3", "PYTHON", "")
    arcpy.SelectLayerByLocation_management(pipe_layer, "WITHIN_A_DISTANCE", district_name, "100 Feet", "NEW_SELECTION", "NOT_INVERT")
    arcpy.CalculateField_management(pipe_layer, field_name, "4", "PYTHON", "")
    arcpy.SelectLayerByLocation_management(pipe_layer, "INTERSECT", district_name, "0 Feet", "NEW_SELECTION", "NOT_INVERT")
    arcpy.CalculateField_management(pipe_layer, field_name, "5", "PYTHON", "")
    arcpy.SelectLayerByAttribute_management(pipe_layer, "CLEAR_SELECTION")

# School + Creek + City_facility + City_Park + City_PumpStation
distance(BS_School, "Risk_School")
distance(NF_Creeks, "Risk_Creek")
distance(FC_FacAllSite_V_Facility, "Risk_Facility")
distance(FC_FacAllSite_V_Park, "Risk_Park")
distance(FC_FacAllSite_V_PumpStation, "Risk_PumpStation")

# Truck_Route
print("calculating Risk_TruckRoute...")
arcpy.CalculateField_management(pipe_layer, "Risk_TruckRoute", "1", "PYTHON", "")
arcpy.SelectLayerByLocation_management(pipe_layer, "WITHIN_A_DISTANCE", TR_TrkRte, "75 Feet", "NEW_SELECTION", "NOT_INVERT")
arcpy.CalculateField_management(pipe_layer, "Risk_TruckRoute", "5", "PYTHON", "")
arcpy.SelectLayerByAttribute_management(pipe_layer, "CLEAR_SELECTION")

# Midtown_TSA
print("calculating Risk_Business...")
arcpy.CalculateField_management(pipe_layer, "Risk_Business", "1", "PYTHON", "")
arcpy.SelectLayerByLocation_management(pipe_layer, "INTERSECT", PL_Business, "0 Feet", "NEW_SELECTION", "NOT_INVERT")
arcpy.CalculateField_management(pipe_layer, "Risk_Business", "5", "PYTHON", "")
arcpy.SelectLayerByAttribute_management(pipe_layer, "CLEAR_SELECTION")

# Pipe_Risk
print("calculating Pipe_Risk...")
pipeRisk_function = """
def pipeRisk(a,b,c,d): # a = diameter, b = material, c = age, d = elevation
    if a == None or b == None or c == None or a == 0 or b == '' or c == '' or b == 'UNK':  
        return None
    else:
        e = 0
# diameter
    if a <= 10:
        e = e + 5
    elif a > 10 and a <=20:
        e = e + 4
    else:
        e = e + 3
# material
    if b[0:1] == 'S' or b=='CIP':
        e = e + 5
    elif b[0:2] == 'DI':
        e = e + 4
    elif b == 'ACP' or b == 'CIP':
        e = e + 3
    elif b == 'RCP':
        e = e + 2
    else:
        e = e + 1
# age
    if c[0:3] == '195' or c[0:3] == '196':
        e = e + 4
    elif c[0:3] == '197' or c[0:3] == '198':
        e = e + 3
    elif c[0:3] == '199' or c[0:3] == '200':
        e = e + 2
    else:
        e = e + 1
# elevation
    if d >= 100:
        e = e + 5
    else:
        e = e + 1
    return e
"""
arcpy.CalculateField_management(pipe_layer, "Risk_Pipe", "pipeRisk(!DIAMETER!, !MATERIAL!, !INSTALLATI!, !Z_Max!)", "PYTHON", pipeRisk_function)

# Diameter
print("calculating Risk_Diameter...")
diameter_function = """
def diameter(a): # a = diameter
    if a == None:
        return None
    elif a <= 10:
        return 1
    elif a > 10 and a <=16:
        return 2
    elif a > 16 and a <=36:
        return 3
    else:
        return 5
"""
arcpy.CalculateField_management(pipe_layer, "Risk_Diameter", "diameter(!DIAMETER!)", "PYTHON", diameter_function)

# Consequences
print("calculating Likelihood, Consequence, and Risk_Index...")
Consequence_function = """
(!Risk_Facility! *4 + !Risk_PumpStation! *5 + !Risk_Park! *2 + !Risk_School! *4 + !Risk_Business! *4 + !Risk_Creek! *5 + !Risk_Diameter! *5)* 10./145
"""
Likelihood_function = """
def likelihood(a,b): # a: pipe risk (20), b: truck route (5)
    if a == None:        
        return None    
    else:        
        return (a + b)/2.5
"""
RiskIndex_function = """
def riskIndex(a,b):
    if a == None or b == None:        
        return None
    else:
        return (a * b)
"""
arcpy.CalculateField_management(pipe_layer, "Consequence", Consequence_function, "PYTHON", "")
arcpy.CalculateField_management(pipe_layer, "Likelihood", "likelihood(!Risk_Pipe!, !Risk_TruckRoute!)", "PYTHON", Likelihood_function)
arcpy.CalculateField_management(pipe_layer, "Risk_Index", "riskIndex( !Consequence!, !Likelihood! )", "PYTHON", RiskIndex_function)

# Clearing IN_MEMORY space
arcpy.Delete_management("in_memory")
print("All done")
