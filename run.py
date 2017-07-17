from dialgarithm.dialgarithm import *

tick = time.clock()
setup()
evolve()
output()
print("TOTAL TOOK:", time.clock() - tick)
