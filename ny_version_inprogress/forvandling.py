def fagel(spelare):
    spelare.vilande={'stats':spelare.stats,'formagor':spelare.formagor,'magier':spelare.magier, 'vapen':spelare.utrust['vapen'],'liv':spelare.liv, 'namn':spelare.namn}
    spelare.vilande['hpdif']=0.75
    spelare.formagor=['Tillbakaförvandling'] 
    spelare.magier=[('Trollstoft',1)]
    spelare.stats['str']=int(spelare.stats['str']*0.8)
    spelare.stats['smi']=spelare.stats['smi']*1.5+3
    spelare.liv=int(spelare.liv*0.75)
    spelare.hp=int(spelare.hp*0.75)
    spelare.utrust['vapen']=''
    print(spelare.namn+' förvandlar sig till en fågel')
    spelare.namn+='(fågel)'

def gorilla(spelare):
    spelare.vilande={'stats':spelare.stats,'formagor':spelare.formagor,'magier':spelare.magier, 'vapen':spelare.utrust['vapen'],'liv':spelare.liv, 'namn':spelare.namn}
    spelare.vilande['hpdif']=1.50
    spelare.formagor=['Tillbakaförvandling'] 
    spelare.magier=[]
    spelare.stats['str']=int(spelare.stats['str']*1.5+3)
    spelare.stats['smi']+=1
    spelare.liv=int(spelare.liv*1.50)
    spelare.hp=int(spelare.hp*1.50)
    spelare.utrust['vapen']=''
    print(spelare.namn+' förvandlar sig till en gorilla')
    spelare.namn+='(gorilla)'

def alva(spelare):
    spelare.vilande={'stats':spelare.stats,'formagor':spelare.formagor,'magier':spelare.magier, 'vapen':spelare.utrust['vapen'],'liv':spelare.liv, 'namn':spelare.namn}
    spelare.vilande['hpdif']=0.50
    spelare.formagor=['Tillbakaförvandling','Mystisk kraft'] 
    spelare.magier=[('Upplyftning',1),('Livskraft',4),('Trollsmäll',4)]
    spelare.stats['str']=int(spelare.stats['str']*0.5)
    spelare.stats['smi']=spelare.stats['smi']*1.5
    spelare.liv=int(spelare.liv*0.50)
    spelare.hp=int(spelare.hp*0.50)
    spelare.utrust['vapen']=''
    print(spelare.namn+' förvandlar sig till en älva')
    spelare.namn+='(älva)'

def tiger(spelare):
    spelare.vilande={'stats':spelare.stats,'formagor':spelare.formagor,'magier':spelare.magier, 'vapen':spelare.utrust['vapen'],'liv':spelare.liv, 'namn':spelare.namn}
    spelare.vilande['hpdif']=1
    spelare.formagor=['Tillbakaförvandling'] 
    spelare.magier=[('Helning',1),('Mystisk attack',3)]
    spelare.stats['str']=int(spelare.stats['str']*2)
    spelare.stats['smi']=spelare.stats['smi']+=2
    spelare.utrust['vapen']=''
    print(spelare.namn+' förvandlar sig till en tiger')
    spelare.namn+='(tiger)'

def tillbakaforvandling(spelare):
    spelare.stats['str']=spelare.vilande['stats']['str']
    spelare.stats['smi']=spelare.vilande['stats']['smi']
    spelare.formagor=spelare.vilande['formagor']
    spelare.magier=spelare.vilande['magier']
    spelare.liv=spelare.vilande['liv']
    spelare.utrust['vapen']=spelare.vilande['vapen']
    spelare.namn=spelare.vilande['namn']
    spelare.hp=int(spelare.hp / spelare.vilande['hpdif'])
    print(spelare.namn+' återgår till mänsklig gestalt')
    spelare.vilande={}
