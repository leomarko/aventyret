    def attack(a, b, nyckelord=''):
        ggr = 1
        if isinstance(a,kls.Spelare):
            spelare = True
            
        #dubbel            
        if nyckelord == 'dubbel' | 'dubbelcritical':
            if not spelare or a.stats['smi']*0.07 + 2.3*random()  >  2:
                ggr = 2
        #loop
        while ggr > 0:
            if a.hit(b) or nyckelord == 'mystisk':
                
                #grundskada
                if nyckelord == 'mystisk':
                    skada = sum(a.stats) + figur.hp/4
                elif nyckelord == 'mörk':
                    skada = a.stats['mkr']*0.85 + a.stats['str']*0.85
                else:
                    skada = a.stats['str']
                try:
                    skada += figur.utrust['vapen'].skada
                except(AttributeError):
                    skada = skada
                    
                #slutskada
                if nyckelord == 'critical' | 'dubbelcritical':
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

    def attackmagi(figur,target,mod,plus=0):
        if isinstance(target, list):
            for f in target:
                skada = int(figur.mkr*(mod+random()) + plus - f.mods[2]*2)
                taskada(f,skada)
        else:
            skada = int(figur.mkr*(mod+random()) + plus - target.mods[2]*2)
            taskada(target,skada)
        return skada

    def taskada(figur,skada):
        if skada < 1:
            skada = 1
        if isinstance(figur,kls.Spelare):
            print(figur.namn+' förlorar '+str(skada)+' hp')
        else:
            print(figur.namnB+' förlorar '+str(skada)+' hp')
        figur.hp-=skada
        k_o(figur)

    def k_o(target):   
        def inbyggd_k_o(figur):
            if figur.hp<1:
                figur.hp=0
                if isinstance(figur,kls.Spelare):
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


def helning(figur, target, mod, mod2=0.2, plus=0):
    if isinstance(target, list):
        for s in target:
            helning = int(figur.mkr*(mod+random()) + s.liv*mod2 + plus)
            difstat(s,'hp',helning)
    else:
        helning = int(figur.mkr*(mod+random()) + target.liv*mod2 + plus)
        difstat(target,'hp',helning)
                
def f_meny(lista):
    n = listval(lista+['Ångra'])
    if n == len(lista): #gå tillbaka
        return False
    return lista[n]

def magi_meny(magier, mkr, dubbel=False):
    tillgangliga = [magi for magi in magier if mkr >= magi[1]]
    if not dubbel:
        spell = listval([m[0]+': '+str(m[1])+' magikraft' for m in tillgangliga]+['Ångra'])
    else:
        spell = listval([m[0]+': '+str(m[1])+' magikraft' for m in tillgangliga]+['(Ingen)'])
    if obj == len(tillgangliga):
        return False
    return magier[spell]
    
def fmal_meny(inventory, aktiva_s, aktiva_f):
    fightprylar=[sak for sak in [f for f in inventory if isinstance(f,kls.EngangsForemal)] if sak.fight]
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
