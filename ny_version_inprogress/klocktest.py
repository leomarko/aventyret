def klocka(smi,sna):
    klocka=12
    klocka -= int(smi*1.6 - smi**1.07 - sna*1.7) 
    #klockan minskar långsammare ju närmare noll, snabbhet räknas negativt
    if klocka < -1:
        klocka = 1
    elif klocka < 1.5:
        klocka = 2
    elif klocka < 3:
        klocka = 3
    else:
        klocka = int(klocka)
    return klocka

for i in range(4,30):
    print('smi: '+str(i)+' långsamhet: +2  == '+str(klocka(i,2)))
print('\n')
for i in range(4,30):
    print('smi: '+str(i)+' snabbhet: 0  == '+str(klocka(i,0)))
print('\n')
for i in range(4,30):
    print('smi: '+str(i)+' snabbhet: -1  == '+str(klocka(i,-1)))
print('\n')
for i in range(4,30):
    print('smi: '+str(i)+' snabbhet: -2  == '+str(klocka(i,-2)))
