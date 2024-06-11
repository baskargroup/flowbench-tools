def write_config_file(re_number,Re_V, mesh_path, save_path):
    content = f"""
#####################################################
InletBCType = "PIPE_FLOW"
################# FEM Parameters #####################
basisFunction = "linear"
################# NS Parameters ######################
TimeStepper = "BDF2";
Re = 1000.0;
DiffFineTerms = True
SecondViscosity = False
VelocityExtrapolationOrder = 1;
DoReRamping = True;
RampingTime = 10000;
RampingRe = 100;
MMS = False;
ImmersedMethod= "SBM"
RatioGPSBM = 0.5

Cb_f = 1e2
totalT_V = [10, 20, 30, 50, 130, 160, 260, 392, 404] # for training
dt_V = [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.1, 0.005, 0.005]
OutputSpan_V = [10000, 10000, 10000, 10000, 10000 , 100000, 10000, 10000, 10] # for training
lvl_V = [-4, -3, -2, -1, 0, 0, 0, 0, 0]
Re_V = {Re_V}
################# MESH Parameters ######################
background_mesh = {{
  baseLevel = 8
  refineLevelBoundary = 6
  # cube domain
  min = [0.0, 0.0, 0.0]
  max = [64.0, 64.0, 2.0]
  #Specify periodicity
  periodicBoundariesAndScale = [0.0, 0.0, 0.0]
}}
# Physical Domain
physDomainMin = [0.0, 0.0, 0.0]
physDomainMax = [64.0,16.0, 2.0]
stlFileName = "model_scaled.stl"
stlRetainInside = false
geometries = (
  {{
    mesh_path = "{mesh_path}"
    name = "circle"
    is_static = false
    position = [5.5,7.5] # change pos
    outer_boundary=false
    type = "meshobject_2d"
    refine_lvl = 14 # on the boundary
    bc_type_V = ["sbm", "sbm", "sbm"]
    #bc_type_V = ["weak", "weak", "weak"]
    dirichlet_V = [0.0, 0.0, 0.0]
  }}
)
region_refine = (
{{
type = "sphere"
refine_region_lvl = 13
  radius = 0.71
  center = [6.0, 8.0, 5.0]
}},
{{
type = "sphere"
refine_region_lvl = 12
  radius = 0.8
  center = [6.0, 8.0, 5.0]
}},
{{
type = "sphere"
refine_region_lvl = 11
  radius = 1
  center = [6.0, 8.0, 5.0]
}},
{{
type = "sphere"
refine_region_lvl = 10
  radius = 2.5
  center = [6.0, 8.0, 5.0]
}},
{{
type = "sphere"
refine_region_lvl = 9
  radius = 3.0
  center = [6.0, 8.0, 5.0]
}},
{{
type = "cylinder"
refine_region_lvl = 10
radius = 2.5
c1 = [6.0, 8.0, 5.0]
c2 = [64.0, 8.0, 5.0]
}},
{{
type = "cylinder"
refine_region_lvl = 9
radius = 3.0
c1 = [6.0, 8.0, 5.0]
c2 = [64.0, 8.0, 5.0]
}}
)
################### Refinement in a Region ###############
rectLowerLeft = [-0.2, -0.2]
rectUpperRight = [-0.8, -0.8]
rect_lvl = 5
################### checkpoint and output setting ###############
checkpointFrequency = 100
checkpointNumberOfBackups = 3
# for output
OutputSpan = 1
################### solver setting ####################
solver_options = {{
  snes_atol = 1e-8
  snes_rtol = 1e-8
  snes_stol = 1e-8
  snes_max_it = 30
  snes_max_funcs = 80000
  ksp_max_it = 2000
  ksp_diagonal_scale = True
  ksp_diagonal_scale_fix = True
  pc_factor_reorder_for_nonzero_diagonal = ""
  ksp_type = "bcgs"
  pc_type = "asm"
  #pc_asm_type = "basic" #This uses full interpolation and restriction. This means that all processes communicate their entire solution to all other processes. This can often improve the quality of the preconditioner, but at the cost of increased communication overhead.
  ksp_atol = 1e-7
  ksp_rtol = 1e-7
  snes_monitor = ""
  snes_converged_reason = ""
}};
"""
    with open(save_path, "w") as file:
        file.write(content)
