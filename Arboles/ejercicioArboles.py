import csv
import time
import random
import sys
sys.setrecursionlimit(20000)

# ══════════════════════════════════════════
#  1. LISTA DE PYTHON (list)
# ══════════════════════════════════════════
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

    def listar_ordenado(self):
        return sorted(self.datos, key=lambda e: e['id'])


# ══════════════════════════════════════════
#  2. ÁRBOL BINARIO DE BÚSQUEDA (ABB)
# ══════════════════════════════════════════
class NodoABB:
    def __init__(self, estudiante):
        self.estudiante = estudiante
        self.izq = None
        self.der = None

class ABB:
    def __init__(self):
        self.raiz = None

    def insertar(self, estudiante):
        self.raiz = self._insertar(self.raiz, estudiante)

    def _insertar(self, nodo, estudiante):
        if nodo is None:
            return NodoABB(estudiante)
        if estudiante['id'] < nodo.estudiante['id']:
            nodo.izq = self._insertar(nodo.izq, estudiante)
        elif estudiante['id'] > nodo.estudiante['id']:
            nodo.der = self._insertar(nodo.der, estudiante)
        return nodo

    def buscar(self, id_buscado):
        return self._buscar(self.raiz, id_buscado)

    def _buscar(self, nodo, id_buscado):
        if nodo is None:
            return None
        if id_buscado == nodo.estudiante['id']:
            return nodo.estudiante
        if id_buscado < nodo.estudiante['id']:
            return self._buscar(nodo.izq, id_buscado)
        return self._buscar(nodo.der, id_buscado)

    def listar_ordenado(self):
        resultado = []
        self._inorden(self.raiz, resultado)
        return resultado

    def _inorden(self, nodo, resultado):
        if nodo:
            self._inorden(nodo.izq, resultado)
            resultado.append(nodo.estudiante)
            self._inorden(nodo.der, resultado)


# ══════════════════════════════════════════
#  3. ÁRBOL B+ (orden t=50)
# ══════════════════════════════════════════
class NodoBPlus:
    def __init__(self, es_hoja=False):
        self.es_hoja = es_hoja
        self.claves = []
        self.hijos = []
        self.siguiente = None

class BPlus:
    def __init__(self, t=50):
        self.t = t
        self.raiz = NodoBPlus(es_hoja=True)

    def insertar(self, estudiante):
        clave = estudiante['id']
        if len(self.raiz.claves) == 2 * self.t - 1:
            nueva_raiz = NodoBPlus(es_hoja=False)
            nueva_raiz.hijos.append(self.raiz)
            self._dividir(nueva_raiz, 0)
            self.raiz = nueva_raiz
        self._insertar_no_lleno(self.raiz, clave, estudiante)

    def _dividir(self, padre, i):
        t = self.t
        hijo = padre.hijos[i]
        nuevo = NodoBPlus(es_hoja=hijo.es_hoja)
        mid = t - 1
        if hijo.es_hoja:
            nuevo.claves = hijo.claves[mid:]
            nuevo.hijos = hijo.hijos[mid:]
            hijo.claves = hijo.claves[:mid]
            hijo.hijos = hijo.hijos[:mid]
            nuevo.siguiente = hijo.siguiente
            hijo.siguiente = nuevo
            padre.claves.insert(i, nuevo.claves[0])
        else:
            nuevo.claves = hijo.claves[mid + 1:]
            nuevo.hijos = hijo.hijos[mid + 1:]
            clave_subir = hijo.claves[mid]
            hijo.claves = hijo.claves[:mid]
            hijo.hijos = hijo.hijos[:mid + 1]
            padre.claves.insert(i, clave_subir)
        padre.hijos.insert(i + 1, nuevo)

    def _insertar_no_lleno(self, nodo, clave, estudiante):
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
        return self._buscar(self.raiz, id_buscado)

    def _buscar(self, nodo, clave):
        if nodo.es_hoja:
            for i, k in enumerate(nodo.claves):
                if k == clave:
                    return nodo.hijos[i]
            return None
        i = 0
        while i < len(nodo.claves) and clave >= nodo.claves[i]:
            i += 1
        return self._buscar(nodo.hijos[i], clave)

    def listar_ordenado(self):
        resultado = []
        nodo = self.raiz
        while not nodo.es_hoja:
            nodo = nodo.hijos[0]
        while nodo:
            resultado.extend(nodo.hijos)
            nodo = nodo.siguiente
        return resultado


