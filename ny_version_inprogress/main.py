from random import randint, random
import os
import time

import klasser as kls
from fightfunks import fight as fightfunc
from lvlup import lvlup
from funktioner import difstat, plusformaga, listval, slowprint, uniquelist, overgang3till4
from collections import OrderedDict

#lägg till / testa:
#platser och rörelse -- FIXAT
#inventorymeny -- FIXAT
#karta -- FIXAT
#hela fightfunks -- FIXAT
#dictionary med föremål, förenkla ladd och spar -- FIXAT
#spar och ladd, detaljerat -- FIXAT
#GÖR SÅ DIALOGVAL SPARAS -- FIXAT

#Djurfrämlingens bok -- FIXAT? #Djufrämlingens namn Zeoidodh
#skuggvärlden


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
                +'\n'+'___'.join([f.namn for f in inventory[1:]])+'\n') #41
        if alri in spelarlista:
            f.write('a\n') #42
        else:
            f.write('x\n') #43
        f.write(str(position)) #44

    
    
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
            magier_2 = list(map(int,f.readline().strip('\n').split('___')))        #11
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
            magier_2 = list(map(int,f.readline().strip('\n').split('___')))        #11
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
            magier_2 = list(map(int,f.readline().strip('\n').split('___')))        #11
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

        inventory=list()  #föremål 0 är bara ett menyval
        for s in f.readline().strip('\n').split('___'):                        #41
            if s != '':
                inventory.append(FDICT[s])

        spelarlista = [sp1, svan]
        special = f.readline().strip()
        if special == 'a':                              #42
            spelarlista.append(alri)

        position = int(f.readline().strip())                        #43


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
        
#ofärdig meny
def meny():
    global inventory
    global progress
    global dialogval
    global position

    nyplats = False
    
    while True:
        plats = PDICT[position]

        if nyplats:
            
            if plats == 'berg':
                if 'berg' not in progress['hittade_skatter'] and randint(0,6) == 6:
                    slowprint('Du hittar en Skyddande ädelsten!')
                    inventory.append(FDICT['Skyddande ädelsten'])
                    progress['hittade_skatter'].add('berg')
                elif randint(0,4) > 1:
                    if progress['main'] < 2:
                        fight()
                    else:
                        fight(OP=1)           
                nyplats = False

            elif plats == 'Buren':
                if 'Zeoidodh' not in progress['döda_fiender']:
                    time.sleep(1.5)
                    print('\nDJURFRÄMLINGEN KOMMER MOT ER\n')
                    time.sleep(1.5)
                    print('Är ni redo?')
                    time.sleep(1.5)
                    if 'Zeoidodh' in progress['hittade_skatter']:
                        #bättre odds om man kan hens namn
                        fight(['Zeoidodh'],True)
                    else:
                        fight(['Djurfrämlingen'],True)
                    progress['döda_fiender'].add('Zeoidodh')
                nyplats = False

            elif plats == 'Djupa dalen':
                if randint(0,3) == 3 and 'Demonen Zlokr' not in progress['döda_fiender']:
                    print('En demon dyker upp...!\n'+
                          'Vill du strida mot demonen?')
                    if listval(['Ja','Nej']) == 0:
                        fight(['Demonen Zlokr'],True)
                        progress['döda_fiender'].add('Demonen Zlokr')
                elif randint(0,4) > 1:
                    if progress['main'] < 2:
                        fight()
                    else:
                        fight(OP=1)
                nyplats = False

            elif plats == 'En grotta': #lägg till bossar och bonusar
                if listval(['Gå in i grottan','Stanna utanför']) == 0:
                    if 'Gaurghus' not in progress['döda_fiender']:
                        fight(['Gaurghus'],True)
                        slowprint('Ni hittar Demondryck, Ormmedicin, Livsfrukt\n'+
                              'och en Mystisk sten, inne i grottan.')
                        for i in ['Demondryck', 'Ormmedicin', 'Livsfrukt', 'Mystisk sten']:
                            inventory.append(FDICT[i])
                        progress['döda_fiender'].add('Gaurghus')
