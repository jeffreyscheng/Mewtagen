from dialgarithm.dialgarithm import *

tick = time.clock()
# setup_with_user_input()
setup_without_user_input()
evolve()
output()
print("TOTAL TOOK:", time.clock() - tick)
