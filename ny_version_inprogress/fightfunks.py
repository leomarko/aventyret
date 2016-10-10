from funktioner import difstat, listval, slowprint, uniquelist
from random import random, randint
from copy import copy, deepcopy
from collections import OrderedDict
from klasser import EngangsForemal, Spelare
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

    def use(self):
        self.funktion(self.target,*self.args)

    def check(self,tick):
        if tick == self.sluttid:
            return True

    def cancel(self, noprint=False):
        if not noprint:
            print(self.target.namn+' är inte längre påverkad av '+self.namn)
        self.funktion(self.target,*self.reverse, noprint=noprint)




#--------------------------------------------------------------------------------------------------
#SEPARATA FUNKTIONER

def randomenc(plats):
    #ska kolla PDICT, där varje plats har en lista med fiendelistor
    #unika fiender kan inte vara i listorna, måste läggas in i main
    lista = PDICT[plats][randint(0,len(PDICT[plats])-1)]
    gruppnamn = lista[0]
    fiender = [f for f in lista[1:]] 
    return (gruppnamn, fiender)

def helning(figur, target, mod, mod2=0.2, plus=0):
    if isinstance(target, list):
        for s in target:
            helning = int(figur.stats['mkr']*(mod+random()) + s.liv*mod2 + plus)
            difstat(s,'hp',helning)
    else:
        helning = int(figur.stats['mkr']*(mod+random()) + target.liv*mod2 + plus)
        difstat(target,'hp',helning)
                
def f_meny(lista):
    try:
        n = listval(lista+['Ångra'])
    except(TypeError):
        n = listval([f.namn for f in lista]+['Ångra'])
    if n == len(lista): #gå tillbaka
        return False
    return lista[n]

def magi_meny(magier, mkr, dubbel=False):
    tillgangliga = [magi for magi in magier if mkr >= magi[1]]
    if not dubbel:
        spell = listval([m[0]+': '+str(m[1])+' magikraft' for m in tillgangliga]+['Ångra'])
    else:
        spell = listval([m[0]+': '+str(m[1])+' magikraft' for m in tillgangliga]+['(Ingen)'])
    if spell == len(tillgangliga):
        return False
    return tillgangliga[spell]
    
def fmal_meny(inventory, aktiva_s, aktiva_f):
    fightprylar=[sak for sak in [f for f in inventory if isinstance(f,EngangsForemal)] if sak.fight]
    ordered = uniquelist(fightprylar)
    antal = OrderedDict()
    for f in ordered:
        antal[f.namn] = inventory.count(f)
    display = [f.namn for f in ordered]
    for i in range(len(display)):
        display[i] += ' ('+ordered[i].bs+')'
        if antal[ordered[i].namn] > 1:
            display[i] += ' ('+str(antal[ordered[i].namn])+'st)'
    obj = listval(display+['Ångra'])
    if obj == len(display): #gå tillbaka
        return False
    sak = ordered[obj]
    sp = aktiva_s[listval([s.namn for s in aktiva_s])]
    res = sak.use(sp)
    if res:
        inventory.remove(sak)
    else:
        print(sp.namn+' kan inte bli hjälpt av det')
    return True


#----------------------------------------------------------------------------
#FIGHT

