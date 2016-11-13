from random import randint, random, shuffle
import os
import time

import klasser as kls
from fightfunks import fight as fightfunc
from lvlup import lvlup
from funktioner import difstat, plusformaga, listval, slowprint, uniquelist, overgang3till4
from collections import OrderedDict

#lägg till / testa:



######################       FUNKTIONER        #############################


#variabler för sparfunktion
savedir=os.curdir+'\\'
aktuell_sparfil=''

#sparfunktion
def spara(kopia=False):
    global aktuell_sparfil
    if aktuell_sparfil!='':
        namn=aktuell_sparfil
        if kopia:
            namn = aktuell_sparfil[:-4] + '_kopia.txt'
    else:
        while True:
            namn=savedir
            namn+=input('Namnge äventyret\n') + '.txt'
            try:
                assert 1==1
                #Bör ändras till relevant assertion vad ett namn kan vara
            except(AssertionError):
                print('Ogiltigt namn')
                continue
            break
        aktuell_sparfil=namn

    #kompatibilitet med äldre filer
    try:
        if inventory[0].namn == 'Gå tillbaka':
            inventory.remove(inventory[0])
    except(IndexError):
        pass
        
    with open(namn,'w') as f:
        f.write(sp1.namn
                +'\n'+str(sp1.liv)+'___'+str(sp1.hp) #2
                +'\n'+str(sp1.stats['str'])+'___'+str(sp1.stats['smi'])+'___'+str(sp1.stats['mkr']) #3
                +'\n'+'___'.join([str(m) for m in sp1.mods]) #4
                +'\n'+sp1.utrust['vapen'].namn+'___'+sp1.utrust['rustning'].namn+'___'+sp1.utrust['ovrigt'].namn #5
                +'\n'+'___'.join([u[0] for u in sp1.utveckling]) #6
                +'\n'+'___'.join([str(u[1]) for u in sp1.utveckling]) #7
                +'\n'+str(sp1.exp)+'___'+str(sp1.lvl) #8
                +'\n'+'___'.join(sp1.formagor) #9
                +'\n'+'___'.join([m[0] for m in sp1.magier]) #10
                +'\n'+'___'.join([str(m[1]) for m in sp1.magier]) #11
                +'\n'+'___'.join(sp1.special) #12
                +'\n'+str(svan.liv)+'___'+str(svan.hp) 
                +'\n'+str(svan.stats['str'])+'___'+str(svan.stats['smi'])+'___'+str(svan.stats['mkr']) 
                +'\n'+'___'.join([str(m) for m in svan.mods]) 
                +'\n'+svan.utrust['vapen'].namn+'___'+svan.utrust['rustning'].namn+'___'+svan.utrust['ovrigt'].namn
                +'\n'+'___'.join([u[0] for u in svan.utveckling]) 
                +'\n'+'___'.join([str(u[1]) for u in svan.utveckling]) 
                +'\n'+str(svan.exp)+'___'+str(svan.lvl) 
                +'\n'+'___'.join(svan.formagor) 
                +'\n'+'___'.join([m[0] for m in svan.magier]) 
                +'\n'+'___'.join([str(m[1]) for m in svan.magier]) 
                +'\n'+'___'.join(svan.special) #23
                +'\n'+str(alri.liv)+'___'+str(alri.hp) 
                +'\n'+str(alri.stats['str'])+'___'+str(alri.stats['smi'])+'___'+str(alri.stats['mkr']) 
                +'\n'+'___'.join([str(m) for m in alri.mods]) 
                +'\n'+alri.utrust['vapen'].namn+'___'+alri.utrust['rustning'].namn+'___'+alri.utrust['ovrigt'].namn
                +'\n'+'___'.join([u[0] for u in alri.utveckling]) 
                +'\n'+'___'.join([str(u[1]) for u in alri.utveckling]) 
                +'\n'+str(alri.exp)+'___'+str(alri.lvl)
                +'\n'+'___'.join(alri.formagor)
                +'\n'+'___'.join([m[0] for m in alri.magier]) 
                +'\n'+'___'.join([str(m[1]) for m in alri.magier]) 
                +'\n'+'___'.join(alri.special) #34
                +'\n'+str(progress['main'])+'___'+str(progress['häxan'])+'___'+str(progress['smeden'])+'___'+str(progress['alkemisten']) #35
                +'\n'+'___'.join(progress['hittade_skatter']) #36
                +'\n'+'___'.join([str(p) for p in progress['upptäckta_platser']]) #37
                +'\n'+'___'.join(progress['döda_fiender']) #38
                +'\n'+'___'.join([str(dialogval.index(i)) for i in dialogval if isinstance(i,str)]) #39
                +'\n'+'___'.join([i for i in dialogval if isinstance(i,str)]) #40
                +'\n'+'___'.join([f.namn for f in inventory])+'\n') #41
        if dvargen in spelarlista: #42
            f.write('d\n')
        elif alri in spelarlista:
            f.write('a\n')
        else:
            f.write('x\n')
        f.write(str(position)+'\n') #43
        #av kompatibilitetsskäl läggs dvärgen in sist
        f.write(str(dvargen.liv)+'___'+str(dvargen.hp) 
                +'\n'+str(dvargen.stats['str'])+'___'+str(dvargen.stats['smi'])+'___'+str(dvargen.stats['mkr']) 
                +'\n'+'___'.join([str(m) for m in dvargen.mods]) 
                +'\n'+dvargen.utrust['vapen'].namn+'___'+dvargen.utrust['rustning'].namn+'___'+dvargen.utrust['ovrigt'].namn
                +'\n'+'___'.join([u[0] for u in dvargen.utveckling]) 
                +'\n'+'___'.join([str(u[1]) for u in dvargen.utveckling]) 
                +'\n'+str(dvargen.exp)+'___'+str(dvargen.lvl)
                +'\n'+'___'.join(dvargen.formagor)
                +'\n'+'___'.join([m[0] for m in dvargen.magier]) 
                +'\n'+'___'.join([str(m[1]) for m in dvargen.magier]) 
                +'\n'+'___'.join(dvargen.special)) #54
    
#laddfunktion
def ladda():
    global spelarlista
    global inventory
    global position
    global progress
    global aktuell_sparfil
    global dialogval

    filer = [n for n in os.listdir(savedir) if n[-4:] == '.txt']
    print('Ange vilket äventyr med en siffra')
    nummer = listval([n[:-4] for n in filer])
    laddfil = savedir+filer[nummer]
    aktuell_sparfil = laddfil
    
    with open(laddfil) as f:
        sp1.namn = f.readline().strip()                               #1
        liv_hp = list(map(int,f.readline().strip('\n').split('___')))          #2
        sp1.liv, sp1.hp = liv_hp
        stats = list(map(int,f.readline().strip('\n').split('___')))           #3
        sp1.stats['str'], sp1.stats['smi'], sp1.stats['mkr'] = stats
        mods = list(map(int,f.readline().strip('\n').split('___')))            #4
        sp1.mods = mods
        utr = f.readline().strip('\n').split('___')                            #5
        utr = [FDICT[utr[0]],FDICT[utr[1]],FDICT[utr[2]]]
        sp1.utrust['vapen'], sp1.utrust['rustning'], sp1.utrust['ovrigt'] = utr
        utv_1 =  f.readline().strip('\n').split('___')                         #6
        utv_2 = list(map(int,f.readline().strip('\n').split('___')))           #7
        sp1.utveckling = []
        for u,v in zip(utv_1,utv_2):
            sp1.utveckling.append([u,v])
        exp_lvl = list(map(int,f.readline().strip('\n').split('___')))         #8
        sp1.exp, sp1.lvl = exp_lvl
        line = f.readline().strip('\n')
        if len(line) > 1:
            sp1.formagor = line.split('___')                   #9
        magier_1 = f.readline().strip('\n').split('___')                       #10
        try:
            magier_2 = list(map(int,f.readline().strip('\n').split('___')))        
            sp1.magier = []
            for m, k in zip(magier_1,magier_2):
                sp1.magier.append((m,k))
        except(ValueError):
            sp1.magier = []
        line = f.readline().strip('\n')
        if len(line) > 1:            
            sp1.special = line.split('___')                    #12

        #svan
        liv_hp = list(map(int,f.readline().strip('\n').split('___')))          
        svan.liv, svan.hp = liv_hp
        stats = list(map(int,f.readline().strip('\n').split('___')))           
        svan.stats['str'], svan.stats['smi'], svan.stats['mkr'] = stats
        mods = list(map(int,f.readline().strip('\n').split('___')))            
        svan.mods = mods
        utr = f.readline().strip('\n').split('___')                            
        utr = [FDICT[utr[0]],FDICT[utr[1]],FDICT[utr[2]]]
        svan.utrust['vapen'], svan.utrust['rustning'], svan.utrust['ovrigt'] = utr
        utv_1 =  f.readline().strip('\n').split('___')                         
        utv_2 = list(map(int,f.readline().strip('\n').split('___')))           
        svan.utveckling = []
        for u,v in zip(utv_1,utv_2):
            svan.utveckling.append([u,v])
        exp_lvl = list(map(int,f.readline().strip('\n').split('___')))         
        svan.exp, svan.lvl = exp_lvl
        line = f.readline().strip('\n')
        if len(line) > 1:
            svan.formagor = line.split('___')                   
        magier_1 = f.readline().strip('\n').split('___')
        try:
            magier_2 = list(map(int,f.readline().strip('\n').split('___')))        
            svan.magier = []
            for m, k in zip(magier_1,magier_2):
                svan.magier.append((m,k))
        except(ValueError):
            svan.magier = []
        line = f.readline().strip('\n')
        if len(line) > 1:
            svan.special = line.split('___')                    #23

        #alri
        liv_hp = list(map(int,f.readline().strip('\n').split('___')))          
        alri.liv, alri.hp = liv_hp
        stats = list(map(int,f.readline().strip('\n').split('___')))           
        alri.stats['str'], alri.stats['smi'], alri.stats['mkr'] = stats
        mods = list(map(int,f.readline().strip('\n').split('___')))            
        alri.mods = mods
        utr = f.readline().strip('\n').split('___')                            
        utr = [FDICT[utr[0]],FDICT[utr[1]],FDICT[utr[2]]]
        alri.utrust['vapen'], alri.utrust['rustning'], alri.utrust['ovrigt'] = utr
        utv_1 =  f.readline().strip('\n').split('___')                         
        utv_2 = list(map(int,f.readline().strip('\n').split('___')))           
        alri.utveckling = []
        for u,v in zip(utv_1,utv_2):
            alri.utveckling.append([u,v])
        exp_lvl = list(map(int,f.readline().strip('\n').split('___')))         
        alri.exp, alri.lvl = exp_lvl
        line = f.readline().strip('\n')
        if len(line) > 1:
            alri.formagor = line.split('___')                   
        magier_1 = f.readline().strip('\n').split('___')
        try:
            magier_2 = list(map(int,f.readline().strip('\n').split('___')))        
            alri.magier = []
            for m, k in zip(magier_1,magier_2):
                alri.magier.append((m,k))
        except(ValueError):
            alri.magier = []
        line = f.readline().strip('\n')
        if len(line) > 1:
            alri.special = line.split('___')                    #34

        progress={'main':0,
                  'häxan':0, #snälla häxan
                  'smeden':0,
                  'alkemisten':0,
                  'hittade_skatter':set(),  #lista med platser
                  'upptäckta_platser':{6,7,11,14},
                  'döda_fiender':set()}
        prnr = list(map(int,f.readline().strip('\n').split('___')))            #35
        if len(prnr) < 4: #tillägg för alkemisten
            prnr.append(0)
        progress['main'],progress['häxan'],progress['smeden'],progress['alkemisten'] = prnr
        for p in f.readline().strip('\n').split('___'):                        #36
            progress['hittade_skatter'].add(p)
        for p in list(map(int,f.readline().strip('\n').split('___'))):         #37
            progress['upptäckta_platser'].add(p)
        for p in f.readline().strip('\n').split('___'):                        #38
            progress['döda_fiender'].add(p)

        dialogval = [0 for i in range(10)]
        d_index = list(map(int,f.readline().strip('\n').split('___')))          #39
        d_line = f.readline().strip('\n').split('___')                          #40
        for index, line in zip(d_index, d_line):
            dialogval[index] = line

        inventory=list()
        for s in f.readline().strip('\n').split('___'):                        #41
            if s != '':
                inventory.append(FDICT[s])

        spelarlista = [sp1, svan]
        special = f.readline().strip()
        if special == 'd':                                  #42
            spelarlista += [alri,dvargen]
        elif special == 'a':                                
            spelarlista.append(alri)

        position = int(f.readline().strip())                        #43

        #dvargen
        if special == 'd':
            liv_hp = list(map(int,f.readline().strip('\n').split('___')))
            dvargen.liv, dvargen.hp = liv_hp
            stats = list(map(int,f.readline().strip('\n').split('___')))           
            dvargen.stats['str'], dvargen.stats['smi'], dvargen.stats['mkr'] = stats
            mods = list(map(int,f.readline().strip('\n').split('___')))            
            dvargen.mods = mods
            utr = f.readline().strip('\n').split('___')                            
            utr = [FDICT[utr[0]],FDICT[utr[1]],FDICT[utr[2]]]
            dvargen.utrust['vapen'], dvargen.utrust['rustning'], dvargen.utrust['ovrigt'] = utr
            utv_1 =  f.readline().strip('\n').split('___')                         
            utv_2 = list(map(int,f.readline().strip('\n').split('___')))           
            dvargen.utveckling = []
            for u,v in zip(utv_1,utv_2):
                dvargen.utveckling.append([u,v])
            exp_lvl = list(map(int,f.readline().strip('\n').split('___')))         
            dvargen.exp, dvargen.lvl = exp_lvl
            line = f.readline().strip('\n')
            if len(line) > 1:
                dvargen.formagor = line.split('___')                   
            magier_1 = f.readline().strip('\n').split('___')
            try:
                magier_2 = list(map(int,f.readline().strip('\n').split('___')))        
                dvargen.magier = []
                for m, k in zip(magier_1,magier_2):
                    dvargen.magier.append((m,k))
            except(ValueError):
                dvargen.magier = []
            line = f.readline().strip('\n')
            if len(line) > 1:
                dvargen.special = line.split('___')                    #54


