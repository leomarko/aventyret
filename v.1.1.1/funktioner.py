#separerbara funktioner

#difstat, karta, markpos, plusförmåga, listval 

import time
import sys

def listval(lista):
    string=''
    n=1
    for d in lista:
        if n>1:
            string+='\n'
        string+=str(n)+': '+d
        n+=1
    print(string)
    while True:
        try:
            ans=int(input())
            assert ans>0 and ans<=len(lista)
        except(ValueError,AssertionError):
            print('Försök igen')
            continue
        break
    return ans-1

def uniquelist(seq):
   seen = set()
   result = []
   for item in seq:
       if item in seen: continue
       seen.add(item)
       result.append(item)
   return result

def karta(position):
    print('')

def markpos(position):
    return True

def difstat(vem,stat,plus,tak=100,mini=0,noprint=False):
    maxad=False
    if stat == 'liv':
        vem.liv+=plus
        if vem.hp > 0:
            vem.hp+=plus
        word='liv'

    elif stat == 'hp':
        if vem.hp == vem.liv and plus > 0:
            return False
        vem.hp+=plus
        if vem.hp > vem.liv:
            vem.hp = vem.liv
            maxad=True
        if vem.hp < 0:
            vem.hp = 0
        word='hp'
        
    elif isinstance(stat,str):
        if vem.stats[stat] >= tak and plus > 0:
            return False
        vem.stats[stat]+=plus
        if vem.stats[stat]>tak:
            vem.stats[stat]=tak
            maxad=True
        if vem.stats[stat]<=mini:
            vem.stats[stat]=1
            maxad=True
    else:
        if vem.mods[stat] >= tak and plus > 0:
            return False
        vem.mods[stat]+=plus
        if vem.mods[stat]>tak:
            vem.mods[stat]=tak
            maxad=True
        if vem.mods[stat]<=mini:
            vem.mods[stat]=0
            maxad=True
        
    if stat=='smi':
        word='smidighet'      
    if stat=='str':
        word='styrka'
    if stat=='mkr':
        word='magikraft'
                                      
    if stat==0:
        if not noprint:
            if plus>0:
                print(vem.namn+' blev långsammare\n')
            if plus<0:
                print(vem.namn+' blev snabbare\n')
        return True
    if stat==1:
        word='pricksäkerhet'
    if stat==2:
        word='magiskt skydd'
    if stat==3:
        word='undvikning'

    if not noprint:
        if maxad:
            if stat == 'hp':
                print(vem.namn+' fick full hp\n')
            elif isinstance(stat,str):
                print(vem.namn+' har nu '+str(vem.stats[stat])+' i '+word+'\n')
            else:
                print(vem.namn+' har nu '+str(vem.mods[stat])+' i '+word+'\n')
        elif plus != 0:
            if stat == 'hp':
                print(vem.namn+' återhämtade '+str(plus)+' hp\n')
            else:
                print(vem.namn+' fick '+str(plus)+' i '+word+'\n')

    return True

def plusformaga(vem,typ,namn,mp=0,tabort=False):
    if typ==1: #förmåga
        vem.formagor.append(namn)
    if typ==2: #magi
        vem.magier.append((namn,mp))
    if typ==3: #special
        vem.special.append(namn)
    if tabort: #uppgradering på förmågor
        vem.formagor.remove(tabort)
    print(vem.namn+' lärde sig '+namn+'\n')

def slowprint(string, extraslow=1):
    for c in string:
        sys.stdout.write(c)
        sys.stdout.flush()
        time.sleep(0.045*extraslow)
