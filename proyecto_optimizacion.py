import matplotlib.pyplot as plt


from pyomo.environ import *
from pyomo.opt import SolverFactory

#SETS
M = ConcreteModel()
#set para identificar a cada familia
Familias = RangeSet(1,5)
M.Familias = Familias
#set para identificar a cada centro
Centros = RangeSer(1,2)
M.Centros = Centros

#PARAMETROS
familias_data = {1:4, 2:3, 3:5, 2:1}
#Parametro que dice cuantos miembros tiene cada familia
M.Miembros_Familias = Param(M.Familias, within=NonNegativeReals, initialize=familias_data)

#Parametro que indica cuantos centros pueden recibir a los refugiados
CantidadCentros = len(Centros) 

#VARIABLES
#Indica a que centro fue asignada cada familia
M.Asignaciones = Var(M.Familias,M.Centros,domain=Binary)
#Indica cuantos ocupantes tiene cada centro
M.Ocupantes_x_Centro = Var(M.Centros,Domain=Integers)
#Indica el promedio actual de ocupantes en los centros de refugiados
M.promedio = Var(Domain=Reals)

#OBJETIVO
#Suma la diferencia de la cantidad de ocupantes de cada miembro con el promedio de ocupantes,
#mientras mas equitativa la reparticion mas baja la diferencia.
M.obj = Objective(expr= sum( abs(M.Ocupantes_x_Centro[j] - M.promedio) for j in M.Centros))


#ECUACIONES