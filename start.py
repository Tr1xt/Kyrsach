import hamming 
import svert

text = 'Антон'

hamming = hamming.hamming()
svert = svert.svert()

a = svert._encode_(text) #Сверточный кодер

a = hamming.encode(a) # Вызывает функцию кодирования

print(a)

a = hamming.decode(a) # Вызвает функцию декодирования


print(svert._decode_(a)) #Сверточный декодер

###python setup.py build_ext --inplace