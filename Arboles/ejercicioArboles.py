"""
Sistema de Benchmark para Estructuras de Datos
================================================
Compara el rendimiento de búsqueda entre tres estructuras:
  - Lista de Python (list)
  - Árbol Binario de Búsqueda (ABB)
  - Árbol B+

Se prueban dos escenarios:
  1. IDs en orden secuencial
  2. IDs en orden aleatorio
"""

import time
import random

# ─────────────────────────────────────────────────────────────────
#  GENERACIÓN DE DATOS
#
#  Genera una lista de 10,000 estudiantes como dicts.
#  - ordenado=True  → IDs del 1 al 10,000 en orden secuencial
#  - ordenado=False → mismos IDs pero en orden aleatorio (shuffle)
# ─────────────────────────────────────────────────────────────────
NOMBRES = [
    'Sofia','Valentina','Isabella','Camila','Daniela','Mariana','Alejandra',
    'Andrea','Natalia','Gabriela','Paula','Sara','Laura','Maria','Ana','Lucia',
    'Diana','Monica','Carolina','Paola','Santiago','Sebastian','Mateo','Samuel',
    'Nicolas','Alejandro','Juan','Carlos','Andres','David','Felipe','Jorge',
    'Luis','Miguel','Pablo','Ricardo','Fernando','Daniel','Jose','Cristian',
    'Valeria','Melissa','Juliana','Tatiana','Vanessa','Esteban','Mauricio',
    'Sergio','Gustavo','Eduardo','Diego','Tomas','Julian','Bryan','Kevin'
]

def generar_estudiantes(ordenado=True):
    """
    Retorna una lista de 10,000 dicts con la forma:
        {'id': int, 'nombre': str, 'edad': int, 'promedio': float}

    Si ordenado=True  los IDs van de 1 a 10,000 en secuencia.
    Si ordenado=False los mismos IDs se mezclan aleatoriamente.
    """
    ids = list(range(1, 10001))
    if not ordenado:
        random.shuffle(ids)

    return [
        {
            'id':       i,
            'nombre':   random.choice(NOMBRES),
            'edad':     random.randint(15, 25),
            'promedio': round(random.uniform(1.0, 5.0), 1)
        }
        for i in ids
    ]


# ─────────────────────────────────────────────────────────────────
#  LISTA DE PYTHON
#
#  Usa una lista nativa de Python.
#  - Inserción: O(1) — agrega al final.
#  - Búsqueda:  O(n) — recorre elemento por elemento.
# ─────────────────────────────────────────────────────────────────
class ListaPython:
    def __init__(self):
        self.datos = []

    def insertar(self, estudiante):
        self.datos.append(estudiante)

    def buscar(self, id_buscado):
        for e in self.datos:
            if e['id'] == id_buscado:
                return e
        return None


# ─────────────────────────────────────────────────────────────────
#  ÁRBOL BINARIO DE BÚSQUEDA (ABB)
#
#  Cada nodo tiene máximo dos hijos: menores a la izquierda,
#  mayores a la derecha.
#  - Inserción: O(log n) promedio, O(n) peor caso (datos ordenados).
#  - Búsqueda:  O(log n) promedio, O(n) peor caso.
#
#  NOTA: Con IDs secuenciales el árbol se degenera en una cadena
#  (todos los nodos hacia la derecha), haciendo la búsqueda O(n).
#  Por eso la inserción es iterativa: evita RecursionError con
#  los 10,000 niveles que tendría el árbol degenerado.
# ─────────────────────────────────────────────────────────────────
class NodoABB:
    def __init__(self, estudiante):
        self.estudiante = estudiante
        self.izq = None
        self.der = None