def fight(spelarlista, inventory, progress, plats, specifik=False, OP=0):
    #för randomencouter är plats en string, annars lista med namn

    #-------------------INBYGGDA FUNKTIONER--------------------
    def fightval(spelare):
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

    def statusrad(bedomning=False):
        def statusstrings(lista):
            statusstrings=[]
            for s in lista:
                sta = s.namn+':'+s.hpstr()+'  '+' '.join('"'+e.namn+'"' for e in effekter if e.target == s)
                statusstrings.append(sta)
            return statusstrings   
        if bedomning:
            print('Bedömning   '+'\n            '.join(statusstrings(aktiva_f)))
        else:
            print('Status   '+'\n         '.join(statusstrings(aktiva_s)))
        
    def uppdatera_effekter(e, annan_ekvivalent=False, ifmsg='', use=True):
        e.sluttid += tick
        duplikat = False
        for effekt in effekter:
            if effekt.namn == e.namn and effekt.target == e.target:
                duplikat = True
                if not annan_ekvivalent:
                    effekter.remove(effekt)
                break
        if use and not duplikat:
            e.use()
        if not annan_ekvivalent or not duplikat:
            effekter.append(e)
        else:
            print(ifmsg)
        
    def aktivlista(figur):
        if isinstance(figur,Spelare):
            return aktiva_s
        else:
            return aktiva_f

    def taskada(figur,skada):
        if isinstance(figur,Spelare):
            print(figur.namn+' förlorar '+str(skada)+' hp')
        else:
            print(figur.namnB+' förlorar '+str(skada)+' hp')
        figur.hp-=skada
        k_o(figur)
        
    def k_o(target):   
        def inbyggd_k_o(figur):
            if figur.hp<1:
                figur.hp=0
                if isinstance(figur,Spelare):
                    print(figur.namn+' är medvetslös.')
                else:
                    print(figur.namnB+' är medvetslös.')
                borta(figur)
                return True
            else:
                return False
        if isinstance(target,list):
            i = 0
            while i < len(target):
                if not inbyggd_k_o(target[i]):
                    i += 1
        else:
            return inbyggd_k_o(target)
                
    def borteffekter(figur):
        i = 0
        while i < len(effekter):
            if effekter[i].target == figur:
                effekter[i].cancel(noprint=True)
                effekter.remove(effekter[i])
            else:
                i += 1

    def borta(figur,bort=True):
        lista = aktivlista(figur)
        if bort:
            borteffekter(figur)
            lista.remove(figur)
        else:
            lista.append(figur)

    def attackmagi(figur,target,mod,plus=0):
        if isinstance(target, list):
            for f in target:
                skada = int(figur.stats['mkr']*(mod+random()) + plus - f.mods[2]*2)
                taskada(f,skada)
        else:
            skada = int(figur.stats['mkr']*(mod+random()) + plus - target.mods[2]*2)
            taskada(target,skada)
        return skada

    def attack(a, b, nyckelord=''):
        ggr = 1
        spelare = False
        if isinstance(a,Spelare):
            spelare = True
            
        #dubbel            
        if 'dubbel' in nyckelord:
            if not spelare or a.stats['smi']*0.07 + 2.3*random()  >  2:
                ggr = 2
        #loop
        while ggr > 0:
            if a.hit(b) or nyckelord == 'mystisk':
                
                #grundskada
                if nyckelord == 'mystisk':
                    skada = sum(a.stats.values()) + figur.hp/4
                elif nyckelord == 'mörk':
                    skada = a.stats['mkr']*0.85 + a.stats['str']*0.85
                else:
                    skada = a.stats['str']
                try:
                    skada += figur.utrust['vapen'].skada
                except(AttributeError):
                    skada = skada
                    
                #slutskada
                if 'critical' in nyckelord:
                    if not spelare or randint(0,4) == 4:
                        skada = int(skada*(2.5 + random() + random()))
                        if spelare:
                            print('Lyckoträff!')
                        else:
                            print('Förödande attack...!')
                elif nyckelord == 'mystisk':
                    skada = int(skada*(0.5 + random() + random()))
                elif nyckelord == 'djärv':
                    skada = int(skada*(2 + random() + random()))
                else:
                    skada = int(skada*(1.5 + random()))

                #rustning    
                skada -= int(b.mods[2] + b.stats['str']*0.1)
                if spelare:
                    skada -= b.rustning
                else:
                    try:
                        skada -= b.utrust['rustning'].skydd
                    except(AttributeError,NameError):
                        skada=skada

                #minimi
                if skada < 1:
                    skada = 1
                b.hp -= skada

                #resultat    
                if spelare:
                    print(a.namn+' attackerar '+b.namnB+' och gör '+str(skada)+' skada.')
                else:
                    print(a.namnB+' attackerar '+b.namn+' och gör '+str(skada)+' skada.')
                if nyckelord == 'djärv':
                    taskada(a, int(skada*(random()*0.35)))
                    
            else: #(miss)
                if spelare:
                    print(a.namn+' attackerar '+b.namnB+' men missar.')
                else:
                    print(a.namnB+' attackerar '+b.namn+' men missar.')
                if nyckelord == 'djärv':
                    taskada(a, int(a.stats['str']*random()))
                    
            if ggr == 2:
                print('Dubbel attack!')
            ggr -= 1
            
        k_o(b)
    
    #-----------------Upplägg och variabler-----------------------
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

    #-----------------------------------LOOP---------------------------------
    while True:
        #----------------------FIENDER----------------------------------
        for figur in aktiva_f:
            if aktiva_s==[]:
                print('Du är besegrad.\nSlut på äventyret.')
                raise SystemExit
            if tick % figur.klocka() == 0:
                print(figur.namn+'s tur')
                input('(tryck enter)')
                mode = figur.mode()

                if mode == 'attack' or mode == 'critical' or mode == 'dubbel':
                    target = aktiva_s[randint(0,len(aktiva_s)-1)]
                    attack(figur, target, mode)

                elif mode == 'other':
                    figur.other()

                elif mode == 'fly':
                    print(figur.namnB+' flyr!')
                    if len(fiender) == 1:
                        return
                    else:
                        borta(figur)
                        f_lista.remove(figur)

                #Nedan alla fienders förmågor och magier. Fiender betalar inte mp
                else:
                    print(figur.namnB+' använder '+mode+'...')

                    if mode == 'Eld':
                        attackmagi(figur, aktiva_s, 2.5)

                    elif mode == 'Förtärande mörker':
                        target = aktiva_s[randint(0,len(aktiva_s)-1)]
                        skada=int(figur.stats['mkr']*(randint(4,6)+figur.hp*0.02))
                        taskada(target,skada)
                        taskada(figur, int(skada*0.3))
                            
                    elif mode == 'Förvrida framtiden':
                        for f in aktiva_f:
                            e=Effekt('Förutbestämmande',difstat,f,(3,4),(3,-4),int(figur.stats['mkr']*random()*0.4) + 5 )
                            uppdatera_effekter(e, annan_ekvivalent=True, ifmsg=f.namn+' manipulerar redan tiden')
                            
                    elif mode == 'Hypnos':
                        target = aktiva_s[randint(0,len(aktiva_s)-1)]
                        if (figur.stats['mkr']+5)*random()*10 > target.liv*0.5 + target.mods[2]*10:
                            e=Effekt('Hypnos',difstat,target,(0,7,10,-3),(0,-7,10,-3),randint(5,12))
                            uppdatera_effekter(e)
                        else:
                            print('...men hypnosen misslyckas.')

                    elif mode == 'Kvävning':
                        for s in aktiva_s:
                            taskada(s, int(s.liv*0.2))
                            
                    elif mode == 'Smärta':
                        target = aktiva_s[randint(0,len(aktiva_s)-1)]
                        attackmagi(figur, target, 2, plus=target.liv*(0.5+random()*0.5))
                        if target in aktiva_s: 
                            difstat(target,0,1)

                    elif mode == 'Stank':
                        for s in aktiva_s:
                            difstat(s,'mkr',-3)
                            e = Effekt('Illamående',difstat,s,('smi',-3),('smi',+3),8)
                            uppdatera_effekter(e)
                            e = Effekt('Utmattning',difstat,s,('str',-3),('str',+3),8)
                            uppdatera_effekter(e)
               
                    elif mode == 'Trollsmäll':
                        target = aktiva_s[randint(0,len(aktiva_s)-1)]
                        attackmagi(figur, target, 8, 40*random())

                    elif mode == 'Trollstoft':
                        helning(figur, aktiva_f, 0.8)
                        for f in aktiva_f:
                            e=Effekt('Trollstoft',difstat,f,(0,-1,10,-3),(0,1,10,-3),int(figur.stats['mkr']*0.5) + randint(5,10) )
                            uppdatera_effekter(e)

                    elif mode == 'Återhämtning':
                        difstat(figur, 'hp', int(figur.liv*0.2))
                    elif mode == 'Återhämtning 2':
                        difstat(figur, 'hp', int(figur.liv*0.32))
                        
                    elif mode == 'Ändra framtiden':
                        for s in aktiva_s:
                            e=Effekt('Ute ur tiden',difstat,s,(0,30),(0,-30),randint(3,5)+int(figur.stats['mkr']*(0.2+random()*0.3)) + 1 )
                            uppdatera_effekter(e)

                    else:
                        raise ValueError('Fel mode')

                del mode
                print('\n')

        #SPELARE        
        for figur in aktiva_s:
            if tick % figur.klocka() == 0:
                turer = 1
                while turer > 0: #LOOP FÖR VARJE TUR
                    if aktiva_f == []:   
                        break
                    print(figur.namn+'s tur')
                    if any('Urkraft' in e.namn for e in effekter if e.target == figur):
                        figur.stats['mkr'] += 2
                        print('Urkraft: '+figur.namn+' får 2 magikraft.')
                    elif any('Mystisk kraft' in e.namn for e in effekter if e.target == figur):
                        figur.stats['mkr'] += 1
                        print('Mystisk kraft: '+figur.namn+' får 1 magikraft.')
                        
                    while True: #LOOP TILLS MAN BESTÄMT HANDLING
                        statusrad()
                        if any('Bedömning' in formagor for formagor in (s.special for s in aktiva_s)):
                            statusrad(bedomning=True)
                        print(figur.namn)
                        mode = fightval(figur)[listval(fightval(figur))]

                        #ATTACK
                        if mode == 'Attackera':
                            target = f_meny(aktiva_f)
                            if not target: #gå tillbaka
                                continue
                            kw = ''
                            if 'Dubbel attack' in figur.special:
                                kw += 'dubbel'
                            if 'Lyckoträff' in figur.special:
                                kw += 'critical'
                            attack(figur,target,nyckelord=kw)
                            break

                        #FÖRMÅGA
                        elif mode=='Använd förmåga':   
                            namn = f_meny(figur.formagor)
                            if not namn: #gå tillbaka
                                continue
                            
                            if namn == 'Djärv attack':
                                target=listval([f.namn for f in aktiva_f])
                                attack(figur, aktiva_f[target], 'djärv')
                                
                            elif namn == 'Fågel':
                                fv.fagel(figur)

                            elif namn == 'Gorilla':
                                fv.gorilla(figur)

                            elif namn == 'Lura naturen':
                                turer += 3
                                figur.formagor.remove(namn)

                            elif namn == 'Mystisk kraft':
                                print(figur.namn+' hämtar kraft...')
                                e=Effekt(namn,difstat,figur,('mkr',0),('mkr',0), int(10 + figur.lvl*0.4))
                                uppdatera_effekter(e, use=False)
                                
                            elif namn == 'Projicera själ':
                                print(figur.namn+' använder '+namn+'...')
                                if len(aktiva_s)>1:
                                    print(figur.namn+' lämnar sin kroppsliga form')
                                    tid = int(6 + figur.lvl*0.1)
                                    for s in [spelare for spelare in aktiva_s if spelare.namn!=figur.namn]:
                                        e=Effekt(figur.namn+'s armar',difstat,s,('str',int(figur.stats['str']*0.7)),('str',-int(figur.stats['str']*0.7)),tid )
                                        uppdatera_effekter(e)

                                        e=Effekt(figur.namn+'s kunskap',difstat,s,('smi',int(figur.stats['smi']*0.7)),('smi',-int(figur.stats['smi']*0.7)),tid )
                                        uppdatera_effekter(e)

                                        e=Effekt(figur.namn+'s hjärta',difstat,s,('mkr',int(figur.stats['mkr']*0.7)),('mkr',-int(figur.stats['mkr']*0.7)),tid )
                                        uppdatera_effekter(e)

                                    e=Effekt('Projicerad själ',borta,figur,[True],[False], tid )
                                    uppdatera_effekter(e)
                                else:
                                    print(namn+' fungerar bara om ni är flera')
                                    continue

                            elif namn == 'Strategi':
                                print(figur.namn+' använder '+namn+'...')
                                if len(aktiva_s)>1:
                                    for s in [spelare for spelare in aktiva_s if spelare.namn!=figur.namn]:
                                        e=Effekt('Strategi',difstat,s,(0,-1,10,-3),(0,1,10,-3),10 )
                                        uppdatera_effekter(e)
                                else:
                                    print(namn+' fungerar bara om ni är flera')
                                    continue

                            elif namn == 'Tillbakaförvandling':
                                fv.tillbakaforvandling(figur)

                            elif namn == 'Urkraft':
                                print(figur.namn+' hämtar kraft...')
                                e=Effekt(namn,difstat,figur,('mkr',0),('mkr',0), randint(3,7))
                                uppdatera_effekter(e, use=False)

                            elif namn == 'Återhämtning':
                                difstat(figur, 'hp', int(figur.liv*0.2))
                            elif namn == 'Återhämtning 2':
                                difstat(figur, 'hp', int(figur.liv*0.32))

                            elif namn == 'Älva':
                                fv.alva(figur)

                            else:
                                raise ValueError('Fel mode')
                            
                            del namn
                            break

                            
                        #FÖREMÅL    
                        elif mode == 'Använd föremål':
                            res = fmal_meny(inventory, aktiva_s, aktiva_f)
                            if res:
                                break

                        #MAGI
                        elif mode == 'Använd magi':
                            antalmagier = 1
                            done = True
                            if 'Dubbel magi' in figur.special:
                                antalmagier += 1
                            for i in range(antalmagier):
                                print('magikraft: '+str(figur.stats['mkr']))
                                if i == 0:
                                    spell = magi_meny(figur.magier,figur.stats['mkr'])
                                    if not spell: #gå tillbaka
                                        done = False #för att inte bryta andra loopen också
                                        break
                                else: #(dubbel)
                                    print('Välj en magi till')
                                    spell = magi_meny(figur.magier,figur.stats['mkr'],dubbel=True)
                                    if not spell:
                                        break #även om man går tillbaka är man klar för turen
                                    
                                if spell[0] == 'Beskydd':
                                    print(figur.namn+' använder '+spell[0]+'...')
                                    for s in aktiva_s:
                                        e=Effekt('Beskydd',difstat,s,(2,5),(2,-5),int(figur.stats['mkr']*(0.3+random()*0.5)) + randint(7,9) )                                        
                                        uppdatera_effekter(e)

                                elif spell[0] == 'Eld':
                                    print(figur.namn+' använder '+spell[0]+'...')
                                    attackmagi(figur, aktiva_f, 2, figur.lvl*(0.5+random()*0.5))

                                elif spell[0] == 'Förtärande mörker':
                                    target=aktiva_f[listval([f.namn for f in aktiva_f])]
                                    print(figur.namn+' använder '+spell[0]+'...')
                                    skada=int(figur.stats['mkr']*(randint(4,6)+figur.hp*0.02))
                                    taskada(target,skada)
                                    taskada(figur,int(skada*0.3))
                                        
                                elif spell[0] == 'Förvrida framtiden':
                                    print(figur.namn+' använder '+spell[0]+'...')
                                    for s in aktiva_s:
                                        e=Effekt('Förutbestämmande',difstat,s,(3,4),(3,-4),int(figur.stats['mkr']*random()*0.4) + 5 )
                                        uppdatera_effekter(e, annan_ekvivalent=True, ifmsg=s.namn+' manipulerar redan tiden')

                                elif spell[0] == 'Helning':
                                    target=aktiva_s[listval([s.namn for s in aktiva_s])]
                                    print(figur.namn+' använder '+spell[0]+'...')
                                    helning(figur, target, 3, mod2=0.3)
                                        
                                elif spell[0] == 'Hypnos':
                                    target=aktiva_f[listval([f.namn for f in aktiva_f])]
                                    print(figur.namn+' använder '+spell[0]+'...')
                                    if (figur.stats['mkr']+5)*random()*10 > target.liv*0.5 + target.mods[2]*10:
                                        e=Effekt('Hypnos',difstat,target,(0,7,10,-3),(0,-7,10,-3),randint(5,12))                                    
                                        uppdatera_effekter(e)
                                    else:
                                        print('...men hypnosen misslyckas.')

                                elif spell[0] == 'Kyla':
                                    target=aktiva_f[listval([f.namn for f in aktiva_f])]
                                    print(figur.namn+' använder '+spell[0]+'...')
                                    attackmagi(figur, target, 2, plus=figur.lvl*(0.5+random()*0.5))

                                elif spell[0] == 'Lindring':
                                    print(figur.namn+' använder '+spell[0]+'...')
                                    helning(figur, aktiva_s, 1)

                                elif spell[0] == 'Livskraft':
                                    n = len([s for s in s_lista if s.hp < 1])
                                    if n < 1:
                                        print(spell[0]+' kan bara användas om en följeslagare är medvetslös')
                                        if i == 0:
                                            done = False #om det är ens första magi får man välja om från början
                                        break
                                    print(figur.namn+' använder '+spell[0]+'...')
                                    if n == 1:
                                        target = [s for s in s_lista if s.hp < 1][0]
                                        target.hp = target.liv
                                        print(target.namn+' fick nya krafter!\n'+target.namn+' återfick full hp.')
                                        aktiva_s.append(target)
                                    else:
                                        for s in [sp for sp in s_lista if sp.hp < 1]:
                                            s.hp = int(s.liv*0.5)
                                            print(s.namn+' fick nya krafter!\n'+s.namn+' återfick halva sin hp.')
                                            aktiva_s.append(s)

                                elif spell[0] == 'Mystisk attack':
                                    target = aktiva_f[listval([f.namn for f in aktiva_f])]
                                    attack(figur,target,'mystisk')
                                    taskada(figur, int(figur.hp/6))

                                elif spell[0] == 'Mörk attack':
                                    target = aktiva_f[listval([f.namn for f in aktiva_f])]
                                    attack(figur,target,'mörk')

                                elif spell[0] == 'Se framtiden':
                                    print(figur.namn+' använder '+spell[0]+'...')
                                    for s in aktiva_s:
                                        e=Effekt('Förutbestämmande',difstat,s,(3,2),(3,-2),int(figur.stats['mkr']*(0.3+random()*0.5)) + randint(8,10) )
                                        uppdatera_effekter(e, annan_ekvivalent=True, ifmsg=s.namn+' manipulerar redan tiden')

                                elif spell[0] == 'Smärta':
                                    target=aktiva_f[listval([f.namn for f in aktiva_f])]
                                    print(figur.namn+' använder '+spell[0]+'...')
                                    attackmagi(figur, target, 2, plus=target.liv*(0.5+random()*0.5))
                                    if target in aktiva_f: 
                                        difstat(target,0,1)

                                elif spell[0] == 'Snabbhet':
                                    print(figur.namn+' använder '+spell[0]+'...')
                                    for s in aktiva_s:
                                        e=Effekt('Snabbhet',difstat,s,(0,-2,10,-4),(0,2,10,-4),int(figur.lvl*0.4) + randint(2,5) )
                                        uppdatera_effekter(e)

                                elif spell[0] == 'Sömnighet':
                                    print(figur.namn+' använder '+spell[0]+'...')
                                    for f in aktiva_f:
                                        e=Effekt('Sömnighet',difstat,f,(0,2,10,-4),(0,-2,10,-4),int(figur.stats['mkr']*random()) + 6 )
                                        uppdatera_effekter(e)

                                elif spell[0] == 'Tillkvicknande':
                                    if len([s for s in s_lista if s.hp < 1]) < 1:
                                        print(spell[0]+' kan bara användas om en följeslagare är medvetslös')
                                        if i == 0:
                                            done = False #om det är ens första magi får man välja om från början
                                        break
                                    else:
                                        target = [s for s in s_lista if s.hp < 1][listval([s.namn for s in s_lista if s.hp < 1])]
                                        print(figur.namn+' använder '+spell[0]+'...')
                                        target.hp = int(target.liv*0.2 + figur.stats['mkr']*0.5)
                                        print(target.namn+' fick nya krafter!\n'+target.namn+' återfick '+str(target.hp)+' hp.')
                                        aktiva_s.append(target)

                                elif spell[0] == 'Trollstyrka':
                                    target=aktiva_s[listval([s.namn for s in aktiva_s])]
                                    print(figur.namn+' använder '+spell[0]+'...')
                                    plus=int(figur.stats['mkr']*random()*0.8)
                                    if plus < 1:
                                        plus = 1
                                    e=Effekt('Trollstyrka',difstat,target,('str',plus),('str',-plus),int(figur.stats['mkr']*0.5) + randint(5,10) )
                                    uppdatera_effekter(e)

                                elif spell[0] == 'Trollsmäll':
                                    target=listval([f.namn for f in aktiva_f])
                                    print(figur.namn+' använder '+spell[0]+'...')
                                    attackmagi(figur, target, 8, plus=40*random())

                                elif spell[0] == 'Trollstoft':
                                    print(figur.namn+' använder '+spell[0]+'...')
                                    helning(figur, aktiva_s, 0.8)
                                    for s in aktiva_s:
                                        e=Effekt('Trollstoft',difstat,s,(0,-1,10,-3),(0,1,10,-3),int(figur.stats['mkr']*0.5) + randint(5,10) )
                                        uppdatera_effekter(e)

                                elif spell[0] == 'Upplyftning':
                                    print(figur.namn+' använder '+spell[0]+'...')
                                    helning(figur, aktiva_s, 3, mod2=0.3)
                                    
                                elif spell[0] == 'Ändra framtiden':
                                    print(figur.namn+' använder '+spell[0]+'...')
                                    for f in aktiva_f:
                                        e=Effekt('Ute ur tiden',difstat,f,(0,30),(0,-30),randint(3,5)+int(figur.stats['mkr']*(0.2+random()*0.3)) + 1 )
                                        uppdatera_effekter(e)

                                else:
                                    raise ValueError('fel namn')                    
                                figur.stats['mkr']-=spell[1]
                                
                            #efter antalmagier-loop:    
                            del spell
                            del antalmagier
                            if done:
                                break
                            
                        elif mode == 'Fly':    #FLY
                            if max(s.klocka() for s in aktiva_s) -min(f.klocka() for f in aktiva_f) < randint(0,4):
                                print('Ni flyr.')
                                for s in s_lista:
                                    for spelare in [sp for sp in spelarlista if sp.namn==s.namn]:
                                        spelare.hp=s.hp
                                return
                            else:
                                print('Ni lyckas inte fly.')

                    print('\n')
                    turer -= 1
                        
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
