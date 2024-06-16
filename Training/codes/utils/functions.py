import numpy as np

def L2_norm(u_ap, u_ex, hx, hy):
    return np.sqrt(np.sum((u_ap - u_ex)**2))*np.sqrt(hx*hy)

def LInf_norm(u_ap, u_ex, hx, hy):
    return np.max(np.abs(u_ap - u_ex))

