#fiender

from klasser import Varelse
from random import random, randint
from funktioner import slowprint

#------------------------------------------Vanliga världen

class Gradvarg(Varelse):
    namn='Grådvärg'
    namnB=namn+'en'

    def __init__(self, nr=0):
        if nr!=0:
            self.namn+=' '+nr
        self.exp=17
        self.liv=27
        self.hp=self.liv
        self.stats={'str':3,'smi':4,'mkr':1}
        self.mods=[-1,0,3,1]   #0:snabbhet,1:pricksäkerhet,2:magiskt skydd(skyddar mot allt men dubbelt mot magi),3:evasion
        self.rustning=0
    
    def mode(self):
        return 'attack'
        
    def drop(self, plus, progress, OP):
        if progress['häxan'] == 2:
            progress['häxan'] += 1
            return 'Gråsten'
        n=randint(0,15)+plus
        if OP > 0:
            if n > 14:
                return 'Mitrilbrynja'
        else:
            if n > 15:
                return 'Mitrilbrynja'
            elif n > 12:
                return 'Mystisk dolk'

        return False

class Stentiger(Varelse):
    namn='Stentiger'
    namnB=namn+'n'

    def __init__(self, nr=0):
        if nr!=0:
            self.namn+=' '+nr
        self.exp=34
        self.liv=45
        self.hp=self.liv
        self.stats={'str':7,'smi':4,'mkr':6}
        self.mods=[0,1,0,1]   #0:snabbhet,1:pricksäkerhet,2:magiskt skydd(skyddar mot allt men dubbelt mot magi),3:evasion
        self.rustning=1
    
    def mode(self):
        mode=randint(0,3)
        if mode < 3:
            return 'attack'
        else:
            return 'Hypnos'
        
    def drop(self, plus, progress, OP):
        n=randint(0,7)+plus
        if n > 7:
            return 'Läkört'
        elif n > 5:
            return 'Mystisk sten'
        else:
            return False

class Bergatroll(Varelse):
    namn='Bergatroll'
    namnB=namn+'et'

    def __init__(self, nr=0):
        if nr!=0:
            self.namn+=' '+nr
        self.exp=50
        self.liv=70
        self.hp=self.liv
        self.stats={'str':8,'smi':2,'mkr':5}
        self.mods=[0,1,0,0]   #0:snabbhet,1:pricksäkerhet,2:magiskt skydd(skyddar mot allt men dubbelt mot magi),3:evasion
        self.rustning=4

    def mode(self):
        mode=randint(0,4)
        if mode<4:
            return 'attack'
        else:
            return 'Trollsmäll'

    def drop(self, plus, progress, OP):
        if randint(0,6) + plus >= 6:
            if OP > 0:
                return 'Guldhandske'
            else:
                return 'Guldring'
        else:
            return False

class Skogstroll(Varelse):
    namn='Skogstroll'
    namnB=namn+'et'

    def __init__(self, nr=0):
        if nr!=0:
            self.namn+=' '+nr
        self.exp=20
        self.liv=35
        self.hp=self.liv
        self.stats={'str':4,'smi':3,'mkr':4}
        self.mods=[0,0,1,0]   #0:snabbhet,1:pricksäkerhet,2:magiskt skydd(skyddar mot allt men dubbelt mot magi),3:evasion
        self.rustning=0

    def mode(self):
        mode=randint(0,3)
        if mode<3:
            return 'attack'
        else:
            return 'Trollstoft'

    def drop(self, plus, progress, OP):
        if progress['häxan'] == 0:
            progress['häxan'] += 1
            return 'Häxrot'
        elif randint(0,6) + plus >= 6:
            if OP > 0:
                return 'Magisk ring'
            else:
                return 'Guldlänk'
        else:
            return False

class Trollslanda(Varelse):
    namn='Trollslända'
    namnB=namn+'n'

    def __init__(self, nr=0):
        if nr!=0:
            self.namn+=' '+nr
        self.exp=13
        self.liv=12
        self.hp=self.liv
        self.stats={'str':2,'smi':6,'mkr':3}
        self.mods=[0,0,2,0]   #0:snabbhet,1:pricksäkerhet,2:magiskt skydd(skyddar mot allt men dubbelt mot magi),3:evasion
        self.rustning=0

    def mode(self):
        mode=randint(0,5)
        if mode > 1:
            return 'attack'
        elif mode == 1:
            return 'critical'
        else:
            return 'other'

    def other(self):
        print('Trollsländan svävar i luften')

    def drop(self, plus, progress, OP):
        if randint(0,9) + plus >= 9:
            return 'Trollsländsvinge'
        else:
            return False