def classhierarchy(obj):
    if isinstance(obj,kls.Foremal):
        return 4
    elif isinstance(obj,kls.EngangsForemal):
        return 3
    elif isinstance(obj,kls.Ovrigt):
        return 2
    elif isinstance(obj,kls.Vapen):
        return 1
    elif isinstance(obj,kls.Rustning):
        return 0

def foremalsmeny():
    global inventory
    while True:
        print('\nFÖREMÅL')
        ordered = uniquelist(inventory)
        ordered.sort(key=classhierarchy)
        antal = OrderedDict()
        for f in ordered:
            antal[f.namn] = inventory.count(f)
        display = [f.namn for f in ordered]
        for i in range(len(display)):
            try:
                display[i] += ' ('+ordered[i].bs+')'
            except(AttributeError):
                pass
            if antal[ordered[i].namn] > 1:
                display[i] += ' ('+str(antal[ordered[i].namn])+'st)'
            
        obj = listval(['Gå tillbaka']+display) - 1
        if obj == -1: #gå tillbaka
            break
        obj = ordered[obj]
        if isinstance(obj,kls.Utrustning):
            print('Välj vem som ska använda '+obj.namn)
            res = spelarlista[listval([s.namn for s in spelarlista])].equip(obj)
            if res:  #res är den gamla utrustningen, eller False om det inte gick
                inventory.remove(obj)
                if res.namn != '':
                    inventory.append(res)
            del res
        elif isinstance(obj,kls.EngangsForemal):
            #if not obj.target: #kollar om man ska välja mål
            sp = spelarlista[listval([s.namn for s in spelarlista])]
            res = obj.use(sp)
            if res:
                inventory.remove(obj)
            else:
                print(sp.namn+' kan inte bli hjälpt av det')
            del res
        elif isinstance(obj,kls.Foremal):
            print(obj.namn+' går inte att använda här.')

def foremaloverallt(fnamn, tabort=False):
    if fnamn in [f.namn for f in inventory]+[f.namn for f in [foremal for utrustning in [s.utrust.values() for s in spelarlista] for foremal in utrustning]]:
        if tabort:
            for f in [fo for fo in inventory if fo.namn == fnamn]:
                inventory.remove(f)
            for s in spelarlista:
                for k in s.utrust:
                    if s.utrust[k].namn == fnamn:
                        s.utrust[k] = kls.Foremal('-')
        return True
    return False

#dialogfunktion,
#mata in vilka frågor som går att ställa till personen
#returnerar vilken fråga spelaren vill ställa 
def dialog(nr_listform):
    lista=[]
    for nr in nr_listform:
        if isinstance(dialogval[nr],str):
            lista.append(dialogval[nr])
    lista.append('Ta avsked')
    return lista[listval(lista)]
        
