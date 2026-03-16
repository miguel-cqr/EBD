# Benchmark de Estructuras de Datos — Búsqueda de Estudiantes

Proyecto académico que compara el rendimiento de búsqueda entre tres estructuras de datos sobre un conjunto de 10,000 estudiantes generados en memoria. Se analiza cómo el orden de inserción (IDs secuenciales vs. aleatorios) afecta el tiempo de búsqueda en cada estructura.

---

## Estructuras comparadas

| Estructura | Búsqueda | Nota |
|---|---|---|
| **Lista de Python** | O(n) | Recorre elemento por elemento |
| **Árbol Binario de Búsqueda (ABB)** | O(log n) promedio / O(n) peor caso | Se degrada con IDs ordenados |
| **Árbol B+** (orden t=50) | O(log n) garantizado | Estable sin importar el orden de inserción |

> **Observación clave:** el ABB insertado con IDs en orden secuencial se convierte en una cadena lineal (todos los nodos hacia la derecha), haciendo la búsqueda tan lenta como la lista plana. El Árbol B+ no sufre este problema porque siempre se mantiene balanceado.

---

## Archivos del proyecto

```
├── ejercicioArboless.py   # Código principal: generación de datos, estructuras y benchmark
└── README.md
```

No se necesitan archivos CSV externos. Los datos se generan directamente en memoria al ejecutar el script.

---

## Requisitos

- Python 3.8 o superior
- No requiere librerías externas (solo `time` y `random` de la librería estándar)

---

## Cómo ejecutar

1. Clona el repositorio:

```bash
git clone https://github.com/miguel-cqr/EBD.git
cd EBD/Arboles
```

2. Ejecuta el script:

```bash
python ejercicioArboless.py
```

El programa genera los datos, construye las tres estructuras y corre cuatro rondas de benchmarks. Presiona **Enter** para avanzar entre rondas.

---

## Qué hace el benchmark

En cada ronda se realizan búsquedas aleatorias sobre los dos conjuntos (IDs ordenados e IDs aleatorios) y se imprime el tiempo total de cada estructura:

| Ronda | Búsquedas |
|---|---|
| 1 | 100 |
| 2 | 1,000 |
| 3 | 2,000 |
| 4 | 4,000 |

### Ejemplo de salida

```
──────────────────────────────────────────
  IDs ordenados   (100 búsquedas)
──────────────────────────────────────────
  Lista : 0.010531 segundos
  ABB   : 0.023776 segundos
  B+    : 0.000226 segundos
──────────────────────────────────────────

──────────────────────────────────────────
  IDs aleatorios  (100 búsquedas)
──────────────────────────────────────────
  Lista : 0.009728 segundos
  ABB   : 0.000209 segundos
  B+    : 0.000240 segundos
──────────────────────────────────────────
```

Con IDs ordenados el ABB es el más lento porque está degenerado. Con IDs aleatorios el ABB y el B+ son comparables y ambos superan ampliamente a la lista.
