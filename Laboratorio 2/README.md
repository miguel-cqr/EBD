# 🌳 KD-Tree para búsqueda espacial en logística

## 📌 Problema

Se simula un sistema de logística con **puntos de entrega representados como coordenadas (x, y)**.

El sistema debe responder:

* ¿Qué puntos están dentro de un radio dado desde una ubicación?
* ¿Cuál es el punto más cercano a una ubicación?

Los datos utilizados son estáticos y se generaron para tamaños de:

```text
10, 100, 1000, 5000, 10000 puntos
```

---

## 🎯 Objetivo

Implementar un **KD-Tree desde cero** y compararlo con un método de **fuerza bruta (listas)** para resolver búsquedas espaciales.

---

## 🧩 Estructura

```
.
├── README.md
├── KDtree.py      # Implementación del árbol y búsquedas
├── test.py        # Visualizaciones y pruebas
├── analisis.py    # Comparación de rendimiento
```

---

## ⚙️ Funcionalidades

### 🌳 KD-Tree

* Construcción usando medianas
* Alternancia de ejes (x, y)
* Árbol balanceado

### 🔍 Búsquedas

* **Range Search:** puntos dentro de un radio
* **Nearest Neighbor:** punto más cercano

### 🔴 Fuerza bruta

* Recorre todos los puntos
* Calcula distancias directamente

---

## 📊 Visualización

Se implementaron gráficas para:

* Ver los puntos en el plano
* Mostrar el radio de búsqueda
* Resaltar:

  * vecinos dentro del radio
  * punto objetivo
  * vecino más cercano
* Mostrar divisiones del KD-Tree

---

## 🧪 Pruebas realizadas

Se probaron ambos métodos con:

```text
10, 100, 1000, 5000, 10000 puntos
```

---

## 📈 Resultados

* Para pocos datos (10, 100):

  * Fuerza bruta y KD-Tree tienen tiempos similares

* Para tamaños medios (1000):

  * KD-Tree empieza a ser más eficiente

* Para tamaños grandes (5000, 10000):

  * KD-Tree es claramente más rápido
  * Reduce el número de comparaciones