#--------------------------------------------------HUVUDDEL AV SPELET
def meny():
    global inventory
    global progress
    global dialogval
    global position
    global spelarlista

    nyplats = False
    
    while True:
        plats = PDICT[position]

        if nyplats:
            
            if plats == 'berg':
                if 'berg' not in progress['hittade_skatter'] and randint(0,6) == 6:
                    slowprint('Du hittar en Skyddande ädelsten!')
                    inventory.append(FDICT['Skyddande ädelsten'])
                    progress['hittade_skatter'].add('berg')
                elif randint(0,4) > 1 and 'Trollkungen' not in progress['döda_fiender']:
                    if progress['main'] < 2:
                        fight()
                    else:
                        fight(OP=1)           

            elif plats == 'Buren':
                if 'Zeoidodh' not in progress['döda_fiender']:
                    time.sleep(1.5)
                    print('\nDJURFRÄMLINGEN KOMMER MOT ER\n')
                    time.sleep(1.5)
                    print('Är ni redo?')
                    time.sleep(1.5)
                    if 'Zeoidodh' in progress['hittade_skatter']:
                        print('Djurfrämlingens makt minskar av att du känner\n'+
                              'hens rätta namn: Zeoidodh')
                        time.sleep(1.5)
                        fight(['Zeoidodh'],True)
                    else:
                        fight(['Djurfrämlingen'],True)
                    progress['döda_fiender'].add('Zeoidodh')
                
            elif plats == 'djup skog' and 'djup skog' not in progress['hittade_skatter']:
                slowprint('Skogen blir mycket tät här.\n')
                if min((s.stats['smi'] for s in spelarlista)) < 12:
                    print('Er grupp är inte tillräckligt smidig för att fortsätta')
                else:
                    slowprint('Ni fortsätter in, och i en glänta hittar ni en alvbåge!\n')
                    inventory.append(FDICT['Alvbåge'])
                    progress['hittade_skatter'].add('djup skog')
                
            elif plats == 'Djupa dalen':
                demon = None
                if randint(0,3) == 3:
                    if position < 300 and 'Zlokr' not in progress['döda_fiender']:
                        demon = 'Zlokr'
                    elif position > 300 and 'Ziriekl' not in progress['döda_fiender']:
                        demon = 'Ziriekl'
                if demon:
                    print('En demon dyker upp...!\n'+
                          'Vill du strida mot demonen?')
                    if listval(['Ja','Nej']) == 0:
                        fight([demon],True)
                        progress['döda_fiender'].add(demon)
                elif randint(0,4) > 1:
                    if progress['main'] < 2:
                        fight()
                    elif position < 300:
                        fight(OP=1)
                    else:
                        fight(OP=2)
                del demon

            elif plats == 'Dvärgbyn':
                print('Det finns många att prata med i dvärgbyn')
                while True:
                    print('Vem vill du prata med?')
                    n = listval(['Byäldsten','En förmögen dvärg','Byfånen','Lämna dvärgbyn'])
                    if n == 0:
                        while True:
                            fraga = dialog([0,7])
                            if fraga == 'Fråga om äventyr':
                                print('Var försiktig när du utforskar de här landen, främling,\n'+
                                      'du ser inte ut att vara lika kraftig som oss.\n'+ 
                                      'I bergen dväljs fasansfulla vidunder,\n'+
                                      'och i dalen västerom byn har en mäktig demon synts till.')
                            elif fraga == 'Fråga om Mästarsmeden':
                                print('En av vårt släkte som med rätta kan kallas mästare\n'+
                                      'lämnade byn och byggde en boning åt nordöst.')
                            else:
                                print('Adjö')
                                break
                    elif n == 1:
                        if 'dvärgbyn' not in progress['hittade_skatter']:
                            print('Var hälsad äventyrare.\n'+
                                  'Jag har en skatt som skulle vara er behjälplig på färden.\n'+
                                  'Ni får den gärna, om ni har något värdefullt att erbjuda i utbyte')
                            ulista = [f.namn for f in inventory if f.namn in ALDICT]
                            ulista = [f for f in ulista if ALDICT[f] > 24]
                            if len(ulista) > 0:
                                n = listval(['Erbjud dvärgen '+f for f in ulista]+['Tacka nej'])
                                if n == len(ulista):
                                    next
                                else:
                                    print('Du gav dvärgen '+ulista[n]+'\n och fick De gamlas ring i utbyte.')
                                    inventory.remove(FDICT[ulista[n]])
                                    inventory.append(FDICT['De gamlas ring'])
                                    progress['hittade_skatter'].add('dvärgbyn')
                            else:
                                slowprint('...',3)
                                print('Jag ser inget jag är intresserad av bland dina saker')
                            del ulista
                        else:
                            print('Jag har inget mer att erbjuda er')
                    elif n == 2:
                        while True:
                            fraga = dialog([0,3])
                            if fraga == 'Fråga om äventyr':
                                print('I den mörka mörka skogen finns märkliga ting,\n'+
                                      'men den som är klumpenduns kommer inte in.')
                            elif fraga == 'Fråga om monster':
                                print('Mina Vänner har namn ingen får höra och leva,\n'+
                                      'om deras sanna namn blir känt förminskas deras makt\n'+
                                      'Jag har en Vän jag träffar på berget.\n'+
                                      '(mumlar:)...Måste hitta vägen till Mörkret för att släppa Vännen fri...')
                            else:
                                print('......')
                                break
                    else:
                        break

            elif plats == 'En boning':
                print('En gammal dvärg bor här\nGråskägge: Mitt namn är Gråskägge, vad är ert ärende?')
                fraga = dialog([0,7])
                if fraga == 'Fråga om äventyr':
                    print('Den rika dvärgen i byn har ett öga för värde,\n'+
                          'men hon ser inte skillnad på unika mästerverk och ting av allmän kvalitet')
                elif fraga == 'Fråga om Mästarsmeden' and 'boning' not in progress['hittade_skatter']:
                    slowprint('Nå nå, det är sant att jag inte har sett den smed\n'+
                          'som kan mäta sig med min smideskonst.\n')
                    time.sleep(1)
                    slowprint('Hmm... Den som smidit detta svärd\n(Gråskägge studerar ditt Mästarsvärd)\n'+
                              'tycks ha försökt efterlikna mitt hantverk.\n'+
                              'Det är inte dåligt gjort, men det är ännu mycket kvar att önska\n')
                    time.sleep(1)
                    slowprint('Om du hittar ett antal monstertänder och en del älvstoft\n'+
                              'kan jag fullända verket\n')
                    if inventory.count(FDICT['Tand']) > 2 and inventory.count(FDICT['Älvstoft']) > 1:
                        slowprint('Du har det? Mycket bra. Vänta då.\n')
                        slowprint('...\n...\n...\n',3)
                        slowprint('Gråskägge förbättrade Mästarsvärdet!')
                        foremaloverallt('Mästarsvärd',tabort=True)
                        foremaloverallt('Tand',tabort=True)
                        foremaloverallt('Älvstoft',tabort=True)
                        inventory.append(FDICT['Mästarsvärdet'])
                        progress['hittade_skatter'].add('boning')
                        

            elif plats == 'En glänta':
                print('Det är en vacker glänta')
                if 'glänta' not in progress['hittade_skatter'] and random() > 0.95:
                    time.sleep(1)
                    slowprint('En älva kommer fram till dig.\n'+
                              'Älvan: Det finns ont om tappra äventyrare dessa dagar,\n'+
                              'ta den här dräkten, må den hjälpa er på färden.\n'+
                              'Ni fick en förtrollad dräkt.')
                    inventory.append(FDICT['Förtrollad dräkt'])
                print('Ni återhämtar kraft, och får full hp.')
                for s in spelarlista:
                    s.hp = s.liv

            elif plats == 'En grotta': #lägg till bossar och bonusar
                if listval(['Gå in i grottan','Stanna utanför']) == 0:
                    if 'Gaurghus' not in progress['döda_fiender']:
                        fight(['Gaurghus'],True)
                        slowprint('Ni hittar Demondryck, Ormmedicin, Livsfrukt\n'+
                              'och en Mystisk sten, inne i grottan.')
                        for i in ['Demondryck', 'Ormmedicin', 'Livsfrukt', 'Mystisk sten']:
                            inventory.append(FDICT[i])
                        progress['döda_fiender'].add('Gaurghus')
                    elif progress['main'] > 3 and 'Entrios' not in progress['döda_fiender']:
                        fight(['Entrios'],True)
                        slowprint('Entrios försvinner in i grottan...\n')
                        time.sleep(1)
                        slowprint('Svan: Han kallar mig.\n')
                        time.sleep(1)
                        slowprint('Svan försvinner in i grottan!\n')
                        slowprint('. . . . .\n',4)
                        slowprint('Plötsligt dyker Svan upp ur mörkret.\n')
                        time.sleep(1)
                        slowprint('Svan lärde sig Förbjuden makt.\n')
                        svan.formagor.append('Förbjuden makt')
                        progress['döda_fiender'].add('Entrios')
                    elif progress['main'] > 4 and 'Grottan' not in progress['hittade_skatter']:
                        slowprint('Ni hittade Skuggornas ring och Okänd materia inne i grottan')
                        progress['hittade_skatter'].add('Grottan')
                        inventory += [FDICT['Skuggornas ring'],FDICT['Okänd materia']]
                    else:
                        print('Grottan verkar vara tom, men ni känner av\n'+
                              'en obehaglig närvaro')

            elif plats == 'En källare': #här får man en uppgradering till Djurfrämlingens bok
                if 'Jotun' in progress['hittade_skatter']:
                    print('Det är en jätte i källaren.')
                    if 'ZZZ' not in progress['hittade_skatter']: 
                        dialogval[8] = d8
                        if dialog([8]) == 'Fråga om böcker':
                            slowprint('När jätten ser att du har Djufrämlingens bok blir hon förskräckt.\n'+
                                  'Det är hon som har skrivit den åt Djurfrämlingen säger hon.\n')
                            time.sleep(1.5)
                            slowprint('Efter en stund så tittar hon i den, tar fram en penna och skriver något...\n')
                            progress['hittade_skatter'].add('ZZZ')
                elif 'källare' in progress['hittade_skatter']:
                    print('Det är ingen här, bara massa böcker.')
                    dialogval[8] = d8 #fråga om böcker
                else:
                    slowprint('Ni ser en jätte, som springer ifrån er.\n'+
                          'Ni springer efter, ner i en källare,\n'+
                          'men just som ni kommit ikapp tar jätten upp en bok,\n'+
                          'och i samma sekund är hon borta!\n')
                    time.sleep(1)
                    slowprint('Ni tittar er omkring i källaren, och hittar en hammare!')
                    inventory.append(FDICT['Jotuns hammare'])
                    progress['hittade_skatter'].add('källare')

            elif plats == 'En äng':
                print('Det känns skönt att vara här!\n'+
                      'Ni fick full hp.')
                for s in spelarlista:
                    s.hp = s.liv
                          
            elif plats == 'Ett fort':
                if not 'fort' in progress['hittade_skatter']: 
                    print('Det är en tiger i fortet.\nTigern: Hej äventyrare')
                    if 'Älva' in alri.formagor and 'Randig gren' in [f.namn for f in inventory]:
                        print('Ge tigern din randiga gren?')
                        if listval(['Ja','Nej']) == 0:
                            slowprint('Tigern blir till en ande och hoppar in i Alri!',2)
                            alri.formagor.append('Tiger')
                            progress['hittade_skatter'].add('fort')
                            for f in [s for s in inventory if s.namn == 'Randig gren']:
                                inventory.remove(f)
                    else:
                        while True:
                            fraga = dialog([0,2,3,8])
                            if fraga == 'Fråga om äventyr':
                                if progress['main'] == 2:
                                    print('Det finns en äng nära här, där man mår bra\n'+
                                          'Annars är det mycket monster här omkring')
                                    dialogval[3] = d3
                                elif 113 not in progress['upptäckta_platser']:
                                    print('Det finns en grotta västerut.\n'+
                                          'Men jag har aldrig vågat gå in...')
                                else:
                                    print('Den som byter skepnad tar fram en annan sida av sin natur,\n'+
                                          'En fågel är smidig men inte så stark.\n'+
                                          'En gorilla är stark och smidig, men har inga särskilda förmågor.\n'+
                                          'En älva är svag men har mäktig trollkraft.\n'+
                                          'Själv är jag en tiger.')
                            elif fraga == 'Fråga om Elaka häxan':
                                print('Den elakaste jag vet är Vildsvinet\n'+
                                      'Jag har hört att Vildsvinet har en bok som tar det till andra världar,\n'+
                                      'kanske har Vildsvinet träffat den där Häxan i en annan värld?')
                            elif fraga == 'Fråga om monster':
                                print('De värsta monstren finns i mörkt vatten,\n'+
                                      'men där finns också magiska hjortar...\n'+
                                      'I Buren bor något som fyller vem som helst med fasa...')
                            elif fraga == 'Fråga om böcker':
                                print('Jotun är den som vet mest om böcker, men jag vet inte var hon tog vägen.')
                            else:
                                print('Hejdå!')
                                break
                else:
                    print('Det är ingen här')

            elif plats == 'Ett hus':
                if progress['main'] < 2:
                    print('Det är ingen hemma.')
                    if alri not in spelarlista:
                        print('Men du ser dig omkring och upptäcker en underlig kvinna\n'+
                              'som flaxar med armarna som om hon vore en fågel')
                        if 'Mystisk fjäder' in [f.namn for f in inventory]:
                            print('Ge henne din mystiska fjäder?')
                            if listval(['Ja','Nej']) == 0:
                                slowprint('Åh, fantastiskt! Fascinerande!\n'+
                                      'Låt mig vara med på dina äventyr och hitta mer magiska ting\n')
                                time.sleep(0.7)
                                slowprint('Alri ansluter sig till ditt sällskap!\n')
                                spelarlista.append(alri)
                                alri.exp=int(sp1.exp*0.8)
                                if ('Tillkvicknande',2) in sp1.magier:
                                    alri.magier.append(('Tillkvicknande',2))
                                lvlup(spelarlista)
                                for f in [s for s in inventory if s.namn == 'Mystisk fjäder']:
                                    inventory.remove(f)
                        else:
                            fraga = dialog([0])
                            if fraga == 'Fråga om äventyr':
                                print('Vem är du? Stör mig inte.')
                #ALKEMISTEN
                elif alri in spelarlista:
                    if progress['alkemisten'] == 0:
                        slowprint('En alkemist har flyttat in i huset.\n'+
                                  'Alri: Det här är min kusin.\n'
                                  'Låt mig presentera '+sp1.namn+' och Svan\n')
                        progress['alkemisten'] += 1
                    print('Alkemisten: Hej, jag kan omforma materia och\n'+
                          'skapa nya föremål av gamla.\n'+
                          'Om du ger mig tillräckligt många saker får du något i utbyte.')
                    while True:
                        if progress['alkemisten'] > 20 and "a1" not in progress['hittade_skatter']:
                            slowprint('Alkemisten skapade en demondryck till er\n')
                            inventory.append(FDICT['Demondryck'])
                            progress['hittade_skatter'].add("a1")
                        elif progress['alkemisten'] > 60 and "a2" not in progress['hittade_skatter']:
                            slowprint('Alkemisten skapade en trollring till er\n')
                            inventory.append(FDICT['Trollring'])
                            progress['hittade_skatter'].add("a2")
                        elif progress['alkemisten'] > 140 and "a3" not in progress['hittade_skatter']:
                            slowprint('Alkemisten skapade ett magiskt armband till er\n')
                            inventory.append(FDICT['Magiskt armband'])
                            progress['hittade_skatter'].add("a3")
                        elif progress['alkemisten'] > 300 and "a4" not in progress['hittade_skatter']:
                            slowprint('Alkemisten skapade en silverbåge till er\n')
                            inventory.append(FDICT['Silverbåge'])
                            progress['hittade_skatter'].add("a4")
                        elif progress['alkemisten'] > 620 and "a5" not in progress['hittade_skatter']:
                            slowprint('Alkemisten skapade en mitrilrustning till er\n')
                            inventory.append(FDICT['Mitrilrustning'])
                            progress['hittade_skatter'].add("a5")
                        elif progress['alkemisten'] > 1260 and "a6" not in progress['hittade_skatter']:
                            slowprint('Alkemisten skapade De vises sten till er\n')
                            inventory.append(FDICT['De vises sten'])
                            progress['hittade_skatter'].add("a6")
                        elif progress['alkemisten'] > 1800:
                            slowprint('Alkemisten skapade en kraftdryck till er\n')
                            inventory.append(FDICT['Kraftdryck'])
                            progress['alkemisten]'] -= 600
                        print('ALKEMISTEN')
                        obj = listval(['Gå tillbaka']+
                                      [f.namn+' - Alkemivärde: '+str(ALDICT[f.namn]) for f in inventory if f.namn in ALDICT])
                        if obj == 0:
                            break
                        else:
                            obj = [f for f in inventory if f.namn in ALDICT][obj-1]
                            print('Du gav '+obj.namn+' till Alkemisten')
                            progress['alkemisten'] += ALDICT[obj.namn]
                            inventory.remove(obj)
                            
                    while True:
                        fraga = dialog([0,4,8])
                        if fraga == 'Fråga om äventyr':
                            print('Alri, om du övar på din själskunskap kan du anknyta\n'+
                                  'till vissa andar du möter på dina äventyr, har jag hört...')
                        elif fraga == 'Fråga om Snälla häxan':
                            print('Jag vet inte vart hon tagit vägen...\n'+
                                  'Och nu står inte allt rätt till här i landet.')
                        elif fraga == 'Fråga om böcker':
                            print('Det kom en ung kvinna resande här nyligen.\n'+
                                  'Jag gav henne mat och husrum, och som tack fick jag\n'+
                                  'en ovärderlig bok om hemlig alkemi.\n'+
                                  'Jag undrar var hon kan ha fått tag på den!')
                            time.sleep(2)
                            print('Mycket märkligt, men innan jag hann fråga närmare\n'+
                                  'reste hon sin väg igen.\n'+
                                  'Hon sa att hennes namn var Una.')
                            dialogval[5] = d5
                        else:
                            print('På återseende!')
                            break

            elif plats == 'Gamla smeden':
                if 'Gamla smeden' not in progress['hittade_skatter']:
                    print('Gamla smeden: Jag tycker ni ser bekanta ut, har vi träffats förut...?\n'+
                          'Jaså ni är äventyrare, några sådana känner jag inte längre...\n'+
                          'Jag skulle gärna hjälpa er men jag har knappt om resurser,\n'+
                          'så ni får stå för materialet.')
                    input('(tryck enter)')
                    print('Den där riddarrustningen kanske jag kan förbättra...')
                    time.sleep(1)
                    if 'Fiskstål' in [f.namn for f in inventory] and foremaloverallt('Ormdräkt'):
                        slowprint('Jag kan nog använda det där märkliga fjälliga stålet och er ormdräkt...\n')                   
                        inventory.remove([f for f in inventory if f.namn=='Fiskstål'][0])
                        foremaloverallt('Ormdräkt',tabort=True)
                        foremaloverallt('Riddarrustning',tabort=True)
                        time.sleep(1)
                        slowprint('Du gav Riddarrustning, Ormdräkt och Fiskstål till smeden.\n')
                        slowprint('.........\n',5)
                        slowprint('Här får du en megarustning!\n')
                        inventory.append(FDICT['Megarustning'])
                        progress['hittade_skatter'].add('Gamla smeden')
                    else:
                        slowprint('Men jag skulle behöva något verkligt bra läder och kraftigt stål.\n')
                while True:
                    fraga = dialog([0,7])
                    if fraga == 'Fråga om äventyr':
                        print('Du borde se vad som försiggår i slottet.\n'+
                              'För att vinna tillit, se till vad soldaterna gör,\n'+
                              'och försök bete dig likadant')
                        dialogval[6] = d6
                    elif fraga == 'Fråga om Mästarsmeden':
                        print('Jag är nog skicklig, men inte som den legendariska smeden från forna tider.')
                    else:
                        print('Farväl')
                        break

            elif plats == 'Gården':
                if progress['main'] == 2:
                    print('Ni kommer till en gård där olika djur bor.\n'+
                          'En hund möter er.\n'+
                          'Hunden: Ni borde inte vara här, det är bäst att ni går.\n')
                    n = listval(['Stanna','Gå'])
                else:
                    print('Räven: Här på gården finns många olika djur. Vill du gå in?')
                    n = listval(['Ja','Nej'])
                    
                if n == 0: #om man väljer att stanna
                    if progress['main'] == 2:
                        print('Hunden visar er runt på Gården\n')

                    n = randint(0,2)

                    if n == 0:
                        if progress['main'] == 2:
                            print('Hunden visar ett bra ställe att gräva på\n')
                            if randint(0,1) == 0:
                                print('Du gräver och hittar en läkört!')
                                inventory.append(FDICT['Läkört'])
                            else:
                                print('Du gräver men hittar ingenting.')
                        else:
                            print('Du följer efter räven, men hamnar vilse...')
                            position = randint(101,116)
                            if position == 105:
                                position = 112
                    elif n == 1 and 'Gården' not in progress['hittade_skatter']:
                        print('Ni tappar bort hunden...\n'+
                              'Ni kommer till en hästhage.\n')
                        if progress['main'] > 2:
                            slowprint('En av hästarna kommer bärande på ett par skor i munnen.\n'+
                                  'Du fick Skuggskor!')
                            inventory.append(FDICT['Skuggskor'])
                            progress['hittade_skatter'].add('Gården')
                        else:
                            print('Hästarna verkar oroliga')
                            sp = [s for s in spelarlista if s.hp>0][randint(0,len([s for s in spelarlista if s.hp>0])-1)]
                            slowprint(sp.namn+' går fram till en häst för att klappa den,\n'+
                                      'men får en spark...!\n')
                            sp.hp = 0
                            print(sp.namn+' är medvetslös.\n'+
                                  'Ni skyndar er därifrån.')
                    else:
                        if progress['main'] == 2:
                            print('Ni träffar på en gris.\n'+
                                  'Grisen: Vilka är ni? Rulla er i leran!\n'+
                                  'Ni rullar er i leran...\n'+
                                  'Grisen: Hahahaha! Här är det min boss Vildsvinet som bestämmer.')
                            if listval(['-Jag är inte rädd för Vildsvinet','Gå därifrån']) == 0:
                                slowprint('Vildsvinet kommer springande...!\n')
                                time.sleep(0.5)
                                fight(['Vildsvinet','Grisen'], True)
                                time.sleep(1.2)
                                slowprint('Vildsvinet springer iväg.\n'+
                                      'Skuggorna tycks lätta...!\n')
                                time.sleep(1)
                                slowprint('En räv dyker upp.\n'+
                                      'Räven: Jag kan visa er var Vildsvinet har sin magiska bok')
                                time.sleep(0.7)
                                slowprint('.............\nNi hittar Djurfrämlingens bok!\n')
                                time.sleep(0.7)
                                slowprint('Räven: Den här boken tillhörde en fruktansvärd demon,\n'+
                                      'den kan användas för att färdas mellan världar.\n'+
                                      '(Du hittar den i huvudmenyn)\n')
                                progress['hittade_skatter'].add('Z')
                                progress['main'] += 1
                        else:
                            print('Ni träffar på Grisen.')
                            try:
                                f = [fo for fo in inventory if isinstance(fo,kls.EngangsForemal)][randint(0, len([fo for fo in inventory if isinstance(fo,kls.EngangsForemal)])-1)]
                                print('Grisen: Ni är fula!')
                                slowprint('.............')
                                print('Grisen tog '+f.namn+' från er.')
                                inventory.remove(f)
                            except(IndexError,ValueError):
                                print('Grisen: Ni är töntar')

            elif plats == 'Huset':
                print('Huset som låg här är kvar men är väldigt nedgånget.\n'+
                      'Inne i huset träffar ni en gammal äventyrare.')
                while True:
                    fraga = dialog([0,3,4,7,8])
                    if fraga == 'Fråga om äventyr':
                        print('Det är inte detsamma att äventyra längre som när Gurgen regerade.\n'+
                              'De säger till och med att äventyr är förbjudet!\n'+
                              'När man pratar med folk är det bäst att låtsas att man bara lever\n'+
                              'för att tjäna konungen och följa den där mystiska Amunos lagar.')
                        dialogval[6] = d6   #(Hell kung kolskägg)
                    elif fraga == 'Fråga om monster':
                        print('Det kan bli en lång historia när jag börjar berätta om alla monster jag mött.\n'+
                              'Jag har varit i mörka skogar, djupa dalar och höga berg...')
                        if sp1.lvl > 40 and 'Magiskt rep' not in [f.namn for f in inventory]:
                            slowprint('Du verkar vara en erfaren äventyrare själv...\n')
                            time.sleep(1)
                            slowprint('Men har du någonsin varit uppe på Höga berget?\n'+
                                      'Jag fick det här magiska repet av en vis dvärg en gång,\n'+
                                      'med det kan man ta sig upp.\n'+
                                      'Jag är för gammal för sådant nu, du får det!\n')
                            inventory.append(FDICT['Magiskt rep'])
                        elif sp1.lvl < 41:
                            print('Du är ännu ingen sann äventyrare som jag.\n'+
                                  'Kom tillbaka när du är mer erfaren.')
                    elif fraga == 'Fråga om Snälla häxan':
                        print('Jag har hört att det bodde en snäll häxa i trakten för länge sen,\n'+
                              'vem vet var hon tog vägen.')
                    elif fraga == 'Fråga om Mästarsmeden':
                        print('På mina resor har jag hört att det en gång bodde en smed vars like\n'+
                              'inte skådats, söderom där Templet nu står.')
                    elif fraga == 'Fråga om böcker':
                        print('Det fanns många böcker här, men de beslagtogs alla av prästerna.\n'+
                              'Jag tror att de har ett mäktigt bibliotek i Templet.')
                    else:
                        print('Må lyckans Gudar le mot er.')
                        break
                            
                
            elif plats == 'Höga berget' and 200 < position < 300:
                if 'blodkristall' not in progress['hittade_skatter']:
                    slowprint('Inne i en grotta i berget hittar du en märklig kristall!\n\n')
                    inventory.append(FDICT['Blodkristall'])
                    progress['hittade_skatter'].add('blodkristall')
                    time.sleep(2)
                if 'Höga berget' not in progress['hittade_skatter']:
                    print('Du träffar på tomten Sirkafirk på bergets topp.')
                    if any(f in {'Zlokr','Ziriekl','Zaumakot','Zeoidodh'} for f in progress['döda_fiender']):
                        slowprint('Sirkafirk: Du har dödat en demon, då är du min vän.\n'+
                                  'Jag ska lära dig en hemlighet.\n')
                        time.sleep(2)
                        slowprint(sp1.namn+' lärde sig Lura naturen!')
                        sp1.formagor.append('Lura naturen')
                        progress['hittade_skatter'].add('Höga berget')
                    else:
                        print('Sirkafirk: Den som kan besegra en demon är min vän')

            elif plats == 'Höga berget' and position < 100:
                if 'Trollkungen' not in progress['döda_fiender']:
                    slowprint('Uppe på berget ligger en borg.\n'+
                              'Ni går in i borgen och där träffar ni ett troll.\n'+
                              'Trollet: Vad gör ni människor här?!\n'+
                              'Kom med mig, ni ska föras inför kungen.\n')
                    time.sleep(3)
                    slowprint('Trollkungen: Ser man på, några människor har hittat hit.\n')
                    fraga = dialog([0,1])
                    if fraga == 'Fråga om äventyr':
                        slowprint('Jag har nog hört om dina äventyr från trollen i skogen,\n'+
                                  'Men den här gången har du bråkat med fel troll!\n')
                    elif fraga == 'Nu ska du få stryk!':
                        slowprint('JASÅ DET TROR DU!!', 3)
                    else:
                        slowprint('Inte så fort! Idag ska vi festa på mänskostuvning!')
                    time.sleep(1.5)
                    fight(['Trollkungen'],True)
                    time.sleep(2)
                    slowprint('Trollkungen: Nåd! Om du skonar mig lovar jag att vi ska vara till hjälp för er framöver.\n'+
                              'Och ni kommer inte bli anfallna mer i skogar och berg.\n')
                    time.sleep(2)
                    slowprint('Ni skonar trollkungen.\n')
                    progress['döda_fiender'].add('Trollkungen')
                else:
                    print('I trollborgen:\n'+
                          'Trollkungen: Välkommen starka krigare!')
                    if 'guldbåge' not in progress['hittade_skatter']:
                        print('Våran hantverkskonst är högre än ni människors.\n'+
                              'Visa mig det mest imponerande föremål du kan hitta,\n'+
                              'så ska vi överträffa det!')
                        time.sleep(2)
                        if 'a4' in progress['hittade_skatter']:
                            slowprint('Vad är det där för silvrig pilbåge?\n'+
                                      'Jag kan inte tro att en människa skapat detta!\n'+
                                      'Låt Mästartrollet titta på den!\n')
                            slowprint('............',5)
                            slowprint('Mästartrollet kommer tillbaks med en gyllene båge!\n'+
                                      'Ni fick en Guldbåge.\n')
                            inventory.append(FDICT['Guldbåge'])
                            foremaloverallt('Silverbåge', tabort=True)
                            progress['hittade_skatter'].add('guldbåge')
                        else:
                            print('Jag ser inga imponerande föremål här...')
                    else:
                        print('Hur gillar ni Guldbågen? Höhöhö')

            elif plats == 'Höga berget' and position > 300:
                if random() > 0.4:
                    print('Ni möter ett väsen på berget,\n'+
                          'det liknar en blandning mellan människa, ko, fågel och fisk\n'+
                          'men framstår annorlunda varje gång du ser på det.')
                    time.sleep(1)
                    print('???: Vad söker ni?')
                    lurat = False
                    fraga = dialog(1,3,8)
                    if fraga == 'Fråga om böcker':
                        print('Den där boken tillhör inte er...')
                        demon = False
                        if listval(['Det gör den visst',
                                    'Vi vill återföra den till sin rätta ägare']) == 1:
                            slowprint('???: Jaså,')
                            time.sleep(1)
                            slowprint(' det är bra.')
                            alt = ['Låt den rätta ägaren tillkännage sig',
                                   'Vad kan du ge mig?',
                                   'Men dess rätta ägare är fast i Skuggvärlden',
                                   'Men dess rätta ägare är jätten Jotun']
                            shuffle(alt)
                            ans = alt[listval(alt)]
                            if ans == 'Låt den rätta ägaren tillkännage sig':
                                time.sleep(2)
                                slowprint('Zeoidodh är mitt namn, hör det och fasa, Människa!\n'+
                                          'Den bokens krafter har ni inte ens börjat förstå.\n'+
                                          'Återlämna den nu till mig!')
                                demon = True
                                lurat = True
                            elif ans == 'Vad kan du ge mig?':
                                slowprint('???: Jag kan ge dig krafter du aldrig drömt om...\n')
                                demon = True
                            else:
                                slowprint('Du vet inte vad du talar om!\n')
                            if demon:
                                if listval(['Ok', 'Nej']) == 0:
                                    slowprint('Du gav Djurfrämlingens bok till Djurfrämlingen...\n')
                                    time.sleep(1.5)
                                    slowprint('Du blev en Demon.......\n Slut på äventyret.',3)
                                    time.sleep(1.5)
                                    raise SystemExit
                            del demon
                                
                        slowprint('Väsendet sträcker sig efter Djurfrämlingens bok!\n'+
                                  '...\n *!*?*! -men en magisk kraft hindrar rörelsen\n'+
                                  'Ni slås till marken av krafturladdningen,\n'+
                                  'väsendet försvinner sin väg\n')
                        for s in spelarlista:
                            s.hp = int(s.hp*0.7)
                        if lurat and 'Zeoidodh' not in progress['hittade_skatter']:
                            slowprint('Du lärde dig Djurfrämlingens rätta namn: Zeoidodh\n',2)
                            progress['hittade_skatter'].add('Zeoidodh')
                    elif fraga == 'Nu ska du få stryk!':
                        print('???: Hahaha. Om ni blott kände till vilka krafter jag besitter,\n'+
                              'men ni ska inte möta er död idag.')
                        time.sleep(1.5)
                        print('\nNi grips av en djup fasa vid tanken på at kämpa mot denna varelse,\n'+
                              'Det verkar bäst att inte provocera ytterligare')
                    else:
                        print('Vad ett monster är beror på vem som betraktar vem')
                    del lurat
                        
            elif plats == 'landsväg':
                if randint(0,4) > 1:
                    fight()
                                    
            elif plats == 'mörkt vatten':
                if 'mörkt vatten' not in progress['hittade_skatter'] and randint(0,6) == 6:
                    print('Du hittar en blå ring!')
                    inventory.append(FDICT['Blå ring'])
                    progress['hittade_skatter'].add('mörkt vatten')
                elif randint(0,4) > 1:
                    fight()                   

            elif plats == 'Smeden':
                print('Du har kommit till Smeden')
                print('-Hej äventyrare')
                while True:
                    if max([s.lvl for s in spelarlista])>2 and progress['smeden']<1:
                        slowprint('Här får du ett svärd.\n')
                        inventory.append(FDICT['Svärd'])
                        progress['smeden']+=1
                    elif max([s.lvl for s in spelarlista])>4 and progress['smeden']<2:
                        slowprint('Här får du en rustning.\n')
                        inventory.append(FDICT['Lätt rustning'])
                        progress['smeden']+=1
                    elif max([s.lvl for s in spelarlista])>8 and progress['smeden']<3:
                        slowprint('Här får du ett bra svärd.\n'+
                              'Svärdet fodrar en del styrka.\n')
                        inventory.append(FDICT['Bra svärd'])
                        progress['smeden']+=1
                    elif max([s.lvl for s in spelarlista])>15 and progress['smeden']<4:
                        slowprint('Här får du en tung rustning.\n')
                        inventory.append(FDICT['Tung rustning'])
                        progress['smeden']+=1
                    elif max([s.lvl for s in spelarlista])>25 and progress['smeden']<5:
                        slowprint('Här får du en guldhandske.\n')
                        inventory.append(FDICT['Guldhandske'])
                        progress['smeden']+=1
                    elif max([s.lvl for s in spelarlista])>39 and progress['smeden']<6:
                        slowprint('Här får du mitt bästa verk\n',2)
                        inventory.append(FDICT['Mästarsvärd'])
                        progress['smeden']+=1
                    else:
                        break

                while True:
                    fraga = dialog([0,2,4])
                    if fraga == 'Fråga om äventyr':
                        if progress['smeden'] < 6:
                            print('När du har äventyrat mer, kom tillbaka hit.')
                        else:
                            print('Kunskapen för att smida mästerliga verk har nästan gått förlorad,'+
                                  'i svunna tider fanns det en dvärg i dessa skogar vars skicklighet är oöverträffad')
                            dialogval[7] = d7 #fråga om mästarsmeden
                    elif fraga == 'Fråga om Elaka häxan':
                        if progress['main'] < 2:
                            print('Om du träffar den elaka häxan, fråga henne inte om något, slå till direkt!')
                            if d1 not in dialogval:
                                dialogval[1]=d1
                        else:
                            print('Jag tror inte att hon har försvunnit, som de säger...')
                    elif fraga == 'Fråga om Snälla häxan':
                        print('Den Snälla häxan har få vänner kvar verkar det som.\n'+
                              'Men hennes vänner kan känna igen den här ringen.')
                        if 'Häxans ring' not in [f.namn for f in inventory]:
                            print('Ta den med dig.')
                            inventory.append(FDICT['Häxans ring'])
                    else:
                        print('Hejdå')
                        break
                
            elif plats == 'skugglandskap':
                if 'skugglandskap' not in progress['hittade_skatter'] and randint(0,5) == 5:
                    print('Du råkar på tomten Jyrgafyrg\n')
                    if len([f for f in inventory if f.namn == 'Mystisk sten']) < 4:
                        print('-Den som är gjord av sten är min vän')
                    else:
                        slowprint('-Ni är gjorda av sten. Då är ni mina vänner,\n'+
                              'jag ska inviga er i vår lära...\n')
                        time.sleep(1)
                        slowprint('Ni kan nu lära er Hemlig lära!')
                        for sak in [f for f in inventory if f.namn == 'Mystisk sten']:
                            inventory.remove(sak)
                        for s in spelarlista:
                            s.utveckling.append(['Hemlig lära',0])
                        progress['hittade_skatter'].add('skugglandskap')
                elif randint(0,4) > 1:
                    fight()                           

            elif plats == 'skog':
                if 'skog' not in progress['hittade_skatter'] and randint(0,4) == 4:
                    print('Du råkar på tomten Heyjafjej\n')
                    if len(progress['upptäckta_platser']) < 15:
                        print('-Den som känner landet väl är min vän')
                    else:
                        slowprint('-Ni känner landet väl. Då är ni mina vänner,\n'+
                              'jag ska lära er en användbar trollformel...\n'+
                              'Ni lärde er Tillkvicknande!')
                        for s in spelarlista:
                            s.magier.append(('Tillkvicknande',2))
                        progress['hittade_skatter'].add('skog')
                elif randint(0,4) > 1 and 'Trollkungen' not in progress['döda_fiender']:
                    if progress['main'] < 2:
                        fight()
                    else:
                        fight(OP=1)

            elif plats == 'Slottet':
                if progress['main'] < 2:
                    if 'Slottet' not in progress['hittade_skatter']:
                        print('En soldat: Var hälsad äventyrare. Härifrån regerar fursten Gurgen.')
                        fraga = dialog([0])
                        if fraga == 'Fråga om äventyr':
                            print('Jag är inte vilken soldat som helst.\n'+
                                  'En gång dräpte jag en stentiger i bergen, det har ingen annan klarat')
                            if 'Stentiger' in progress['döda_fiender']:
                                time.sleep(0.7)
                                slowprint('Har du också dräpt en stentiger? Otroligt!\n'+
                                          'Gurgen måste få träffa en sådan tapper kämpe...\n')
                                time.sleep(0.5)
                                slowprint('Ni ledsagas in i slottet, till tronrummet...\n'+
                                          'Furste Gurgen: Jag har hört om er tapperhet,\n'+
                                          'Mottag denna pilbåge som en gåva.\n'+
                                          'Du fick en pilbåge!')
                                inventory.append(FDICT['Pilbåge'])
                                progress['hittade_skatter'].add('Slottet')
                    else:
                        print('-Var hälsad slagskämpe!')
                        fraga = dialog([0])
                        if fraga == 'Fråga om äventyr':
                            print('Det bor en besynnerlig kvinna sydväst härifrån,\n'+
                                  'jag har hört att hon gillar fåglar')
                            
                elif progress['main'] == 3:
                    if 'Slottet' in progress['hittade_skatter']:
                        print('-Var hälsad slagskämpe!\n'+
                              'Jag beklagar men ingen kommer in här.')
                    else:
                        print('En soldat: Här kommer ingen in.')
                    while True:
                        fraga = dialog([0,2,4])
                        if fraga == 'Fråga om äventyr':
                            print('Har du träffat den märkliga mannen som flyttat in\n'+
                                  'i huset här i närheten? Det sägs att han besitter kraft\n'+
                                  'att förvandla ett material till ett annat.')
                        elif fraga == 'Fråga om Elaka häxan':
                            print('Den elaka häxan är borta,\n'+
                                  'det är bara monster kvar i Tornet')
                        elif fraga == 'Fråga om Snälla häxan':
                            print('Ja jag undrar var hon tagit vägen.\n'+
                                  'Gurgen brukade värdera hennes råd, och nu...')
                            time.sleep(2)
                            print('...Eller vänta vadå, vad menar ni.\n'+
                                  'Jag vet inte vad ni pratar om')
                            if 'Häxans ring' in [f.namn for f in inventory]:
                                time.sleep(2)
                                slowprint('Vänta, jag känner igen den där ringen.\n'+
                                      'Ni är verkligen den snälla häxans vänner eller hur?\n'+
                                      'Jag vet inte riktigt vad som pågår här,\n'+
                                      'men hovet vill inte längre höra talas om den snälla häxan.\n'+
                                      'Och Gurgen talar inte med någon utom sin nya rådgivare Amuno.\n'+
                                      'Jag såg dem ta med någon som jag tror är häxans vän\n'+
                                      'ned till fängelsehålan. Jag kan inte gå ned dit utan ärende,\n'+
                                      'men jag kan visa er vägen.\n')
                                if listval(['Gå ner i fängelsehålan','Vänta']) == 0:
                                    print('Ni kommer ned i en mörk tunnel.')
                                    time.sleep(2)
                                    print('Soldaten lämnar er och återgår till sin post.\n'+
                                          'Ni fortsätter vidare.')
                                    time.sleep(2)
                                    print('Ni kommer fram till den port som soldaten beskrivit.\n'+
                                          'Då hör ni en röst bakom er.')
                                    time.sleep(0.7)
                                    slowprint('Riddare Otak: Vad har ni här att göra?\n'+
                                              'Riddare Joshki: Det måste vara den elaka häxans\n'+
                                              'hantlangare, som Amuno varnat för!\n')
                                    fight(['Otak','Joshki'], True)
                                    print('Ni hittade en blå mantel')
                                    inventory.append(FDICT['Blå mantel'])
                                    time.sleep(1)
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
                                    position += 200
                                    progress['main'] = 4
                                    progress['hittade_skatter'].add('ZZ')
                                    progress['upptäckta_platser'].add(position)
                                    print('Ni står utanför slottet.')
                                    break
                        else:
                            print('Farväl')
                            break

                elif progress['main'] > 3 and position == 14:
                    if 'Shäxan' not in progress['hittade_skatter']:
                        print('Slottet är väl bevakat, ni kan inte närma er utan att bli upptäckta\n'+
                          'och ni har ingen chans att ta er in med våld.')
                    else:
                        print('En soldat: Var hälsade, fursten träffar er gärna.')
                        time.sleep(1)
                        print('Gurgen: Välkomna äventyrare. Det är en skam att jag lät\n'+
                              'mig förblindas av den elaka häxans trollkonst.')
                        if 'gurgens' not in progress['hittade_skatter']:
                            progress['hittade_skatter'].add('gurgens')
                            time.sleep(1.5)
                            slowprint('Mottag denna magiska mantel, den kan hjälpa er besegra henne\n')
                            inventory.append(FDICT['Gurgens mantel'])
                        else:
                            print('Må godheten nu segra.')

                elif position == 214:
                    print('En soldat: Hell kung Kolskägg! Signat vare prästerskapet!')
                    fraga = dialog([0,6])
                    if fraga == 'Fråga om äventyr':
                        print('Äventyret är inte tillåtet!')
                    elif fraga == 'Hell kung Kolskägg! Signat vare prästerskapet!':
                        print('Välkommen in frände.')
                        if 'vägtilldvärgen' in progress['hittade_skatter']:
                            print('Det är nog säkrast att inte gå in till borggården.')
                        else:
                            time.sleep(1.5)
                            print('Ni går in till borggården.\n'+
                                  'Där ser ni Unghäxan, som ni mötte i fängelsehålan för 50 år sedan!')
                            time.sleep(1)
                            print('Unghäxan: Det är ju ni! Äventyrarna från länge sen!\n'+
                                  'Ingen här vet vem jag egentligen är, så låt oss tala där ingen hör...')
                            while True:
                                fraga = dialog([2,3,4])
                                if fraga == 'Fråga om Elaka häxan':
                                    print('Amuno och den elaka häxan är en och samma.\n'+
                                          'Hon har låtit bygga ett tempel där tornet låg.')
                                    if 'Tempelbrosch' not in [f.namn for f in inventory]:
                                        slowprint('Om du har på dig den här broschen blir du insläppt.\n'+
                                                  '(Du fick en Tempelbrosch!)\n')
                                        inventory.append(FDICT['Tempelbrosch'])
                                        time.sleep(1)
                                    if 'templet' in progress['hittade_skatter']:
                                        slowprint('Ni kan inte komma åt Amuno i templet säger ni?\n'+
                                                  'Så ni vill hitta en väg in i slottet...\n')
                                        time.sleep(1)
                                        slowprint('Ok, vänta här...\n')
                                        slowprint('.....\n'*3,3)
                                        slowprint('Kusten är klar! Jag ska visa dig till kungens kammare.\n'+
                                                  'Men ingen annan kan följa med, då blir vi upptäckta.\n')
                                        spelarlista = [sp1]
                                        time.sleep(2)
                                        slowprint('Ni går upp många trappor, och kommer till kungens kammare\n'
                                                  'Ni går in, och där står riddare Joshki och kung Kolskägg...!\n'+
                                                  'Unghäxan lämnar rummet och låser dörren.\n'+
                                                  '-Förlåt mig.\n')
                                        time.sleep(1)
                                        slowprint('Kung Kolskägg: Tror ni jag är så dåraktig att jag lät en av häxans\n'+
                                                  'bundsförvanter röra sig fritt i mitt slott?\n'+
                                                  'Amuno har skänkt mig både vishet och styrka, inget undslipper min makt!\n\n'+
                                                  'Riddare Joshki: Låt mig undanröja denna fiende åt er, min konung!\n'+
                                                  'Kung Kolskägg: Låt gå!')
                                        time.sleep(2)
                                        fight(['Joshki2'],True)
                                        time.sleep(2)
                                        slowprint('Riddare Joshki: Jag har svikit ers majestät...\n'+
                                                  'Kung Kolskägg: Vilken beskvikelse!\n'+
                                                  'Nåja, nu ska du få känna på riktig makt!\n')
                                        time.sleep(1)
                                        slowprint('Men då...!\n')
                                        time.sleep(1)
                                        slowprint('Fönstret till kammaren krossas!\n'+
                                                  'In flyger en stor fågel bärande på en reslig krigare,\n'+
                                                  'fågeln byter skepnad och blir en kvinna.\n'+
                                                  'Alri och Svan: Vi förstod snart att något var fel,\n'+
                                                  'låt oss se vad den här falska kungen går för!\n')
                                        spelarlista = [sp1, svan, alri]
                                        time.sleep(1)
                                        slowprint('Kung Kolskägg: Ni ska alla dö!\n')
                                        fight(['Kolskägg'],True)
                                        time.sleep(2)
                                        slowprint('Kung Kolskägg: Aaargh!\n',2)
                                        print('Ni tog kungens gyllene mantel')
                                        inventory.append(FDICT['Gyllene mantel'])
                                        time.sleep(2)
                                        slowprint('Unghäxan kommer in i kammaren.\n'+
                                                  'Unghäxan: Vänta! Ni kan inte åstadkomma något mer genom att döda kungen.\n'+
                                                  'Jag vet att jag har svikit den snälla häxan.\n'+
                                                  'Men jag vet en annan vän till henne som jag hemlighållit för den elaka häxan.\n'+
                                                  'Det är en dvärg, och han bor nu i vildmarken i sydväst, jag ska förklara vägen för er.\n')
                                        time.sleep(1)
                                        slowprint('Ni lärde er vägen till dvärgens boning.\n'+
                                                  'Ni låter kungen och unghäxan gå och lämnar slottet.')
                                        progress['hittade_skatter'].add('vägtilldvärgen')
                                        break
                                elif fraga == 'Fråga om monster':
                                    print('Kungens riddare håller de flesta monstren borta från landsvägen,\n'+
                                          'men de andra är vredare och mer fruktansvärda än någonsin.')
                                elif fraga == 'Fråga om Snälla häxan':
                                    print('Den snälla häxan har övergivit oss. Vi måste klara oss själva nu')
                                else:
                                    print('Var försiktig')
                                    break                                       
                                
            elif plats == 'Stugan' and progress['main']>0:
                if progress['main']<2:
                    print('Snälla häxan: Hej äventyrare, vila en stund och återhämta er')
                    for s in spelarlista:
                        s.hp=s.liv
                    print('(Ni fick full hp)')

                    #sidequest
                    if progress['häxan'] == 0:
                        print('-Vill du lära dig trollkonst?\n'+
                              'Om du hittar en häxrot kan jag hjälpa dig')
                    elif 'Häxrot' in [f.namn for f in inventory]:
                        slowprint('-Har du hittat en häxrot säger du? Dåså...\n'+
                              'Den snälla häxan lagar till en häxbrygd...\n'+
                              'Du dricker av den, och sedan uttalar hon mystiska trollformler\n'+
                              'Du fick 50 exp, och kan nu lära dig trolldom!')
                        sp1.utveckling.append(['Trolldom',0])
                        sp1.exp += 50
                        lvlup(spelarlista)
                        progress['häxan']+=1
                        assert progress['häxan'] == 2
                        for f in [s for s in inventory if s.namn == 'Häxrot']:
                            inventory.remove(f)
                    elif progress['häxan'] == 2:
                        print('-Om du hittar en vacker grå sten på dina äventyr får du gärna komma med den till mig...')
                    elif 'Gråsten' in [f.namn for f in inventory]:
                        slowprint('-Åh! En gråsten! Tack, den kommer till användning\n'+
                                  'Ta den här fjädern som tack, och en läkört.\n')
                        inventory.append(kls.Foremal('Mystisk fjäder'))
                        inventory.append(FDICT['Läkört'])
                        progress['häxan']+=1
                        assert progress['häxan'] == 4
                        for f in [s for s in inventory if s.namn == 'Gråsten']:
                            inventory.remove(f)

                    while True:
                        fraga = dialog([0,2])
                        if fraga == 'Fråga om äventyr':
                            print('-Du måste besegra den elaka häxan som bor i tornet.\n'
                                  +'Smeden kan också hjälpa dig.\n'+
                                  'akta dig för demonen som bor i djupa dalen')
                            if d2 not in dialogval:
                                dialogval[2]=d2
                        elif fraga == 'Fråga om Elaka häxan':
                            print('Den elaka häxan är lömsk, lita inte på henne')
                        else:
                            print('Hejdå')
                            break

                #senare
                elif progress['main'] == 3 and d4 not in dialogval:
                #första gången tillbaks i vanliga världen 
                    if alri not in spelarlista:
                        if 9 in progress['upptäckta platser']:
                            slowprint('Den underliga kvinnan som du sett stå och flaxa med armarna är i Stugan\n')
                        else:
                            slowprint('En underlig kvinna är i Stugan\n')
                        slowprint('Alri: Den Snälla häxan har försvunnit, och den Elaka också.\n'+
                              'Och nu är alla monster starkare och fursten Gurgen gömmer sig.\n'+
                              'Jag tror att den Elaka häxan har hittat på något otyg...\n')
                        time.sleep(0.5)
                        slowprint('Vilka är ni?\n')
                        time.sleep(0.5)
                        slowprint('Jaså ni är vänner till den Snälla häxan.'+
                              'Då följer jag med er så ställer vi det här till rätta tillsammans\n'+
                              'Alri ansluter sig till ditt sällskap!\n')
                        spelarlista.append(alri)
                        alri.exp = int(sp1.exp*0.8)
                        if ('Tillkvicknande',2) in sp1.magier:
                            alri.magier.append(('Tillkvicknande',2))
                        if 'skugglandskap' in progress['hittade_skatter']:
                            alri.utveckling.append(['Hemlig lära',0])
                        lvlup(spelarlista)
                    else:
                        slowprint('Tomten Heyjafjej är i Stugan\n'+
                              'Heyjafjej: Den Snälla häxan har försvunnit, och den Elaka också.\n'+
                              'Och nu är alla monster starkare och fursten Gurgen gömmer sig.\n'+
                              'Jag tror att den Elaka häxan har hittat på något otyg...\n'+
                              'Jag vet att ni är den Snälla häxans vänner. Försök att hitta henne!\n')
                    dialogval[4] = d4 #fråga om snälla häxan

                elif progress['main'] < 5:
                    print('Det är ingen i Stugan')

                elif progress['main'] == 5 and 'Shäxan' not in progress['hittade_skatter']:
                    slowprint('Ulon: Här har jag byggt en hemlig källare\nUlon: ')
                    slowprint('LONME\n',2)
                    time.sleep(1)
                    slowprint('Golvet blir till en trappa ned!\n'+
                              'I källaren träffar ni den snälla häxan igen\n'+
                              'Snälla häxan: Det verkar som ni kom ut ur Skuggvärlden och\n'+
                              'har blivit mycket starkare. Bra gjort!\n'+
                              'Den elaka häxans inflytande blev mycket starkt så jag har\n'+
                              'varit tvungen att gömma mig och bida min tid.\n'+
                              'Men nu är det dags att konfrontera henne!\n')
                    time.sleep(1.5)
                    slowprint('Ni beger er till Slottet.\n')
                    time.sleep(1.5)
                    slowprint('Snälla häxan: Låt mig träffa Gurgen!\n'+
                              'Soldat: Men... Gurgen håller inga audienser mer.\n'+
                              'Snälla häxan: Ur vägen, ditt fån.\n'+
                              'Tillsammans med den snälla häxan går ni upp till Gurgen.\n'+
                              'Tronrummet är tomt, Gurgen sitter istället i en liten sidokammare.\n'+
                              'Snälla häxan: Det är dags för dig att återta ditt styre,\n'+
                              'och vakna upp: den som kallar sig Amuno som du lånat ditt öra,\n'+
                              'är ingen mindre än den Elaka häxan!\n')
                    time.sleep(1.5)
                    slowprint('Furste Gurgen vaknar ur sitt handlingsförlamade tillstånd\n'+
                              'Tillsammans går ni alla för att leta rätt på "Amuno".\n'+
                              'Men han finns ingenstans i Slottet.\n')
                    time.sleep(1)
                    slowprint('Snälla häxan: Amuno, eller snarare den elaka häxan,\n'+
                              'vågar inte visa sig här nu.\n'+
                              'Hon är försiktig...\n'+
                              'Hon måste ha flytt från slottet tillbaka till sitt Torn redan!\n')
                    time.sleep(1.5)
                    slowprint('Resten lämnar jag till er, äventyrare.\n'+
                              'Besegra elaka häxan i tornet och bringa frid till landet!\n')
                    position = 14
                    progress['hittade_skatter'].add('Shäxan')
                else:
                    print('Snälla häxan: Hej äventyrare, vila en stund och återhämta er')
                    for s in spelarlista:
                        s.hp=s.liv
                    print('(Ni fick full hp)')
                if 1 < progress['main'] < 5:
                    #(finns två olika fal då detta stämmer)
                    print('Den snälla häxans magi finns fortfarande kvar.\n'+
                          'Ni kan vila och återhämta er.')
                    for s in spelarlista:
                        s.hp=s.liv
                    print('(Ni fick full hp)')
                    
            elif plats == 'Templet':
                entre = 'Tempelbrosch' in [f.namn for f in inventory]
                if entre:    
                    print('En präst: Du är andligt upplyst ser jag,\n'+
                          'Gå i frid, signat vare prästerskapet.\n'+
                          'Ni går in i Templet.')
                    time.sleep(2)
                    print('En annan präst: Välkommen, vad söker Ni?')
                else:
                    print('En präst: Du får inte komma in här, detta är en helig plats')
                while True:
                    fraga = dialog([0,2,6,8])
                    if fraga == 'Fråga om äventyr':
                        print('Här ägnar vi oss inte åt sådant, utan åt Amunos lära.\n'+
                              'Vi är de magiska ordens beskyddare.')
                        dialogval[8] = d8
                    elif fraga == 'Fråga om Elaka häxan' and entre:
                        print('Amuno?\nTemplets innersta är skyddat av mäktig magi, det går inte att komma in.\n'+
                              'Men det talas om att Han ibland ger sig tillkänna på Slottet...\n'+
                              'Endast konungen är värdig att personligen möta Amuno, sägs det.')
                        progress['hittade_skatter'].add('templet')
                        if 'Häxans smaragd' in [f.namn for f in inventory] and listval(['Använd Häxans smaragd','Gör inget']) == 0:
                            pass #Hitta något coolt och möta en fet boss, se elaka häxan men hon försvinner
                    elif fraga == 'Fråga om Elaka häxan':
                        print('Några häxor finns inte mer här i landet.')
                    elif fraga == 'Hell kung Kolskägg! Signat vare prästerskapet!':
                        print('Hell kung Kolskägg! Signat vare prästerskapet!')
                    elif fraga == 'Fråga om böcker' and entre:
                        print('Vi har ett rikt bibliotek, prisa Amuno.\n'+
                              'Låt mig visa vägen')
                        time.sleep(2)
                        if 'Jotun' not in progress['hittade_skatter']:
                            print('Natu här är vår högst lärda.\n'+
                                  'Natu: ... Ja...? Vad gäller det?')
                            fraga2 = dialog([5,8])
                            if fraga2 == 'Fråga om böcker':
                                print('Natu: Hmm... Jag vet några som kan vara av intresse för er.\n'+
                                      'Hon tar fram ett antal volymer.')
                                if 'lärdom' not in progress['hittade_skatter']:
                                    slowprint('Ni får 800 exp!\n', 2)
                                    for s in spelarlista:
                                        s.exp += 800
                                    lvlup(spelarlista)
                                    progress['hittade_skatter'].add('lärdom')
                                else:
                                    print('Ni tittar bland böckerna men har redan läst allt ni kunde ta till er.')
                            elif fraga2 == 'Fråga om Una':
                                slowprint('Natu: ..........\n',2)
                                time.sleep(1)
                                slowprint('Bibliotekarien ser förskräct ut och börjar vända sig om och gå,\n'+
                                          'ni följer efter, men när ni rundar en bokhylla är hon försvunnen....!\n')
                                progress['hittade_skatter'].add('Jotun')
                            del fraga2
                        else:
                            print('Vår bibliotekarie har försvunnit, men ni är välkomna att se er omkring.')
                            if 'lärdom' not in progress['hittade_skatter']:
                                slowprint('Ni hittar en intressant bok där "Natu" försvann\n')
                                slowprint('Ni får 800 exp!\n', 2)
                                for s in spelarlista:
                                    s.exp += 800
                                lvlup(spelarlista)
                                progress['hittade_skatter'].add('lärdom')
                            else:
                                print('Ni tittar bland böckerna men har redan läst allt ni kunde ta till er.')
                        print('Ni går tillbaka från biblioteket tillbaka till prästen ni pratade med.')
                    elif fraga == 'Fråga om böcker':
                        print('Vi har ett fantastiskt bibliotek och en otroligt kunnig bibliotekarie.\n'+
                              'Men det är inte något som sådana som ni ska ta del av.')
                    else:
                        print('Adjö. Prisa Amuno.')
                        break
                           
            elif plats == 'Tornet':
                if progress['main'] < 2:
                    print('Du går upp för trapporna i tornet...\n'+
                          'Uppe hör du en röst som säger: Kom in...\n'+
                          'Elaka häxan: Välkomna vackra äventyrare')
                    while True:
                        fraga = dialog([0,1,2])
                        if fraga == 'Fråga om äventyr':
                            slowprint('-Kom med mig här, det finns så mycket jag kan lära er...\n'+
                                  '...\n...\n...\n'+
                                  'Du är ute ur tornet igen och du kommer inte ihåg vad som hände')
                            for s in spelarlista:
                                s.hp -= randint(1,5)
                                if s.hp < 1:
                                    s.hp = 1
                            break
                        elif fraga == 'Nu ska du få stryk!':
                            slowprint('-Hihihihihi!')
                            time.sleep(0.5)
                            fight(['Elaka häxan'],True)
                            progress['main'] += 1
                            print('Elaka häxan: Jag kan inte tro det!\n'+
                                  'Men ni ska inte besegra mig så lätt...!')
                            slowprint('.!?.!?.!?.!?.!?.!?.!?.!?.!?.!?.!?.!?.!?.!?.!?\n'+
                                      'Ni faller genom mörker...')
                            time.sleep(1.5)
                            print('Ni befinner er i en märklig värld av skuggor.')
                            position += 100
                            break
                        elif fraga == 'Fråga om Elaka häxan':
                            print('Den elaka häxan är lömsk, lita inte på henne\n'+
                                  'Hon bor i en stuga i skogen')
                        else:
                            print('Farväl då')
                            break
                elif 'Shäxan' not in progress['hittade_skatter']:
                    slowprint('Tornet är fullt av monster')
                    fight()
                else:
                    if 'tsv' not in progress['döda_fiender']:
                        print('En fruktansvärd tvåhövdad best vaktar ingången till tornet.\n'+
                              'Vill ni fortsätta?')
                        if listval(['Ja','Inte nu']) == 0:
                            fight(['Tornets väktare'],True)
                            progress['döda_fiender'].add('tsv')
                    if 'tsv' in progress['döda_fiender']:
                        print('Vill du fortsätta upp till elaka häxan?')
                        if listval(['Ja','Inte nu']) == 0:
                            slowprint('Ni går upp för trapporna till tornet...\n')
                            slowprint('Och ni går och går...........\n'+
                                      'Trapporna verkar inte ta slut?\n',2.5)
                            slowprint('Då hör ni ljud nedifrån, någon verkar vara på väg upp.\n'+
                                      'De är snart ikapp er\n')
                            time.sleep(1)
                            slowprint('Ni gör er redo för strid!\n')
                            time.sleep(1)
                            slowprint('Men upp kommer snälla häxan och unghäxan!\n'+
                                      '-Du kan inte skydda dig längre, Elaka häxa.\n'+
                                      'En vägg och dörr uppenbarar sig där trappan nyss fortsatte\n'+
                                      '-Gå nu äventyrare.\n'+
                                      'Jag och den elaka häxan är sammanbundna av gammal magi,\n'+
                                      'och kan aldrig strida mot varandra\n')
                            slowprint('Du stiger in till tornets högsta kammare\n',2)
                            slowprint('Elaka häxan: Ni har övervunnit många hinder, äventyrare.\n'+
                                      'Men har ni verkligen makt som kan mätas med min?\n')
                            time.sleep(1)
                            fight(['Elaka häxan2'],True)
                            time.sleep(2)
                            slowprint('Häxan blir till en skugga och försvinner från er syn.\n'+
                                      'Snälla häxan: Ni gjorde det...!\n'+
                                      'Då är det också dags för mig att blekna bort,\n'+
                                      'och återkomma i en annan tid...\n'+
                                      'Nu kommer det råda frid i landet, ni har gjort gott.\n'+
                                      'Må lyckan le mot er i framtida äventyr.\n')
                            time.sleep(2)
                            slowprint('Äventyret är slut.')
                            time.sleep(5)
                            raise SystemExit

            elif plats == 'trollskog':
                if 'trollskog' not in progress['hittade_skatter'] and random() > 0.8:
                    print('Ni träffar på tomten Gurtaburt.')
                    if foremaloverallt('Guldbåge') and foremaloverallt('Mästarsvärdet'):
                        slowprint('Gurtaburt: Ni är väldigt väl utrustade, då är ni mina vänner.\n'+
                                  'Jag ska lära er en magi och en stridsteknik.\n')
                        time.sleep(1.5)
                        for s in spelarlista:
                            s.magier.append(('Förgöra',4))
                            s.special.append('Kontring')
                        slowprint('Ni lärde er Förgöra och Kontring!\n')
                        progress['hittade_skatter'].add('trollskog')
                    else:
                        print('Gurtaburt: De som har de bästa vapnen är mina vänner.')
                elif randint(0,3) > 0:
                    fight()

            elif plats == 'träsk':
                if 'skog' in progress['hittade_skatter'] and 'Höga berget' not in progress['hittade_skatter'] and random() > 0.9:
                    print('Ni träffar på den gamla tomten Heyjafjej.\n'+
                          'Heyjafjej: Vi är redan vänner sedan gammalt,\n'+
                          'men jag tror inte du har träffat min kusin Sirkafirk\n'+
                          'som håller till på Höga berget.\nDet är bra att vara hans vän.')
                elif randint(0,4) > 1:
                    fight()

            elif plats == 'vilda berg':
                if random() > 0.9 and 'bergstrakter' not in progress['hittade_skatter']:
                    slowprint('Ni hittade en mäktig hammare!')
                    inventory.append(FDICT['Mäktig hammare'])
                    progress['hittade_skatter'].add('bergstrakter')
                elif randint(0,3) > 0:
                    fight()

            elif plats == 'vildmark':
                if random() > 0.9:
                    foremal = ['Mystisk sten','Livsfrukt','Kniv','Förtrollad sköld'][randint(0,3)]
                    slowprint('Ni hittar en '+foremal+'.\n')
                    inventory.append(FDICT[foremal])
                    del foremal
                if progress['main'] > 4:
                    print('Den snälla dvärgen möter er.\n'+'Dvärgen: Den snälla häxan...?\n'+
                          'Jag vet inte var hon är nu, hon försvann för 20 år sedan.\n'+
                          'Innan dess så var hon säker i en hemlig källare\n'+
                          'som jag byggde i hennes stuga.\n'+
                          'Den öppnade sig bara för den som sa "Lonme"...\n'+
                          'Men nu är stugan förstörd, och kvar är bara ett ödsligt fält.')
                elif 'vägtilldvärgen' in progress['hittade_skatter']:
                    print('Det verkar farligt, men vill du fortsätta mot dvärgens boning?')
                    if listval(['Ja', 'Nej']) == 0:
                        slowprint('Det är en svår väg, men ni lyckas undvika vilddjur och monster,\n'+
                                  'och till slut närmar ni er platsen där den snälla dvärgen ska bo.\n')
                        time.sleep(2)
                        slowprint('Där ser ni någon komma springande.\n'+
                                  'Han vinkar till er, det verkar vara rätt person!\n')
                        time.sleep(1.5)
                        slowprint('Dvärgen Ulon: Akta! Ni har väckt den fruktansvärda draken!\n'+
                                  'Titta bakom er....!!\n', 2)
                        spelarlista.append(dvargen)
                        if ('Tillkvicknande',2) in sp1.magier:
                            dvargen.magier.append(('Tillkvicknande',2))
                        if 'skugglandskap' in progress['hittade_skatter']:
                            dvargen.utveckling.append(['Hemlig lära',0])
                        fight(['Draken'], True)
                        if not foremaloverallt('Drakfjällsrustning'):
                            print('Ni hittade Drakfjällsrustning')
                            inventory.append(FDICT['Drakfjällsrustning'])
                        time.sleep(2)
                        slowprint('Ulon: Vi klarade det! Vilken strid!\n'+
                                  'kom in i min boning och vila upp er.\n')
                        for s in spelarlista:
                            s.hp = s.liv
                        print('Ni fick full hp.')
                        time.sleep(1.5)
                        slowprint('Varför har ni tappra äventyrare sökt upp mig på denna avlägsna plats?\n'+
                                  'Den snälla häxan...?\n'+
                                  'Jag vet inte var hon är nu, hon försvann för 20 år sedan.\n'+
                                  'Innan dess så var hon säker i en hemlig källare\n'+
                                  'som jag byggde i hennes stuga.\n'+
                                  'Den öppnade sig bara för den som sa "Lonme"...\n'+
                                  'Men nu är stugan förstörd, och kvar är bara ett ödsligt fält.\n')
                        time.sleep(1.5)
                        slowprint('Om er avsikt är att bistå den snälla häxan, låt mig hjälpa till.\n'+
                                  'Ulon anluter sig till ditt sällskap!\n')
                        progress['main'] = 5  
                else:
                    print('Det är för farligt att ge sig längre ut i vildmarken utan att veta vägen.')

            elif plats == 'ödemark':
                if 'ödemark' not in progress['hittade_skatter'] and random() > 0.9:
                    slowprint('Du hittar en välsignad rustning!')
                    progress['hittade_skatter'].add('ödemark')
                    inventory.append(FDICT['Välsignad rustning'])
                elif random() > 0.9:
                    slowprint('Du hittar en häxbrygd!')
                    inventory.append(FDICT['Häxbrygd'])
                elif random() > 0.6:
                    fight()
                                     
            elif plats == 'Ödsliga fältet':
                if random() > 0.7 and 'Ödsliga fältet' not in progress['hittade_skatter']:
                    slowprint('Du ser ett mäktigt lejon. Det verkar vänligt inställt...\n')
                    time.sleep(2)
                    godkand = False
                    for lista in alri.utveckling:
                        if lista[0] == 'Själskunskap' and lista[1] > 25:
                            godkand = True
                    if godkand:
                        slowprint('Lejonet kommer fram till Alri och räcker över en randig gren.\n',2)
                        inventory.append(FDICT['Randig gren'])
                        progress['hittade_skatter'].add('Ödsliga fältet')
                    else:
                        slowprint('Lejonet tycks vilja något, men ni kan inte få kontakt med det.\n')
                    slowprint('Lejonet går sin väg.\n')
                    del godkand
                elif random() > 0.7 and 'Zaumakot' not in progress['döda_fiender']:
                    print('En demon dyker upp...!\n'+
                          'Vill du strida mot demonen?')
                    if listval(['Ja','Nej']) == 0:
                        fight(['Zaumakot'],True)
                        progress['döda_fiender'].add('Zaumakot')
                else:
                    print('Det är väldigt ödsligt.')

        nyplats = False        
        print('\nMENY')
        val = ['Utforska','Föremål','Stats','Karta','Spara','Ladda','Avsluta']
        if 'Z' in progress['hittade_skatter']:
            val.insert(4,'Djurfrämlingens bok')
        mode=listval(val)
        
        if val[mode]=='Utforska':                   #utforska
            karta.rita(progress['upptäckta_platser'], position)
            print('Vart går ni?')
            riktning=listval(('Norr','Söder','Väst','Öst','Vänta lite'))
            if riktning==4:
                continue
            
            utfo = utforska(riktning)
            if utfo == 1:
                if progress['main']<1:
                    progress['main']=1
                nyplats=True
                continue
            elif utfo == 0:
                continue
            else:
                print('ogiltig riktning')
                continue

        elif val[mode]=='Föremål':
            foremalsmeny()
            continue

        elif val[mode]=='Stats':
            for s in spelarlista:
                print('\n'+s.namn+':\n'+
                      'nivå '+str(s.lvl)+'  '+s.hpstr()+'\n'+
                      'Styrka: '+str(s.stats['str'])+'  Smidighet: '+str(s.stats['smi'])+'  Magikraft: '+str(s.stats['mkr'])+'\n'+
                      'Vapen: '+s.utrust['vapen'].namn+' (S+'+str(int(getattr(s.utrust['vapen'],'skada',0)*2))+
                      ' M+'+str(int(getattr(s.utrust['vapen'],'magi',0)*2))+')'+
                      '  Rustning: '+s.utrust['rustning'].namn+' (S+'+str(getattr(s.utrust['rustning'],'skydd',0))+
                      ' M+'+str(getattr(s.utrust['rustning'],'mskydd',0))+')'+
                      '\nÖvrigt: '+s.utrust['ovrigt'].namn+' ('+getattr(s.utrust['ovrigt'],'kortbs','')+')')
                if len(s.formagor) > 0:
                    print('Förmågor: '+', '.join(set(s.formagor)))
                if len(s.magier) > 0:
                    print('Magier: '+', '.join(set(spell[0] for spell in s.magier)))
                if len(s.special) > 0:
                    print('Specialförmågor: '+', '.join(set(s.special)))
            input('\n(tryck enter för att fortsätta)')
            continue

        elif val[mode]=='Karta':
            karta.rita(progress['upptäckta_platser'], position)
            continue

        elif val[mode]=='Avsluta':
            print('Slut på äventyret')
            raise SystemExit
        
        elif val[mode]=='Spara':
            spara()
            print('Sparat!')
            continue
        
        elif val[mode]=='Ladda':
            ladda()
            print('Laddat!')
            #test
            print('Äventyrare: '+sp1.namn)
            lvlup(spelarlista)
            if progress['main'] == 2 and position < 100:
                slowprint('Den elaka häxan har skickat dig till en underlig värld av skuggor!')
                position = 116
            elif progress['main'] == 4 and 214 not in progress['upptäckta_platser']:
                position += 200
                progress['upptäckta_platser'].add(position)
                overgang3till4()
                
        elif val[mode]=='Djurfrämlingens bok':
            lista = ['Vanliga världen', 'Skuggvärlden']        
            if 'ZZ' in progress['hittade_skatter']:
                lista.append('50 år framåt')
            if 'ZZZ' in progress['hittade_skatter']:
                lista.append('200 år bakåt')
            if position < 100:
                lista.remove('Vanliga världen')
            elif position < 200:
                lista.remove('Skuggvärlden')
            elif position < 300:
                lista.remove('50 år framåt')
            else:
                lista.remove('200 år bakåt')
            varld = lista[listval(lista)]
            print('Du läser ur Djurfrämlingens bok...!')
            time.sleep(1)
                
            position -= 300
            while True:
                if varld == 'Vanliga världen' and position > 0 and position < 100:
                    print('Ni är nu i '+varld)
                    break
                elif varld == 'Skuggvärlden' and position > 100 and position < 200:
                    print('Ni är nu i '+varld)
                    break
                elif varld == '50 år framåt' and position > 200 and position < 300:
                    print('Ni är nu '+varld+' i tiden')
                    break
                elif varld == '200 år bakåt' and position > 300:
                    print('Ni är nu '+varld+' i tiden')
                    break
                position += 100
            nyplats = True
            progress['upptäckta_platser'].add(position)
            print('Ni kommer till '+PDICT[position])
                
                
