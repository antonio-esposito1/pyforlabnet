from labnet import XR_VPE
import shelve

print('Compara due db \n') 
db1 = shelve.open(input('inserisci il nome del primo db: '))
db2 = shelve.open(input('inserisci il nome del secondo db: '))
dev = input('inserisci il nome del device sotto analisi: ')
print(len(db1)), print(len(db2))

if db1[dev] == db2[dev]:
    print('nessuna differenza')
else:
    print(db1[dev].isis_neighbors)
    print(db2[dev].isis_neighbors)