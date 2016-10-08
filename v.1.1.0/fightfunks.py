from funktioner import difstat, listval, slowprint
from random import random, randint
from copy import copy, deepcopy
from klasser import EngangsForemal
import forvandling as fv
import fiender as fi


#------------------------------------------------------------------------------
#KLASSER

class Effekt:
    def __init__(self,namn,funktion,target,args,reverse,varaktighet):
        self.namn=namn
        self.funktion=funktion
        self.target=target
        self.args=args
        self.reverse=reverse
        self.sluttid=varaktighet

    def use(self, noprint=False):
        self.funktion(self.target,*self.args, noprint=noprint)

    def check(self,tick):
        if tick == self.sluttid:
            return True

    def cancel(self, noprint=False):
        if not noprint:
            print(self.target.namn+' är inte längre påverkad av '+self.namn)
        self.funktion(self.target,*self.reverse, noprint=noprint)




#--------------------------------------------------------------------------------------------------
#FUNKTIONER

def fightval(spelare, inventory, specifik=False):
    lista=['Attackera']
    if len(spelare.formagor)>0:
        lista.append('Använd förmåga')
    if len([s for s in [f for f in inventory if isinstance(f,EngangsForemal)] if s.fight]) > 0:
        lista.append('Använd föremål')
    if len(spelare.magier)>0:
        if spelare.stats['mkr'] >= min([m[1] for m in spelare.magier]):
            lista.append('Använd magi')
    if not specifik:
        lista.append('Fly')
    return lista

def randomenc(plats):
    #ska kolla PDICT, där varje plats har en lista med fiendelistor
    #unika fiender kan inte vara i listorna, måste läggas in i main
    lista = PDICT[plats][randint(0,len(PDICT[plats])-1)]
    gruppnamn = lista[0]
    fiender = [f for f in lista[1:]] 
    return (gruppnamn, fiender)


def borteffekter(effekter,figur):
    i = 0
    while i < len(effekter):
        if effekter[i].target == figur:
            effekter[i].cancel(noprint=True)
            effekter.remove(effekter[i])
        else:
            i += 1

def uniquelist(seq):
   seen = set()
   result = []
   for item in seq:
       if item in seen: continue
       seen.add(item)
       result.append(item)
   return result



#----------------------------------------------------------------------------
#FIGHT



