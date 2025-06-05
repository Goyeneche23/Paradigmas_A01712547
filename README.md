# Paradigmas_A01712547
#### Juan José Goyenche Sánchez

Para esta evidencia se eligio realizar un problema que haga uso de paralelismo. Esto para fortalezer este paradigma, al ser el que mas me costo poner en practica en los ejercicios realizados. Para esto decidi hacer un problema de renderizaciónde imagenes en el lenguaje Python, se termino eligiendo python porque despues de 3 horas intentando fue imposible instalar openCV en c++, haciendo uso de OPEN CL, abundare mas en esto mas adelante.

### ¿Qué es el paralelismo?
El paralelismo se refiere a la ejecución simultánea de tareas de manera simultanea. Se divide el trabajo en multiples subprocesos que se ejecutaran al mismo tiempo.  

### Concurrencia Vs Paralelismo
El paralelismo no es un paradigma de programación en si mismo, en cambio perteneceria al paradigma de concurrencia, el cual basicamente es la ejecución simultánea o aparente de múltiples procesos, pero en ningun momento la **concurrencia** especifica que los multiples procesos tengan que estar trabajando en paralelo, en cambio los trabaja de manera **simultanea**, utilizando sleeps, para poder ir centrandose en tasks especificos, esto para maximizar la utilización de la CPU minimizando el tiempo de inactividad. Por otro lado, el **paralelismo** intenta realizar los procesos **al mismo tiempo**.

