import sys
import traceback

def handleExc():
    ex_class,exception,trcback=sys.exc_info()
    excName=ex_class.__name__
    try:
        excArgs = exception.__dict__["args"]
    except KeyError:
        excArgs = "<no args>"
    excTb = traceback.format_tb(trcback, 5)
    return (excName, excArgs, excTb)
