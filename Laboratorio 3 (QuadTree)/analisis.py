from QuadTree import *
import time

N_REPETICIONES = 5

def brute_force_radio(puntos, target, radio):
    resultado = []
    for p in puntos:
        dx = p[0] - target[0]
        dy = p[1] - target[1]
        if (dx*dx + dy*dy) ** 0.5 <= radio:
            resultado.append(p)
    return resultado

def brute_force_vecino(puntos, target):
    mejor = None
    mejor_dist = float('inf')
    for p in puntos:
        dx = p[0] - target[0]
        dy = p[1] - target[1]
        dist = (dx*dx + dy*dy) ** 0.5
        if dist < mejor_dist:
            mejor_dist = dist
            mejor = p
    return mejor

def comparar(n_puntos):
    puntos = generate_data(n_puntos)
    arbol = construir_arbol(puntos)

    target = [5000, 5000]
    radio = 2000
    bf_radio_time = 0
    for _ in range(N_REPETICIONES):
        start = time.time()
        brute_force_radio(puntos, target, radio)
        bf_radio_time += time.time() - start
    bf_radio_time /= N_REPETICIONES

    qt_radio_time = 0
    for _ in range(N_REPETICIONES):
        start = time.time()
        busqueda_radio(arbol, target, radio)
        qt_radio_time += time.time() - start
    qt_radio_time /= N_REPETICIONES


    bf_nn_time = 0
    for _ in range(N_REPETICIONES):
        start = time.time()
        brute_force_vecino(puntos, target)
        bf_nn_time += time.time() - start
    bf_nn_time /= N_REPETICIONES

    qt_nn_time = 0
    for _ in range(N_REPETICIONES):
        start = time.time()
        vecino_mas_cercano(arbol, target)
        qt_nn_time += time.time() - start
    qt_nn_time /= N_REPETICIONES

    print(f"\n--- {n_puntos} puntos ---")
    print(f"Fuerza bruta radio:       {bf_radio_time:.6f}s")
    print(f"Quadtree radio:           {qt_radio_time:.6f}s")
    print(f"Fuerza bruta más cercano: {bf_nn_time:.6f}s")
    print(f"Quadtree más cercano:     {qt_nn_time:.6f}s")

    diferencia_radio = bf_radio_time / qt_radio_time
    diferencia_vecino = bf_nn_time / qt_nn_time
    return diferencia_radio, diferencia_vecino

print("Comparando fuerza bruta vs quadtree...\n")

diferencias_R=[]
diferencias_V=[]
comparaciones = [5, 10, 100, 1000, 5000, 10000]

for n in comparaciones:
    dr, dv = comparar(n)
    diferencias_R.append(dr)
    diferencias_V.append(dv)


fbv_rapido=[]
fbr_rapido=[]
qdv_rapido=[]
qdr_rapido=[]
parecidosr=[]
parecidosv=[]
for i in range(len(diferencias_R)):
    if diferencias_R[i] <= 1 :
        fbr_rapido.append(comparaciones[i])
    elif diferencias_R[i] < 10:
       parecidosr.append(comparaciones[i])
    else:
       qdr_rapido.append(comparaciones[i])

    if diferencias_V[i] <= 1:
        fbv_rapido.append(comparaciones[i])
    elif diferencias_V[i] < 10:
        parecidosv.append(comparaciones[i])
    else:
        qdv_rapido.append(comparaciones[i])
    
print("\nResumen:")
print(f"Pruebas hechas con {comparaciones} puntos, repitiendo las comparaciones {N_REPETICIONES} veces cada una para promediar los tiempos y que los resultados sean más precisos.")
print(f"\t-> Quadtree claramente más rápido en radio para: {qdr_rapido} puntos")
print(f"\t-> Fuerza bruta más rápido en radio para: {fbr_rapido} puntos")
print(f"\t-> Quadtree claramente más rápido en vecino para: {qdv_rapido} puntos")
print(f"\t-> Fuerza bruta más rápido en vecino para: {fbv_rapido} puntos")
print(f"\t-> Resultados parecidos en busqueda por radio (Quadtree comienza a ser más rápido): {parecidosr} puntos")
print(f"\t-> Resultados parecidos en busqueda por vecino (Quadtree comienza a ser más rápido): {parecidosv} puntos")