import time 
s = time.time()
doc = open('/home/telematica/Documentos/prueba/prueba.txt','a')
for i in range(0,100000):
    for j in range(0,6250):
        doc.write("1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 ")
    doc.write("\n")

doc.close()
f = time.time()
print(f-s)