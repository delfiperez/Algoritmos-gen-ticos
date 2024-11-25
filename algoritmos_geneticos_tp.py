'''
Condiciones
~~~~~~~~~~~
1. Hay 5 casas.
2. El Matematico vive en la casa roja.
3. El hacker programa en Python.
4. El Brackets es utilizado en la casa verde.
5. El analista usa Atom.
6. La casa verde esta a la derecha de la casa blanca.
7. La persona que usa Redis programa en Java
8. Cassandra es utilizado en la casa amarilla
9. Notepad++ es usado en la casa del medio.
10. El Desarrollador vive en la primer casa.
11. La persona que usa HBase vive al lado de la que programa en JavaScript.
12. La persona que usa Cassandra es vecina de la que programa en C#.
13. La persona que usa Neo4J usa Sublime Text.
14. El Ingeniero usa MongoDB.
15. EL desarrollador vive en la casa azul.

Quien usa vim?


Resumen:
Colores = Rojo, Azul, Verde, Blanco, Amarillo
Profesiones = Matematico, Hacker, Ingeniero, Analista, Desarrollador
Lenguaje = Python, C#, JAVA, C++, JavaScript
BD = Cassandra, MongoDB, Neo4j, Redis, HBase
editor = Brackets, Sublime Text, Atom, Notepad++, Vim
'''

import random
import copy

# Constantes del problema
casas = 5
atributos = ['Profesion', 'Color', 'Lenguaje', 'Database', 'Editor']

# Atributos posibles para cada casa
PROFESION = ['Matemático', 'Hacker', 'Desarrollador', 'Analista', 'Ingeniero']
COLOR = ['Roja', 'Verde', 'Blanca', 'Amarilla', 'Azul']
LENGUAJE = ['Python', 'C#', 'Java', 'C++', 'JavaScript']
DATABASE = ['Cassandra', 'MongoDB', 'HBase', 'Neo4J', 'Redis']
EDITOR = ['Brackets', 'Sublime Text', 'Atom', 'Notepad++', 'Vim']

# Generar un individuo aleatorio
def generar_individuo():
    #Mezcla los atributos aleatoriamente
    random.shuffle(COLOR)
    random.shuffle(PROFESION)
    random.shuffle(LENGUAJE)
    random.shuffle(DATABASE)
    random.shuffle(EDITOR)
    
    # Crea una lista de diccionarios, cada uno representando una casa con sus atributos
    individuo = [{"Color": COLOR[i], "Profesion": PROFESION[i], "Lenguaje": LENGUAJE[i],
                  "Database": DATABASE[i], "Editor": EDITOR[i]} for i in range(casas)]
    
    #Devuelve la lista de casas generada y la aptitud calculada para ese individuo 
    return {"casas": individuo, "aptitud": evaluar_aptitud(individuo)}

# Evaluar la aptitud de un individuo
def evaluar_aptitud(individuo):
    aptitud = 0

    # Restricciones (se evalúan en base al enunciado)
    for i, casa in enumerate(individuo):
        if casa["Profesion"] == "Matemático" and casa["Color"] == "Roja":
            aptitud += 1
        if casa["Profesion"] == "Hacker" and casa["Lenguaje"] == "Python":
            aptitud += 1
        if casa["Editor"] == "Brackets" and casa["Color"] == "Verde":
            aptitud += 1
        if casa["Profesion"] == "Analista" and casa["Editor"] == "Atom":
            aptitud += 1
        if i > 0 and casa["Color"] == "Verde" and individuo[i - 1]["Color"] == "Blanca":
            aptitud += 1
        if casa["Database"] == "Redis" and casa["Lenguaje"] == "Java":
            aptitud += 1
        if casa["Database"] == "Cassandra" and casa["Color"] == "Amarilla":
            aptitud += 1
        if i == 2 and casa["Editor"] == "Notepad++":
            aptitud += 1
        if i == 0 and casa["Profesion"] == "Desarrollador":
            aptitud += 1
        if casa["Database"] == "HBase" and (
            (i > 0 and individuo[i - 1]["Lenguaje"] == "JavaScript") or
            (i < len(individuo) - 1 and individuo[i + 1]["Lenguaje"] == "JavaScript")):
            aptitud += 1
        if casa["Database"] == "Cassandra" and (
            (i > 0 and individuo[i - 1]["Lenguaje"] == "C#") or
            (i < len(individuo) - 1 and individuo[i + 1]["Lenguaje"] == "C#")):
            aptitud += 1
        if casa["Database"] == "Neo4J" and casa["Editor"] == "Sublime Text":
            aptitud += 1
        if casa["Profesion"] == "Ingeniero" and casa["Database"] == "MongoDB":
            aptitud += 1
        if casa["Profesion"] == "Desarrollador" and casa["Color"] == "Azul":
            aptitud += 1

    return aptitud

