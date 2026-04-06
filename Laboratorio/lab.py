import hashlib
import multiprocessing
import itertools
import time
import sys
import math

def hasheo(m):
    encode= m.encode("utf-8")
    hash = hashlib.sha256(encode)

    return hash.hexdigest()

def merkletree(x):
    print(x)
    if(len(x)==1):
        return x[0]
    y=[]
    if(len(x)%2==0):
        for i in range(0,len(x),+2):
            y.append(hasheo(x[i]+x[i+1]))
    else:
        for i in range(0,len(x)-1,+2):
            y.append(hasheo(x[i]+x[i+1]))
        y.append(x[len(x)-1])

    return merkletree(y)

def arbolp(x):
    y=[]
    for a in x:
       y.append(hasheo(a))
    return merkletree(y)

# ══════════════════════════════════════════════════════════════════════════════
#  PROBLEMA 1
#  Encontrar la secuencia de 10 dígitos [0-9] concatenados que produce un hash
# ══════════════════════════════════════════════════════════════════════════════
 
def _buscar_digitos_rango(args):
    inicio, fin, target, resultado = args
    for n in range(inicio, fin):
        if not resultado.empty():
            return
        tmp = n
        digits = []
        for _ in range(10):
            digits.append(str(tmp % 10))
            tmp //= 10
        digits.reverse()
        if arbolp(digits) == target:
            resultado.put(digits)
            return
 
 
def buscar_secuencia_digitos(target: str, num_workers: int = None):
    """
    Problema 1: busca los 10 dígitos (cada uno en [0,9]) cuyo Merkle Tree
    produce el hash `target`.
 
    Uso:
        secuencia = buscar_secuencia_digitos("a3f1...c4d2")
    """
    target = target.strip().lower()
    if len(target) != 64 or not all(c in "0123456789abcdef" for c in target):
        print("ERROR: El hash debe tener 64 caracteres hexadecimales.")
        return None
 
    if num_workers is None:
        num_workers = multiprocessing.cpu_count()
 
    TOTAL = 10 ** 10
    bloque = TOTAL // num_workers
    rangos = []
    for i in range(num_workers):
        inicio = i * bloque
        fin = inicio + bloque if i < num_workers - 1 else TOTAL
        rangos.append((inicio, fin))
 
    resultado = multiprocessing.Queue()
 
    print(f"\n{'═'*60}")
    print(f"  PROBLEMA 1 - Búsqueda de secuencia de 10 dígitos")
    print(f"{'═'*60}")
    print(f"  Hash objetivo:  {target}")
    print(f"  Espacio total:  {TOTAL:,} combinaciones")
    print(f"  Workers:        {num_workers}")
    print(f"  Rango/worker:   ~{bloque:,} combinaciones")
    print(f"{'─'*60}")
 
    t0 = time.time()
    args = [(inicio, fin, target, resultado) for inicio, fin in rangos]
 
    with multiprocessing.Pool(processes=num_workers) as pool:
        job = pool.map_async(_buscar_digitos_rango, args)
        while not job.ready():
            time.sleep(5)
            if not resultado.empty():
                break
            print(f"  [{time.time()-t0:6.0f}s] Buscando...", flush=True)
        pool.terminate()
 
    elapsed = time.time() - t0
 
    if not resultado.empty():
        secuencia = resultado.get()
        print(f"\n  SECUENCIA ENCONTRADA: {' '.join(secuencia)}")
        print(f"  Concatenada:          {''.join(secuencia)}")
        print(f"  Hash verificado:      {arbolp(secuencia)}")
        print(f"  Tiempo:               {elapsed:.2f}s")
        print(f"{'═'*60}\n")
        return secuencia
    else:
        print(f"\n  Hash no encontrado tras {elapsed:.2f}s.")
        print(f"{'═'*60}\n")
        return None
 
 
# ══════════════════════════════════════════════════════════════════════════════
#  PROBLEMA 2
#  Encontrar el orden de transacciones conocidas que produce un hash root dado
# ══════════════════════════════════════════════════════════════════════════════
 
def _buscar_orden_rango(args):
    """
    Itera sobre un subconjunto de permutaciones (por índice léxico) buscando
    el orden cuyo Merkle Tree coincida con el hash objetivo.
    """
    transacciones, indices_perm, target, resultado = args
 
    n = len(transacciones)
    for idx in indices_perm:
        if not resultado.empty():
            return
        # Obtener la permutación número `idx` en orden léxico
        perm = _permutacion_por_indice(list(range(n)), idx)
        orden = [transacciones[i] for i in perm]
        if arbolp(orden) == target:
            resultado.put(orden)
            return
 
 
def _permutacion_por_indice(elementos, idx):
    """Devuelve la permutación número `idx` (0-based) en orden léxico."""
    elementos = list(elementos)
    n = len(elementos)
    resultado = []
    for i in range(n, 0, -1):
        fact = math.factorial(i - 1)
        pos = idx // fact
        idx %= fact
        resultado.append(elementos[pos])
        elementos.pop(pos)
    return resultado
 
 
