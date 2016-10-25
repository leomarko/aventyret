#klasser
#Varelse, Spelare, alla typer av föremål

from funktioner import difstat, plusformaga
from random import random, randint

##########KLASSER

class Varelse:    
    def hpstr(self):
        return str(self.hp)+'/'+str(self.liv)

    def klocka(self):
        klocka=12
        klocka -= int(self.stats['smi']*1.6 - self.stats['smi']**1.07 - self.mods[0]*1.7) 
        #klockan minskar långsammare ju närmare noll, snabbhet räknas negativt
        if klocka < -1:
            klocka = 1
        elif klocka < 1.5:
            klocka = 2
        elif klocka < 3:
            klocka = 3
        else:
            klocka = int(klocka)
        return klocka

    def hit(self,other):
        if (self.stats['smi']*1.5 + self.mods[1]*3)*(0.5 + random()) + randint(2,5)  >  other.stats['smi'] + other.mods[3]*3: 
            return True
        else:
            return False

class Spelare(Varelse):
    def __init__(self, namn, liv, styrka, smidighet, magikraft,utveckling):
        self.namn=namn
        self.liv=liv
        self.hp=liv
        self.stats={'str':styrka,'smi':smidighet,'mkr':magikraft}
        self.mods=[0,0,0,0]
        self.utveckling=utveckling #i form av ett gäng listor med två element,klassnamn och lvl

        self.utrust={'vapen':Foremal('-'),'rustning':Foremal('-'), 'ovrigt':Foremal('-')}
        self.formagor=[]
        self.magier=[]  #i form av tuples, där andra elementet är mpkostnad
        self.special=[]
        
        self.lvl=1
        self.exp=0

        self.vilande={}
    
    def equip(self,sak):
        gammalt = Foremal('')
        if isinstance(sak, Vapen):
            if sak.ok(self):
                plus = sak.skada
                if self.utrust['vapen'].namn != '-':
                    print(self.namn+' la ned '+self.utrust['vapen'].namn+' i packningen.')
                    gammalt = self.utrust['vapen']
                    plus -= gammalt.skada
                self.utrust['vapen']=sak
                print(self.namn+' använder nu '+self.utrust['vapen'].namn+'.')
                print(self.namn+' fick '+str(int(plus*2))+' i attack jämfört med tidigare')
                return gammalt
        if isinstance(sak, Rustning):
            if sak.ok(self):
                plus = sak.skydd
                if self.utrust['rustning'].namn != '-':
                    print(self.namn+' la ned '+self.utrust['rustning'].namn+' i packningen.')
                    gammalt = self.utrust['rustning']
                    plus -= gammalt.skydd
                self.utrust['rustning']=sak
                print(self.namn+' använder nu '+self.utrust['rustning'].namn+'.')
                print(self.namn+' fick '+str(plus)+' i skydd jämfört med tidigare')
                return gammalt
        if isinstance(sak, Ovrigt):
            if sak.ok(self):
                if self.utrust['ovrigt'].namn != '-':
                    print(self.namn+' la ned '+self.utrust['ovrigt'].namn+' i packningen.')
                    gammalt = self.utrust['ovrigt']
                    gammalt.equip(self, False)
                self.utrust['ovrigt']=sak
                print(self.namn+' använder nu '+self.utrust['ovrigt'].namn+'.')
                self.utrust['ovrigt'].equip(self)
                return  gammalt
        print('du kan inte använda det')
        return False

class Foremal:
    def __init__(self,namn):
        self.namn=namn
        
class EngangsForemal:
    def __init__(self,namn,bs,funktion=None, args=None, fight=False, target=False):
        self.namn=namn
        self.bs = bs
        self.funktion=funktion
        self.args=args
        self.fight=fight
        self.target=target

    def use(self,target):
        res = self.funktion(target,*self.args)
        return res

class Utrustning:
    def __init__(self,namn,krav,attribut):
        self.namn=namn
        self.krav=krav
        self.attribut=attribut

    def ok(self,spelare):
        if self.krav:
            if spelare.stats[self.attribut]<self.krav:
                return False
        return True

