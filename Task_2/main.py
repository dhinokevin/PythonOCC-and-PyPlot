from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeBox
from OCC.Core.gp import gp_Trsf, gp_Vec, gp_Ax1, gp_Pnt, gp_Dir
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_Transform
from OCC.Core.TopoDS import TopoDS_Compound
from OCC.Core.BRep import BRep_Builder
from OCC.Display.SimpleGui import init_display
from OCC.Core.gp import gp_EulerAngles
import math

# === PARAMETERS (MATCHING REFERENCE DRAWING) ===
I_BEAM_HEIGHT = 6096  # mm (20 ft)
BEAM_SPACING = 450  # mm (out to out)

# ISMB 200 Dimensions (from provided description and image, assuming ISMB 200)
I_BEAM_WIDTH = 200  # mm flange width  (Assumed ISMB 200)
FLANGE_THICKNESS = 9  # mm flange thickness (Assumed ISMB 200)
WEB_THICKNESS = 5.7  # mm web thickness    (Assumed ISMB 200)

# Lacing Flat Dimensions
LACING_WIDTH = 100  # mm
LACING_THICKNESS = 8  # mm
LACING_LENGTH = BEAM_SPACING - WEB_THICKNESS # changed to be equal to the clear distance between the I-beams.  Lacing connects the webs.
LACING_SPACING = 450  # mm vertical spacing (center to center)

# Batten Plate Dimensions
BATTEN_WIDTH = 300  # mm  (Given in description)
BATTEN_HEIGHT = 300  # mm (Consistent with previous code, and implied by description "300mm depth")
BATTEN_THICKNESS = 10  # mm (Given in description)

# === SHAPE FUNCTIONS ===

def make_i_beam(length):
    builder = BRep_Builder()
    compound = TopoDS_Compound()
    builder.MakeCompound(compound)

    # Web
    web_height = I_BEAM_WIDTH - 2 * FLANGE_THICKNESS
    web = BRepPrimAPI_MakeBox(length, WEB_THICKNESS, web_height).Shape()
    trsf_web = gp_Trsf()
    trsf_web.SetTranslation(gp_Vec(0, (I_BEAM_WIDTH - WEB_THICKNESS) / 2, FLANGE_THICKNESS))
    web = BRepBuilderAPI_Transform(web, trsf_web, True).Shape()
    builder.Add(compound, web)

    # Bottom flange
    bottom_flange = BRepPrimAPI_MakeBox(length, I_BEAM_WIDTH, FLANGE_THICKNESS).Shape()
    builder.Add(compound, bottom_flange)

    # Top flange
    top_flange = BRepPrimAPI_MakeBox(length, I_BEAM_WIDTH, FLANGE_THICKNESS).Shape()
    trsf_top = gp_Trsf()
    trsf_top.SetTranslation(gp_Vec(0, 0, I_BEAM_WIDTH - FLANGE_THICKNESS))
    top_flange = BRepBuilderAPI_Transform(top_flange, trsf_top, True).Shape()
    builder.Add(compound, top_flange)

    return compound

def make_plate(width, height, thickness):
    return BRepPrimAPI_MakeBox(width, thickness, height).Shape()
def make_lacing_flat(length, thickness, width):
    return BRepPrimAPI_MakeBox(length, thickness, width).Shape() # order of arguments corrected

# === MAIN ASSEMBLY ===
builder = BRep_Builder()
assembly = TopoDS_Compound()
builder.MakeCompound(assembly)

# Beam 1
beam1 = make_i_beam(I_BEAM_HEIGHT)
builder.Add(assembly, beam1)

# Beam 2 (shifted along X)
beam2 = make_i_beam(I_BEAM_HEIGHT)
trsf_beam2 = gp_Trsf()
trsf_beam2.SetTranslation(gp_Vec(BEAM_SPACING - WEB_THICKNESS, 0, 0)) # Changed to shift by WEB_THICKNESS
beam2 = BRepBuilderAPI_Transform(beam2, trsf_beam2, True).Shape()
builder.Add(assembly, beam2)

# Lacing flats
num_lace_intervals = int(I_BEAM_HEIGHT // LACING_SPACING)
for i in range(num_lace_intervals):
    z_start = i * LACING_SPACING + (I_BEAM_WIDTH-LACING_THICKNESS)/2 #start at the edge of the flange.
    y_offset = (I_BEAM_WIDTH - LACING_THICKNESS) / 2

    # Lacing 1 (Horizontal)
    start_point1 = gp_Pnt(WEB_THICKNESS/2, y_offset, z_start) #start at the WEB
    end_point1 = gp_Pnt(BEAM_SPACING - WEB_THICKNESS/2, y_offset, z_start) # end at the other WEB

    lace1 = make_lacing_flat(LACING_LENGTH, LACING_THICKNESS, LACING_WIDTH)
    transform1 = gp_Trsf()

    # Calculate rotation angle around Z-axis.
    angle1 = 0
    
    # Position at the start point
    transform1.SetTranslation(gp_Vec(start_point1.X(), start_point1.Y(), start_point1.Z()));

    # Rotate around Z-axis
    transform1.SetRotation(gp_Ax1(start_point1, gp_Dir(0, 0, 1)), angle1);

    lace1_transformed = BRepBuilderAPI_Transform(lace1, transform1, True).Shape()
    builder.Add(assembly, lace1_transformed)



# Top batten plate
top_batten = make_plate(BATTEN_WIDTH, BATTEN_HEIGHT, BATTEN_THICKNESS)
trsf_top_batt = gp_Trsf()
trsf_top_batt.SetTranslation(gp_Vec((BEAM_SPACING - BATTEN_WIDTH) / 2, I_BEAM_HEIGHT - BATTEN_THICKNESS, (I_BEAM_WIDTH - BATTEN_HEIGHT) / 2))
top_batten = BRepBuilderAPI_Transform(top_batten, trsf_top_batt, True).Shape()
builder.Add(assembly, top_batten)

# Bottom batten plate
bottom_batten = make_plate(BATTEN_WIDTH, BATTEN_HEIGHT, BATTEN_THICKNESS)
trsf_bot_batt = gp_Trsf()
trsf_bot_batt.SetTranslation(gp_Vec((BEAM_SPACING - BATTEN_WIDTH) / 2, 0, (I_BEAM_WIDTH - BATTEN_HEIGHT) / 2))
bottom_batten = BRepBuilderAPI_Transform(bottom_batten, trsf_bot_batt, True).Shape()
builder.Add(assembly, bottom_batten)

# === DISPLAY ===
display, start_display, add_menu, add_function_to_menu = init_display()
display.DisplayShape(assembly, update=True)
start_display()
