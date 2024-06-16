def write_config_file(Gr_number, mesh_path,save_path):
    content = f"""
dt = 1
totalT = 502
SolveHT = true
SolveNS = true



#########################

ImmersedMethod= "SBM"

SBM = {{
SBMGeo = "arbitrary"
RatioGPSBM = 0.5
}}

#Debug_Integrand = true
###########################

############For Project I am working on############
InletBCType = "LDC_ARBITRARY"

HeatTimestepper="BDF2"
NSTimestepper = "BDF2"
NavierStokesSolverType = "LINEAR_NS"
HeatSolverType = "stabilizedHT"

###################################################



geometries = (
  {{

    mesh_path = "{mesh_path}"
    name = "circle"
    is_static = false
    position = [0.0,0.0] # change pos
    outer_boundary=false
    type = "meshobject_2d"
    refine_lvl = 3 # on the boundary

    # cool temperature at the circle
    bc_type_V = ["sbm", "sbm", "sbm", "dirichlet", "sbm"] # u,v,w,p,T
    dirichlet_V = [0.0, 0.0, 0.0, 0.0, 0.0] # pow(0.5,3)
  }}
)

##########Coefficient  ###########################
Cb_f = 100
Cb_e = 400


#########################


gp_handle = 0

tauM_scale = 0.1
G_dir = 1

### block iteration
blockTolerance = 1e-3
iterMaxBlock = 8

###########################
###background_mesh########
elemOrder = 1
channel_mesh = {{
  refine_lvl_base = 9
  refine_lvl_channel_wall = 5
  enable_subda = false
  min = [0, 0, 0]
  max = [2.0, 2.0, 0.0]
  refine_walls = true
}}

#######################
### Coe setup
NondimensionType = "mix_conv"
Ci_e = 36
Ci_f = 36

# for free_conv
Re = 50  # original Re =100, now domain size is twice                  #Ra=Gr.Pr Gr=Ri.Re^2
Pe = 35 # Pr = 0.7

# Ri = Gr/Re^2 -> Ri = 0.01, 1, 5
Gr = {Gr_number/8}

### ICs
initial_condition = {{
  vel_ic_type = "user_defined"
  vel_ic = [0.0, 0.0, 0.0]
  temperature_ic_type = "user_defined"
  temperature_ic = 0
  #pressure_ic_type = "user_defined"
  #pressure_ic = 0.0
}}


OutputStartTime = 0
OutputInterval = 10000
CheckpointInterval = 50
SurfaceMonitor = [2]
PostProcessingInterval = 50
averageStartTimeStep =  10000

#################### solver setting ####################
solver_options_ns = {{
  snes_atol = 1e-8
  snes_rtol = 1e-8
  snes_stol = 1e-8
  snes_max_it = 10
  snes_max_funcs = 80000
  snes_max_linear_solve_fail = 4
  ksp_diagonal_scale = True
  ksp_diagonal_scale_fix = True
  ksp_max_it = 1000
  ksp_atol = 1e-10
  ksp_rtol = 1e-10
  ksp_type = "bcgs"
  pc_type = "lu"

  #pc_type = "asm"
  #sub_pc_type = "lu"

  # monitor
  snes_monitor = ""
  snes_converged_reason = ""
  #ksp_monitor = ""
  ksp_monitor_short = ""
  ksp_converged_reason = ""
}};
solver_options_ht = {{
  ksp_max_it = 500000
  ksp_type = "bcgs"
  pc_type = "lu"

  #pc_type = "jacobi"
  #sub_pc_type = "lu"

  ksp_atol = 1e-12
  ksp_rtol = 1e-12
  #ksp_monitor = ""
  ksp_monitor_short = ""
  ksp_converged_reason = ""
}}
"""
    with open(save_path, "w") as file:
        file.write(content)

# Example usage:
# mesh_path = "./arbitrary_mesh_complex.msh"
# save_path = "config.txt"
# write_config_file(50.0, 1, 1000, 5, False, 10000, 100, mesh_path, save_path)