class Varg(Varelse):
    namn='Varg'
    namnB=namn+'en'

    def __init__(self, nr=0):
        if nr!=0:
            self.namn+=' '+nr
        self.exp=17
        self.liv=25
        self.hp=self.liv
        self.stats={'str':3,'smi':4,'mkr':3}
        self.mods=[0,1,0,0]   #0:snabbhet,1:pricksäkerhet,2:magiskt skydd(skyddar mot allt men dubbelt mot magi),3:evasion
        self.rustning=1
    
    def mode(self):
        mode=randint(0,3)
        if mode<3:
            return 'attack'
        else:
            return 'critical'

    def drop(self, plus, progress, OP):
        if randint(0,9) + plus >= 9:
            return 'Vargblod'
        else:
            return False

class Valnad(Varelse):
    namn='Vålnad'
    namnB=namn+'en'

    def __init__(self, nr=0):
        if nr!=0:
            self.namn+=' '+nr
        self.exp=40
        self.liv=25
        self.hp=self.liv
        self.stats={'str':13,'smi':5,'mkr':3}
        self.mods=[1,0,3,3]   #0:snabbhet,1:pricksäkerhet,2:magiskt skydd(skyddar mot allt men dubbelt mot magi),3:evasion
        self.rustning=0

    def other(self):
        print('Vålnaden vandrar rastlöst omkring')
    
    def mode(self):
        mode=randint(0,4)
        if mode>2:
            return 'attack'
        else:
            return 'other'

    def drop(self, plus, progress, OP):
        if randint(0,9) + plus >= 9:
            return 'Själsstoft'
        else:
            return False

class Vatte(Varelse):
    namn='Vätte'
    namnB=namn+'n'

    def __init__(self, nr=0):
        if nr!=0:
            self.namn+=' '+nr
        self.exp=9
        self.liv=20
        self.hp=self.liv
        self.stats={'str':3,'smi':3,'mkr':1}
        self.mods=[0,0,0,0]   #0:snabbhet,1:pricksäkerhet,2:magiskt skydd(skyddar mot allt men dubbelt mot magi),3:evasion
        self.rustning=0
    
    def mode(self):
        return 'attack'
        
    def drop(self, plus, progress, OP):
        if randint(1,100) + plus + OP > 99: #superrare drop
            return 'Blodkristall'
        n = randint(0,6) + plus
        
        if n > 5:
            return 'Brynja'
        elif n > 4:
            return 'Kniv'
        elif n > 2:
            return 'Salva'
        else:
            return False

#------------------------------------------Skuggvärlden


class Demonpanter(Varelse):
    namn='Demonpanter'
    namnB=namn+'n'

    def __init__(self, nr=0):
        if nr!=0:
            self.namn+=' '+nr
        self.exp=200
        self.liv=150
        self.hp=self.liv
        self.stats={'str':14,'smi':13,'mkr':13}
        self.mods=[0,0,5,0]   #0:snabbhet,1:pricksäkerhet,2:magiskt skydd(skyddar mot allt men dubbelt mot magi),3:evasion
        self.rustning=5
    
    def mode(self):
        mode=randint(0,2)
        if mode > 0:
            return 'attack'
        else:
            return 'Eld'
        
    def drop(self, plus, progress, OP):
        n=randint(0,7)+plus
        if n > 6:
            return 'Magisk rustning'
        else:
            return 'Mystisk sten'
        
class ElVatte(Varelse):
    namn='Elak vätte'
    namnB='Den elaka vätten'

    def __init__(self, nr=0):
        if nr!=0:
            self.namn+=' '+nr
        self.exp=40
        self.liv=40
        self.hp=self.liv
        self.stats={'str':4,'smi':8,'mkr':1}
        self.mods=[0,0,1,0]   #0:snabbhet,1:pricksäkerhet,2:magiskt skydd(skyddar mot allt men dubbelt mot magi),3:evasion
        self.rustning=1
    
    def mode(self):
        if randint(0,3) > 0:
            return 'attack'
        else:
            return 'dubbel'
        
    def drop(self, plus, progress, OP):
        n = randint(0,6) + plus
        if n > 5:
            return 'Drakfjällsbrynja'
        elif n > 3:
            return 'Läkört'
        else:
            return False

