import cv2
import numpy as np
import multiprocessing as mp
import time

#Secuencial Funcion
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

#Funcion intermedia
def paraCadaUna(segmento):
    return BlancoNegroSecuencial(segmento)

#PAralelo funcion
def ParaleloBlancoNegro(img, threads):
    alto = img.shape[0] #Funcion 0 =alto

    # Lista para guardar segmentos
    segmentos = []

    # Se divide la imagen en partes horizontales
    for i in range(threads):
        seg = i * alto // threads #i = parte actual, alto = total de filas, threads = procesos
        fin_seg = (i + 1) * alto // threads  #calcula el final de la parte
        segmento = img[seg:fin_seg, :] #Dara todas las columnas entre las filas seg y fin_seg, : = all
        segmentos.append(segmento) #esto se guarda en la lista

    # grupo de procesos
    pool = mp.Pool(processes=threads) # crea los procesos que diga threads
    resultados = pool.map(paraCadaUna, segmentos) # todos los procesos trabajaran la funcion 'paraCadaUna()'
    pool.close() #No acepta mas proces
    pool.join() #Espera a que terminen todo los procesos

    res = np.vstack(resultados) #reconstruye la imagen gris con numpy
    return res

if __name__ == "__main__":
    # Carga imagen
    ruta = "pasto.png"
    imagen = cv2.imread(ruta) 

    # Valida que se haya cargado
    if (imagen is None):
        exit()
    

    # -------- secuencial--------
    inicio = time.time() #guarda el momento de inicio
    imgSecuencialGris = BlancoNegroSecuencial(imagen)
    fin = time.time() #guarda el momento de final
    tiempoSec = fin - inicio #total
    # -------- secuencial--------


    # -------- paralelo --------
    inicioPar = time.time()
    imgParaleloGris = ParaleloBlancoNegro(imagen, threads=8)
    finPar = time.time()
    tiempoPar = finPar - inicioPar 
    # -------- paralelo --------

    print(f"Tiempo secuencial: {tiempoSec:.3f}s")
    print(f"Tiempo paralelo: {tiempoPar:.3f}s")

    # desplegar imagenes 
    cv2.imshow("Imagen", imagen)
    cv2.imshow("blancoynegro", imgParaleloGris)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    
    
    