![image](https://github.com/user-attachments/assets/39fcf80d-40b8-465f-85a1-8bdea43f5213)

### Librerias
OpenCv: libreria de vision artificial desarrollada por intel, basicamente serra la que nos ayude a trabajar con imagenes, sacar totale de altura, seleccionar pixeles y modificar sus colores.

Numpy: Esta libreria nos servira para crear matrices las imagenes seran 
una matriz (altura, ancho, rgb). y hacer operaciones vectoriales, esto para cambiar el color.

multiprocessing: Funciona de manera similar al threads esta nos permite crear nuevos subprocesos y tambien poder manipular estos.

time: Simplemente lo usaremos para calcular tiempo y comparar los secuencial con lo paralelo

### ¿Como pasar una imagen a blanco y negro?
En términos técnicos, la conversión de una imagen a blanco y negro o mejor llamado escala de grises esta basada en promediar los valores de los canales de color Red, Green y Blue(RGB) : 

Promedio aritmético: (R + G + B) / 3
Promedio ponderado (el más común): 0.299R + 0.587G + 0.114B

Por lo cual al multiplicar de un pixel sus valores dentro del rgb la fórmula del promedio ponderado, esto lo pasará a escala de grises. Por lo tanto tenemos que recorrer todos los pixeles de la imagen para realizar esto, pero son mucho y esto podria ser muy tardado.

### Formula base

Aqui tenemos el proceso basico o de base para poder pasar una imagen a un escala de grises, no abundare tampoco tanto en esto porque lo importante del proyecto es el uso del paralelismo que encontraremos mas adelante. 

```
def BlancoNegroSecuencial(segmento):
    alto, ancho, _ = segmento.shape #Funcion de 'OpenCV', nos regresa el alto, ancho y rgb , que es igual a 3
    blancoNegroImg = np.zeros((alto, ancho), dtype=np.uint8) #crea matriz numpy, y rgb se establece que sera integrer de 8 bits


    for y in range(alto): #selecciona el primer pixel
        for x in range(ancho): #todos los pixeles a la derecha los recorre
            #BGR
            rojo = segmento[y, x, 2]   #Rer
            verde = segmento[y, x, 1]  #Green
            azul = segmento[y, x, 0]   #Blue
           
            gris = int(0.299 * rojo + 0.587 * verde + 0.114 * azul) #formula estandar para pasar a blanco y negr
            blancoNegroImg[y, x] = gris #se devuelve con nuevos colores


    return blancoNegroImg

```  

Basicamente se crea una matriz con la altura, ancho y (red, green, blue) de la matriz, despues se establece el tipo de dato, y ya finalmente entramos a el proceso de recorrido.

![image](https://github.com/user-attachments/assets/3b8b1f74-6f13-4d54-8309-c791c6741105)

### Multiplesprocesos paralelos

La funcion anterior es un implementación correcta, apesar de esto se haria muy tardada y puede ser optimizada, es simple, si la imagen es mas chica, es mas rapido recorrerla. Entonces debemos dividir la imagen en pequeñas partes y que se recorran de manera sincrona. Esto se puede hacer porque contamos con diferentes nucleos.

```
def ParaleloBlancoNegro(img, threads):
    alto = img.shape[0] #Funcion 0 =alto


    # Lista para guardar segmentos
    segmentos = []


    # Se divide la imagen en partes horizontales
    for i in range(threads):
        seg = i * alto // threads #i = parte actual, alto = total de filas, threads = procesos
        fin_seg = (i + 1) * alto // threads  #calcula el final de la parte
        segmento = img[seg:fin_seg, :] #Dara todas las columnas entre las filas seg y fin_seg
        segmentos.append(segmento) #esto se guarda en la lista


    # grupo de procesos
    pool = mp.Pool(processes=threads) # crea los procesos que diga threads
    resultados = pool.map(paraCadaUna, segmentos) # todos los procesos trabajaran la funcion 'paraCadaUna()'
    pool.close() #No acepta mas proces
    pool.join() #Espera a que terminen todo los procesos
    res = np.vstack(resultados) #reconstruye la imagen gris con numpy
    return res

```
En la primer parte del codigo se definen los segmentos, los limites y luego esos segmentos se insertaran a la lista. Se hara uso de map, que es parte de la libreria opencv, para crear los multiprocesos que trabajaran en paralelo, cada uno ingresara en la funcion anterior que vimos y finalmente se reconstruye metiendolos al stack.

![image](https://github.com/user-attachments/assets/59ff3d35-2c35-4471-a464-c3059d04e2dd)
(en el ejemplo los límites son con ancho, en el código con alto, en este caso se debería usar .hstack())

### OverHead

El primer codigo que implemente (incorrecto), me daba un tiempo mucho mayor en el parallelo esto por el ‘overhead’ esto se refiere al tiempo y recursos adicionales que se necesitan para gestionar el paralelismo. Aun podemos ver ejemplo de esto al usar este codigo con un solo segmento, la diferencia teorica enre un paralelismo de un segmento y la funcion baso no existe pero en la practica alg crear el pool de uno y otras tareas se gastan recursos.

![Captura de pantalla 2025-05-23 021018](https://github.com/user-attachments/assets/d8e6d0e2-9f31-4361-bd8b-7188ffc267cc)

En cambio al probar con mas procesos que dividan la imagen y realicen el paralelismo como debe ser tenemos el siguiente resultado: 

![Captura de pantalla 2025-05-23 021137](https://github.com/user-attachments/assets/43b0229b-2299-47fb-b9cf-350b7ceddf0b)

![Captura de pantalla 2025-05-23 131940](https://github.com/user-attachments/assets/20beb2e5-c9b8-4c2c-a280-6b7d8460140d)

### Complejidad

Ambas funciones tienen un complejidad de O(n), pero logiicamente como pudimos aprecirar la paralela es mas rapida, esto tiene como causante que realmente tiene una complejidad de O(n / (threads + overhead) ). La velocidad en nustros ejemplos usando 8 threads, es mas rapido con el paralelismo para eso podemos agregar una formula mas (tiempo secuencial / tiempo paralelo) : ![image](https://github.com/user-attachments/assets/82a0c006-79ad-459b-af64-3d5c943f8bdb)

Esto puede cambiar dependiendo de la cantidad de threads, el tamaño de la imagen y adicionalmente el overhead tambien puede cambiar dependiendo la optimización del codigo y donde se corra (C++ seria mas rapido).

```
O ( n / threads + overhead )
```


### Otro paradigma 

Este  es un enfoque en programación que se basa en la aplicación de funciones matemáticas para transformar datos y resolver problemas. Se enfoca en la composición de funciones puras, evadiendo el uso de estado mutable y efectos secundarios. 

```
def blanconegrofuncinoal(imagen):
    rojo = imagen[:, :, 2]
    verde = imagen[:, :, 1]
    azul = imagen[:, :, 0]
    gris = 0.299 * rojo + 0.587 * verde + 0.114 * azul
    return gris
```
Esta función (no se si sea correcta) lo que hace basicamente es por medio de vectores, tomar todos los pixeles que pertenezcan a los canales rojo, verde , azul y tras esto les aplica la formula para pasar a blanco y negro.

Para comparar ambas soluciones son relativamente parecidas aunque este para lo realiza de manera secuencial lo cual es mas lento, de igual manera se podria tambien decir que de cierta manera la solucion paralela es parte del paradigma funcional, concurrente y paralelo.

### Concluision

El paradigma de paralelismo es muy utiles, para tareas grandes, a pesar de que para ciertas tareas puede general overhead, en realidad me parece muy aplicable a prácticamente cualquier tipo de proyectos, el único problema puede ser el desafío que representa pero en lo personal no me parecio tan desafía tomando en cuenta el beneficio en los recursos o mejor dicho tiempo que ahorra.

### Referencias

Saez, F., Piccoli, F., Printista, M., & Raiul Gallard. (2003). Paradigmas de programación paralela. Universidad Nacional de La Plata. Recuperado de https://sedici.unlp.edu.ar/bitstream/handle/10915/21554/Documento_completo.pdf?sequence=1


DeepSeek. (2025). DeepSeek AI Assistant. 


Mdo, D. (s.f.). Paradigma Concurrente. Prezi. Recuperado de https://prezi.com/9dn7zhw0x7si/paradigma-concurrente/
prezi.com

GeeksforGeeks. (2021). Introduction to Parallel Computing. Recuperado de https://www.geeksforgeeks.org/introduction-to-parallel-computing/






