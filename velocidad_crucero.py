# -*- coding: utf-8 -*-
"""

@author: Team REOS

Esta función proporciona la velocidad exacta de crucero para que el
empuje sea igual a la resistencia.

"""



from modeloISA import density, temperature, GAMMA, R_AIR, gravity
from modelo_empuje import thrust
from aero_avion import  k, cd0, cd_inducida, S_W
from aero_avion import resistencia, sustentacion
from aero_misil import cdll, SREF_MISIL




def vuelo_crucero(M):


    
      #------------------------CARACTERÍSTICAS DE LA AERONAVE------------------------
    
     
    
    
    
    h = 12000  # Altitud inicial (m).
       
    g0 =gravity(h)  # Aceleración g0itatoria (m/s2).
    W = 14273 * g0
    rho = density(h)  # Densidad inicial del aire (kg/m3).
    
    T = temperature(h)  # Temperatura inicial del aire (K).
    
      #A la altura inicial el avión vuela en vuelo estacionario.
    v = M * (GAMMA * R_AIR * T)**.5  # Velocidad inicial (m/s).
    
      #Coeficientes aerodinámicos
    
    '''Ecuacion de vuelo en crucero L = W ''' 
    CL = 2 * W / (rho * v**2 * S_W)
    k1 = k(M)
    CD01 = cd0(M)
    CDmisilavion = cdll(M, v)
    CD_inducida1 = cd_inducida(k1, CL)
    CD = CD01 + CD_inducida1  # Polar del avión.  Coeficiente de resistencia.
    
    
      #Fuerzas.
    Davion = resistencia(v, rho, CD)  # Resistencia aerodinámica (N).
    Dmisil = 0.5 * rho * CDmisilavion * SREF_MISIL * v**2
      
    D = Davion + Dmisil
    
    L = sustentacion(v, rho, CL)  # Sustentación aerodinámica (N).
    Th = thrust(M, rho)  # Empuje (N).
    
    ''' Esta es la ecuacion en eje horizontal T = D que es la condicion que queremos cumplir
    por ello calculamos la diferencia y en el while se intenta que sea 0 '''
    
    diferencia_T_D = Th - D
    
    
    dM = 0.00001 #Variaremos el Mach para iterar
    
    if diferencia_T_D < 0:
        print('Error. La resistencia es mayor que el empuje en vuelo rectilíneo')
        
    
        
        
    while diferencia_T_D >= 0:
     
      M = M + dM
      v = M * (GAMMA * R_AIR * T)**.5  # Velocidad inicial (m/s).
    
      
    
      #Coeficientes aerodinámicos
    
      '''Ecuacion de vuelo en crucero L = W ''' 
      CL = 2 * W / (rho * v**2 * S_W)
      k1 = k(M)
      CD01 = cd0(M)
      CDmisilavion = cdll(M, v)
      CD_inducida1 = cd_inducida(k1, CL)
      CD = CD01 + CD_inducida1  # Polar del avión.  Coeficiente de resistencia.
    

      #Fuerzas.
      Davion = resistencia(v, rho, CD)  # Resistencia aerodinámica (N).
      Dmisil = 0.5 * rho * CDmisilavion * SREF_MISIL * v**2
      D = Davion + Dmisil

      Th = thrust(M, rho)  # Empuje (N).
    
      ''' Esta es la ecuacion en eje horizontal T = D que es la condicion que queremos cumplir
      por ello calculamos la diferencia y en el while se intenta que sea 0 '''
    
      diferencia_T_D = Th - D
    
#    print('El número de Mach es: ',M)
#    
#    print('Thrust: ', Th) 
#    
#    print('Drag: ', D)
    
  
    return M