class Fiskmonster(Varelse):
    namn='Fiskmonster'
    namnB='Fiskmonstret'

    def __init__(self, nr=0):
        if nr!=0:
            self.namn+=' '+nr
        self.exp=120
        self.liv=140
        self.hp=self.liv
        self.stats={'str':13,'smi':10,'mkr':7}
        self.mods=[0,0,0,-1]   #0:snabbhet,1:pricksäkerhet,2:magiskt skydd(skyddar mot allt men dubbelt mot magi),3:evasion
        self.rustning=7
    
    def mode(self):
        mode=randint(0,4)
        if mode > 0:
            return 'attack'
        else:
            return 'Kvävning'
        
    def drop(self, plus, progress, OP):
        n = randint(0,10)+plus
        if n > 9:
            return 'Fiskstål'
        elif n > 8:
            return 'Fiskspjut'
        return False

class Hjort(Varelse):
    namn='Magisk hjort'
    namnB='Den magiska hjorten'

    def __init__(self, nr=0):
        if nr!=0:
            self.namn+=' '+nr
        self.exp=350
        self.liv=40
        self.hp=self.liv
        self.stats={'str':5,'smi':10,'mkr':10}
        self.mods=[1,0,6,3]   #0:snabbhet,1:pricksäkerhet,2:magiskt skydd(skyddar mot allt men dubbelt mot magi),3:evasion
        self.rustning=0
    
    def mode(self):
        mode=randint(0,2)
        if mode == 2:
            return 'attack'
        elif mode == 1:
            return 'Trollsmäll'
        else:
            return 'fly'
        
    def drop(self, plus, progress, OP):
        if randint(0,90)+plus > 89:
            return 'Uråldrig kristall'
        return False

class Nvidunder(Varelse):
    namn='Namnlöst vidunder'
    namnB='Det namnlösa vidundret'

    def __init__(self, nr=0):
        if nr!=0:
            self.namn+=' '+nr
        self.exp=100
        self.liv=160
        self.hp=self.liv
        self.stats={'str':10,'smi':6,'mkr':5}
        self.mods=[0,0,0,-1]   #0:snabbhet,1:pricksäkerhet,2:magiskt skydd(skyddar mot allt men dubbelt mot magi),3:evasion
        self.rustning=4
        self.ordning=randint(0,5)

    def mode(self):
        if self.ordning == 0:
            self.ordning += 1
            return 'Stank'
        elif self.ordning == 5:
            self.ordning = 0
            return 'attack'
        else:
            self.ordning += 1
            return 'attack'

    def drop(self, plus, progress, OP):
        n = randint(0,10) + plus
        if n == 0:
            return 'Lyckosmycke'
        elif n > 9:
            return 'Tung rustning'
        else:
            return False

class Skuggkatt(Varelse):
    namn='Skuggkatt'
    namnB=namn+'en'

    def __init__(self, nr=0):
        if nr!=0:
            self.namn+=' '+nr
        self.exp=60
        self.liv=40
        self.hp=self.liv
        self.stats={'str':6,'smi':8,'mkr':8}
        self.mods=[0,0,1,0]   #0:snabbhet,1:pricksäkerhet,2:magiskt skydd(skyddar mot allt men dubbelt mot magi),3:evasion
        self.rustning=1
    
    def mode(self):
        mode=randint(0,6)
        if mode > 1:
            return 'attack'
        elif mode == 1:
            return 'Trollstoft'
        elif mode == 0:
            return 'Ändra framtiden'
        
    def drop(self, plus, progress, OP):
        n=randint(0,9)+plus
        if n > 9:
            return 'Elixir'
        elif n == 9:
            return 'Magisk ring'
        elif n == 8:
            return 'Själsstoft'
        else:
            return False

class Tanddvarg(Varelse):
    namn='Tanddvärg'
    namnB=namn+'en'

    def __init__(self, nr=0):
        if nr!=0:
            self.namn+=' '+nr
        self.exp=50
        self.liv=60
        self.hp=self.liv
        self.stats={'str':7,'smi':5,'mkr':1}
        self.mods=[0,0,6,0]   #0:snabbhet,1:pricksäkerhet,2:magiskt skydd(skyddar mot allt men dubbelt mot magi),3:evasion
        self.rustning=0
    
    def mode(self):
        if randint(0,3) > 0:
            return 'attack'
        else:
            return 'critical'
        
    def drop(self, plus, progress, OP):
        n=randint(0,13)+plus
        if n > 11:
            return 'Tandkniv'
        elif n > 9:
            return 'Mystisk sten'
        elif n > 6:
            return 'Tand'
        else:
            return False

#------------------------------------------Framtiden: landsväg