##                    elif progress['main'] > 4 and nånting not in progress['hittade_skatter']:
##                        fight(['Boss'],True)
##                        #svan lär sig nån specialgrej
##                    elif progress['main'] > 5 and nånting in progress['hittade_skatter']:
##                        #få nånting
                    else:
                        print('Grottan verkar vara tom, men ni känner av\n'+
                              'en obehaglig närvaro')
                nyplats = False

            elif plats == 'En källare': #här får man en uppgradering till Djurfrämlingens bok
                if 'Jotun' in progress['hittade_skatter']:
                    print('Det är en jätte i källaren.')
                    if 'ZZZ' not in progress['hittade skatter']: 
                        dialogval[8] = d8
                        if dialog([8]) == 'Fråga om böcker':
                            slowprint('När jätten ser att du har Djufrämlingens bok blir hon förskräckt.\n'+
                                  'Det är hon som har skrivit den åt Djurfrämlingen säger hon.\n'+
                                  'Efter en stund så tittar hon i den, tar fram en penna och skriver något...')
                            progress['hittade_skatter'].add('ZZZ')
                elif 'källare' in progress['hittade_skatter']:
                    print('Det är ingen här, bara massa böcker')
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

                nyplats=False

            elif plats == 'En äng':
                print('Det känns skönt att vara här!\n'+
                      'Ni fick full hp.')
                for s in spelarlista:
                    s.hp = s.liv
                nyplats = False
                          
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
                                else:
                                    print('Det finns en grotta västerut.\n'+
                                          'Men jag har aldrig vågat gå in...')
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
                nyplats = False

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
                        if progress['alkemisten'] > 1260:
                            print('Alkemisten: Jag kan inte skapa något mer till er.')
                            break
                        print('ALKEMISTEN')
                        obj = listval([inventory[0].namn]+
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
                        
                            
                            
                nyplats = False

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
                            
                nyplats = False
                            
            elif plats == 'mörkt vatten':
                if 'mörkt vatten' not in progress['hittade_skatter'] and randint(0,6) == 6:
                    print('Du hittar en blå ring!')
                    inventory.append(FDICT['Blå ring'])
                    progress['hittade_skatter'].add('mörkt vatten')
                elif randint(0,4) > 1:
                    fight()                   
                nyplats = False

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
                    elif max([s.lvl for s in spelarlista])>22 and progress['smeden']<5:
                        slowprint('Här får du en guldhandske.\n')
                        inventory.append(FDICT['Guldhandske'])
                        progress['smeden']+=1
                    elif max([s.lvl for s in spelarlista])>32 and progress['smeden']<6:
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
                        nyplats=False
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
                nyplats = False

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
                elif randint(0,4) > 1:
                    if progress['main'] < 2:
                        fight()
                    else:
                        fight(OP=1)
                nyplats = False

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

                elif progress['main'] == 4 and position == 14:
                    print('Slottet är väl bevakat, ni kan inte närma er utan att bli upptäckta\n'+
                          'och ni har ingen chans att ta er in med våld.')

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
                                                  'Unghäxan lämnar rummet och låser dörren.\n+
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
                                        slowprint('Men då...!')
                                        time.sleep(1)
                                        slowprint('Fönstret till kammaren krossas!\n'+
                                                  'In flyger en stor fågel bärande på en reslig krigare,\n'+
                                                  'fågeln byter skepnad och blir en kvinna.\n'+
                                                  'Alri och Svan: Vi förstod snart att något var fel,\n'+
                                                  'låt oss se vad den här falska kungen går för!\n')
                                        time.sleep(1)
                                        slowprint('Kung Kolskägg: Ni ska alla dö!')
                                        fight(['Kolskägg'],True)
                                        time.sleep(2)
                                        slowprint('Kung Kolskägg: Aaargh!',2)
                                        print('Ni tog kungens gyllene mantel')
                                        inventory.append(FDICT['Gyllene mantel'])
                                        time.sleep(2)
                                        slowprint('Unghäxan kommer in i kammaren.\n'+
                                                  'Unghäxan: Vänta! Ni kan inte åstadkomma något mer genom att döda kungen.\n'+
                                                  'Jag vet att jag har svikit den snälla häxan.\n'+
                                                  'Men jag vet en annan vän till henne som jag hemlighållit för den elaka häxan.\n'+
                                                  'Det är en dvärg, och han bor nu i vildmarken, jag ska förklara vägen för er.\n')
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
                nyplats = False                           
                            
                        
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
                                  'Ta den här fjädern som tack, och en läkört')
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
                            nyplats=False
                            break

                #senare
                else:
                #första gången tillbaks i vanliga världen
                    if progress['main'] == 3 and d4 not in dialogval: 
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
                            if 'Hemlig lära' in [u[0] for u in sp1.utveckling]:
                                alri.utveckling.append(['Hemlig lära',0])
                            lvlup(spelarlista)
                        else:
                            slowprint('Tomten Heyjafjej är i Stugan\n'+
                                  'Heyjafjej: Den Snälla häxan har försvunnit, och den Elaka också.\n'+
                                  'Och nu är alla monster starkare och fursten Gurgen gömmer sig.\n'+
                                  'Jag tror att den Elaka häxan har hittat på något otyg...\n'+
                                  'Jag vet att ni är den Snälla häxans vänner. Försök att hitta henne!\n')
                        dialogval[4] = d4 #fråga om snälla häxan

                    else:
                        print('Det är ingen i Stugan')
                    #oavsett
                    print('Den snälla häxans magi finns fortfarande kvar.\n'+
                          'Ni kan vila och återhämta er.')
                    for s in spelarlista:
                        s.hp=s.liv
                    print('(Ni fick full hp)')
                    nyplats = False
                           
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
                else:
                    slowprint('Tornet är fullt av monster')
                    fight()
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
                      s.hpstr()+'\n'+
                      'Styrka: '+str(s.stats['str'])+'  Smidighet: '+str(s.stats['smi'])+'  Magikraft: '+str(s.stats['mkr'])+'\n'+
                      'Vapen: '+s.utrust['vapen'].namn+' (+'+str(int(s.utrust['vapen'].skada*2))+')'+
                      '  Rustning: '+s.utrust['rustning'].namn+' (+'+str(s.utrust['rustning'].skydd)+')'+
                      '\nÖvrigt: '+s.utrust['ovrigt'].namn+' ('+s.utrust['ovrigt'].kortbs+')')
                if len(s.formagor) > 0:
                    print('Förmågor: '+', '.join(set(s.formagor)))
                if len(s.magier) > 0:
                    print('Magier: '+', '.join(set(spell[0] for spell in s.magier)))
                if len(s.special) > 0:
                    print('Specialförmågor: '+', '.join(set(s.special))+'\n')
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
                

        if val[mode]=='Djurfrämlingens bok':
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
                
                
#fler funktioner:

