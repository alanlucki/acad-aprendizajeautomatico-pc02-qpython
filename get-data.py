import androidhelper
import time
import requests
import platform

droid = androidhelper.Android()
URL = "http://191.232.209.15:3000/entrenar"
genero = 'hombre'
edad = 'joven'

users = ['Franz' , 'Alan', 'Daniel', 'Alonso']
accions = ['salir', 'parar', 'caminar', 'saltar']

def setTerminal():
    print('Seleccione su usuario: ')
    for i in range(len(users)):
        print('  ',i,':  ',users[i])
    index = input('Ingrese el indice de su usuario: ')
    return str(users[int(index)])

def setAccion():
    print('Seleccione accion: ')
    for i in range(len(accions)):
        print('  ',i,':  ',accions[i])
    index = input('Ingrese el orden de la accion: ')
    return accions[int(index)]

def getAccelerometerMetrics():
    data = []
    dt = 10
    endTime = 3000 #sample for 3000ms
    timeSensed=0
    droid.startSensingTimed(1,dt)
    while timeSensed <= endTime:
        time.sleep(dt/1000.0)
        dataSense = droid.sensorsReadAccelerometer().result
        print(dataSense)
        if dataSense[0]:
            data.append(dataSense)
            timeSensed+=dt
    droid.stopSensing()
    return data

def saveDataServer(terminal, data, accion):
    json = {
        'terminal': terminal,
        'date': '',
        'accion': accion,
        'data': data,
        'genero': genero,
        'edad': edad
        } 
    print(json)
    r = requests.post(url = URL, json = json) 

    if r.ok:
        print('Data guardada con exito')
    else:
        print('Repita la accion')
    return r.ok

def main():
    terminal = setTerminal()
    i = 0
    while True:
        print('#########################################')
        print('Intento: ', i)
        print('#########################################')
        accion = setAccion()
        if accion == 'salir':
            break
        while True:
            print('//////////////////////////////////')
            print('Accion a grabar: ', accion)
            input('Presione para continuar: ')
            time.sleep(3)
            print('Iniciando metrica')
            data = getAccelerometerMetrics()
            i = i + 1
            if saveDataServer(terminal, data, accion):
                break


main()