class Riddare(Varelse):
    namn='Riddare'
    namnB=namn+'n'

    def __init__(self, nr=0):
        if nr!=0:
            self.namn+=' '+nr
        self.exp=180
        self.liv=140
        self.hp=self.liv
        self.stats={'str':12,'smi':9,'mkr':5}
        self.mods=[0,0,3,0]
        self.rustning=6

    def mode(self):
        mode = randint(0,5)
        if mode > 3:
            return 'critical'
        else:
            return 'attack'

    def drop(self, plus, progress, OP):
        n = randint(0,12)+plus
        if n > 11:
            return 'Förtrollad sköld'
        elif n > 9:
            return 'Tungt svärd'
        else:
            return False

class Soldat(Varelse):
    namn='Soldat'
    namnB=namn+'en'

    def __init__(self, nr=0):
        if nr!=0:
            self.namn+=' '+nr
        self.exp=110
        self.liv=90
        self.hp=self.liv
        self.stats={'str':10,'smi':9,'mkr':5}
        self.mods=[0,0,3,0]
        self.rustning=3

    def mode(self):
        if randint(0,1) > 0 and self.hp < 30:
            return 'Återhämtning 2'
        else:
            return 'attack'

    def drop(self, plus, progress, OP):
        n = randint(0,100)+plus
        if n > 99:
            return 'Tapperhetsmedalj'
        else:
            return False

class Tempelprefekt(Varelse):
    namn='Tempelprefekt'
    namnB=namn+'en'

    def __init__(self, nr=0):
        if nr!=0:
            self.namn+=' '+nr
        self.exp=140
        self.liv=100
        self.hp=self.liv
        self.stats={'str':5,'smi':8,'mkr':13}
        self.mods=[0,0,9,2]
        self.rustning=0
        self.ordning = randint(0,4)

    def mode(self):
        self.ordning += 1
        if self.ordning == 5:
            self.ordning = 1
        if self.ordning == 1 :
            return 'Sömnighet'
        elif self.ordning == 2: 
            return 'Beskydd'
        else:
            return 'Kyla'

    def drop(self, plus, progress, OP):
        n = randint(0,9)+plus
        if n > 8:
            return 'Förhäxad spira'
        else:
            return 'Häxbrygd'

class Bandit(Varelse):
    namn='Bandit'
    namnB=namn+'en'

    def __init__(self, nr=0):
        if nr!=0:
            self.namn+=' '+nr
        self.exp=150
        self.liv=90
        self.hp=self.liv
        self.stats={'str':11,'smi':14,'mkr':5}
        self.mods=[0,0,1,0]
        self.rustning=4
        self.ordning=0

    def mode(self):
        n = randint(0,6)
        if n == 0:
            return 'fly'
        elif n < 3:
            return 'dubbel'
        else:
            return 'attack'

    def drop(self, plus, progress, OP):
        n = randint(0,20)+plus
        if n == 0:
            return 'Lyckosmycke'
        elif n > 20:
            return 'Rubin'
        else:
            return False


#------------------------------------------Framtiden: träsk och ödemark

class Otroll(Varelse):
    namn='Otroll'
    namnB=namn+'et'

    def __init__(self, nr=0):
        if nr!=0:
            self.namn+=' '+nr
        self.exp=420
        self.liv=240
        self.hp=self.liv
        self.stats={'str':17,'smi':10,'mkr':15}
        self.mods=[0,0,3,0]
        self.rustning=6

    def mode(self):
        mode = randint(0,5)
        if mode == 5:
            return 'attack'
        elif mode == 4:
            return 'Trollstoft'
        elif mode == 3:
            return 'Smärta'
        elif mode == 2 and self.hp < 50:
            return 'Återhämtning 2'
        else:
            return 'critical'

    def drop(self, plus, progress, OP):
        n = randint(0,13)+plus
        if n > 11:
            return 'Förtrollad hammare'
        elif n > 7:
            return 'Häxbrygd'
        else:
            return False

class Jarnkrokodil(Varelse):
    namn = 'Järnkrokodil'
    namnB = namn+'en'

    def __init__(self, nr=0):
        if nr!=0:
            self.namn+=' '+nr
        self.exp=550
        self.liv=180
        self.hp=self.liv
        self.stats={'str':16,'smi':13,'mkr':7}
        self.mods=[0,0,7,0]   #0:snabbhet,1:pricksäkerhet,2:magiskt skydd(skyddar mot allt men dubbelt mot magi),3:evasion
        self.rustning=12
    
    def mode(self):
        mode=randint(0,4)
        if mode > 0:
            return 'attack'
        else:
            return 'Kvävning'
        
    def drop(self, plus, progress, OP):
        n = randint(0,10)+plus
        if n > 10:
            return 'Elixir'
        elif n > 9:
            return 'Järnskinnsdräkt'
        return False

