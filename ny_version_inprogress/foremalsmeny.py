from collections import OrderedDict
from funktioner import uniquelist

def classhierarchy(obj):
    if isinstance(obj,kls.Foremal):
        return 0
    elif isinstance(obj,kls.EngangsForemal):
        return 1
    elif isinstance(obj,kls.Ovrigt):
        return 2
    elif isinstance(obj,kls.Vapen):
        return 3
    elif isinstance(obj,kls.Rustning):
        return 4

def foremalsmeny():
    global inventory
    while True:
        print('\nFÖREMÅL')
        inv = OrderedDict()
        ordered = uniquelist(inventory).sort(key=classhierarchy)
        for f in ordered:
            inv[f.namn] = ': '+str(inventory.count(f))
            
        obj = listval(['Gå tillbaka']+
                      [f.namn+' ('+f.bs+')'+antal for f, antal in inv.items()] - 1
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