def buscar_orden_transacciones(transacciones: list, target: str, num_workers: int = None):
    """
    Problema 2: dado un listado de transacciones (strings) y un hash root,
    encuentra el orden en que deben estar para que su Merkle Tree produzca
    dicho hash.
 
    Parámetros
    ----------
    transacciones : lista de strings (las transacciones conocidas)
    target        : hash SHA-256 root esperado (64 chars hex)
 
    Uso:
        txs = ["tx_a", "tx_b", "tx_c", ...]
        orden = buscar_orden_transacciones(txs, "a3f1...c4d2")
    """
    target = target.strip().lower()
    if len(target) != 64 or not all(c in "0123456789abcdef" for c in target):
        print("ERROR: El hash debe tener 64 caracteres hexadecimales.")
        return None
 
    if num_workers is None:
        num_workers = multiprocessing.cpu_count()
 
    n = len(transacciones)
    TOTAL = math.factorial(n)
 
    # Dividir los índices de permutación entre workers
    bloque = TOTAL // num_workers
    rangos_idx = []
    for i in range(num_workers):
        inicio = i * bloque
        fin = inicio + bloque if i < num_workers - 1 else TOTAL
        rangos_idx.append(range(inicio, fin))
 
    resultado = multiprocessing.Queue()
 
    print(f"\n{'═'*60}")
    print(f"  PROBLEMA 2 - Búsqueda de orden de transacciones")
    print(f"{'═'*60}")
    print(f"  Hash objetivo:      {target}")
    print(f"  Transacciones ({n}):  {transacciones}")
    print(f"  Permutaciones:      {TOTAL:,}  ({n}!)")
    print(f"  Workers:            {num_workers}")
    print(f"  Permutaciones/wrk:  ~{bloque:,}")
    print(f"{'─'*60}")
 
    if TOTAL <= 5_000_000:
        # Para n<=12 aproximadamente, un solo proceso con itertools es más rápido
        print(f"  Modo: itertools (espacio pequeño, sin overhead de procesos)")
        t0 = time.time()
        for perm in itertools.permutations(transacciones):
            if arbolp(list(perm)) == target:
                elapsed = time.time() - t0
                orden = list(perm)
                print(f"\n  ORDEN ENCONTRADO:")
                for i, tx in enumerate(orden, 1):
                    print(f"    {i}. {tx}")
                print(f"  Hash verificado: {arbolp(orden)}")
                print(f"  Tiempo:          {elapsed:.4f}s")
                print(f"{'═'*60}\n")
                return orden
        elapsed = time.time() - t0
        print(f"\n  Hash no encontrado tras {elapsed:.2f}s.")
        print(f"{'═'*60}\n")
        return None
    else:
        # Para espacios grandes, multiprocessing con índices de permutación
        print(f"  Modo: multiprocessing (espacio grande)")
        t0 = time.time()
        args = [(transacciones, rango, target, resultado) for rango in rangos_idx]
 
        with multiprocessing.Pool(processes=num_workers) as pool:
            job = pool.map_async(_buscar_orden_rango, args)
            while not job.ready():
                time.sleep(5)
                if not resultado.empty():
                    break
                print(f"  [{time.time()-t0:6.0f}s] Buscando...", flush=True)
            pool.terminate()
 
        elapsed = time.time() - t0
 
        if not resultado.empty():
            orden = resultado.get()
            print(f"\n  ORDEN ENCONTRADO:")
            for i, tx in enumerate(orden, 1):
                print(f"    {i}. {tx}")
            print(f"  Hash verificado: {arbolp(orden)}")
            print(f"  Tiempo:          {elapsed:.2f}s")
            print(f"{'═'*60}\n")
            return orden
        else:
            print(f"\n  Hash no encontrado tras {elapsed:.2f}s.")
            print(f"{'═'*60}\n")
            return None
 
 
# ══════════════════════════════════════════════════════════════════════════════
#  CONFIGURACIÓN - Edita aquí tus datos
# ══════════════════════════════════════════════════════════════════════════════
 
if __name__ == "__main__":

    # Problema 1
    hash_1 = "d073dd6208f76179423b603e44fd2f5e5cd82b8507dac3ba2ceb2b3de3300cff" #Hash a encontrar dependiendo de la secuencia de numeros
    print(f"Demo Problema 11 →  hash: {hash_1}")
    buscar_secuencia_digitos(hash_1)
 
    # Problema 2
    txs = ["hola", "ho", "la", "x"]
    hash_2 = "" #Hash a encontrar dependiendo del orden de las transacciones
    print(f"Demo Problema 2 →  hash: {hash_2}")
    buscar_orden_transacciones(txs, hash_2)
