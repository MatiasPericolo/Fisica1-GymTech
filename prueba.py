import math

import numpy as np

Promedio_x_munieca = -0.039034449
ErrorX_munieca = 0.004237752


Promedio_y_munieca = -0.208962806
ErrorY_munieca = 0.004533017


Promedio_x_hombro = -0.01621702
ErrorX_hombro = 0.007541687


Promedio_y_hombro = 0.242088395
ErrorY_hombro = 0.008639661


#arctan((y1/x1) - arctan(y2/x2))

#X1
def derivadaAngulo_X1 (x1,y1,x2,y2):
    return (y1/((x1**2)+(y1**2)))
#X2
def derivadaAngulo_X2 (x1,y1,x2,y2):
    return -(y2/((x2**2)+(y2**2)))
#Y1
def derivadaAngulo_Y1 (x1,y1,x2,y2):
    return -(x1/((y1**2)+(x1**2)))
#Y2
def derivadaAngulo_Y2 (x1,y1,x2,y2):
    return (x2/((y2**2)+(x2**2)))


def medicionIndirectaAngulo():
    derivadaAnguloX1 = derivadaAngulo_X1(Promedio_x_munieca,Promedio_y_munieca,Promedio_x_hombro,Promedio_y_hombro)
    derivadaAnguloY1 = derivadaAngulo_Y1(Promedio_x_munieca,Promedio_y_munieca,Promedio_x_hombro,Promedio_y_hombro)
    derivadaAnguloX2 = derivadaAngulo_X2(Promedio_x_munieca,Promedio_y_munieca,Promedio_x_hombro,Promedio_y_hombro)
    derivadaAnguloY2 = derivadaAngulo_Y2(Promedio_x_munieca,Promedio_y_munieca,Promedio_x_hombro,Promedio_y_hombro)
    return (derivadaAnguloX1**2)*(ErrorX_munieca**2) + (derivadaAnguloY1**2)*(ErrorY_munieca**2) + (derivadaAnguloX2**2)*(ErrorX_hombro**2) + (derivadaAnguloY2**2)*(ErrorY_hombro**2)

print(math.sqrt(medicionIndirectaAngulo()))
## RETORNA 0.03697078466826649 radianes

