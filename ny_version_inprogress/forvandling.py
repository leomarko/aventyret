def fagel(spelare):
    spelare.vilande={'stats':spelare.stats,'formagor':spelare.formagor,'magier':spelare.magier,'liv':spelare.liv, 'namn':spelare.namn}
    spelare.vilande['hpdif']=0.75
    spelare.formagor=['Tillbakaförvandling'] 
    spelare.magier=[('Trollstoft',1)]
    spelare.stats['str']=int(spelare.stats['str']*0.7)
    spelare.stats['smi']=int(spelare.stats['smi']*1.2+3)
    spelare.liv=int(spelare.liv*0.75)
    spelare.hp=int(spelare.hp*0.75)
    print(spelare.namn+' förvandlar sig till en fågel')
    spelare.namn+='(fågel)'

def gorilla(spelare):
    spelare.vilande={'stats':spelare.stats,'formagor':spelare.formagor,'magier':spelare.magier,'liv':spelare.liv, 'namn':spelare.namn}
    spelare.vilande['hpdif']=1.50
    spelare.formagor=['Tillbakaförvandling'] 
    spelare.magier=[]
    spelare.stats['str']=int(spelare.stats['str']*1.5)
    spelare.stats['smi']+=1
    spelare.liv=int(spelare.liv*1.50)
    spelare.hp=int(spelare.hp*1.50)
    print(spelare.namn+' förvandlar sig till en gorilla')
    spelare.namn+='(gorilla)'

def alva(spelare):
    spelare.vilande={'stats':spelare.stats,'formagor':spelare.formagor,'magier':spelare.magier,'liv':spelare.liv, 'namn':spelare.namn}
    spelare.vilande['hpdif']=0.50
    spelare.formagor=['Tillbakaförvandling','Mystisk kraft'] 
    spelare.magier=[('Tillkvicknande',1),('Upplyftning',2),('Trollsmäll',3),('Livskraft',4)]
    spelare.stats['str']=int(spelare.stats['str']*0.4)
    spelare.stats['smi']=int(spelare.stats['smi']*1.2+3)
    spelare.liv=int(spelare.liv*0.50)
    spelare.hp=int(spelare.hp*0.50)
    print(spelare.namn+' förvandlar sig till en älva')
    spelare.namn+='(älva)'

def tiger(spelare):
    spelare.vilande={'stats':spelare.stats,'formagor':spelare.formagor,'magier':spelare.magier,'liv':spelare.liv, 'namn':spelare.namn}
    spelare.vilande['hpdif']=1
    spelare.formagor=['Tillbakaförvandling', 'Mystisk kraft'] 
    spelare.magier=[('Helning',1),('Tillkvicknande',1),('Mystisk attack',3)]
    spelare.stats['str']=int(spelare.stats['str']*1.4)
    spelare.stats['smi']+=2
    print(spelare.namn+' förvandlar sig till en tiger')
    spelare.namn+='(tiger)'

def tillbakaforvandling(spelare):
    spelare.stats['str']=spelare.vilande['stats']['str']
    spelare.stats['smi']=spelare.vilande['stats']['smi']
    spelare.formagor=spelare.vilande['formagor']
    spelare.magier=spelare.vilande['magier']
    spelare.liv=spelare.vilande['liv']
    spelare.namn=spelare.vilande['namn']
    spelare.hp=int(spelare.hp / spelare.vilande['hpdif'])
    print(spelare.namn+' återgår till mänsklig gestalt')
    spelare.vilande={}