class Traskdvarg(Varelse):
    namn='Träskdvärg'
    namnB = namn+'en'

    def __init__(self, nr=0):
        if nr!=0:
            self.namn+=' '+nr
        self.exp=200
        self.liv=100
        self.hp=self.liv
        self.stats={'str':13,'smi':13,'mkr':12}
        self.mods=[-1,0,8,0]   #0:snabbhet,1:pricksäkerhet,2:magiskt skydd(skyddar mot allt men dubbelt mot magi),3:evasion
        self.rustning=0
    
    def mode(self):
        mode=randint(0,4)
        if mode > 2:
            return 'attack'
        elif mode > 0:
            return 'dubbel'
        else:
            return 'Förvrida framtiden'
        
    def drop(self, plus, progress, OP):
        n = randint(0,10)+plus
        if n > 9:
            return 'Dödlig kniv'
        elif n > 8:
            return 'Mitrilbrynja'
        return False

class Fantom(Varelse):
    namn='Fantom'
    namnB=namn+'en'

    def __init__(self, nr=0):
        if nr!=0:
            self.namn+=' '+nr
        self.exp=130
        self.liv=55
        self.hp=self.liv
        self.stats={'str':40,'smi':10,'mkr':3}
        self.mods=[1,0,13,7]   #0:snabbhet,1:pricksäkerhet,2:magiskt skydd(skyddar mot allt men dubbelt mot magi),3:evasion
        self.rustning=0

    def other(self):
        print('Fantomen är stilla')
    
    def mode(self):
        mode=randint(0,4)
        if mode>2:
            return 'critical'
        else:
            return 'other'

    def drop(self, plus, progress, OP):
        if randint(0,15) + plus > 15:
            return ['Demondryck','Livsfrukt','Ormmedicin',False][randint(0,3)]
        else:
            return False

#-----------------------------------------------------Dåtiden, skog
class Vitvarg(Varelse):
    namn = 'Vitvarg'
    namnB = namn+'en'

    def __init__(self, nr=0):
        if nr!=0:
            self.namn+=' '+nr
        self.exp=500
        self.liv=250
        self.hp=self.liv
        self.stats={'str':19,'smi':16,'mkr':7}
        self.mods=[0,0,6,0]   #0:snabbhet,1:pricksäkerhet,2:magiskt skydd(skyddar mot allt men dubbelt mot magi),3:evasion
        self.rustning=6
    
    def mode(self):
        mode=randint(0,3)
        if mode > 0:
            return 'attack'
        else:
            return 'critical'
        
    def drop(self, plus, progress, OP):
        n = randint(0,15)+plus
        if n > 14:
            return 'Blodkristall'
        return False

class Olyckskorp(Varelse):
    namn = 'Olyckskorp'
    namnB = namn+'en'

    def __init__(self, nr=0):
        if nr!=0:
            self.namn+=' '+nr
        self.exp=350
        self.liv=100
        self.hp=self.liv
        self.stats={'str':14,'smi':23,'mkr':7}
        self.mods=[0,0,5,0]   #0:snabbhet,1:pricksäkerhet,2:magiskt skydd(skyddar mot allt men dubbelt mot magi),3:evasion
        self.rustning=3
    
    def mode(self):
        mode=randint(0,3)
        if mode > 1:
            return 'attack'
        elif mode == 1:
            return 'Ändra framtiden'
        else:
            return 'critical'
        
    def drop(self, plus, progress, OP):
        return False

class Skogsvasen(Varelse):
    namn = 'Skogsväsen'
    namnB = namn+'det'

    def __init__(self, nr=0):
        if nr!=0:
            self.namn+=' '+nr
        self.exp=600
        self.liv=200
        self.hp=self.liv
        self.stats={'str':5,'smi':18,'mkr':19}
        self.mods=[0,0,14,0]   #0:snabbhet,1:pricksäkerhet,2:magiskt skydd(skyddar mot allt men dubbelt mot magi),3:evasion
        self.rustning=0
    
    def mode(self):
        mode=randint(0,6)
        if mode == 0:
            return 'Naturkraft'
        elif mode == 1:
            return 'Upplyftning'
        else:
            return 'Eld'
        
    def drop(self, plus, progress, OP):
        n = randint(0,15)+plus
        if n > 14:
            return 'Trädgrenskrona'
        elif n > 8:
            return 'Älvstoft'
        return False