class Ovrigt(Utrustning): #kan ge förmåga och/eller ändra stat
    def __init__(self, namn, bs, stat, plus, formaga=None, krav=False, attribut=''):
        super().__init__(namn,krav,attribut)
        self.kortbs = bs
        self.bs = 'Attiralj: '+bs
        self.stat=stat
        self.plus=plus
        self.formaga=formaga #tupel med 3 element        
    
    def equip(self,spelare,on=True):
        if on:
            difstat(spelare,self.stat,self.plus)
        else:
            difstat(spelare,self.stat,-self.plus)
        if on and self.formaga:
            plusformaga(spelare, *self.formaga)
        elif self.formaga:
            borta = True
            if self.formaga[0] == 1:
                spelare.formagor.remove(self.formaga[1])
                if self.formaga[1] in spelare.formagor:
                    borta = False
            if self.formaga[0] == 2:
                spelare.magier.remove((self.formaga[1],self.formaga[2]))
                if self.formaga[1] in [m[0] for m in spelare.magier]:
                    borta = False
            if self.formaga[0] == 3:
                spelare.special.remove(self.formaga[1])
                if self.formaga[1] in spelare.special:
                    borta = False
            if borta:
                print(spelare.namn+' kan inte längre använda '+self.formaga)
                
class Vapen(Utrustning):
    def __init__(self,namn,skada,krav=False, attribut='',magi=0):
        super().__init__(namn,krav,attribut)
        self.skada=skada
        self.magi=magi
        self.bs = 'Vapen: +'+str(int(skada*2))
        if magi != 0:
            self.bs += ', magi +'+str(int(magi*2))

class Rustning(Utrustning):
    def __init__(self,namn,skydd,krav=False, attribut='',mskydd=0):
        super().__init__(namn,krav,attribut)
        self.skydd=skydd
        self.mskydd=mskydd
        self.bs = 'Rustning: +'+str(skydd)
        if mskydd != 0:
            self.bs += ', m-skydd +'+str(mskydd)

class Kartdict:
    def __init__(self,dictionary,u):
        self.d = dictionary
        self.u = u
        
    def namn(self,nyckel):
        if nyckel in self.u:                
            namn = self.d[nyckel]
        else:
            namn = '???'
        space = 14 - len(namn)
        if space % 2 == 0:
            space = int(space*0.5)
            namn = (' '*space)+namn+(' '*space)
        else:
            a = int(space/2)
            b = int(space/2 + 1)
            namn = (' '*a)+namn+(' '*b)
        return namn

class Karta:
    def __init__(self,pdict):
        self.PDICT = pdict

    def markp(self,nuvarande_position,kartposition):
        if nuvarande_position == kartposition:
            return '--Du är här-- '
        else:
            return ' '*14

    def rita(self,upptackt,p):
        #u är set med upptäckta platser
        d = Kartdict(self.PDICT,upptackt)
        if p < 100:
            x = 0
        elif p < 200:
            x = 100
        elif p < 300:
            x = 200
        else:
            x = 300
        print('\n\n'+
              '    '+'-'*26+'NORR'+'-'*26+'    \n\n'+
              '-   '+d.namn(x + 13)+d.namn(x + 14)+d.namn(x + 15)+d.namn(x + 16)+'   -\n'+
              '-   '+self.markp(p,x+13)+self.markp(p,x+14)+self.markp(p,x+15)+self.markp(p,x+16)+'   -\n'+
              '-   '+' '*56+'   -\n'+
              'V   '+d.namn(x + 9)+d.namn(x + 10)+d.namn(x + 11)+d.namn(x + 12)+'   -\n'+
              'Ä   '+self.markp(p,x+9)+self.markp(p,x+10)+self.markp(p,x+11)+self.markp(p,x+12)+'   Ö\n'+
              'S   '+' '*56+'   S\n'+
              'T   '+d.namn(x + 5)+d.namn(x + 6)+d.namn(x + 7)+d.namn(x + 8)+'   T\n'+
              '-   '+self.markp(p,x+5)+self.markp(p,x+6)+self.markp(p,x+7)+self.markp(p,x+8)+'   -\n'+
              '-   '+' '*56+'   -\n'+
              '-   '+d.namn(x + 1)+d.namn(x + 2)+d.namn(x + 3)+d.namn(x + 4)+'   -\n'+
              '-   '+self.markp(p,x+1)+self.markp(p,x+2)+self.markp(p,x+3)+self.markp(p,x+4)+'   -\n'+
              '\n    '+'-'*26+'SYD'+'-'*27+'    '+'\n\n')