#fler funktioner:

def fight(plats='plats', specifik=False, OP=0):
    if plats == 'plats':
        plats = PDICT[position]
    loot = fightfunc(spelarlista, inventory, progress, plats, specifik, OP=OP)
    if loot == 'game over':
        print('Du är besegrad.\nSlut på äventyret.')
        time.sleep(4)
        raise SystemExit
    if loot != None:
        for f in loot:
            inventory.append(FDICT[f])
    lvlup(spelarlista)
    

def utforska(riktning):
    global position
    gammalpos = position
    grid_pos = position
    while grid_pos > 100:
        grid_pos -= 100
        #grid_pos används för att kolla att man inte hamnar utanför grid oavsett vilken värld

    if riktning==0: #norr
        if grid_pos < 13:
            position+=4
        else:
            print('Ni kommer inte längre i den riktningen\n')
            return 0            
    elif riktning==1: #söder
        if grid_pos > 4:
            position-=4
        else:
            print('Ni kommer inte längre i den riktningen\n')
            return 0            
    elif riktning==2: #väst
        if not (grid_pos-1) % 4 == 0:
            position-=1
        else:
            print('Ni kommer inte längre i den riktningen\n')
            return 0            
    elif riktning==3: #öst
        if not grid_pos % 4 == 0:
            position+=1
        else:
            print('Ni kommer inte längre i den riktningen\n')
            return 0            
    else:
        return False

    #special
    if progress['main'] == 2:
        if position < 107 or position == 109 or position == 113:
            position = gammalpos
            print('Skuggorna är för täta för att komma vidare...')
            return 0
    elif PDICT[position] == 'Höga berget' and abs(gammalpos - position) < 50: #special, höga berget
        if 'Magiskt rep' not in [f.namn for f in inventory] and abs(gammalpos - position) < 50:
            progress['upptäckta_platser'].add(position)
            position = gammalpos
            print('Ni kan inte ta er upp på Höga berget')
            return 0
    elif position == 105 and gammalpos < 200 and gammalpos > 100: #special, buren
        position = gammalpos
        print('Ni stoppas av ett konstigt enormt stängsel som verkar skyddas av magi.\n'+
              'Någonstans där inuti anar ni en främmande fruktansvärd makt.')
        progress['upptäckta_platser'].add(105)
        return 0

    if progress['main'] != 2: #platser sparas först inte på kartan i skuggvärlden
        progress['upptäckta_platser'].add(position)
    plats = PDICT[position]

    #randomencounter
    if plats in LANDSKAP: 
        print('Ni går genom '+ plats +'...\n')
    elif plats == 'landsväg':
        print('Ni går på '+ plats +'...\n')
    else:
        print('Ni kommer till '+plats+'\n')

    return 1



