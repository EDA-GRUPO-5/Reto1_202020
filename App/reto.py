"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad de Los Andes
 * 
 * Contribución de:
 *
 * Cristian Camilo Castellanos
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 """

"""
  Este módulo es una aplicación básica con un menú de opciones para cargar datos, contar elementos, y hacer búsquedas sobre una lista .
"""

import config as cf
import sys
import csv
from ADT import list as lt
from DataStructures import listiterator as it
from DataStructures import liststructure as lt

from Sorting.insertionsort import insertionSort 
from Test.sorting.less_greater import less_count
from Test.sorting.less_greater import greater_count
from Test.sorting.less_greater import less_average
from Test.sorting.less_greater import greater_average

from time import process_time 

def printMenu():
    """
    Imprime el menu de opciones
    """
    print("\nBienvenido")
    print("1- Cargar Datos")
    print("2- Ranking de peliculas")
    print("3- Conocer un director")
    print("4- Conocer un actor")
    print("5- Entender un genero")
    print("6- Crear ranking")
    print("0- Salir")

def loadCSVFile (file, sep=";"): #Cargar Datos
    
    lst = lt.newList("ARRAY_LIST") #Usando implementacion arraylist
    print("Cargando archivo ....")
    t1_start = process_time() #tiempo inicial
    dialect = csv.excel()
    dialect.delimiter=sep
    try:
        with open(file, encoding="utf-8") as csvfile:
            spamreader = csv.DictReader(csvfile, dialect=dialect)
            for row in spamreader: 
                lt.addLast(lst,row)
    except:
        print("Hubo un error con la carga del archivo")
    t1_stop = process_time() #tiempo final
    print("Tiempo de ejecución ",t1_stop-t1_start," segundos")
    return lst

def RankingPeliculas(lst, num_peliculas, mejor_peor, criterio): #Ranking de peliculas
    
    lista_nueva=[]
    if criterio.lower()=="count":
        t1_start = process_time()
        if mejor_peor.lower()=="peor":
            insertionSort(lst,less_count)
        else:
            insertionSort(lst, greater_count)
        for peliculas in lst["elements"]:
            if len(lista_nueva)<num_peliculas:
                lista_nueva.append((peliculas["original_title"],peliculas["vote_count"]))
        t1_stop = process_time()
        print("Tiempo de ejecución ",t1_stop-t1_start," segundos")
    else:
        t1_start = process_time()
        if mejor_peor.lower()=="peor":
            insertionSort(lst,less_average)
        else:
            insertionSort(lst, greater_average)
        for peliculas in lst["elements"]:
            if len(lista_nueva)<num_peliculas:
                lista_nueva.append((peliculas["original_title"],peliculas["vote_average"]))
        t1_stop = process_time()
        print("Tiempo de ejecución ",t1_stop-t1_start," segundos")
    return lista_nueva

def ConocerDirector(criteria, column, lst, lst2): #Conocer un director
    
    lista_id=[]
    if lst['size']==0:
        print("La lista esta vacía")  
        return 0
    else:
        t1_start = process_time() #tiempo inicial
        counter=0
        iterator = it.newIterator(lst)
        while  it.hasNext(iterator):
            element = it.next(iterator)
            if criteria.lower() in element["director_name"].lower():
                counter+=1
                lista_id.append((element["id"]))
        lista_peliculas=[]
        lista_promedio = []
        iterator = it.newIterator(lst2)
        while  it.hasNext(iterator):
            element = it.next(iterator)
            if element["id"] in lista_id:
                lista_peliculas.append(element["original_title"])
                lista_promedio.append(element["vote_average"])
        lista_promedio1 = map(float,lista_promedio)
        promedio_final = sum(lista_promedio1)/len(lista_promedio)
        t1_stop = process_time() #tiempo final
    print("Tiempo de ejecución ",t1_stop-t1_start," segundos")
    return lista_peliculas, counter, promedio_final

def ConocerActor(lst1, lst2, ActorName):
    An = ActorName.lower()
    if lst1['size'] == 0 or lst2['size'] == 0:
        print("La lista esta vacía")  
        return 0
    else:
        t1_start = process_time() #tiempo inicial

        ListaPeli = []
        ListaPeliculas = []
        ListaDirectores = []
        PromPeliculas = []
        DirectorColaboraciones = ""

        iterator = it.newIterator(lst2)
        while  it.hasNext(iterator):
            element = it.next(iterator)
            if An in (element["actor1_name"].lower(), element["actor2_name"].lower(), element["actor3_name"].lower(), element["actor4_name"].lower(), element["actor5_name"].lower()):
                ListaPeli.append(element["id"])
                ListaDirectores.append(element["director_name"])

        x = len(ListaPeli)
        DirectorColaboraciones = max(set(ListaDirectores), key=ListaDirectores.count)
        
        iterator2 = it.newIterator(lst1)
        while  it.hasNext(iterator2):
            element = it.next(iterator2)
            if element["id"] in ListaPeli:
                ListaPeliculas.append(element["original_title"])
                PromPeliculas.append(float(element["vote_average"]))

        PromedioP = sum(PromPeliculas)/x
        t1_stop = process_time() #tiempo final

        print("Tiempo de ejecución ",t1_stop-t1_start," segundos")

    return (ListaPeliculas, PromedioP, DirectorColaboraciones, x)
        
def EntenderGenero(lst, genero): #Entender un genero
    
    lista_peliculas=[]
    lista_votos=[]
    t1_start = process_time()
    for peliculas in lst["elements"]:
        if genero.lower() in peliculas["genres"].lower():
            lista_peliculas.append(peliculas["original_title"])
            lista_votos.append(int(peliculas["vote_count"]))
    total_votos=0
    for votos in lista_votos:
        total_votos+=votos
    promedio=total_votos/len(lista_votos)
    lista_final=[len(lista_peliculas), lista_peliculas, promedio]
    t1_stop = process_time()
    print(lista_votos)
    print("Tiempo de ejecución ",t1_stop-t1_start," segundos")
    return lista_final
   
def CrearRanking (lst, num_peliculas, mejor_peor, criterio, genero): #Crear ranking

    lista_nueva=[]
    if genero.lower in lst["genres"]:
        if criterio.lower()=="count":
            t1_start = process_time()
            if mejor_peor.lower()=="peor":
               insertionSort(lst,less_count)
            else:
                insertionSort(lst, greater_count)
            for peliculas in lst["elements"]:
                if len(lista_nueva)<num_peliculas:
                    lista_nueva.append((peliculas["original_title"],peliculas["vote_count"]))
            t1_stop = process_time()
            print("Tiempo de ejecución ",t1_stop-t1_start," segundos")
        else:
            t1_start = process_time()
            if mejor_peor.lower()=="peor":
                insertionSort(lst,less_average)
            else:
                insertionSort(lst, greater_average)
            for peliculas in lst["elements"]:
                if len(lista_nueva)<num_peliculas:
                    lista_nueva.append((peliculas["original_title"],peliculas["vote_average"]))
            t1_stop = process_time()
            print("Tiempo de ejecución ",t1_stop-t1_start," segundos")
    return lista_nueva

def main():
    
    lista = lt.newList()   # se require usar lista definida
    lista2 = []
    while True:
        printMenu() #imprimir el menu de opciones en consola
        inputs =input('Seleccione una opción para continuar\n') #leer opción ingresada
        if len(inputs)>0:
            if int(inputs[0])==1: #opcion 1
                lista = loadCSVFile("Data/themoviesdb/SmallMoviesDetailsCleaned.csv")
                print("Datos cargados:",lista['size'],"elementos cargados")

            elif int(inputs[0])==2: #opcion 2
                if lista==None or lista['size']==0:
                    print("La lista está vacía")
                else:
                    num_peliculas=int(input("Ingrese el número de películas para su ranking\n"))
                    if num_peliculas<10:
                        print("El número de películas debe ser 10 o más")
                    else:
                        mejor_peor=input("Ingrese si desea su ranking de MEJOR o PEOR\n")
                        criteria = input("Ingrese el criterio COUNT o AVERAGE\n")
                        lista_nueva=RankingPeliculas(lista,num_peliculas,mejor_peor,criteria)
                        print("Su lista ordernada es:",lista_nueva)
                        
            elif int(inputs[0])==3: #opcion 3
                if lista==None or lista['size']==0:
                    print("La lista está vacía")
                else:
                    lista = loadCSVFile("Data/themoviesdb/MoviesCastingRaw-small.csv")
                    lista2 = loadCSVFile("Data/themoviesdb/SmallMoviesDetailsCleaned.csv")
                    criteria =input('Ingrese el criterio de búsqueda\n')
                    counter=ConocerDirector(criteria,0,lista, lista2)
                    print("Lista, numero y promedio de peliculas de", criteria,"\n",counter)

            elif int(inputs[0])==4: #opcion 4
                if lista==None or lista['size']==0:
                    print("La lista está vacía")
                else:
                    lista2 = loadCSVFile("Data/themoviesdb/MoviesCastingRaw-small.csv")
                    NombreActor = input("Ingrese el nombre del actor del cual quiere conocer\n")
                    rtaLP, rtaPP, rtaDC, rtaLen = ConocerActor(lista, lista2, NombreActor)
                    print(f"El actor {NombreActor} ha participado en {rtaLen} peliculas y son {rtaLP}\nCon un promedio de {rtaPP} y el director con el que mas ha colaborado es {rtaDC}")

            elif int(inputs[0])==5: #opcion 5
                if lista==None or lista["size"]==0:
                    print("La lista está vacía")
                else:
                    genero=input("Ingrese el género a consultar\n")
                    lista_final=EntenderGenero(lista,genero)
                    print("La cantidad de películas del género", genero,"es:", lista_final[0], ", los nombres de las películas son:", lista_final[1], "y el promedio de votos es:", lista_final[2])

            elif int(inputs[0])==6: #opcion 6
                if lista==None or lista['size']==0:
                    print("La lista está vacía")
                else:
                    num_peliculas=int(input("Ingrese el número de películas para su ranking\n"))
                    if num_peliculas<10:
                        print("El número de películas debe ser 10 o más")
                    else:
                        genero = input("Ingrese el genero de su interes\n")
                        mejor_peor=input("Ingrese si desea su ranking de MEJOR o PEOR\n")
                        criteria = input("Ingrese el criterio COUNT o AVERAGE\n")
                        lista_nueva=CrearRanking(lista,num_peliculas,mejor_peor,criteria, genero)
                        print("Su lista ordernada es:",lista_nueva)

            elif int(inputs[0])==0: #opcion 0, salir
                sys.exit(0)
                
if __name__ == "__main__":
    main()