# Seleccionar padres mediante torneo
def seleccionar_padres(poblacion):
    tamano_torneo = 5 #individuos que compiten 
    torneo = random.sample(poblacion, tamano_torneo) #Selecciona tamano_torneo individuos de la población
    return max(torneo, key=lambda x: x['aptitud']) # Retorna el individuo con mayor aptitud

# Cruce de dos padres
def cruce(padre1, padre2):
    punto_cruce = random.randint(1, casas - 2) # Selecciona un punto de cruce aleatorio 
    hijo = padre1["casas"][:punto_cruce] + padre2["casas"][punto_cruce:]  # Combina las casas de los padres en base al punto de cruce
    return {"casas": hijo, "aptitud": evaluar_aptitud(hijo)} #Retorna el hijo 

# Mutación de un individuo
def mutar(individuo):
    individuo_mutado = copy.deepcopy(individuo) #copia del individuo
    casa_idx = random.randint(0, casas - 1) #selecciona casa
    atributo1, atributo2 = random.sample(atributos, 2) #selecciona dos atributos al azar
    casa = individuo_mutado["casas"][casa_idx] #se accede a la casa
    casa[atributo1], casa[atributo2] = casa[atributo2], casa[atributo1] #se intercambian los atributos
    individuo_mutado["aptitud"] = evaluar_aptitud(individuo_mutado["casas"]) #se valua la aptitud
    return individuo_mutado if individuo_mutado["aptitud"] >= individuo["aptitud"] else individuo
# Devuelve el individuo producto de la mutación si la aptitud de este es mejor que la del individuo original

# Algoritmo genético
def algoritmo_genetico():
    tamano_poblacion = 3000 #definir tamaño de la población
    maximo_generaciones = 50 #definir núm máximo de generaciones
    max_aptitud = 14  # Máxima aptitud posible (todas las restricciones cumplidas)

    # Generar población inicial
    poblacion = [generar_individuo() for _ in range(tamano_poblacion)]

    for generacion in range(maximo_generaciones):
        for individuo in poblacion:
            individuo['aptitud'] = evaluar_aptitud(individuo["casas"]) #evalua la aptitud de cada ind. de la población
        
        mejor_individuo = max(poblacion, key=lambda x: x['aptitud']) #encontrar el mejor individuo

        print(f"Generación {generacion}: Mejor aptitud = {mejor_individuo['aptitud']}")
        #Para cada generación, señala el individuo con mayor aptitud. 

        if mejor_individuo['aptitud'] == max_aptitud:
            return mejor_individuo
        #si la aptitud del mejor individuo es la misma que la que se asigna a max, devolverlo

        # Crear nueva generación
        nueva_poblacion = []
        while len(nueva_poblacion) < tamano_poblacion:
            padre1 = seleccionar_padres(poblacion)
            padre2 = seleccionar_padres(poblacion)
            hijo = cruce(padre1, padre2)
            hijo = mutar(hijo)
            nueva_poblacion.append(hijo)

        poblacion = nueva_poblacion

    return None

# Resolver el problema
solucion_final = algoritmo_genetico()

if solucion_final:
    # Verificar si existe alguna casa con Editor "Vim"
    usuario_vim = next((casa["Profesion"] for casa in solucion_final["casas"] if casa["Editor"] == "Vim"), None)
    if usuario_vim:
        print(f"El usuario que utiliza Vim es {usuario_vim}.")
    else:
        print("No se encontró ningún usuario que utilice Vim en la solución.")
else:
    print("No se encontró una solución al problema propuesto.")

print(solucion_final)