#---------------------------------------------konstanter

# dictionary med alla föremål
FDICT = {
    '-': kls.Foremal('-'), #tomt namn
    'Fiskstål': kls.Foremal('Fiskstål'),
    'Gråsten': kls.Foremal('Gråsten'),
    'Mystisk sten': kls.Foremal('Mystisk sten'),
    'Mystisk fjäder': kls.Foremal('Mystisk fjäder'),
    'Häxrot': kls.Foremal('Häxrot'),
    'Tand': kls.Foremal('Tand'),
    'Tempelbrosch': kls.Foremal('Tempelbrosch'),
    'Häxans ring': kls.Foremal('Häxans ring'),
    'Randig gren': kls.Foremal('Randig gren'),
    'Okänd materia': kls.Foremal('Okänd materia'),
    'Älvstoft': kls.Foremal('Älvstoft'),
    'Magiskt rep': kls.Foremal('Magiskt rep'),
    'Kniv': kls.Vapen('Kniv',0.7),
    'Svärd': kls.Vapen('Svärd',1),
    'Bra svärd': kls.Vapen('Bra svärd',2,5,'str'),
    'Mystisk dolk': kls.Vapen('Mystisk dolk',2,5,'mkr',magi=1),
    'Pilbåge': kls.Vapen('Pilbåge',2,5,'smi'),
    'Tandkniv': kls.Vapen('Tandkniv',2.5),
    'Fiskspjut': kls.Vapen('Fiskspjut',3),
    'Bra pilbåge': kls.Vapen('Bra pilbåge',3.5,7,'smi'),
    'Jotuns hammare': kls.Vapen('Jotuns hammare',3,7,'str',magi=3),
    'Mystiskt spjut': kls.Vapen('Mystiskt spjut',4.5,7,'mkr',magi=1.5),
    'Tungt svärd': kls.Vapen('Tungt svärd',5,9,'str'),
    'Förhäxad spira': kls.Vapen('Förhäxad spira',2.5,9,'mkr',magi=3.5),
    'Dödlig kniv': kls.Vapen('Dödlig kniv',6,11,'smi'),
    'Förtrollad hammare': kls.Vapen('Förtrollad hammare',5.5,9,'mkr',magi=1.5),
    'Konungasvärd': kls.Vapen('Konungasvärd',6,9,'str',magi=2),
    'Skuggsvärd': kls.Vapen('Skuggsvärd',5,magi=4),
    'Mäktig hammare': kls.Vapen('Mäktig hammare',7.5,12,'str',magi=2),
    'Alvbåge': kls.Vapen('Alvbåge',6.5,14,'smi',magi=4.5),
    'Silvertunga': kls.Vapen('Silvertunga',7.5,11,'mkr',magi=3),
    'Guldspira': kls.Vapen('Guldspira',3,magi=7),
    'Mästarsvärd': kls.Vapen('Mästarsvärd',6.5,7,'str',magi=3),
    'Mästarsvärdet': kls.Vapen('Mästarsvärdet',9.5,11,'str',magi=5),
    'Silverbåge': kls.Vapen('Silverbåge',6.5,9,'smi',magi=3.5),
    'Guldbåge': kls.Vapen('Guldbåge',8.5,11,'smi',magi=6),
    'Lätt rustning': kls.Rustning('Lätt rustning',1),
    'Brynja': kls.Rustning('Brynja',2),
    'Drakfjällsbrynja': kls.Rustning('Drakfjällsbrynja',3,5,'str',mskydd=1),
    'Tung rustning': kls.Rustning('Tung rustning',5,6,'str'),
    'Magisk rustning': kls.Rustning('Magisk rustning',5,6,'mkr',mskydd=5),
    'Riddarrustning': kls.Rustning('Riddarrustning',6,8,'str',mskydd=3),
    'Ormdräkt': kls.Rustning('Ormdräkt',7,8,'smi',mskydd=5),
    'Välsignad rustning': kls.Rustning('Välsignad rustning',6,7,'mkr',mskydd=5),
    'Mitrilbrynja': kls.Rustning('Mitrilbrynja',7,mskydd=2),
    'Järnskinnsdräkt': kls.Rustning('Järnskinnsdräkt',9,10,'str'),
    'Drakfjällsrustning': kls.Rustning('Drakfjällsrustning',8,10,'mkr',mskydd=7),
    'Dimsilverbrynja': kls.Rustning('Dimsilverbrynja',6,mskydd=10),
    'Mitrilrustning': kls.Rustning('Mitrilrustning',10,mskydd=4),
    'Megarustning': kls.Rustning('Megarustning',9,mskydd=8),
    'Ziriekls rustning': kls.Rustning('Ziriekls rustning', 10, mskydd=10),
    'Skyddande ädelsten': kls.Ovrigt('Skyddande ädelsten','+1 beskydd',2,1),
    'Svart mantel': kls.Ovrigt('Svart mantel','+3 beskydd',2,3),
    'Förtrollad sköld': kls.Ovrigt('Förtrollad sköld','+4 beskydd',2,4),
    'Gyllene mantel': kls.Ovrigt('Gyllene mantel','+6 beskydd',2,6),
    'Grön mantel': kls.Ovrigt('Grön mantel','+40 liv','liv',40),
    'Zaumakots ring': kls.Ovrigt('Zaumakots ring','+100 liv','liv',100),
    'Blå mantel': kls.Ovrigt('Blå mantel','+2 snabbhet',0,-2),
    'Dvärgens mantel': kls.Ovrigt('Dvärgens mantel', '+3 styrka, Lyckoträff', 'str',3,(3,'Lyckoträff')),
    'Gurgens mantel': kls.Ovrigt('Gurgens mantel', '+1 smidighet, Lura döden', 'smi',1,(3,'Lura döden')),
    'Guldlänk': kls.Ovrigt('Guldlänk','+2 magikraft','mkr',2),
    'Magisk ring': kls.Ovrigt('Magisk ring','+3 magikraft','mkr',3),
    'Trollring': kls.Ovrigt('Trollring','+4 magikraft','mkr',4),
    'Skuggornas ring': kls.Ovrigt('Skuggornas ring','+5 magikraft','mkr',5),
    'Guldring': kls.Ovrigt('Guldring','+3 styrka','str',3),
    'Guldhandske': kls.Ovrigt('Guldhandske','+4 styrka','str',4),
    'Kraftring': kls.Ovrigt('Kraftring','+5 styrka', 'str', 5),
    'Amulett': kls.Ovrigt('Amulett','+3 smidighet','smi',3),
    'Skuggskor': kls.Ovrigt('Skuggskor','+4 smidighet','smi',4),
    'Förtrollad dräkt': kls.Ovrigt('Förtrollad dräkt', '+5 smidighet', 'smi', 5),
    'Zlokrs kappa': kls.Ovrigt('Zlokrs kappa','+7 undvikning',3,7),
    'Magiskt armband': kls.Ovrigt('Magiskt armband','+5 pricksäkerhet',1,5),
    'Djurfrämlingens mask': kls.Ovrigt('Djurfrämlingens mask','+15 styrka', 'str', 15),
    'Blå ring': kls.Ovrigt('Blå ring','+10 liv, Förmåga-Återhämtning 2','liv',10,(1,'Återhämtning 2')),
    'Lyckosmycke': kls.Ovrigt('Lyckosmycke','+1 smidighet, Skattletande"','smi',1,(3,'Skattletande')),
    'Rubin': kls.Ovrigt('Rubin','+2 smidighet, Skattletande 2','smi',2,(3,'Skattletande 2')),
    'Blodkristall': kls.Ovrigt('Blodkristall','+2 styrka, Dubbel attack','str',1,(3,'Dubbel attack')),
    'Tapperhetsmedalj': kls.Ovrigt('Tapperhetsmedalj','+15 liv, Stridsinsikt','liv',15,(3,'Stridsinsikt')),
    'Förbannad juvel': kls.Ovrigt('Förbannad juvel','+2 magikraft, Magi-Förtärande mörker','mkr',2,(2,'Förtärande mörker',5)),
    'Trädgrenskrona': kls.Ovrigt('Trädgrenskrona','+3 magikraft, Förmåga-Urkraft','mkr',3,(1,'Urkraft')),
    'De gamlas ring': kls.Ovrigt('De gamlas ring','+60 liv, Magi-Lindring','liv',60,(2,'Lindring',1)),
    'Uråldrig kristall': kls.Ovrigt('Uråldrig kristall','+3 magikraft, Magi-Livskraft','mkr',3,(2,'Livskraft',5)),
    'De vises sten': kls.Ovrigt('De vises sten','+2 magikraft, Dubbel magi','mkr',2,(3,'Dubbel magi')),
    'Salva': kls.EngangsForemal('Salva','Läkande',difstat,('hp',15),fight=True),
    'Läkört': kls.EngangsForemal('Läkört','Läkande',difstat,('hp',60),fight=True),
    'Häxbrygd': kls.EngangsForemal('Häxbrygd','Läkande',difstat,('hp',150),fight=True),
    'Elixir': kls.EngangsForemal('Elixir','Återställer full hp',difstat,('hp',2000),fight=True),
    'Själsstoft': kls.EngangsForemal('Själsstoft','+1 magikraft permanent',difstat,('mkr',1,7)),
    'Trollsländsvinge': kls.EngangsForemal('Trollsländsvinge','+1 smidighet permanent',difstat,('smi',1,7)),
    'Vargblod': kls.EngangsForemal('Vargblod','+1 styrka permanent',difstat,('str',1,7)),
    'Demondryck': kls.EngangsForemal('Demondryck','+1 magikraft permanent',difstat,('mkr',1)),
    'Ormmedicin': kls.EngangsForemal('Ormmedicin','+1 smidighet permanent',difstat,('smi',1)),
    'Livsfrukt': kls.EngangsForemal('Livsfrukt','+1 styrka permanent',difstat,('str',1)),
    'Kraftdryck': kls.EngangsForemal('Kraftdryck','+20 liv',difstat,('liv',20))
    }