class ABB:
    def __init__(self):
        self.raiz = None

    def insertar(self, estudiante):
        nuevo = NodoABB(estudiante)
        if self.raiz is None:
            self.raiz = nuevo
            return
        nodo = self.raiz
        while True:
            if estudiante['id'] < nodo.estudiante['id']:
                if nodo.izq is None:
                    nodo.izq = nuevo; return
                nodo = nodo.izq
            else:
                if nodo.der is None:
                    nodo.der = nuevo; return
                nodo = nodo.der

    def buscar(self, id_buscado):
        """Recorre el árbol comparando en cada nodo hasta encontrar el ID."""
        nodo = self.raiz
        while nodo:
            if id_buscado == nodo.estudiante['id']:
                return nodo.estudiante
            nodo = nodo.izq if id_buscado < nodo.estudiante['id'] else nodo.der
        return None


# ─────────────────────────────────────────────────────────────────
#  ÁRBOL B+
#
#  Árbol balanceado de orden t. Todos los datos viven en las hojas,
#  que están enlazadas entre sí. Los nodos internos solo guardan
#  claves de navegación.
#  - Inserción: O(log n) garantizado (siempre balanceado).
#  - Búsqueda:  O(log n) garantizado.
#
#  Con t=50 cada nodo almacena entre 50 y 99 claves, reduciendo
#  la altura del árbol y manteniéndolo eficiente sin importar
#  el orden de inserción.
# ─────────────────────────────────────────────────────────────────
class NodoBPlus:
    def __init__(self, es_hoja=False):
        self.es_hoja   = es_hoja
        self.claves    = []    # IDs en hojas, claves de navegación en internos
        self.hijos     = []    # datos en hojas, nodos hijos en internos
        self.siguiente = None  # enlace al siguiente nodo hoja

class BPlus:
    def __init__(self, t=50):
        self.t    = t
        self.raiz = NodoBPlus(es_hoja=True)

    def insertar(self, estudiante):
        """Inserta dividiendo nodos cuando alcanzan su capacidad máxima (2t-1)."""
        clave = estudiante['id']
        if len(self.raiz.claves) == 2 * self.t - 1:
            nueva_raiz = NodoBPlus(es_hoja=False)
            nueva_raiz.hijos.append(self.raiz)
            self._dividir(nueva_raiz, 0)
            self.raiz = nueva_raiz
        self._insertar_no_lleno(self.raiz, clave, estudiante)

    def _dividir(self, padre, i):
        """Parte el i-ésimo hijo del padre en dos nodos."""
        t     = self.t
        hijo  = padre.hijos[i]
        nuevo = NodoBPlus(es_hoja=hijo.es_hoja)
        mid   = t - 1

        if hijo.es_hoja:
            # Las hojas copian la clave del medio al padre
            nuevo.claves    = hijo.claves[mid:]
            nuevo.hijos     = hijo.hijos[mid:]
            hijo.claves     = hijo.claves[:mid]
            hijo.hijos      = hijo.hijos[:mid]
            nuevo.siguiente = hijo.siguiente
            hijo.siguiente  = nuevo
            padre.claves.insert(i, nuevo.claves[0])
        else:
            # Los nodos internos suben la clave del medio al padre
            nuevo.claves = hijo.claves[mid + 1:]
            nuevo.hijos  = hijo.hijos[mid + 1:]
            clave_subir  = hijo.claves[mid]
            hijo.claves  = hijo.claves[:mid]
            hijo.hijos   = hijo.hijos[:mid + 1]
            padre.claves.insert(i, clave_subir)

        padre.hijos.insert(i + 1, nuevo)

    def _insertar_no_lleno(self, nodo, clave, estudiante):
        """Desciende hasta la hoja correcta e inserta en orden."""
        if nodo.es_hoja:
            i = 0
            while i < len(nodo.claves) and clave > nodo.claves[i]:
                i += 1
            nodo.claves.insert(i, clave)
            nodo.hijos.insert(i, estudiante)
        else:
            i = len(nodo.claves) - 1
            while i >= 0 and clave < nodo.claves[i]:
                i -= 1
            i += 1
            if len(nodo.hijos[i].claves) == 2 * self.t - 1:
                self._dividir(nodo, i)
                if clave >= nodo.claves[i]:
                    i += 1
            self._insertar_no_lleno(nodo.hijos[i], clave, estudiante)

    def buscar(self, id_buscado):
        """Navega por nodos internos hasta llegar a la hoja y busca allí."""
        nodo = self.raiz
        while not nodo.es_hoja:
            i = 0
            while i < len(nodo.claves) and id_buscado >= nodo.claves[i]:
                i += 1
            nodo = nodo.hijos[i]
        for i, k in enumerate(nodo.claves):
            if k == id_buscado:
                return nodo.hijos[i]
        return None