def fight(spelarlista, inventory, progress, plats, specifik=False, OP=0):
    #för randomencouter är plats en string, annars lista med namn
    tick=1
    effekter=[]
    slowprint('!!!!!!!!!!!!!!!!!!!!!!!\n')

    if specifik:
        fiender = []
        for fiende in plats:
            fiender.append(MDICT[fiende])
        print(' och '.join([f.namn for f in fiender])+' angriper\n')       
    else:
        fiender=randomenc(plats)
        print(fiender[0]+' angriper\n')
        fiender = fiender[1]
    
    s_lista=deepcopy(spelarlista)
    for s in s_lista:
        s.formagor = uniquelist(s.formagor) #eliminerar dubletter 
        s.magier = uniquelist(s.magier) #eliminerar dubletter
    f_lista=[]
    for f in fiender:
        f_lista.append(copy(f))
    if OP != 0:
        if OP == 1:
            for f in f_lista:
                f.liv = int((f.liv+3)*2)
                f.hp = f.liv
                f.rustning += 2
                f.mods[2] += 1
                for stat in f.stats:
                    f.stats[stat] = int((f.stats[stat]+1)*2)
        elif OP == 2:
            for f in f_lista:
                f.liv = int((f.liv+10)*3)
                f.hp = f.liv
                f.rustning = int((f.rustning+2)*2)
                f.mods[2] += 1
                for stat in f.stats:
                    f.stats[stat] = int((f.stats[stat]+3)*3)
                for mod in f.mods:
                    mod *= 2
    aktiva_s=[s for s in s_lista if s.hp>0]
    aktiva_f=f_lista

    #LOOP
    while True:
        #FIENDER
        for figur in aktiva_f:
            if aktiva_s==[]:
                print('Du är besegrad.\nSlut på äventyret.')
                raise SystemExit
            if tick % figur.klocka() == 0:
                print(figur.namnB+'s tur')
                input('(tryck enter)')
                mode = figur.mode()

                if mode == 'attack' or mode == 'critical' or mode == 'dubbel attack':
                    target=randint(0,len(aktiva_s)-1)
                    if figur.hit(aktiva_s[target]):
                        skada=int(figur.stats['str']*(1.5+random()) - aktiva_s[target].mods[2] - aktiva_s[target].stats['str']*0.1)
                        if mode == 'critical':
                            print('Förödande attack...!')
                            skada+=int(figur.stats['str']*(1+random()))
                        try:
                            skada-=aktiva_s[target].utrust['rustning'].skydd
                        except(AttributeError,NameError):
                            skada=skada
                        if skada < 1:
                            skada = 1
                        print(figur.namnB+' attackerar '+aktiva_s[target].namn+' och gör '+str(skada)+' skada.')
                        aktiva_s[target].hp-=skada
                    else:
                        print(figur.namn+' attackerar '+aktiva_s[target].namn+' men missar.')
                    if mode == 'dubbel attack':
                        print('Dubbel attack!')
                        if figur.hit(aktiva_s[target]):
                            skada=int(figur.stats['str']*(1.5+random()) - aktiva_s[target].mods[2] - aktiva_s[target].stats['str']*0.1)
                            try:
                                skada-=aktiva_s[target].utrust['rustning'].skydd
                            except(AttributeError,NameError):
                                skada=skada
                            if skada < 1:
                                skada = 1
                            print(figur.namnB+' attackerar '+aktiva_s[target].namn+' och gör '+str(skada)+' skada.')
                            aktiva_s[target].hp-=skada
                            if aktiva_s[target].hp<1:
                                print(aktiva_s[target].namn+' är medvetslös.')
                                aktiva_s[target].hp=0
                                borteffekter(effekter,aktiva_s[target])
                                aktiva_s.remove(aktiva_s[target])
                        else:
                            print(figur.namn+' attackerar '+aktiva_s[target].namn+' men missar.')
                    if aktiva_s[target].hp<1:
                            print(aktiva_s[target].namn+' är medvetslös.')
                            aktiva_s[target].hp=0
                            borteffekter(effekter,aktiva_s[target])
                            aktiva_s.remove(aktiva_s[target])

                elif mode == 'other':
                    figur.other()

                elif mode == 'fly':
                    print(figur.namnB+' flyr!')
                    if len(fiender) == 1:
                        return
                    else:
                        aktiva_f.remove(figur)

                #Nedan alla fienders förmågor och magier. Fiender betalar inte mp

                elif mode == 'Eld':
                    print(figur.namnB+' använder '+mode+'...')
                    for s in aktiva_s:
                        skada=int(figur.stats['mkr']*(2+random()*1.5) - s.mods[2]*2)
                        print(s.namn+' förlorar '+str(skada)+' hp')
                        s.hp-=skada
                        if s.hp<1:
                            print(s.namn+' är medvetslös.')
                            s.hp = 0
                            borteffekter(effekter,s)
                            aktiva_s.remove(s)

                elif mode == 'Förtärande mörker':
                        target = randint(0,len(aktiva_s)-1)
                        print(figur.namnB+' använder '+mode+'...')
                        skada=int(figur.stats['mkr']*(randint(4,6)+figur.hp*0.02))
                        print(aktiva_s[target].namn+' förlorar '+str(skada)+' hp')
                        aktiva_s[target].hp-=skada
                        if aktiva_s[target].hp<1:
                            print(aktiva_s[target].namn+' är medvetslös.')
                            aktiva_s[target].hp=0
                            borteffekter(effekter,aktiva_s[target])
                            aktiva_s.remove(aktiva_s[target])
                        sjalvskada=int(skada*0.3)
                        print(figur.namnB+' förlorar '+str(sjalvskada)+' hp')
                        figur.hp -= sjalvskada
                        if figur.hp<1:
                            print(figur.namnB+' är medvetslös.')
                            figur.hp=0
                            borteffekter(effekter,figur)
                            aktiva_f.remove(figur)

                elif mode == 'Förvrida framtiden':
                    print(figur.namnB+' använder '+mode+'...')
                    for f in aktiva_f:
                        e=Effekt('Förutbestämmande',difstat,f,(3,4),(3,-4),int(figur.stats['mkr']*random()*0.4) + 5 )
                        e.sluttid+=tick
                        duplikat=False
                        for effekt in effekter:
                            if effekt.namn==e.namn and effekt.target==e.target:
                                print(f.namn+' manipulerar redan tiden')
                                duplikat=True
                        if not duplikat:
                            e.use()
                            effekter.append(e)
                    
                    del duplikat

                elif mode == 'Hypnos':
                    target = randint(0,len(aktiva_s)-1)
                    print(figur.namnB+' använder '+mode+'...')
                    if figur.stats['mkr']*0.007+0.5+random()>1:
                        e=Effekt('Hypnos',difstat,aktiva_s[target],(0,6,10,-3),(0,-6,10,-3),randint(5,12))
                        e.sluttid+=tick
                        duplikat=False
                        for effekt in effekter:
                            if effekt.namn==e.namn and effekt.target==e.target:
                                effekter.remove(effekt)
                                duplikat=True
                        if not duplikat:
                            e.use()
                        effekter.append(e)
                        
                        del duplikat
                    else:
                        print('...men hypnosen misslyckas.')

                elif mode == 'Kvävning':
                    print(figur.namnB+' använder '+mode+'...')
                    for s in aktiva_s:
                        skada=int(s.liv*0.2)
                        print(s.namn+' förlorar '+str(skada)+' hp')
                        s.hp -= skada
                        if s.hp<1:
                            print(s.namn+' är medvetslös.')
                            s.hp=0
                            borteffekter(effekter,s)
                            aktiva_s.remove(s)
                        
                elif mode == 'Smärta':
                    target = randint(0,len(aktiva_s)-1)
                    print(figur.namnB+' använder '+mode+'...')
                    skada=int(figur.stats['mkr']*(1.5 + random()*1.5) + aktiva_s[target].liv*0.1 - aktiva_s[target].mods[2]*2)
                    print(aktiva_s[target].namn+' förlorar '+str(skada)+' hp')
                    aktiva_s[target].hp-=skada
                    if aktiva_s[target].hp<1:
                        print(aktiva_s[target].namn+' är medvetslös.')
                        s_lista[target].hp=0
                        borteffekter(effekter,aktiva_s[target])
                        aktiva_s.remove(aktiva_s[target])
                    else:
                        difstat(aktiva_s[target],0,int(skada*0.1))

                elif mode == 'Stank':
                    print(figur.namnB+' använder '+mode+'...')
                    for s in aktiva_s:
                        s.stats['mkr'] -= 3
                        if s.stats['mkr'] < 0:
                            s.stats['mkr'] = 0
                        print(s.namn+' förlorar 3 magikraft\n')
                        e = Effekt('Illamående',difstat,s,('smi',-3),('smi',+3),8 )
                        e.sluttid+=tick
                        duplikat=False
                        for effekt in effekter:
                            if effekt.namn==e.namn and effekt.target==e.target:
                                effekter.remove(effekt)
                                duplikat=True
                        if not duplikat:
                            e.use()
                        effekter.append(e)
                        
                        e = Effekt('Utmattning',difstat,s,('str',-3),('str',+3),8 )
                        e.sluttid+=tick
                        duplikat=False
                        for effekt in effekter:
                            if effekt.namn==e.namn and effekt.target==e.target:
                                effekter.remove(effekt)
                                duplikat=True
                        if not duplikat:
                            e.use()
                        effekter.append(e)
           
                elif mode == 'Trollsmäll':
                    target=randint(0,len(aktiva_s)-1)
                    print(figur.namnB+' använder '+mode+'...')
                    skada=int(figur.stats['mkr']*8*random() + 40*random() - aktiva_s[target].mods[2]*2)
                    if skada < 1:
                            skada = 1
                    print(aktiva_s[target].namn+' förlorar '+str(skada)+' hp')
                    aktiva_s[target].hp-=skada
                    if aktiva_s[target].hp<1:
                        print(aktiva_s[target].namn+' är medvetslös.')
                        aktiva_s[target].hp=0
                        borteffekter(effekter,aktiva_s[target])
                        aktiva_s.remove(aktiva_s[target])

                elif mode == 'Trollstoft':
                    print(figur.namnB+' använder '+mode+'...')
                    plus=int(figur.stats['mkr']*0.8*random())
                    for f in aktiva_f:
                        f.hp+=plus+int(f.liv*0.25)
                        if f.hp>=f.liv:
                            print(f.namn+' fick full hp')
                            f.hp=f.liv
                        else:
                            print(f.namn+' återhämtade '+str(plus+int(f.liv*0.25))+' hp')
                        e=Effekt('Trollstoft',difstat,f,(0,-1,10,-3),(0,1,10,-3),int(figur.stats['mkr']*0.5) + randint(5,10) )
                        e.sluttid+=tick
                        duplikat=False
                        for effekt in effekter:
                            if effekt.namn==e.namn and effekt.target==e.target:
                                effekter.remove(effekt)
                                duplikat=True
                        if not duplikat:
                            e.use()
                        effekter.append(e)
                    del plus
                    
                    del duplikat

                elif mode == 'Återhämtning' or mode == 'Återhämtning 2':
                        print(figur.namnB+' använder '+mode+'...')
                        if mode == 'Återhämtning':
                            plus=int(figur.liv*0.2)
                        else:
                            plus=int(figur.liv*0.32)
                        figur.hp+=plus
                        if figur.hp>=figur.liv:
                            print(figur.namnB+' fick full hp')
                            figur.hp=figur.liv
                        else:
                            print(figur.namnB+' återhämtade '+str(plus)+' hp')

                elif mode == 'Ändra framtiden':
                    print(figur.namnB+' använder '+mode+'...')
                    for s in aktiva_s:
                        e=Effekt('Ute ur tiden',difstat,s,(0,30),(0,-30),randint(3,5)+int(figur.stats['mkr']*(0.2+random()*0.3)) + 1 )
                        e.sluttid+=tick
                        duplikat=False
                        for effekt in effekter:
                            if effekt.namn==e.namn and effekt.target==e.target:
                                effekter.remove(effekt)
                                duplikat=True
                        if not duplikat:
                            e.use()
                        effekter.append(e)
                    
                    del duplikat

                else:
                    raise ValueError('Fel mode')

                del mode
                print('\n')

        #SPELARE        
        for figur in aktiva_s:
            if aktiva_f==[]:   
                break
            if tick % figur.klocka() == 0:
                print(figur.namn+'s tur')
                if any('Urkraft' in e.namn for e in effekter if e.target == figur):
                    figur.stats['mkr'] += 2
                    print('Urkraft: '+figur.namn+' får 2 magikraft.')
                elif any('Mystisk kraft' in e.namn for e in effekter if e.target == figur):
                    figur.stats['mkr'] += 1
                    print('Mystisk kraft: '+figur.namn+' får 1 magikraft.')
                #statusrad:
                statusstrings=[]
                for s in aktiva_s:
                    sta = s.namn+':'+s.hpstr()+'  '+' '.join('"'+e.namn+'"' for e in effekter if e.target == s)
                    statusstrings.append(sta)
                print('Status   '+'\n         '.join(statusstrings))
                if any('Bedömning' in formagor for formagor in (s.special for s in aktiva_s)):
                    statusstrings=[]
                    for f in aktiva_f:
                        sta = f.namn+':'+f.hpstr()+'   '+' '.join('"'+e.namn+'"' for e in effekter if e.target == f)
                        statusstrings.append(sta)
                    print('Bedömning   '+'\n            '.join(statusstrings))
                mode=listval(fightval(figur, inventory, specifik))

                #ATTACK
                if mode==0:
                    target=listval([f.namn for f in aktiva_f])
                    if figur.hit(aktiva_f[target]):
                        skada=figur.stats['str']
                        if 'Lyckoträff' in figur.special and randint(0,4) == 4:
                            print('Lyckoträff!')
                            skada+=int(figur.stats['str']*(1+random()))
                        try:
                            skada += figur.utrust['vapen'].skada
                        except(AttributeError):
                            skada = skada
                        skada*=1.5+random()
                        skada=int(skada - aktiva_f[target].rustning - aktiva_f[target].mods[2] - aktiva_f[target].stats['str']*0.1)
                        if skada < 1:
                            skada = 1
                        print(figur.namn+' attackerar '+aktiva_f[target].namnB+' och gör '+str(skada)+' skada.')
                        aktiva_f[target].hp-=skada
                    else:
                        print(figur.namn+' attackerar '+aktiva_f[target].namnB+' men missar.')

                    if 'Dubbel attack' in figur.special:
                        if figur.stats['smi']*0.07 + 2.3*random()  >  2:
                            print('Dubbel attack!')
                            if figur.hit(aktiva_f[target]):
                                skada=figur.stats['str']
                                if 'Lyckoträff' in figur.special and randint(0,4) == 4:
                                    print('Lyckoträff!')
                                    skada+=int(figur.stats['str']*(1+random()))
                                try:
                                    skada += figur.utrust['vapen'].skada
                                except(AttributeError):
                                    skada = skada
                                skada*=1.5+random()
                                skada=int(skada - aktiva_f[target].rustning - aktiva_f[target].mods[2] - aktiva_f[target].stats['str']*0.1)
                                if skada < 1:
                                    skada = 1
                                print(figur.namn+' attackerar '+aktiva_f[target].namnB+' och gör '+str(skada)+' skada.')
                                aktiva_f[target].hp-=skada
                            else:
                                print(figur.namn+' attackerar '+aktiva_f[target].namnB+' men missar.')
                            
                    if aktiva_f[target].hp<1:
                        print(aktiva_f[target].namnB+' är medvetslös.')
                        aktiva_f[target].hp=0
                        borteffekter(effekter,aktiva_f[target])
                        aktiva_f.remove(aktiva_f[target])

                #FÖRMÅGA
                elif fightval(figur, inventory)[mode]=='Använd förmåga':   
                    namn=figur.formagor[listval(figur.formagor)]

                    if namn == 'Djärv attack':
                        target=listval([f.namn for f in aktiva_f])
                        if figur.hit(aktiva_f[target]):
                            skada=figur.stats['str']
                            try:
                                skada += figur.utrust['vapen'].skada
                            except(AttributeError):
                                skada = skada
                            skada*=2+random()+random()
                            sjalvskada=int(skada*(random()*0.35))
                            skada=int(skada - aktiva_f[target].rustning - aktiva_f[target].mods[2] - aktiva_f[target].stats['str']*0.1)
                            if skada < 1:
                                skada = 1
                            print(figur.namn+' attackerar '+aktiva_f[target].namnB+' och gör '+str(skada)+' skada.')
                            
                            print(figur.namn+' förlorar '+str(sjalvskada)+' hp')
                            aktiva_f[target].hp-=skada
                            if aktiva_f[target].hp<1:
                                print(aktiva_f[target].namnB+' är medvetslös.')
                                aktiva_f[target].hp=0
                                borteffekter(effekter,aktiva_f[target])
                                aktiva_f.remove(aktiva_f[target])
                            figur.hp-=sjalvskada
                            if figur.hp<1:
                                print(figur.namn+' är medvetslös.')
                                figur.hp=0
                                borteffekter(effekter,figur)
                                aktiva_s.remove(figur)
                        else:
                            sjalvskada=int(figur.stats['str']*random())
                            print(figur.namn+' attackerar '+aktiva_f[target].namnB+' men missar.')
                            print(figur.namn+' förlorar '+str(sjalvskada)+' hp')
                            figur.hp-=sjalvskada
                            if figur.hp<1:
                                print(figur.namn+' är medvetslös.')
                                figur.hp=0
                                borteffekter(effekter,figur)
                                aktiva_s.remove(figur)
                        del sjalvskada

                    if namn == 'Fågel':
                        fv.fagel(figur)

                    if namn == 'Gorilla':
                        fv.gorilla(figur)

                    if namn == 'Mystisk kraft':
                        print(figur.namn+' hämtar kraft...')
                        e=Effekt(namn,difstat,figur,('mkr',0),('mkr',0), int(10 + figur.lvl*0.4))
                        e.sluttid += tick
                        effekter.append(e)

                    if namn == 'Projicera själ':    #FUNKAR INTE med alla effekter, VARFÖR? Kanske funkar nu...?
                        print(figur.namn+' använder '+namn+'...')
                        if len(aktiva_s)>1:
                            print(figur.namn+' lämnar sin kroppsliga form')
                            tid = int(6 + figur.lvl*0.1)
                            for s in [spelare for spelare in aktiva_s if spelare.namn!=figur.namn]:
                                e=Effekt(figur.namn+'s armar',difstat,s,('str',int(figur.stats['str']*0.7)),('str',-int(figur.stats['str']*0.7)),tid )
                                e.sluttid += tick
                                e.use()
                                effekter.append(e)

                                e=Effekt(figur.namn+'s kunskap',difstat,s,('smi',int(figur.stats['smi']*0.7)),('smi',-int(figur.stats['smi']*0.7)),tid )
                                e.sluttid += tick
                                e.use()
                                effekter.append(e)

                                e=Effekt(figur.namn+'s hjärta',difstat,s,('mkr',int(figur.stats['mkr']*0.7)),('mkr',-int(figur.stats['mkr']*0.7)),tid )
                                e.sluttid += tick
                                e.use()
                                effekter.append(e)

                            e=Effekt('Projicerad själ',borta,figur,(aktiva_s, effekter, True),(aktiva_s, effekter, False), tid )
                            e.sluttid += tick
                            e.use()
                            effekter.append(e)
                        else:
                            print(namn+' fungerar bara om ni är flera')

                    if namn == 'Strategi':
                        print(figur.namn+' använder '+namn+'...')
                        if len(aktiva_s)>1:
                            for s in [spelare for spelare in aktiva_s if spelare.namn!=figur.namn]:
                                e=Effekt('Strategi',difstat,s,(0,-1,10,-3),(0,1,10,-3),10 )
                                e.sluttid+=tick
                                duplikat=False
                                for effekt in effekter:
                                    if effekt.namn==e.namn and effekt.target==e.target:
                                        effekter.remove(effekt)
                                        duplikat=True
                                if not duplikat:
                                    e.use()
                                effekter.append(e)
                            
                            del duplikat
                        else:
                            print(namn+' fungerar bara om ni är flera')

                    if namn == 'Tillbakaförvandling':
                        fv.tillbakaforvandling(figur)

                    if namn == 'Urkraft':
                        print(figur.namn+' hämtar kraft...')
                        e=Effekt(namn,difstat,figur,('mkr',0),('mkr',0), randint(3,7))
                        e.sluttid += tick
                        effekter.append(e)

                    if namn == 'Återhämtning' or namn == 'Återhämtning 2':
                        print(figur.namn+' använder '+namn+'...')
                        if namn == 'Återhämtning':
                            plus=int(figur.liv*0.2)
                        else:
                            plus=int(figur.liv*0.32)
                        figur.hp+=plus
                        if figur.hp>=figur.liv:
                            print(figur.namn+' fick full hp')
                            figur.hp=figur.liv
                        else:
                            print(figur.namn+' återhämtade '+str(plus)+' hp')

                    if namn == 'Älva':
                        fv.alva(figur)

                    
                    del namn

                    
                #FÖREMÅL    
                elif fightval(figur, inventory)[mode]=='Använd föremål':   
                    fightprylar=[sak for sak in [f for f in inventory if isinstance(f,EngangsForemal)] if sak.fight]
                    sak = fightprylar[listval([f.namn for f in fightprylar])]
                    #if not sak.target:
                    sp = aktiva_s[listval([s.namn for s in aktiva_s])]
                    res = sak.use(sp)
                    if res:
                        inventory.remove(sak)
                    else:
                        print(sp.namn+' kan inte bli hjälpt av det')
                    del res                         
                    del fightprylar
                    del sak


                #MAGI
                elif fightval(figur, inventory)[mode]=='Använd magi':   
                    print('magikraft: '+str(figur.stats['mkr']))
                    tillgangliga=[magi for magi in figur.magier if figur.stats['mkr']>=magi[1]]
                    spell=tillgangliga[listval([magi[0]+': '+str(magi[1])+' magikraft' for magi in tillgangliga])]

                    if spell[0] == 'Eld':
                        print(figur.namn+' använder '+spell[0]+'...')
                        for f in aktiva_f:
                            skada=int(figur.stats['mkr']*(2+random()) + figur.lvl*(0.5+random()*0.5) - f.mods[2]*2)
                            print(f.namn+' förlorar '+str(skada)+' hp')
                            f.hp-=skada
                            if f.hp<1:
                                print(f.namnB+' är medvetslös.')
                                f.hp = 0
                                borteffekter(effekter,f)
                                aktiva_f.remove(f)

                    elif spell[0] == 'Förtärande mörker':
                        target=listval([f.namn for f in aktiva_f])
                        print(figur.namn+' använder '+spell[0]+'...')
                        skada=int(figur.stats['mkr']*(randint(4,6)+figur.hp*0.02))
                        print(aktiva_f[target].namn+' förlorar '+str(skada)+' hp')
                        aktiva_f[target].hp-=skada
                        if aktiva_f[target].hp<1:
                            print(aktiva_f[target].namnB+' är medvetslös.')
                            aktiva_f[target].hp=0
                            borteffekter(effekter,aktiva_f[target])
                            aktiva_f.remove(aktiva_f[target])
                        sjalvskada=int(skada*0.3)
                        print(figur.namn+' förlorar '+str(sjalvskada)+' hp')
                        figur.hp -= sjalvskada
                        if figur.hp<1:
                            print(figur.namn+' är medvetslös.')
                            figur.hp=0
                            borteffekter(effekter,figur)
                            aktiva_s.remove(figur)
                            
                    elif spell[0] == 'Förvrida framtiden':
                        print(figur.namn+' använder '+spell[0]+'...')
                        for s in aktiva_s:
                            e=Effekt('Förutbestämmande',difstat,s,(3,4),(3,-4),int(figur.stats['mkr']*random()*0.4) + 5 )
                            e.sluttid+=tick
                            duplikat=False
                            for effekt in effekter:
                                if effekt.namn==e.namn and effekt.target==e.target:
                                    print(s.namn+' manipulerar redan tiden')
                                    duplikat=True
                            if not duplikat:
                                e.use()
                                effekter.append(e)
                        
                        del duplikat

                    elif spell[0] == 'Helning':
                        target=listval([s.namn for s in aktiva_s])
                        print(figur.namn+' använder '+spell[0]+'...')
                        plus=int(figur.stats['mkr']*randint(4,7) + aktiva_s[target].liv*0.1)
                        aktiva_s[target].hp+=plus
                        if aktiva_s[target].hp>=aktiva_s[target].liv:
                            print(aktiva_s[target].namn+' fick full hp')
                            aktiva_s[target].hp=aktiva_s[target].liv
                        else:
                            print(aktiva_s[target].namn+' återhämtade '+str(plus)+' hp')
                        del plus
                            
                    elif spell[0] == 'Hypnos':
                        target=listval([f.namn for f in aktiva_f])
                        print(figur.namn+' använder '+spell[0]+'...')
                        if figur.stats['mkr']*0.007+0.5+random()>1:
                            e=Effekt('Hypnos',difstat,aktiva_f[target],(0,6,10,-3),(0,-6,10,-3),randint(5,12))
                            e.sluttid+=tick
                            duplikat=False
                            for effekt in effekter:
                                if effekt.namn==e.namn and effekt.target==e.target:
                                    effekter.remove(effekt)
                                    duplikat=True
                            if not duplikat:
                                e.use()
                            effekter.append(e)
                            
                            del duplikat
                        else:
                            print('...men hypnosen misslyckas.')

                    elif spell[0] == 'Kyla':
                        target=listval([f.namn for f in aktiva_f])
                        print(figur.namn+' använder '+spell[0]+'...')
                        skada=int(figur.stats['mkr']*(2+random()) + figur.lvl*(0.5+random()*0.5) - aktiva_f[target].mods[2]*2)
                        print(aktiva_f[target].namn+' förlorar '+str(skada)+' hp')
                        aktiva_f[target].hp-=skada
                        if aktiva_f[target].hp<1:
                            print(aktiva_f[target].namnB+' är medvetslös.')
                            aktiva_f[target].hp=0
                            borteffekter(effekter,aktiva_f[target])
                            aktiva_f.remove(aktiva_f[target])

                    elif spell[0] == 'Lindring':
                        print(figur.namn+' använder '+spell[0]+'...')
                        plus=int(figur.stats['mkr']*(0.5+random()*0.5))
                        for s in aktiva_s:
                            s.hp+=plus+int(s.liv*0.2)
                            if s.hp>=s.liv:
                                print(s.namn+' fick full hp')
                                s.hp=s.liv
                            else:
                                print(s.namn+' återhämtade '+str(plus+int(s.liv*0.2))+' hp')
                        del plus

                    elif spell[0] == 'Livskraft':
                        n = len([s for s in s_lista if s.hp < 1])
                        if n < 1:
                            print(spell[0]+' kan bara användas om en följeslagare är medvetslös')
                            figur.stats['mkr'] += spell[1]
                        elif n == 1:
                            target = [s for s in s_lista if s.hp < 1][0]
                            print(figur.namn+' använder '+spell[0]+'...')
                            target.hp = target.liv
                            print(target.namn+' fick nya krafter!\n'+target.namn+' återfick full hp.')
                            aktiva_s.append(target)
                        else:
                            print(figur.namn+' använder '+spell[0]+'...')
                            for s in [sp for sp in s_lista if sp.hp < 1]:
                                s.hp = int(s.liv*0.5)
                                print(s.namn+' fick nya krafter!\n'+s.namn+' återfick halva sin hp.')
                                aktiva_s.append(s)

                    elif spell[0] == 'Mystisk attack':
                        print(figur.namn+' använder '+spell[0]+'...')
                        target=listval([f.namn for f in aktiva_f])
                        #kan inte missa
                        skada = figur.stats['str'] + figur.stats['mkr'] + figur.stats['smi'] + figur.hp/4
                        try:
                            skada += figur.utrust['vapen'].skada
                        except(AttributeError):
                            skada = skada
                        skada*=0.5+random()+random()
                        skada=int(skada - aktiva_f[target].rustning - aktiva_f[target].mods[2] - aktiva_f[target].stats['str']*0.1)
                        if skada < 1:
                            skada = 1
                        print(figur.namn+' attackerar '+aktiva_f[target].namnB+' och gör '+str(skada)+' skada.')
                        aktiva_f[target].hp-=skada
                        if aktiva_f[target].hp<1:
                            print(aktiva_f[target].namnB+' är medvetslös.')
                            aktiva_f[target].hp=0
                            borteffekter(effekter,aktiva_f[target])
                            aktiva_f.remove(aktiva_f[target])
                        sjalvskada = int(figur.hp/6)
                        print(figur.namn+' förlorar '+str(sjalvskada)+' hp')
                        figur.hp -= sjalvskada


                    elif spell[0] == 'Mörk attack':
                        print(figur.namn+' använder '+spell[0]+'...')
                        target=listval([f.namn for f in aktiva_f])
                        if figur.hit(aktiva_f[target]):
                            skada=figur.stats['str']*0.8 + figur.stats['mkr']
                            try:
                                skada += figur.utrust['vapen'].skada
                            except(AttributeError):
                                skada = skada
                            skada*=1.5+random()
                            skada=int(skada - aktiva_f[target].rustning - aktiva_f[target].mods[2] - aktiva_f[target].stats['str']*0.1)
                            if skada < 1:
                                skada = 1
                            print(figur.namn+' attackerar '+aktiva_f[target].namnB+' och gör '+str(skada)+' skada.')
                            aktiva_f[target].hp-=skada
                            if aktiva_f[target].hp<1:
                                print(aktiva_f[target].namnB+' är medvetslös.')
                                aktiva_f[target].hp=0
                                borteffekter(effekter,aktiva_f[target])
                                aktiva_f.remove(aktiva_f[target])
                        else:
                            print(figur.namn+' attackerar '+aktiva_f[target].namnB+' men missar.')

                    elif spell[0] == 'Se framtiden':
                        print(figur.namn+' använder '+spell[0]+'...')
                        for s in aktiva_s:
                            e=Effekt('Förutbestämmande',difstat,s,(3,2),(3,-2),int(figur.stats['mkr']*(0.3+random()*0.5)) + randint(8,10) )
                            e.sluttid+=tick
                            duplikat=False
                            for effekt in effekter:
                                if effekt.namn==e.namn and effekt.target==e.target:
                                    print(s.namn+' manipulerar redan tiden')
                                    duplikat=True
                            if not duplikat:
                                e.use()
                                effekter.append(e)
                        
                        del duplikat

                    elif spell[0] == 'Smärta':
                        target=listval([f.namn for f in aktiva_f])
                        print(figur.namn+' använder '+spell[0]+'...')
                        skada=int(figur.stats['mkr']*(1.5+random()) + figur.lvl*(0.5+random()*0.5) + aktiva_f[target].liv*0.1 - aktiva_f[target].mods[2]*2)
                        print(aktiva_f[target].namn+' förlorar '+str(skada)+' hp')
                        aktiva_f[target].hp-=skada
                        if aktiva_f[target].hp<1:
                            print(aktiva_f[target].namnB+' är medvetslös.')
                            aktiva_f[target].hp=0
                            borteffekter(effekter,aktiva_f[target])
                            aktiva_f.remove(aktiva_f[target])
                        else:
                            difstat(aktiva_f[target],0,int(skada*0.1))

                    elif spell[0] == 'Snabbhet':
                        print(figur.namn+' använder '+spell[0]+'...')
                        for s in aktiva_s:
                            e=Effekt('Snabbhet',difstat,s,(0,-2,10,-3),(0,2,10,-3),int(figur.lvl*0.4) + randint(2,5) )
                            e.sluttid+=tick
                            duplikat=False
                            for effekt in effekter:
                                if effekt.namn==e.namn and effekt.target==e.target:
                                    effekter.remove(effekt)
                                    duplikat=True
                            if not duplikat:
                                e.use()
                            effekter.append(e)
                        
                        del duplikat

                    elif spell[0] == 'Sömnighet':
                        print(figur.namn+' använder '+spell[0]+'...')
                        for f in aktiva_f:
                            minus=int(2 + figur.stats['mkr']*0.3*random())
                            e=Effekt('Sömnighet',difstat,f,(0,minus,10,-3),(0,-minus,10,-3),int(figur.stats['mkr']*0.5) + randint(5,10) )
                            e.sluttid+=tick
                            duplikat=False
                            for effekt in effekter:
                                if effekt.namn==e.namn and effekt.target==e.target:
                                    effekter.remove(effekt)
                                    duplikat=True
                            if not duplikat:
                                e.use()
                            effekter.append(e)
                        
                        del duplikat
                        del minus

                    elif spell[0] == 'Tillkvicknande':
                        if len([s for s in s_lista if s.hp < 1]) < 1:
                            print(spell[0]+' kan bara användas om en följeslagare är medvetslös')
                            figur.stats['mkr'] += spell[1]
                        else:
                            target = [s for s in s_lista if s.hp < 1][listval([s.namn for s in s_lista if s.hp < 1])]
                            print(figur.namn+' använder '+spell[0]+'...')
                            plus = int(target.liv*0.2 + figur.stats['mkr']*0.5)
                            target.hp = plus
                            print(target.namn+' fick nya krafter!\n'+target.namn+' återfick '+str(plus)+' hp.')
                            aktiva_s.append(target)

                    elif spell[0] == 'Trollstyrka':
                        target=listval([s.namn for s in aktiva_s])
                        print(figur.namn+' använder '+spell[0]+'...')
                        plus=int(figur.stats['mkr']*random()*0.8)
                        if plus < 1:
                            plus = 1
                        e=Effekt('Trollstyrka',difstat,aktiva_s[target],('str',plus),('str',-plus),int(figur.stats['mkr']*0.5) + randint(5,10) )
                        e.sluttid+=tick
                        duplikat=False
                        for effekt in effekter:
                            if effekt.namn==e.namn and effekt.target==e.target:
                                effekter.remove(effekt)
                                duplikat=True
                        if not duplikat:
                            e.use()
                        effekter.append(e)
                        
                        del duplikat
                        

                    elif spell[0] == 'Trollsmäll':
                        target=listval([f.namn for f in aktiva_f])
                        print(figur.namn+' använder '+spell[0]+'...')
                        skada=int(figur.stats['mkr']*8*random() + 40*random() - aktiva_f[target].mods[2]*2)
                        print(aktiva_f[target].namn+' förlorar '+str(skada)+' hp')
                        aktiva_f[target].hp-=skada
                        if aktiva_f[target].hp<1:
                            print(aktiva_f[target].namnB+' är medvetslös.')
                            aktiva_f[target].hp=0
                            borteffekter(effekter,aktiva_f[target])
                            aktiva_f.remove(aktiva_f[target])

                    elif spell[0] == 'Trollstoft':
                        print(figur.namn+' använder '+spell[0]+'...')
                        plus=int(figur.stats['mkr']*(0.8+random()))
                        for s in aktiva_s:
                            s.hp+=plus+int(s.liv*0.2)
                            if s.hp>=s.liv:
                                print(s.namn+' fick full hp')
                                s.hp=s.liv
                            else:
                                print(s.namn+' återhämtade '+str(plus+int(s.liv*0.25))+' hp')
                            e=Effekt('Trollstoft',difstat,s,(0,-1,10,-3),(0,1,10,-3),int(figur.stats['mkr']*0.5) + randint(5,10) )
                            e.sluttid+=tick
                            duplikat=False
                            for effekt in effekter:
                                if effekt.namn==e.namn and effekt.target==e.target:
                                    effekter.remove(effekt)
                                    duplikat=True
                            if not duplikat:
                                e.use()
                            effekter.append(e)
                        del plus
                        
                        del duplikat

                    elif spell[0] == 'Upplyftning':
                        print(figur.namn+' använder '+spell[0]+'...')
                        plus=int(figur.stats['mkr']*(1.5+random()))
                        for s in aktiva_s:
                            s.hp+=plus+int(s.liv*0.3)
                            if s.hp>=s.liv:
                                print(s.namn+' fick full hp')
                                s.hp=s.liv
                            else:
                                print(s.namn+' återhämtade '+str(plus)+' hp')
                        del plus

                    elif spell[0] == 'Ändra framtiden':
                        print(figur.namn+' använder '+spell[0]+'...')
                        for f in aktiva_f:
                            e=Effekt('Ute ur tiden',difstat,f,(0,30),(0,-30),randint(3,5)+int(figur.stats['mkr']*(0.2+random()*0.3)) + 1 )
                            e.sluttid+=tick
                            duplikat=False
                            for effekt in effekter:
                                if effekt.namn==e.namn and effekt.target==e.target:
                                    effekter.remove(effekt)
                                    duplikat=True
                            if not duplikat:
                                e.use()
                            effekter.append(e)
                        
                        del duplikat


                    else:
                        raise ValueError('fel namn')                    
                    figur.stats['mkr']-=spell[1]
                    del spell

                    
                elif fightval(figur, inventory)[mode]=='Fly':    #FLY
                    if max(s.klocka() for s in aktiva_s) -min(f.klocka() for f in aktiva_f)<randint(0,4):
                        print('Ni flyr.')
                        for s in s_lista:
                            for spelare in [sp for sp in spelarlista if sp.namn==s.namn]:
                                spelare.hp=s.hp
                        return
                    else:
                        print('Ni lyckas inte fly.')

                print('\n')
                        
        if aktiva_f==[]:   
            break
        tick+=1
        i = 0
        while i < len(effekter):
            if effekter[i].check(tick):
                effekter[i].cancel()
                effekter.remove(effekter[i])
            else:
                i += 1
        del i
        

    #SLUT
    print('Striden är över!')
    print('-----------------------------------------')
    
    for s in [sp for sp in aktiva_s if 'Tillbakaförvandling' in sp.formagor]:
        fv.tillbakaforvandling(s)

    for s in s_lista:     #hpdif
        for spelare in [sp for sp in spelarlista if sp.namn==s.namn]:
            spelare.hp=s.hp

    #Exp
    if OP == 1:
        xp = int(sum([f.exp+3 for f in fiender])*2)
    elif OP ==2:
        xp = sum([f.exp+10 for f in fiender])*3
    else:
        xp = sum([f.exp for f in fiender])
    print('Ni fick '+str(xp)+' exp')
    for s in spelarlista:
        s.exp += xp

    #Läkekonst
    lakekonst_lista=[0]
    for s in aktiva_s:
        if 'Läkekonst 2' in s.special:
            lakekonst_lista.append( (s.stats['smi'] + s.lvl + randint(0,2))*1.7 )
        elif 'Läkekonst' in s.special:
            lakekonst_lista.append( s.stats['smi'] + s.lvl + randint(0,2) )
    if max(lakekonst_lista)>0:
        print('Läkekonst:')
        for s in [sp for sp in spelarlista if sp.namn in [a.namn for a in aktiva_s] ]:
            s.hp  +=  int(s.liv * max(lakekonst_lista)*0.008)
            if s.hp>=s.liv:
                print(s.namn+' fick full hp')
                s.hp=s.liv
            else:
                print(s.namn+' återfick '+str(int(s.liv * max(lakekonst_lista)*0.008))+' hp')

    #Loot
    loot=[]
    if any('Skattletande 2' in formagor for formagor in (s.special for s in aktiva_s)):
        lycka = randint(2,3)
    elif any('Skattletande' in formagor for formagor in (s.special for s in aktiva_s)):
        lycka = randint(1,2)
    else:
        lycka = 0
    for f in fiender:
        drop = f.drop(lycka,progress,OP)
        if drop:
            loot.append(drop)
    if len(loot)>0:
        print('Ni hittade ' + ', '.join(loot) + '.')

    #specialdjur
    if 'Stentiger' in [f.namn for f in fiender]:
        progress['döda_fiender'].add('Stentiger')
            
    return loot