ALDICT = {
    'Okänd materia': 50,
    'Älvstoft': 8,
    'Svärd': 3,
    'Bra svärd': 6,
    'Tungt svärd': 12,
    'Kniv': 2,
    'Mystisk dolk': 6,
    'Tandkniv': 8,
    'Fiskspjut': 10,
    'Mystiskt spjut': 15,
    'Jotuns hammare': 15,
    'Pilbåge': 6,
    'Bra pilbåge': 12,
    'Tungt svärd': 18,
    'Förhäxad spira': 18,
    'Förtrollad hammare': 22,
    'Dödlig kniv': 22,
    'Konungasvärd': 24,
    'Skuggsvärd': 28,
    'Guldspira': 38,
    'Alvbåge': 34,
    'Mäktig hammare': 34,
    'Lätt rustning': 3,
    'Brynja': 5,
    'Drakfjällsbrynja': 8,
    'Tung rustning': 10,
    'Magisk rustning': 12,
    'Välsignad rustning': 18,
    'Mitrilbrynja': 20,
    'Drakfjällsrustning': 25,
    'Dimsilverbrynja': 25,
    'Guldlänk': 6,
    'Skyddande ädelsten': 4,
    'Förtrollad sköld': 20,
    'Magisk ring': 12,
    'Trollring': 20,
    'Guldring': 12,
    'Guldhandske': 20,
    'Kraftring': 30,
    'Amulett': 12,
    'Skuggskor': 20,
    'Förtrollad dräkt': 30,
    'Blå ring': 18,
    'Lyckosmycke': 20,
    'Rubin': 30,
    'Blodkristall': 25,
    'Tapperhetsmedalj': 30,
    'Förbannad juvel': 22,
    'Trädgrenskrona': 25,
    'Uråldrig kristall': 35,
    'Salva': 1,
    'Läkört': 5,
    'Häxbrygd':10,
    'Elixir': 20,
    }

