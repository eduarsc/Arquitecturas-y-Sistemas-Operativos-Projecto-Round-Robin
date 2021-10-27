# author: eduars-elizalde
# materia: Arquitectura y Sistemas Operativos
# carrera: Tecnicatura Universitaria en Programación

# El objetivo de este pequeño programa es demostrar de
# forma didactica el proceso de planificación round robin
# aplicado al manejo de procesos en un sistema operativo

from random import randrange
from os import system
from platform import system as sy
from copy import deepcopy
from timeit import timeit



# funcion que limpia la consola
# segun el sistema operativo en
# el que este

def clear_screen():
    if sy() == "Windows":
        system("cls")
    else:
        system("clear")

# funcion que imprime una lista y cada 3
# elementos baja una linea

def imprimir_lista(lista, elems_count = 3):
    cont = 0 # contador de elementos dentro de la lista
    for elem in lista:
        if cont % elems_count == 0: # cada 3 elementos hace un bajo de linea
            print()
        print(elem, end="\t")
        cont += 1

# funcion que muestra por pantalla el titulo del proyecto
# ademas de el tamaño del quamtum y la cantidad de procesos
# a ejecutar
# incluye la lista de procesos original


def banner_grupo_10(process_list, quamtum):
    print("===================================================================")
    print("\t\tGrupo 10 - Planificaciónn Round Robin")
    print("\t\t\tCalvete - Elizalde           ")
    print("===================================================================")
    print(f"\t\tquatum:{quamtum} [ut]\tn° de procesos:{len(process_list)}")
    print("===================================================================")
    imprimir_lista(process_list)
    print("\n===================================================================")


'''
    Algortimo Round Robin
    
    Todos llegan en tiempo 0 // todos tiene la misma prioridad

    A cada proceso se le asigna un intervalo de tiempo llamado Quamtum "q"

    Cada proceso se ejecuta durante este "q"

    Cuanddo un proceso se recibe en la CPU pueden ocurrir 2 cosas:
	
        El proceso tiene una "rafaga" de Cpu <= "q" entonces el
        proceso termina antes de "q" y se planifica un nuevo
        proceso.
	    
        El proceso tiene un "rafaga" de Cpu > "q" entonces el
        proceso se agota el "q" y el proceso es expulsado de
        la Cpu dando paso a un nuevo proceso. EL mismo sera
        puesto al final de la cola.
	
'''


def round_robin(process_list, quamtum):
    context_change = 0
    last_process = "" 
    
        
    origin_list = deepcopy(process_list)    # deepcopy para evitar referenciamiento cruzados 
    
    list_process_processed = [] # lista de procesos terminado
    
    quamtum_counter = 0 # contador de quamtums
    
    while process_list != []: # mientras la lista de procesos no este vacia
        clear_screen()
        banner_grupo_10(origin_list, quamtum)

        # siempre recuperamos el primer elemento de la lista( comportamiento cola o FIFO)
        process_actual = process_list[0]
        
        quamtum_counter += abs(process_actual[1]) if process_actual[1] - quamtum <= 0 else quamtum
        
        list_process_processed.append([process_actual[0], quamtum_counter])

        print(f"entro en el cpu el {process_actual[0]} con una rafaga de {process_actual[1]} [ut]")
        
        if (process_actual[1] - quamtum) <= 0:
            print(f"\n{process_actual[0]} finalizado")
            process_list.pop(0) # sacamos el primer elemento pues ya fue finalizado
        else:
            print(
                f"\nno se termino el {process_actual[0]}\nrestan {process_actual[1] - quamtum} [ut]\nse coloca el proceso al final de la cola\nse continua con el siguiente proceso")
            process_actual[1] -= quamtum
            process_list.append(process_list.pop(0))  # el primer elemento lo colocamos al final, luego lo eliminamos del principio
            
        
        context_change += 0 if last_process == process_actual[0] else 1  # revisar aqui
        last_process = process_actual[0]
        
        if process_list != []:
            print("Procesos en cola")
            imprimir_lista(process_list)
        
        print()
        
        if list_process_processed != []:
            print("\n[proceso finalizado: quamtum utilizado]")
            imprimir_lista(list_process_processed)
            print()
        
        print(f"cambios de contexto {context_change-1}")
        
        input("presione enter para continuar")
        clear_screen()
    
    print("Procesos finalizado")
    return None

# funcion que dado la cantidad de procesos y el quamtum
# genera al azar para cada proceso una cantidad aleatoria
# de ragafas de cpu necesarias para terminar el proceso
# se calculan de manera arbitrarias


def generador_procesos(quamtum, process_number):
    """this function simulate a list of process with id and his rafaga

    Args:
        quamtum (int): unit of time generic (ut)
        process_number (int): number of process to simulate

    Returns:
        list: list with process_number
    """    
    process_rafaga = [randrange(5, 20) for i in range(1, process_number+1)]
    process_list_id = ["proceso "+str(i) for i in range(1, process_number+1)]
    process_list = list(zip(process_list_id, process_rafaga))
    process_list = [[process_[0], process_[1]] for process_ in process_list]
    return process_list



def main():
    clear_screen()
    '''
        Nota: 
        quamtums muy grandes, mala respuesta a peticiones interactivas cortas
        quamtums muy pequeñps, demasiadas conmutaciones, reduce eficiencia del CPU
    '''

    quamtum = int(input("tamaño en ut del quamtum: "))
    
    process_number = int(input("Numero de procesos en cola: "))  # numero de procesos en la cola de ejecución

    process_list = generador_procesos(quamtum, process_number)  # se genera la cola de procesos con sus id y rafagas respectivamente
                                                                # se muestra el titulo del proyecto
                                                                # y la cola original
    banner_grupo_10(process_list, quamtum)

    input("presione enter para continuar")
    
    round_robin(process_list, quamtum) # llamada a funcion que realiza el algoritmo principal

if __name__ == '__main__':
    main()