class Gammeltroll(Varelse):
    namn = 'Gammeltroll'
    namnB = namn+'et'

    def __init__(self, nr=0):
        if nr!=0:
            self.namn+=' '+nr
        self.exp=850
        self.liv=450
        self.hp=self.liv
        self.stats={'str':23,'smi':14,'mkr':20}
        self.mods=[0,0,6,0]   #0:snabbhet,1:pricksäkerhet,2:magiskt skydd(skyddar mot allt men dubbelt mot magi),3:evasion
        self.rustning=4
    
    def mode(self):
        mode=randint(0,3)
        if mode == 0 and 99 < self.hp < 200:
            return 'Återhämtning 2'
        elif mode == 1:
            return 'Trollsmäll'
        else:
            return 'attack'
        
    def drop(self, plus, progress, OP):
        n = randint(0,16)+plus
        if n > 15:
            return 'Kraftring'
        return False

#-----------------------------------------------------Dåtiden, berg

#Gammeltroll, Draken

class Dimdvarg(Varelse):
    namn='Dimdvärg'
    namnB = namn+'en'

    def __init__(self, nr=0):
        if nr!=0:
            self.namn+=' '+nr
        self.exp=450
        self.liv=210
        self.hp=self.liv
        self.stats={'str':15,'smi':17,'mkr':14}
        self.mods=[-1,0,10,0]   #0:snabbhet,1:pricksäkerhet,2:magiskt skydd(skyddar mot allt men dubbelt mot magi),3:evasion
        self.rustning=0
    
    def mode(self):
        mode=randint(0,4)
        if mode > 2:
            return 'attack'
        elif mode > 0:
            return 'dubbel'
        else:
            return 'Förvrida framtiden'
        
    def drop(self, plus, progress, OP):
        n = randint(0,13)+plus
        if n > 12:
            return 'Dimsilverbrynja'
        return False

class Sfinx(Varelse):
    namn = 'Sfinx'
    namnB = namn+'en'

    def __init__(self, nr=0):
        if nr!=0:
            self.namn+=' '+nr
        self.exp=1800
        self.liv=1000
        self.hp=self.liv
        self.stats={'str':23,'smi':18,'mkr':23}
        self.mods=[0,0,7,0]   #0:snabbhet,1:pricksäkerhet,2:magiskt skydd(skyddar mot allt men dubbelt mot magi),3:evasion
        self.rustning=5
        self.modes = ['Förgöra','attack','dubbel','Eld','Helning',
                      'Sömnighet','Kvävning','Skräck','other']
    
    def mode(self):
        return self.modes[randint(0,8)]
        
    def other(self):
        slowprint('Sfinxen är stilla\n')
        
    def drop(self, plus, progress, OP):
        n = randint(0,19)+plus
        if n > 18:
            return 'Guldspira'
        return False

#----------------------------------------------------------------------
#BOSSAR

class ElakaHaxan1(Varelse):
    exp=100
    liv=120
    hp=liv
    stats={'str':7,'smi':7,'mkr':8}
    mods=[0,0,3,0]
    rustning=3
    fly=False
    namn='Elaka häxan'
    namnB=namn

    def mode(self):
        mode = randint(0,6)
        if mode > 2:
            return 'attack'
        elif mode == 2:
            return 'Förvrida framtiden'
        else:
            return 'Smärta'

    def drop(self, plus, progress, OP):
        return 'Svart mantel'

class Vildsvinet(Varelse):
    exp=180
    liv=240
    hp=liv
    stats={'str':9,'smi':6,'mkr':1}
    mods=[-1,0,0,0]
    rustning=4
    fly=False
    namn='Vildsvinet'
    namnB=namn

    def mode(self):
        mode = randint(0,5)
        if mode > 0:
            return 'attack'
        else:
            return 'critical'

    def drop(self, plus, progress, OP):
        return 'Grön mantel'

class Grisen(Varelse):
    exp=50
    liv=45
    hp=liv
    stats={'str':7,'smi':8,'mkr':6}
    mods=[0,0,0,0]
    rustning=5
    fly=False
    namn='Grisen'
    namnB=namn

    def mode(self):
        mode = randint(0,4)
        if mode > 0:
            return 'attack'
        else:
            return 'Smärta'

    def drop(self, plus, progress, OP):
        return False

