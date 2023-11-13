import matplotlib.pyplot as plt

import matplotlib.pyplot as plt
from pyomo.environ import *
from pyomo.opt import SolverFactory

#SETS
M = ConcreteModel()
#set para identificar a cada familia
#AJUSTAR ESTE PARAMETRO PARA CAMBIAR LA CANTIDAD DE FAMILIAS
Familias = RangeSet(1,10)
M.Familias = Familias
#set para identificar a cada centro
#AJUSTAR ESTE PARAMETRO PARA CAMBIAR LA CANTIDAD DE CENTROS
Centros = RangeSet(1,5)
M.Centros = Centros

#PARAMETROS
familias_data = {1:4, 2:3, 3:5, 4:1, 5:3, 6:7, 7:2, 8:5, 9:1, 10:3}
#Parametro que dice cuantos miembros tiene cada familia
M.Miembros_Familias = Param(M.Familias, within=NonNegativeReals, initialize=familias_data)

#Parametro que indica cuantos centros pueden recibir a los refugiados
CantidadCentros = len(Centros) 

#VARIABLES
#Indica a que centro fue asignada cada familia
M.Asignaciones = Var(M.Familias,M.Centros,domain=Binary)
#Indica cuantos ocupantes tiene cada centro
M.Ocupantes_x_Centro = Var(M.Centros,domain=Integers)
#Indica el promedio actual de ocupantes en los centros de refugiados
M.promedio = Var(domain=Reals)

#OBJETIVO
#Suma la diferencia de la cantidad de ocupantes de cada miembro con el promedio de ocupantes,
#mientras mas equitativa la reparticion mas baja la diferencia.
M.obj = Objective(expr= sum( abs(M.Ocupantes_x_Centro[j] - M.promedio) for j in M.Centros))


#ECUACIONES

#Esta restriccion se utiliza para recalcular el promedio
M.res1 = Constraint(expr= sum(M.Ocupantes_x_Centro[j]/(CantidadCentros+0.1) for j in M.Centros)==M.promedio)

#Esta restricción se usa para asegurar que cada familia esta asignada a un centro de refugiados. 
def Asignado_rule(Model, i):
    return sum(M.Asignaciones[i,j] for j in M.Centros) == 1
M.Asignado = Constraint(M.Familias,rule= Asignado_rule)

#Esta restricción se utiliza para asegurar que la ocupación del centro de refugiados sea equivalente a la suma de la cantidad de miembros de las familias que lo ocupan. 
def Coherencia_rule(Model,j):
    return sum(M.Asignaciones[i,j]*M.Miembros_Familias[i] for i in M.Familias)==M.Ocupantes_x_Centro[j]
M.Coherencia = Constraint(M.Centros, rule=Coherencia_rule)

SolverFactory('mindtpy').solve(M,mip_solver='glpk',nlp_solver='ipopt')

xi = [value(M.Centros[j]) for j in Centros]
y = [value(M.Ocupantes_x_Centro[j]) for j in Centros]

fig, ax = plt.subplots()
ax.bar(x=xi,tick_label= xi, height= y,color = '#9BBB34')
plt.xlabel('Centro')
plt.ylabel('Ocupantes')
plt.title('Ocupación')
plt.show()


M.display()