PDICT={
    1:'Djupa dalen',
    2:'berg',
    3:'skog',
    4:'skog',
    5:'Höga berget',
    6:'berg',
    7:'Stugan',
    8:'Smeden',
    9:'Ett hus',
    10:'skog',
    11:'skog',
    12:'skog',
    13:'berg',
    14:'Slottet',
    15:'skog',
    16:'Tornet',
    101:'En källare',
    102:'skugglandskap',
    103:'mörkt vatten',
    104:'mörkt vatten',
    105:'Buren',
    106:'skugglandskap',
    107:'mörkt vatten',
    108:'skugglandskap',
    109:'skugglandskap',
    110:'skugglandskap',
    111:'Ett fort',
    112:'En äng',
    113:'En grotta',
    114:'Gården',
    115:'skugglandskap',
    116:'skugglandskap',
    201:'vildmark',
    202:'träsk',
    203:'träsk',
    204:'En glänta',
    205:'Höga berget',
    206:'landsväg',
    207:'Ödsliga fältet',
    208:'Gamla smeden',
    209:'Huset',
    210:'landsväg',
    211:'ödemark',
    212:'träsk',
    213:'landsväg',
    214:'Slottet',
    215:'landsväg',
    216:'Templet',
    301:'Djupa dalen',
    302:'Dvärgbyn',
    303:'trollskog',
    304:'trollskog',
    305:'Höga berget',
    306:'vilda berg',
    307:'trollskog',
    308:'trollskog',
    309:'vilda berg',
    310:'vilda berg',
    311:'trollskog',
    312:'En boning',
    313:'vilda berg',
    314:'djup skog',
    315:'trollskog',
    316:'trollskog'
    }

