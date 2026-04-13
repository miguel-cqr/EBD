import random
from operator import itemgetter

random.seed(10000)

def generar_datos(n):

    return [
        [random.randint(0,10000),random.randint(0,10000)]
        for i in range(1,n+1)
    ] 
# class Nodo:
#     def __init__(self,point):
#         self.left = None
#         self.point = point
#         self.right = None

# def construir_arbol(x):
#     root=None
#     for i in x:
#         insertar_nodo()

# def insertar_nodo(root,axis):
#     root, pos, axis = median(root,axis)
#     point = root[pos]
#     if len(root)==1:
#         return Nodo(point)

#     root.left = construir_arbol(root[0:pos-1],axis)
#     root.right = construir_arbol(root[pos+1:len(root)-1],axis)

# def median(array,axis):
    
#     if len(array)>1:
#         array = sorted(array, key=itemgetter(axis))
#         mitad = int(len(array) / 2)
#     else:
#         mitad = 0
#     if(axis==1):
#         axis = 0
#     else:
#         axis = 1

#     return array, mitad, axis
class Node:
   def __init__(self, point):
      self.point = point
      self.left = None
      self.right = None

def insertNode(root, point, depth):
    if root is None:
        return Node(point)
    
    cd = depth % 2
    
    if point[cd] < root.point[cd]:
        root.left = insertNode(root.left, point, depth + 1)
    else:
        root.right = insertNode(root.right, point, depth + 1)
    
    return root

def constructKdTree(points):
    root = None
    for point in points:
        root = insertNode(root, point, 0)
    return root

def printKdTree(root):
    if root is None:
        return
    print("(", root.point[0], ", ", root.point[1], ")")
    printKdTree(root.left)
    printKdTree(root.right)

x = generar_datos(10)

printKdTree(constructKdTree(x))
