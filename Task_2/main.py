from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeBox
from OCC.Core.gp import gp_Trsf, gp_Vec
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_Transform
from OCC.Core.TopoDS import TopoDS_Compound
from OCC.Core.BRep import BRep_Builder
from OCC.Display.SimpleGui import init_display

# === PARAMETERS ===
I_BEAM_LENGTH = 6096  # mm (20 ft)
BEAM_SPACING = 450  # mm (center-to-center distance)
I_BEAM_WIDTH = 200  # mm flange width
FLANGE_THICKNESS = 9  # mm
WEB_THICKNESS = 5.7  # mm

LACING_THICKNESS = 10  # mm square cross-section
LACING_COUNT = 5  # number of lacing bars

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

def make_lacing_bars():
    lacing_compound = TopoDS_Compound()
    builder = BRep_Builder()
    builder.MakeCompound(lacing_compound)

    spacing = I_BEAM_LENGTH / (LACING_COUNT + 1)
    
    # Position lacing bars to touch both webs
    lacing_length = BEAM_SPACING - WEB_THICKNESS  # Adjusted to go from one web to the other

    for i in range(1, LACING_COUNT + 1):
        x_pos = i * spacing

        lacing_bar = BRepPrimAPI_MakeBox(
            LACING_THICKNESS, lacing_length, LACING_THICKNESS
        ).Shape()

        # Center vertically between flanges
        z_center = (I_BEAM_WIDTH - LACING_THICKNESS) / 2

        # Align with inner side of the first web
        y_start = WEB_THICKNESS / 2

        trsf = gp_Trsf()
        trsf.SetTranslation(gp_Vec(
            x_pos,
            y_start,
            z_center
        ))
        transformed_bar = BRepBuilderAPI_Transform(lacing_bar, trsf, True).Shape()
        builder.Add(lacing_compound, transformed_bar)

    return lacing_compound

# === MAIN ASSEMBLY ===
builder = BRep_Builder()
assembly = TopoDS_Compound()
builder.MakeCompound(assembly)

# Beam 1
beam1 = make_i_beam(I_BEAM_LENGTH)
builder.Add(assembly, beam1)

# Beam 2 (shifted along Y-axis)
beam2 = make_i_beam(I_BEAM_LENGTH)
trsf_beam2 = gp_Trsf()
trsf_beam2.SetTranslation(gp_Vec(0, BEAM_SPACING, 0))
beam2 = BRepBuilderAPI_Transform(beam2, trsf_beam2, True).Shape()
builder.Add(assembly, beam2)

# Add lacing bars
lacing_bars = make_lacing_bars()
builder.Add(assembly, lacing_bars)

# === DISPLAY ===
display, start_display, add_menu, add_function_to_menu = init_display()
display.DisplayShape(assembly, update=True)
start_display()