class Gaurghus(Varelse):
    exp=220
    liv=220
    hp=liv
    stats={'str':10,'smi':12,'mkr':10}
    mods=[0,0,4,0]
    rustning=4
    fly=False
    namn='Gaurghus ormen'
    namnB=namn

    def mode(self):
        mode = randint(0,5)
        if mode == 0 and self.hp < 120:
            return 'Återhämtning'
        elif mode == 1:
            return 'Hypnos'
        else:
            return 'attack'

    def drop(self, plus, progress, OP):
        return 'Ormdräkt'

class Entrios(Varelse):
    exp=900
    liv=550
    hp=liv
    stats={'str':18,'smi':13,'mkr':17}
    mods=[-1,0,5,3]
    rustning=5
    fly=False
    namn='Entrios'
    namnB=namn+' nattens väktare'

    def mode(self):
        mode = randint(0,4)
        if mode == 0 and self.hp > 300:
            return 'Förbjuden makt'
        elif mode == 1:
            return 'Eld'
        elif mode == 2:
            return 'Ändra framtiden'
        else:
            return 'attack'

    def drop(self, plus, progress, OP):
        return 'Skuggsvärd'

class Otak(Varelse):
    exp=175
    liv=160
    hp=liv
    stats={'str':14,'smi':9,'mkr':5}
    mods=[0,0,3,0]
    rustning=8
    fly=False
    namn='Riddare Otak'
    namnB=namn

    def mode(self):
        mode = randint(0,5)
        if mode > 3:
            return 'critical'
        else:
            return 'attack'

    def drop(self, plus, progress, OP):
        return 'Riddarrustning'

class Joshki(Varelse):
    exp=165
    liv=140
    hp=liv
    stats={'str':11,'smi':10,'mkr':9}
    mods=[0,0,5,0]
    rustning=4
    fly=False
    namn='Riddare Joshki'
    namnB=namn

    def mode(self):
        mode = randint(0,7)
        if mode == 0:
            return 'Förtärande mörker'
        elif mode == 1:
            return 'critical'
        else:
            return 'attack'

    def drop(self, plus, progress, OP):
        return 'Mystiskt spjut'

class Joshki2(Varelse):
    exp=200
    liv=170
    hp=liv
    stats={'str':13,'smi':11,'mkr':9}
    mods=[0,0,4,0]
    rustning=4
    fly=False
    namn='Riddare Joshki'
    namnB=namn

    def mode(self):
        mode = randint(0,7)
        if mode == 0:
            return 'Förtärande mörker'
        elif mode == 1:
            return 'Se framtiden'
        elif mode < 4:
            return 'Smärta'
        else:
            return 'attack'

    def drop(self, plus, progress, OP):
        return 'Förbannad juvel'

class Kolskagg(Varelse):
    exp=1200
    liv=500
    hp=liv
    stats={'str':20,'smi':14,'mkr':9}
    mods=[-1,0,6,0]
    rustning=6
    fly=False
    namn='Kung Kolskägg'
    namnB=namn

    def mode(self):
        mode = randint(0,6)
        if mode < 2:
            return 'mystisk'
        elif mode == 2 and 50 < self.hp < 150:
            return 'Helning'
        elif mode == 3:
            return 'dubbel'
        else:
            return 'attack'

    def drop(self, plus, progress, OP):
        return 'Konungasvärd'

class Draken(Varelse):
    namn = 'Drake'
    namnB = namn+'n'

    def __init__(self, nr=0):
        if nr!=0:
            self.namn+=' '+nr
        self.exp=1600
        self.liv=900
        self.hp=self.liv
        self.stats={'str':24,'smi':12,'mkr':17}
        self.mods=[-1,0,8,0]   #0:snabbhet,1:pricksäkerhet,2:magiskt skydd(skyddar mot allt men dubbelt mot magi),3:evasion
        self.rustning=8
        self.modes = ['critical','attack','attack','Eld','Eld','Svansattack']
    
    def mode(self):
        return self.modes[randint(0,5)]
        
    def drop(self, plus, progress, OP):
        n = randint(0,15)+plus
        if n > 14:
            return 'Drakfjällsrustning'
        return False

class Trollkungen(Varelse):
    exp=2000
    liv=1200
    hp=liv
    stats={'str':24,'smi':17,'mkr':19}
    mods=[-1,0,7,0]
    rustning=7
    fly=False
    namn='Trollkungen'
    namnB=namn
    modes = ['critical','attack','attack','attack','Trollstoft',
             'Trollsmäll','Trollsmäll','Sömnighet','Se framtiden']
    
    def mode(self):
        return self.modes[randint(0,8)]

    def drop(self, plus, progress, OP):
        return 'Silvertunga'

