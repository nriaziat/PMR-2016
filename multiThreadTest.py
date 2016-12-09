import time
from multiprocessing import Process, Value

i = 0

def function1():
    print('1')
    time.sleep(5)
    global var
    print('string')
    var.value = 50
    return

        
def function2():
    print('Hi')
    return
        
def multiMain():
    if __name__ == '__main__':
        global var
        var = Value('i', 0)
        p1 = Process(target=function1)
        p1.start()
        while p1.is_alive():
            function2()
    
multiMain()