# ─────────────────────────────────────────────────────────────────
#  CONSTRUCCIÓN
# ─────────────────────────────────────────────────────────────────
def construir_estructuras(estudiantes):
    """Inserta la misma lista de estudiantes en las tres estructuras."""
    lista = ListaPython()
    abb   = ABB()
    bplus = BPlus(t=50)
    for e in estudiantes:
        lista.insertar(e)
        abb.insertar(e)
        bplus.insertar(e)
    return lista, abb, bplus


# ─────────────────────────────────────────────────────────────────
#  BENCHMARK
# ─────────────────────────────────────────────────────────────────
def benchmark(lista, abb, bplus, n, etiqueta):
    """
    Realiza n búsquedas sobre IDs aleatorios y muestra el tiempo
    total de cada estructura.
    """
    ids = random.sample(range(1, 10001), n)

    t0  = time.perf_counter()
    for i in ids: lista.buscar(i)
    t_l = time.perf_counter() - t0

    t0  = time.perf_counter()
    for i in ids: abb.buscar(i)
    t_a = time.perf_counter() - t0

    t0  = time.perf_counter()
    for i in ids: bplus.buscar(i)
    t_b = time.perf_counter() - t0

    print(f"\n{'─'*42}")
    print(f"  {etiqueta} ({n} búsquedas)")
    print(f"{'─'*42}")
    print(f"  Lista : {t_l:.6f} segundos")
    print(f"  ABB   : {t_a:.6f} segundos")
    print(f"  B+    : {t_b:.6f} segundos")
    print(f"{'─'*42}")


# ─────────────────────────────────────────────────────────────────
#  MAIN
# ─────────────────────────────────────────────────────────────────
if __name__ == '__main__':
    random.seed(10000)

    # Generar datos directamente en memoria
    print("\nGenerando estudiantes con IDs ordenados...")
    est_ord  = generar_estudiantes(ordenado=True)
    print("Generando estudiantes con IDs aleatorios...")
    est_rand = generar_estudiantes(ordenado=False)
    print(f"  {len(est_ord)} estudiantes por conjunto.")

    # Construir las tres estructuras para cada conjunto
    print("\nConstruyendo estructuras con IDs ordenados...")
    lista_o, abb_o, bplus_o = construir_estructuras(est_ord)
    print("Construyendo estructuras con IDs aleatorios...")
    lista_r, abb_r, bplus_r = construir_estructuras(est_rand)
    print("  ✓ Listo.\n")

    # ── 100 búsquedas ──
    benchmark(lista_o, abb_o, bplus_o, 100,  "IDs ordenados  ")
    benchmark(lista_r, abb_r, bplus_r, 100,  "IDs aleatorios ")
    input("\n  Presiona Enter para continuar...")

    # ── 1000 búsquedas ──
    benchmark(lista_o, abb_o, bplus_o, 1000, "IDs ordenados  ")
    benchmark(lista_r, abb_r, bplus_r, 1000, "IDs aleatorios ")
    input("\n  Presiona Enter para continuar...")

    # ── 2000 búsquedas ──
    benchmark(lista_o, abb_o, bplus_o, 2000, "IDs ordenados  ")
    benchmark(lista_r, abb_r, bplus_r, 2000, "IDs aleatorios ")
    input("\n  Presiona Enter para continuar...")

    # ── 4000 búsquedas ──
    benchmark(lista_o, abb_o, bplus_o, 4000, "IDs ordenados  ")
    benchmark(lista_r, abb_r, bplus_r, 4000, "IDs aleatorios ")
    input("\n  Presiona Enter para finalizar...")
