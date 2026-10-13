import numpy as np
import time
import random
import os
from utils import (crea_barco_aleatorio,recibir_disparo,comprueba_coordenada_x,comprueba_coordenada_y\
                   ,menu,imprimir_tablero_color,crea_barco_aleatorio_j1)

def iniciar():

    menu_salida=menu()

    while menu_salida==1:

        tablero1=np.full((10,10),'~') #tablero de los barcos del jugador 1
        tablero2=np.full((10,10),'~') #tablero de los barcos del jugador 2
        tablero1_marcar=np.full((10,10),'~') #tablero del radar del tablero del jugador 2
        tablero2_marcar=np.full((10,10),'~') #tablero del radar del tablero del jugador 1

        dict_barcos_j1={"Destructor (size 2)":0, "Acorazado (size 3)":0, "Portaaviones (size 4)":0}
        dict_barcos_j2={"Destructor (size 2)":0, "Acorazado (size 3)":0, "Portaaviones (size 4)":0}

        jugador1=input("Introduce tu nombre, jugador 1: ")
        jugador2="Jugador 2"

        barcos_j1=[]
        barcos_j2=[]
        esloras=[2,2,2,3,3,4]

        # Creación barcos iniciales j1
        for i in esloras:
            tablero1,barco1=crea_barco_aleatorio_j1(tablero1,i,dict_barcos_j1,jugador1)
            barco_eslora=[i,barco1]
            barcos_j1.append(barco_eslora)
        time.sleep(3)
        #os.system("cls" if os.name == "nt" else "clear")

        # Creación barcos iniciales j2
        for i in esloras:
            tablero2,barco2=crea_barco_aleatorio(tablero2,i,dict_barcos_j2)
            barco_eslora=[i,barco2]
            barcos_j2.append(barco_eslora)

        #Lista con todas las coordenadas del tablero del jugador 2
        coordenadas_j2=[]
        for i in range(np.shape(tablero2)[0]):
            for j in range(np.shape(tablero2)[1]):
                coordenadas_j2.append((i,j))
    
        num_x_1=0
        num_x_2=0

        while True:
            print(f"""\n⚔️   TURNO DE {jugador1.upper()} ⚔️\n**********************""")
            x1=input(f"{jugador1}, introduce la coordenada x del barco que quieres derribar (numero del 1 al {tablero1.shape[0]}): ")
            x1=comprueba_coordenada_x(x1,jugador1,tablero1)
            if x1=="salir":
                print("Saliendo de la partida...")
                time.sleep(2)
                print("Partida cancelada\n")
                break
            x1=int(x1)
            y1=input(f"{jugador1}, introduce la coordenada y del barco que quieres derribar (numero del 1 al  {tablero1.shape[1]}): ")
            y1=comprueba_coordenada_y(y1,jugador1,tablero1)
            print("\n")
            if y1=="salir":
                print("Saliendo de la partida...")
                time.sleep(2)
                print("Partida cancelada\n")
                break
            y1=int(y1)
            disparo_j1=recibir_disparo(tablero2,(x1-1,y1-1),dict_barcos_j2,barcos_j2,jugador1)
    
            while disparo_j1==False and (tablero2[x1-1,y1-1]=="X" or tablero2[x1-1,y1-1]=="-"):
                x1=input(f"{jugador1}, introduce la coordenada x del barco que quieres derribar (numero del 1 al {tablero1.shape[0]}): ")
                x1=comprueba_coordenada_x(x1,jugador1,tablero1)
                print("\n")
                if x1=="salir":
                    break
                y1=input(f"{jugador1}, introduce la coordenada y del barco que quieres derribar (numero del 1 al {tablero1.shape[1]}): ")
                y1=comprueba_coordenada_y(y1,jugador1,tablero1)
                print("\n")
                if y1=="salir":
                    break
                if x1!="salir" or y1!="salir":
                    x1=int(x1)
                    y1=int(y1)
                    disparo_j1=recibir_disparo(tablero2,(x1-1,y1-1),dict_barcos_j2,barcos_j2,jugador1)
            if x1=="salir" or y1=="salir":
                print("Saliendo de la partida...")
                time.sleep(2)
                print("Partida cancelada\n")
                break

            x1=int(x1)
            y1=int(y1)
            if disparo_j1 and tablero2[(x1-1,y1-1)]=="X":
                num_x_1+=1
                tablero1_marcar[(x1-1,y1-1)]="X"
                                    
            if disparo_j1 and tablero2[(x1-1,y1-1)]=="-":
                tablero1_marcar[(x1-1,y1-1)]="-"
                    
            print(f"Puntos de {jugador1}: {num_x_1}")
            print("Radar del tablero del jugador 2:")
            imprimir_tablero_color(tablero1_marcar)

            if sum(dict_barcos_j2.values())==0:
                break

            

            time.sleep(2)


        
            print(f"""\n⚔️   TURNO DEL JUGADOR 2 ⚔️\n************************""")
            coordenada_j2=random.choice(coordenadas_j2)
            coordenadas_j2.remove(coordenada_j2)

            x2=coordenada_j2[0]
            y2=coordenada_j2[1]

            disparo_j2 = recibir_disparo(tablero1,(x2,y2),dict_barcos_j1,barcos_j1,jugador2)

            if disparo_j2 and tablero1[(x2,y2)]=="X":
                num_x_2+=1
                tablero2_marcar[(x2,y2)]="X"

            if disparo_j2 and tablero1[(x2,y2)]=="-":
                tablero2_marcar[(x2,y2)]="-"

            print(f"Puntos del jugador 2: {num_x_2}\n\n")

            if sum(dict_barcos_j1.values())==0:
                break

            time.sleep(3)
            #os.system("cls" if os.name == "nt" else "clear")
        
        
        if sum(dict_barcos_j2.values())==0:
            print(f"{jugador1} ha ganado\n")
        if sum(dict_barcos_j1.values())==0:
            print("Jugador 2 ha ganado\n")

        time.sleep(2)
        menu_salida=menu()

    if menu_salida==2:
        print("Saliendo del juego...\n")
        time.sleep(2)
        print("Juego finalizado")


if __name__ == "__main__":
    iniciar()








#coordenadas_j1=[]
# for i in range(np.shape(tablero1)[0]):
#     for j in range(np.shape(tablero1)[1]):
#         coordenadas_j1.append((i,j))


# CREACION BARCOS J1 PRUEBA
# for i in esloras:
#     tablero1,barco1=crea_barco_aleatorio(tablero1,i,dict_barcos_j1)
#     barco_eslora=[i,barco1]
#     barcos_j1.append(barco_eslora)



# #CODIGO JUGADOR 1 PRUEBA RAPIDA
# coordenada_j1=random.choice(coordenadas_j1)
# coordenadas_j1.remove(coordenada_j1)

# x1=coordenada_j1[0]
# y1=coordenada_j1[1]

# disparo_j1 = recibir_disparo(tablero2,(x1,y1),dict_barcos_j2,barcos_j2,jugador1)

# if disparo_j1 and tablero2[(x1,y1)]=="X":
#     num_x_1+=1
#     tablero1_marcar[(x1,y1)]="X"

# if disparo_j1 and tablero2[(x1,y1)]=="-":
#     tablero1_marcar[(x1,y1)]="-"

# print(f"Puntos del jugador 1: {num_x_1}\n\n")
# print("Radar del jugador 2:")
# imprimir_tablero_color(tablero1_marcar)

# if sum(dict_barcos_j2.values())==0:
#     break