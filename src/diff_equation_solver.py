import numpy as np
from scipy.integrate import solve_ivp
from global_consts import GM_sun, GM_earth, rtol_val, atol_val, G, m_cruithne, M_earth

def equations_of_motion(t, y):
    xE, yE, zE, vxE, vyE, vzE, xC, yC, zC, vxC, vyC, vzC = y

    rE_sun = np.sqrt(xE**2 + yE**2 + zE**2)
    rC_sun = np.sqrt(xC**2 + yC**2 + zC**2)
    rCE = np.sqrt((xC - xE)**2 + (yC - yE)**2 + (zC - zE)**2)

    axE_sun = -GM_sun * xE / (rE_sun**3)
    ayE_sun = -GM_sun * yE / (rE_sun**3)
    azE_sun = -GM_sun * zE / (rE_sun**3)

    axC_sun = -GM_sun * xC / (rC_sun**3)
    ayC_sun = -GM_sun * yC / (rC_sun**3)
    azC_sun = -GM_sun * zC / (rC_sun**3)

    axC_earth = -GM_earth * (xC - xE) / (rCE**3)
    ayC_earth = -GM_earth * (yC - yE) / (rCE**3)
    azC_earth = -GM_earth * (zC - zE) / (rCE**3)

    return [
        vxE, vyE, vzE, axE_sun, ayE_sun, azE_sun,  
        vxC, vyC, vzC, axC_sun + axC_earth, ayC_sun + ayC_earth, azC_sun + azC_earth  
    ]

def solve_orbits(equations_of_motion, t_span, y0, t_eval):
    return solve_ivp(equations_of_motion, t_span, y0, method='RK45', t_eval=t_eval, rtol=rtol_val, atol=atol_val)

def calculate_energy(y):
    xE, yE, zE, vxE, vyE, vzE, xC, yC, zC, vxC, vyC, vzC = y

    rE_sun = np.sqrt(xE**2 + yE**2 + zE**2)
    rC_sun = np.sqrt(xC**2 + yC**2 + zC**2)
    rCE = np.sqrt((xC - xE)**2 + (yC - yE)**2 + (zC - zE)**2)

    KE_earth = 0.5 * M_earth * (vxE**2 + vyE**2 + vzE**2)
    KE_cruithne = 0.5 * m_cruithne * (vxC**2 + vyC**2 + vzC**2)

    PE_sun_earth = -GM_sun * M_earth / rE_sun
    PE_sun_cruithne = -GM_sun * m_cruithne / rC_sun
    PE_earth_cruithne = -GM_earth * m_cruithne / rCE

    total_energy = KE_earth + KE_cruithne + PE_sun_earth + PE_sun_cruithne + PE_earth_cruithne
    return total_energy

def calculate_angular_momentum(y):
    xE, yE, zE, vxE, vyE, vzE, xC, yC, zC, vxC, vyC, vzC = y

    rE = np.array([xE, yE, zE])

    rC = np.array([xC, yC, zC])

    vE = np.array([vxE, vyE, vzE])

    vC = np.array([vxC, vyC, vzC])

    M_earth = GM_earth / G  

    L_earth = np.cross(rE, M_earth * vE)

    L_cruithne = np.cross(rC, m_cruithne * vC)

    total_angular_momentum = L_earth + L_cruithne

    return total_angular_momentum