def fight(plats='plats', specifik=False, OP=0):
    if plats == 'plats':
        plats = PDICT[position]
    loot = fightfunc(spelarlista, inventory, progress, plats, specifik, OP=OP)
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
    elif position == 5 and gammalpos < 100: #special, höga berget
        position = gammalpos
        print('Ni kan inte ta er upp på Höga berget')
        progress['upptäckta_platser'].add(5)
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
    else:
        print('Ni kommer till '+plats+'\n')

    return 1


#språkfunktioner
def namn():
    string=[]
    n=0
    for i in range(len(spelarelista)):
        if i>0:
            if i==len(spelarlista)-1:
                string.append(' och ')
            else:
                string.append(', ')
        string.append(spelarlista[i])
    return "".join(string)



#konstanter

# dictionary med alla föremål
FDICT = {
    '-': kls.Foremal('-'), #tomt namn
    'Fiskstål': kls.Foremal('Fiskstål'),
    'Gråsten': kls.Foremal('Gråsten'),
    'Mystisk sten': kls.Foremal('Mystisk sten'),
    'Mystisk fjäder': kls.Foremal('Mystisk fjäder'),
    'Häxrot': kls.Foremal('Häxrot'),
    'Tand': kls.Foremal('Tand'),
    'Häxans ring': kls.Foremal('Häxans ring'),
    'Randig gren': kls.Foremal('Randig gren'),
    'Svärd': kls.Vapen('Svärd',1),
    'Bra svärd': kls.Vapen('Bra svärd',2,5,'str'),
    'Mästarsvärd': kls.Vapen('Mästarsvärd',6,6,'str'),
    'Kniv': kls.Vapen('Kniv',0.7),
    'Mystisk dolk': kls.Vapen('Mystisk dolk',2,5,'mkr'),
    'Tandkniv': kls.Vapen('Tandkniv',2.5),
    'Zlokrs kniv': kls.Vapen('Zlokrs kniv',7,9,'smi'),
    'Fiskspjut': kls.Vapen('Fiskspjut',3),
    'Mystiskt spjut': kls.Vapen('Mystiskt spjut',3.5,7,'mkr'),
    'Jotuns hammare': kls.Vapen('Jotuns hammare',4,7,'str'),
    'Pilbåge': kls.Vapen('Pilbåge',2,5,'smi'),
    'Bra pilbåge': kls.Vapen('Bra pilbåge',3.5,7,'smi'),
    'Silverbåge': kls.Vapen('Silverbåge',6,9,'smi'),
    'Lätt rustning': kls.Rustning('Lätt rustning',1),
    'Brynja': kls.Rustning('Brynja',2),
    'Drakfjällsbrynja': kls.Rustning('Drakfjällsbrynja',3,5,'str'),
    'Tung rustning': kls.Rustning('Tung rustning',5,6,'str'),
    'Magisk rustning': kls.Rustning('Magisk rustning',6,6,'mkr'),
    'Riddarrustning': kls.Rustning('Riddarrustning',6,8,'str'),
    'Ormdräkt': kls.Rustning('Ormdräkt',7,8,'smi'),
    'Mitrilbrynja': kls.Rustning('Mitrilbrynja',7),
    'Mitrilrustning': kls.Rustning('Mitrilrustning',9),
    'Skyddande ädelsten': kls.Ovrigt('Skyddande ädelsten','+1 magiskt skydd',2,1),
    'Svart mantel': kls.Ovrigt('Svart mantel','+3 magiskt skydd',2,3),
    'Grön mantel': kls.Ovrigt('Grön mantel','+40 liv','liv',40),
    'Blå mantel': kls.Ovrigt('Blå mantel','+2 snabbhet',0,-2),
    'Guldlänk': kls.Ovrigt('Guldlänk','+2 magikraft','mkr',2),
    'Magisk ring': kls.Ovrigt('Magisk ring','+3 magikraft','mkr',3),
    'Trollring': kls.Ovrigt('Trollring','+4 magikraft','mkr',4),
    'Guldring': kls.Ovrigt('Guldring','+3 styrka','str',3),
    'Guldhandske': kls.Ovrigt('Guldhandske','+4 styrka','str',4),
    'Amulett': kls.Ovrigt('Amulett','+3 smidighet','smi',3),
    'Skuggskor': kls.Ovrigt('Skuggskor','+4 smidighet','smi',4),
    'Demonkappa': kls.Ovrigt('Demonkappa','+6 undvikning',3,6),
    'Magiskt armband': kls.Ovrigt('Magiskt armband','+5 pricksäkerhet',1,5),
    'Blå ring': kls.Ovrigt('Blå ring','"Förmåga-Återhämtning 2"',1,0,'Återhämtning 2'),
    'Lyckosmycke': kls.Ovrigt('Lyckosmycke','"Skattletande"',3,0,'Skattletande'),
    'Blodkristall': kls.Ovrigt('Blodkristall','"Dubbel attack"',3,0,'Dubbel attack'),
    'Uråldrig kristall': kls.Ovrigt('Uråldrig kristall','"Magi-Livskraft"',2,5,'Livskraft'),
    'De vises sten': kls.Ovrigt('De vises sten','"Dubbel magi"',3,0,'Dubbel magi'),
    'Salva': kls.EngangsForemal('Salva','Läkande',difstat,('hp',15),fight=True),
    'Läkört': kls.EngangsForemal('Läkört','Läkande',difstat,('hp',60),fight=True),
    'Häxbrygd': kls.EngangsForemal('Häxbrygd','Läkande',difstat,('hp',200),fight=True),
    'Elixir': kls.EngangsForemal('Elixir','Återställer full hp',difstat,('hp',2000),fight=True),
    'Själsstoft': kls.EngangsForemal('Själsstoft','+1 magikraft permanent',difstat,('mkr',1,7)),
    'Trollsländsvinge': kls.EngangsForemal('Trollsländsvinge','+1 smidighet permanent',difstat,('smi',1,7)),
    'Vargblod': kls.EngangsForemal('Vargblod','+1 styrka permanent',difstat,('str',1,7)),
    'Demondryck': kls.EngangsForemal('Demondryck','+1 magikraft permanent',difstat,('mkr',1)),
    'Ormmedicin': kls.EngangsForemal('Ormmedicin','+1 smidighet permanent',difstat,('smi',1)),
    'Livsfrukt': kls.EngangsForemal('Livsfrukt','+1 styrka permanent',difstat,('str',1))
    }

ALDICT = {
    'Svärd': 3,
    'Bra svärd': 6,
    'Kniv': 2,
    'Mystisk dolk': 6,
    'Tandkniv': 8,
    'Zlokrs kniv': 50,
    'Fiskspjut': 10,
    'Mystiskt spjut': 12,
    'Jotuns hammare': 15,
    'Pilbåge': 6,
    'Bra pilbåge': 12,
    'Lätt rustning': 3,
    'Brynja': 5,
    'Drakfjällsbrynja': 8,
    'Tung rustning': 10,
    'Magisk rustning': 12,
    'Riddarrustning': 12,
    'Ormdräkt': 16,
    'Mitrilbrynja': 20,
    'Guldlänk': 6,
    'Skyddande ädelsten': 6,
    'Magisk ring': 12,
    'Guldring': 12,
    'Guldhandske': 18,
    'Amulett': 12,
    'Skuggskor': 18,
    'Demonkappa': 40,
    'Blå ring': 14,
    'Lyckosmycke': 15,
    'Blodkristall': 18,
    'Uråldrig kristall': 28,
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
    216:'Templet'
    }

karta = kls.Karta(PDICT)

LANDSKAP = {'skog', 'berg', 'skugglandskap', 'mörkt vatten'}

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