class ToVaktare(Varelse):
    namn = 'Tornets väktare'
    namnB = namn
    exp=2000
    liv=1500
    hp=liv
    stats={'str':30,'smi':17,'mkr':17}
    mods=[-1,0,8,-1]   #0:snabbhet,1:pricksäkerhet,2:magiskt skydd(skyddar mot allt men dubbelt mot magi),3:evasion
    rustning=8
    
    def mode(self):
        n = randint(0,6)
        if n == 0:
            return 'Skräck'
        elif n == 1:
            return 'dubbel'
        elif n < 4:
            return 'Svansattack'
        return 'attack'
        
    def drop(self, plus, progress, OP):
        return 'Kraftdryck'

class ElakaHaxan2(Varelse):
    exp=0
    liv=1700
    hp=liv
    stats={'str':24,'smi':19,'mkr':24}
    mods=[-1,0,10,0]
    rustning=7
    fly=False
    namn='Elaka häxan'
    namnB=namn
    modes = ['Eld','Eld','attack','attack','Förgöra',
             'Ändra framtiden','Smärta','Smärta']
    
    def mode(self):
        return self.modes[randint(0,7)]

    def drop(self, plus, progress, OP):
        return False

#----------------------------------------------------------------------
#DEMONER

class DemonenZl(Varelse):
    exp=800
    liv=1900
    hp=liv
    stats={'str':32,'smi':40,'mkr':20}
    mods=[0,0,10,0]
    rustning=2
    fly=True
    namn='Demonen Zlokr'
    namnB=namn

    def mode(self):
        mode = randint(0,6)
        if mode > 2:
            return 'attack'
        elif mode == 2:
            return 'critical'
        elif mode == 1:
            return 'Förvrida framtiden'
        else:
            return 'other'

    def other(self):
        slowprint('Demonen Zlokr skrattar ett infernaliskt skratt\n')

    def drop(self, plus, progress, OP):
        return 'Zlokrs kappa'

class DemonenZa(Varelse):
    exp=1200
    liv=3200
    hp=liv
    stats={'str':55,'smi':15,'mkr':2}
    mods=[-1,0,0,0]
    rustning=10
    fly=True
    namn='Demonen Zaumakot'
    namnB=namn
    ordning = 1

    def mode(self):
        self.ordning += 1
        if self.ordning > 13:
            return 'Förgöra verkligheten'
        elif self.ordning == 5 or self.ordning == 12:
            return 'other'
        mode = randint(0,9)
        if mode > 0:
            return 'attack'
        else:
            return 'Stank'

    def other(self):
        if self.ordning == 5:
            slowprint('Zaumakots ögon svartnar\n',3)
        else:
            slowprint('Zaumakot börjar glöda och skaka\n',3)

    def drop(self, plus, progress, OP):
        return 'Zaumakots armband'

class DemonenZi(Varelse):
    exp=4000
    liv=2400
    hp=liv
    stats={'str':27,'smi':27,'mkr':27}
    mods=[0,0,10,0]
    rustning=10
    fly=True
    namn='Demonen Ziriekl'
    namnB=namn

    def mode(self):
        mode = randint(0,9)
        if mode == 0:
            return 'dubbel'
        elif mode < 3:
            return 'Förgöra'
        elif mode == 3:
            return 'Beskydd'
        else:
            return 'Eld'

    def drop(self, plus, progress, OP):
        return 'Ziriekls rustning'

class Zeoidodh(Varelse):
    exp=6000
    liv=4000
    hp=liv
    stats={'str':55,'smi':30,'mkr':20}
    mods=[-1,0,8,0]
    rustning=10
    fly=False
    namn='Zeoidodh'
    namnB=namn

    def mode(self):
        if self.stats['mkr'] > 30:
            return 'Eld'
        mode = randint(0,6)
        if mode < 4:
            return 'attack'
        elif mode == 4:
            return 'Naturkraft'
        else:
            return 'Kyla'

    def drop(self, plus, progress, OP):
        return 'Djurfrämlingens mask'

class Djurframlingen(Varelse):
    exp=6000
    liv=6000
    hp=liv
    stats={'str':60,'smi':35,'mkr':20}
    mods=[-1,0,8,0]
    rustning=10
    fly=False
    namn='Djurfrämlingen'
    namnB=namn

    def mode(self):
        mode = randint(0,5)
        if mode > 0:
            return 'attack'
        else:
            return 'Svansattack'

    def drop(self, plus, progress, OP):
        return 'Djurfrämlingens mask'
