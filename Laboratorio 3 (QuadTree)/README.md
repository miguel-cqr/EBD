# Quadtree para búsqueda espacial en logística

## Problema

Se simula un sistema de logística con **puntos de entrega representados como coordenadas (x, y)**.

El sistema debe responder:

* ¿Qué puntos están dentro de un radio dado desde una ubicación?
* ¿Cuál es el punto más cercano a una ubicación?

Los datos utilizados son estáticos y se generaron para tamaños de:

```text
5, 10, 100, 1000, 5000, 10000 puntos
```

---

## Objetivo

Implementar un **Quadtree desde cero** y compararlo con un método de **fuerza bruta (listas)** para resolver búsquedas espaciales.

---

## Estructura

```
.
├── README.md
├── quadtree.py    # Implementación del árbol y búsquedas
├── test.py        # Visualizaciones y pruebas
├── analisis.py    # Comparación de rendimiento
```

---

## Funcionalidades

### Quadtree

* Construcción dividiendo el espacio geométricamente por la mitad
* División simultánea en ambos ejes (x, y)
* 4 cuadrantes por nodo: SO, SE, NO, NE

### Búsquedas

* **Búsqueda por radio:** puntos dentro de un radio
* **Vecino más cercano:** punto más cercano

### Fuerza bruta

* Recorre todos los puntos
* Calcula distancias directamente

---

## Visualización

Se implementaron gráficas para:

* Ver los puntos en el plano
* Mostrar el radio de búsqueda
* Resaltar:

  * vecinos dentro del radio
  * punto objetivo
  * vecino más cercano
* Mostrar divisiones del Quadtree

---

## Pruebas realizadas

Se probaron ambos métodos con:

```text
5, 10, 100, 1000, 5000, 10000 puntos
```

---

## Resultados

* Para pocos datos (5, 10):

  * Fuerza bruta y Quadtree tienen tiempos similares, incluso fuerza bruta puede ser más rápido por el overhead de construir el árbol

* Para tamaños medios (100, 1000):

  * Quadtree empieza a ser más eficiente

* Para tamaños grandes (5000, 10000):

  * Quadtree es claramente más rápido gracias a la poda de cuadrantes completos