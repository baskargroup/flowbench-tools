def write_config_file(re_number, dt, t_final, OutputSpan, lvl_V, CdStartTimeStep, baseLevel, DoReRamping, RampingTime, RampingRe, mesh_path, save_path):
    content = f"""
################# FEM Parameters #####################
basisFunction = "linear"
################# NS Parameters ######################
TimeStepper = "BDF2";
Re = {re_number/2};
DiffFineTerms = True;
SecondViscosity = False
VelocityExtrapolationOrder = 1;

DoReRamping = {DoReRamping};
RampingTime = {RampingTime};
RampingRe = {RampingRe/2};
MMS = False;
ImmersedMethod= "SBM"
RatioGPSBM = 0.5
Cb_f = 1e2

totalT_V = {t_final}
dt_V = {dt}
OutputSpan_V = {OutputSpan}
CdStartTimeStep = {CdStartTimeStep}
lvl_V = {lvl_V}
################# MESH Parameters ######################
background_mesh = {{
  baseLevel = {baseLevel}
  refineLevelBoundary = {baseLevel}

  # cube domain
  min = [0.0, 0.0, 0.0]
  max = [2.0, 2.0, 2.0]

  #Specify periodicity
  periodicBoundariesAndScale = [0.0, 0.0, 0.0]
}}

# Physical Domain
physDomainMin = [0.0, 0.0, 0.0]
physDomainMax = [2.0, 2.0, 2.0]

stlFileName = "{mesh_path}"
stlRetainInside = false

geometries = (
  {{
    mesh_path = "{mesh_path}"
    name = "circle"
    is_static = false
    position = [0.0, 0.0, 0.0]  # change pos
    outer_boundary = false
    type = "meshobject"
    refine_lvl = 9  # on the boundary

    bc_type_V = ["sbm", "sbm", "sbm", "sbm"]
    dirichlet_V = [0.0, 0.0, 0.0, 0.0] 
  }}
)

################### Refinement in a Region ###############

rectLowerLeft = [-0.2, -0.2, -0.2]
rectUpperRight = [-0.8, -0.8, -0.8]
rect_lvl = 5

################### checkpoint and output setting ###############
checkpointFrequency = 50
checkpointNumberOfBackups = 3

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
  sub_pc_type = "lu"

  # monitor
  snes_monitor = ""
  snes_converged_reason = ""
  ksp_converged_reason = ""
  
}};
"""
    with open(save_path, "w") as file:
        file.write(content)

# Example usage:
# mesh_path = "./arbitrary_mesh_complex.msh"
# save_path = "config.txt"
# write_config_file(50.0, 1, 1000, 5, False, 10000, 100, mesh_path, save_path)
