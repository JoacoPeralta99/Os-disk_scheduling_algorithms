import random
from turtle import left, right

# establezco un Tamaño limite para las peticiones

tamaño = 6

# Establezco una posición aleatoria en el disco.

ultima_ubicacion = random.randint(0, 999)

# listas donde se van a almacenar las peticiones/procesos 

procesos = []


procesos2 = []          # se crea exclusivamente para el metodo sstf 


# Sstf_procesos = []  # variable global en el caso que se requiera mantener un registro acumulativo de los valores en la funcion

for i in range(tamaño):             
    i = random.randint(0, 999)              # random para generar numeros al azar 
    procesos.append(i)                      # añado a la lista procesos


procesos2.extend(procesos)   # se realiza una copia de los procesos mediante extend para poder trabajar los datos
                             # en el formato de listas dentro de psg 
                             # ademas esto logra independizar y evitar que se pierdan los datos dentro de la lista procesos
                             # cuando utilizamos el metodo SSTF 


# la creacion de la estructura de datos pila

def pila(procesos):     
        return(list(reversed(procesos)))       # se utiliza para reversar la lista procesos con el fin de generar la pila    


# --------------- Funciones Metodos Administración -------------------

# First Come First Served

def fcfs(procesos):
    print("Processes:",procesos)
    for x in procesos:
        return procesos


# Shortest Seek Time First

def sstf(procesos2, ultima_ubicacion):
        Sstf_procesos = []
        visualizar = f"Processes:{procesos}" # para poder ver los procesos en carga cuando se generaban del random
        localizacion = f"Last Location: {ultima_ubicacion}"  # se genera la variable localizacion con el fin de guardar el valor para poder ser retornado antes de que ultima ubicacion modifique su valor 
        # print('procesos2:',procesos2)
        # Inicializo en cero el proceso mejor proximidad de la posicion en el disco
        Proximidad_proceso = 0
        tamaño_Particion = 1000    
        # recorrido del disco
        for x in range(tamaño_Particion):
            # lectura de peticiones dentro del disco
            for i in procesos2:
                # Busco el dato más cercano de la ultima posicion de proceso en el disco
                Proximidad_proceso = min(procesos2, key=lambda x:abs(x-ultima_ubicacion))
               

                # Actualizo la ultima ubicacion para que coincida con el proceso a realizar
                ultima_ubicacion = Proximidad_proceso
                # Elimino el proceso de proximidad de la lista procesos para evitar repeticiones de sector
                procesos2.remove(Proximidad_proceso)
                Sstf_procesos.append(Proximidad_proceso)
        
        return(localizacion,f"Ssft Method:{Sstf_procesos}")    # devuelve la ultima ubicacion y los datos del de la funcion para ser utilizados en psg formato lista


# SCAN Elevator

def scan(ultima_ubicacion,procesos):
    visualizar2 = f"Processes:{procesos}"
    # print(visualizar2)
    localizacion2= f"Last Location: {ultima_ubicacion}"
    # print(localizacion2)

    R_or_L = ["right" ,"left"]
    direction = random.choice(R_or_L)   # la direccion se elegira aleatoriamente
    # print(f"Direccion: {direction}")


    right = []   # listas para los datos de direccion derecha
        


    left = []    # listas para los datos de direccion izquierda

   
    for x in range(tamaño):

        if (procesos[x] < ultima_ubicacion):
            left.append(procesos[x])

        elif (procesos[x] > ultima_ubicacion):
            right.append(procesos[x])
            
      

    left.sort()             # se ordenan las listas menor a mayor 
    right.sort()
    left = list(reversed(left))   

    
    run = 5    #recorrido
    while run != 0:
        if direction == 'left':
            L_Data=(f"Data search to the left:{left}")
                                 

            direction = "right"     # se realiza el cambio de dirección hacia la derecha
        
        elif direction == "right":
            R_Data = (f"Data search to the Right:{right}")
                
            direction = "left"  # se realiza el cambio de dirección hacia la izquierda

        run -= 1

    return (visualizar2,localizacion2,L_Data,R_Data)     
  

# C-SCAN Circular Elevator

def c_scan(ultima_ubicacion,procesos): 
    visualizar3 = f"Processes:{procesos}"
    localizacion3= f"Last Location: {ultima_ubicacion}"
    # contador_operaciones = 0
    # distance = 0
    head = ultima_ubicacion  # head seria el cabezal 
    sector = sorted(procesos) #ordena los sectores de menor a mayor
    seek = [] # se establece para la busqueda
    for i in sector: #Agrego los sector de mayor numeracion cercanos al cabezal
        if head <= i:   
            head = i
            seek.append(i)

    head = 0 #el cabezal vuelve a cero y se vuelve a buscar desde el principio
    for i in sector: #agrego el resto de sectores a la lista
        if head <= i and i not in seek:   
            head = i
            seek.append(i)
    return (visualizar3,localizacion3,f"C-scan Method:{seek}")


#  PRUEBAS DE EJECUCIÓN

#|1| First Come First Served

#print(fcfs(procesos))

#|2| Shortest Seek Time First

# sstf(procesos2,ultima_ubicacion)

#|3| SCAN

# scan(ultima_ubicacion,procesos)


#|4| C-SCAN

# c_scan(ultima_ubicacion,procesos)

# print(procesos)
# pila(procesos)