karta = kls.Karta(PDICT)

LANDSKAP = {'skog', 'berg', 'skugglandskap', 'mörkt vatten', 'träsk', 'ödemark'}

#position i rutnät 4*4 (16 platser)
position=7


#progress,ett dictionary
progress={'main':0,
          'häxan':0, #snälla häxan
          'smeden':0,
          'alkemisten':0,
          'hittade_skatter':{'x'},  #set med platsnamn och en del andra namn
          'upptäckta_platser':{6,7,11,14},
          'döda_fiender':{'x'}}

#dialogval, somliga kommer till och försvinner beroende på quests
d0='Fråga om äventyr'
d1='Nu ska du få stryk!'
d2='Fråga om Elaka häxan'
d3='Fråga om monster'
d4='Fråga om Snälla häxan'
d5='Fråga om Una'
d6='Hell kung Kolskägg! Signat vare prästerskapet!'
d7='Fråga om Mästarsmeden'
d8='Fråga om böcker'
dX='Ta avsked'

#från början
dialogval=[d0,0,0,0,0,0,0,0,0,
           dX]

#inventory
inventory=list()
        
#vänner
svan = kls.Spelare('Svan',30,3,2,3,[['Kamp',0],['Dunkel konst',0]])
alri = kls.Spelare('Alri',25,3,3,4,[['Skicklighet',0],['Själskunskap',0]])
dvargen = kls.Spelare('Ulon',121,11,10,10,[['Trolldom',20],['Uthållighet',0]])
dvargen.utrust['vapen'] = FDICT['Förtrollad hammare']
dvargen.utrust['rustning'] = FDICT['Mitrilbrynja']
dvargen.utrust['ovrigt'] = FDICT['Dvärgens mantel']
dvargen.lvl = 40
dvargen.exp = 20738
dvargen.formagor = ['Mystisk kraft']
dvargen.magier = [('Hypnos',1),('Lindring',1),('Kyla',2),('Trollstyrka',1),('Helning',1),('Sömnighet',3),('Upplyftning',3)]
dvargen.special = ['Lyckoträff']



#början av spelet
print('\nVälkommen till Sagan om äventyret\n')

if listval(['Nytt äventyr','Ladda']) == 1:
    sp1=kls.Spelare('x',25,3,3,3,[['Kamp',0],['Skicklighet',0]]) #meningslös mall
    ladda()
    print('Laddat!')
    #test
    print('Äventyrare: '+sp1.namn)
    lvlup(spelarlista)
    if progress['main'] == 2 and position < 100:
        slowprint('Den elaka häxan har skickat dig till en underlig värld av skuggor!')
        position = 116
    elif progress['main'] == 4 and 214 not in progress['upptäckta_platser']:
        position += 200
        progress['upptäckta_platser'].add(position)
        overgang3till4()

else:
    #spelare
    spelarnamn = input('Vad heter äventyraren?\n')
    sp1=kls.Spelare(spelarnamn,25,3,3,3,[['Kamp',0],['Skicklighet',0]])
    del spelarnamn
    spelarlista=[sp1, svan]

    slowprint('\nDetta är sagan om '+sp1.namn+'\n')

    slowprint('Du hade lämnat hemstaden för att söka lyckan\n'+
          'men gått vilse i Gamla skogen\n'+
          'Som tur var hittade du en grön stuga där det bodde en snäll häxa\n'+
          'som gav dig mat och husrum. \n\n'+
          'Sen sa den snälla häxan: Nu ska du gå på äventyr.\n'+
          'Akta dig för monster i skogen, och ännu mer i bergen.\n'+
          'Om du är skadad kan du komma tillbaka hit och få hjälp.\n\n'+
          'Jag låter Svan följa dig på vägen. Han är en duglig man på alla sätt.\n')

    #startforemål
    startforemal = set()
    while True:
        x = ['Svärd','Kniv','Lätt rustning','Salva','Salva','Salva','Trollsländsvinge','Vargblod'][randint(0,7)]
        startforemal.add(x)
        if len(startforemal) == 3:
            break
    startforemal = list(startforemal)
    for f in startforemal:
        inventory.append(FDICT[f])
    slowprint('Den snälla häxan gav dig '+startforemal[0]+', '+startforemal[1]+' och '+startforemal[2]+'\n')
    del startforemal
    del x

meny()

print('Äventyret är slut')