# ─────────────────────────────────────────
#  CARGA Y CONSTRUCCIÓN
# ─────────────────────────────────────────
def cargar_csv(ruta):
    estudiantes = []
    with open(ruta, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            estudiantes.append({
                'id':       int(row['ID']),
                'nombre':   row['Nombre'],
                'edad':     int(row['Edad']),
                'promedio': float(row['Promedio'])
            })
    return estudiantes

def construir_estructuras(estudiantes):
    lista = ListaPython()
    abb   = ABB()
    bplus = BPlus(t=50)
    for e in estudiantes:
        lista.insertar(e)
        abb.insertar(e)
        bplus.insertar(e)
    return lista, abb, bplus


# ─────────────────────────────────────────
#  UTILIDADES
# ─────────────────────────────────────────
def medir(fn_lista, fn_abb, fn_bplus):
    t0 = time.perf_counter(); r = fn_lista();  t_l = time.perf_counter() - t0
    t0 = time.perf_counter(); fn_abb();        t_a = time.perf_counter() - t0
    t0 = time.perf_counter(); fn_bplus();      t_b = time.perf_counter() - t0
    return r, t_l, t_a, t_b

def imprimir_tiempos(titulo, t_l, t_a, t_b):
    print(f"\n{'─'*40}")
    print(f"  {titulo}")
    print(f"{'─'*40}")
    print(f"  Lista : {t_l:.6f} segundos")
    print(f"  ABB   : {t_a:.6f} segundos")
    print(f"  B+    : {t_b:.6f} segundos")
    print(f"{'─'*40}")


# ─────────────────────────────────────────
#  MENÚ
# ─────────────────────────────────────────
def menu(lista, abb, bplus):
    while True:
        print("\n╔══════════════════════════════════════╗")
        print("║   Sistema de Búsqueda de Estudiantes ║")
        print("╠══════════════════════════════════════╣")
        print("║  1. Buscar estudiante por ID         ║")
        print("║  2. Insertar nuevo estudiante        ║")
        print("║  3. Listar todos en orden por ID     ║")
        print("║  4. Benchmark búsqueda (100 IDs)     ║")
        print("║  5. Salir                            ║")
        print("╚══════════════════════════════════════╝")
        opcion = input("  Opción: ").strip()

        if opcion == '1':
            try:
                id_ = int(input("  ID a buscar: "))
            except ValueError:
                print("  ✗ ID inválido."); continue

            resultado, t_l, t_a, t_b = medir(
                lambda: lista.buscar(id_),
                lambda: abb.buscar(id_),
                lambda: bplus.buscar(id_)
            )
            imprimir_tiempos(f"Búsqueda ID {id_}", t_l, t_a, t_b)
            if resultado:
                print(f"\n  ID       : {resultado['id']}")
                print(f"  Nombre   : {resultado['nombre']}")
                print(f"  Edad     : {resultado['edad']}")
                print(f"  Promedio : {resultado['promedio']}")
            else:
                print("  ✗ Estudiante no encontrado.")

            input("\n  Presiona Enter para continuar...")

        elif opcion == '2':
            try:
                id_      = int(input("  ID       : "))
                nombre   = input("  Nombre   : ").strip()
                edad     = int(input("  Edad     : "))
                promedio = float(input("  Promedio : "))
            except ValueError:
                print("  ✗ Datos inválidos."); continue
            e = {'id': id_, 'nombre': nombre, 'edad': edad, 'promedio': promedio}
            _, t_l, t_a, t_b = medir(
                lambda: lista.insertar(e),
                lambda: abb.insertar(e),
                lambda: bplus.insertar(e)
            )
            imprimir_tiempos(f"Inserción ID {id_}", t_l, t_a, t_b)
            input("\n  Presiona Enter para continuar...")

        elif opcion == '3':
            datos, t_l, t_a, t_b = medir(
                lambda: lista.listar_ordenado(),
                lambda: abb.listar_ordenado(),
                lambda: bplus.listar_ordenado()
            )
            
            print(f"\n  {'ID':<8} {'Nombre':<15} {'Edad':<6} {'Promedio'}")
            print(f"  {'─'*38}")
            for e in datos:
                print(f"  {e['id']:<8} {e['nombre']:<15} {e['edad']:<6} {e['promedio']}")
            imprimir_tiempos("Listar todos en orden por ID", t_l, t_a, t_b)
            print(f"\n  Total: {len(datos)} estudiantes listados.")
            input("\n  Presiona Enter para continuar...")

        elif opcion == '4':
            ids_prueba = random.sample(range(1, 10001), 100)
            _, t_l, t_a, t_b = medir(
                lambda: [lista.buscar(i) for i in ids_prueba],
                lambda: [abb.buscar(i)   for i in ids_prueba],
                lambda: [bplus.buscar(i) for i in ids_prueba]
            )
            imprimir_tiempos("Benchmark: 100 búsquedas aleatorias", t_l, t_a, t_b)
            input("\n  Presiona Enter para continuar...")

        elif opcion == '5':
            print("  ¡Hasta luego!"); break
        else:
            print("  ✗ Opción no válida.")


# ─────────────────────────────────────────
#  MAIN
# ─────────────────────────────────────────
if __name__ == '__main__':
    
    ruta = 'estudiantes_random.csv'

    print(f"\nCargando '{ruta}'...")
    estudiantes = cargar_csv(ruta)
    print(f"  {len(estudiantes)} estudiantes cargados.")

    print("Construyendo estructuras (Lista, ABB, B+)...")
    lista, abb, bplus = construir_estructuras(estudiantes)
    print("  ✓ Listo.")

    menu(lista, abb, bplus)
