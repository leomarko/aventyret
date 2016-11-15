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
            if stat == 'mkr':
                vem.stats[stat]=0
            else:
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
        word='beskydd'
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

def nollutrustning(spelare):
    foremal = list()
    for s in spelare:
        foremal += s.unequip()
    return foremal

#funktion för att ladda gamla filer med ny version
def overgang3till4():
    slowprint('I fängelsehålan möter ni Unghäxan.\n')
    time.sleep(0.5)
    slowprint('Unghäxan: Jag var den snälla häxans elev.\n'+
              'Den elaka häxan har lyckats nästla sig in här på slottet\n'+
              'och styr i praktiken bakom kulisserna.\n'+
              'Jag blev tillfångatagen, men den snälla häxan har lyckats gömma sig.\n')
    time.sleep(0.7)
    slowprint('Mer soldater kommer att komma snart. Men ni kom ifrån skuggvärlden,\n'+
              'den snälla häxan sa att ni måste ha hitttat Djurfrämlingens bok?\n')
    time.sleep(0.7)
    slowprint('Otroligt...!\n'+
              'Men det verkar som en del av den magiska skriften bleknat bort...\n'+
              'Unghäxan uttalar en lång trollformel...!\n')
    time.sleep(1)
    slowprint('Det kommer fram symboler på tomma sidor i boken!\n'+
              'Unghäxan: Jag vågar inte lova var ni hamnar men om ni läser här\n'+
              'kommer ni förflyttas någon annanstans...\n'+
              'Hitta den snälla häxan! Använd boken nu, innan soldaterna kommer!\n')
    time.sleep(2)
    slowprint('Du läser ur Djurfrämlingens bok...\n',2)
    time.sleep(2)
    slowprint('Ni hamnade 50 år framåt i tiden!\n')
    print('Ni står utanför slottet.')