#Föremåls/magiers/förmågors funktioner    
def borta(spelare,alista,effekter,bort,noprint):
    if bort:
        borteffekter(effekter,spelare)
        alista.remove(spelare)
    else:
        alista.append(spelare)



#----------------------------------------------------------------------------------
#KONSTANTER

PDICT = {
    'skog':[
    ['En trollslända',fi.Trollslanda()],
    ['Två trollsländor',fi.Trollslanda(),fi.Trollslanda('B')],
    ['Tre vättar',fi.Vatte(),fi.Vatte('B'),fi.Vatte('C')],
    ['En vätte och ett skogstroll', fi.Vatte(),fi.Skogstroll()],
    ['Ett skogstroll',fi.Skogstroll()],
    ['En varg',fi.Varg()],
    ['Två vargar',fi.Varg(),fi.Varg('B')]
    ],    
    'berg':[
    ['En grådvärg',fi.Gradvarg()],
    ['Två grådvärgar',fi.Gradvarg(),fi.Gradvarg('B')],
    ['Två grådvärgar och två vättar',fi.Gradvarg(),fi.Gradvarg('B'),fi.Vatte(),fi.Vatte('B')],
    ['En stentiger',fi.Stentiger()],
    ['Två stentigrar',fi.Stentiger(),fi.Stentiger('B')],
    ['Ett bergatroll',fi.Bergatroll()],
    ['Ett bergatroll och en vätte',fi.Bergatroll(),fi.Vatte()]
    ],
    'Djupa dalen':[
    ['Tre trollsländor',fi.Trollslanda(),fi.Trollslanda('B'),fi.Trollslanda('C')],
    ['Två stentigrar',fi.Stentiger(),fi.Stentiger('B')],
    ['En vålnad',fi.Valnad()],
    ['En vålnad',fi.Valnad()],
    ['En vålnad',fi.Valnad()],
    ['Två vålnader',fi.Valnad(),fi.Valnad('B')]
    ],
    'skugglandskap':[
    ['En tanddvärg och en elak vätte', fi.Tanddvarg(),fi.ElVatte()],
    ['Två tanddvärgar', fi.Tanddvarg(),fi.Tanddvarg('B')],
    ['Två skuggkatter',fi.Skuggkatt(),fi.Skuggkatt('B')],
    ['Ett namnlöst vidunder',fi.Nvidunder()],
    ['Fyra elaka vättar',fi.ElVatte(),fi.ElVatte('B'),fi.ElVatte('C'),fi.ElVatte('D')]
    ],
    'mörkt vatten':[
    ['En elak vätte, en skuggkatt och en vålnad',fi.ElVatte(),fi.Skuggkatt(),fi.Valnad()],
    ['En magisk hjort',fi.Hjort()],
    ['Ett fiskmonster och en skuggkatt', fi.Fiskmonster(), fi.Skuggkatt()],
    ['Två fiskmonster', fi.Fiskmonster(),fi.Fiskmonster('B')],
    ['Två namnlösa vidunder och en tanddvärg', fi.Nvidunder(),fi.Nvidunder('B'),fi.Tanddvarg()],
    ['En demonpanter och en skuggkatt', fi.Demonpanter(), fi.Skuggkatt()]
    ],
    'Tornet':[
    ['Ett fiskmonster och en skuggkatt', fi.Fiskmonster(), fi.Skuggkatt()],
    ['Tre skuggkatter',fi.Skuggkatt(),fi.Skuggkatt('B'),fi.Skuggkatt('C')],
    ['Två namnlösa vidunder', fi.Nvidunder(),fi.Nvidunder('B')],
    ['Fyra elaka vättar',fi.ElVatte(),fi.ElVatte('B'),fi.ElVatte('C'),fi.ElVatte('D')]
    ]}

#för unika fiender och bestämda encounters
MDICT = {'Demonen Zlokr':fi.DemonenZ(),
         'Elaka häxan': fi.ElakaHaxan1(),
         'Vildsvinet': fi.Vildsvinet(),
         'Grisen': fi.Grisen(),
         'Zeoidodh': fi.Zeoidodh(),
         'Djurfrämlingen': fi.Djurframlingen(),
         'Gaurghus': fi.Gaurghus(),
         'Otak': fi.Otak(),
         'Joshki': fi.Joshki()}








