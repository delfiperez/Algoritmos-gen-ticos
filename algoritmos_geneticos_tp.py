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
    random.shuffle(COLOR)
    random.shuffle(PROFESION)
    random.shuffle(LENGUAJE)
    random.shuffle(DATABASE)
    random.shuffle(EDITOR)
    
    individuo = [{"Color": COLOR[i], "Profesion": PROFESION[i], "Lenguaje": LENGUAJE[i],
                  "Database": DATABASE[i], "Editor": EDITOR[i]} for i in range(casas)]
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
    tamano_torneo = 5
    torneo = random.sample(poblacion, tamano_torneo)
    return max(torneo, key=lambda x: x['aptitud'])

# Cruce de dos padres
def cruce(padre1, padre2):
    punto_cruce = random.randint(1, casas - 2)
    hijo = padre1["casas"][:punto_cruce] + padre2["casas"][punto_cruce:]
    return {"casas": hijo, "aptitud": evaluar_aptitud(hijo)}

# Mutación de un individuo
def mutar(individuo):
    individuo_mutado = copy.deepcopy(individuo)
    casa_idx = random.randint(0, casas - 1)
    atributo1, atributo2 = random.sample(atributos, 2)
    casa = individuo_mutado["casas"][casa_idx]
    casa[atributo1], casa[atributo2] = casa[atributo2], casa[atributo1]
    individuo_mutado["aptitud"] = evaluar_aptitud(individuo_mutado["casas"])
    return individuo_mutado if individuo_mutado["aptitud"] >= individuo["aptitud"] else individuo

# Algoritmo genético
def algoritmo_genetico():
    tamano_poblacion = 3000
    maximo_generaciones = 50
    max_aptitud = 14  # Máxima aptitud posible (todas las restricciones cumplidas)

    # Generar población inicial
    poblacion = [generar_individuo() for _ in range(tamano_poblacion)]

    for generacion in range(maximo_generaciones):
        for individuo in poblacion:
            individuo['aptitud'] = evaluar_aptitud(individuo["casas"])
        
        mejor_individuo = max(poblacion, key=lambda x: x['aptitud'])

        print(f"Generación {generacion}: Mejor aptitud = {mejor_individuo['aptitud']}")

        if mejor_individuo['aptitud'] == max_aptitud:
            return mejor_individuo

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
