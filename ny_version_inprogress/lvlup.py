from funktioner import difstat, plusformaga
from fightfunks import listval
from random import random, randint

class Bonus:
    def __init__(self,namn,funktion,args):
        self.namn=namn
        self.funktion=funktion
        self.args=args
    def use(self,spelare):
        self.funktion(spelare,*self.args)


def lvlup(spelarlista):
    while True:
        for spelare in spelarlista:
            if spelare.exp  >=  (25*spelare.lvl) + (spelare.lvl**2.7):
                spelare.lvl+=1
                print(spelare.namn+' är nu nivå '+str(spelare.lvl)+'!')
                if len(spelare.utveckling)<1: #om maxat utvecklingen
                    randombonus=[plushp,plushp,plushp,plushp,plushp,plusstr,plussmi,plusmkr]
                    randombonus[randint(0,7)].use(spelare)
                else:
                    n=listval([u[0]+': '+LEVELUP[u[0]][u[1]].namn for u in spelare.utveckling])
                    LEVELUP[spelare.utveckling[n][0]][spelare.utveckling[n][1]].use(spelare)
                    spelare.utveckling[n][1]+=1
                    if spelare.utveckling[n][1]==len(LEVELUP[spelare.utveckling[n][0]]):
                        spelare.utveckling.remove(spelare.utveckling[n])
        if not any([spelare.exp  >=  (25*spelare.lvl) + (spelare.lvl**2.7) for spelare in spelarlista]):
            break


################################      KONSTANTER       ###############################
        
PLUSSTR=Bonus('Bli starkare',difstat,('str',1))
PLUSHP=Bonus('Bli tåligare',difstat,('liv',7))
PLUSMKR=Bonus('Få magikraft',difstat,('mkr',1))
PLUSSMI=Bonus('Bli rörligare',difstat,('smi',1))
PLUSSNA=Bonus('Bli snabbare',difstat,(0,-1))
PLUSPRI=Bonus('Bli mer pricksäker',difstat,(1,1))
PLUSSKY=Bonus('Få mer motståndskraft',difstat,(2,1))
PLUSEVA=Bonus('Förbättra reflexer',difstat,(3,1))
PLUSNONE=Bonus('Ingenting',difstat,('liv',0))

KAMPLISTA=[PLUSSTR,
           PLUSHP,
           PLUSSTR,
           Bonus('Förmåga-Återhämtning',plusformaga,(1,'Återhämtning')),
           PLUSHP,
           PLUSSMI,
           PLUSSTR,
           PLUSHP,
           Bonus('Förmåga-Djärv attack',plusformaga,(1,'Djärv attack')),
           PLUSPRI,
           PLUSHP,
           PLUSSTR,
           PLUSSKY,
           PLUSHP,
           PLUSSMI,
           Bonus('Förmåga-Återhämtning 2',plusformaga,(1,'Återhämtning 2',0,'Återhämtning')),
           PLUSSTR,
           PLUSHP,
           PLUSSMI,
           PLUSSTR,
           PLUSHP,
           PLUSPRI,
           PLUSSTR,
           PLUSSKY,
           Bonus('Dubbel attack', plusformaga,(3,'Dubbel attack')),
           PLUSSTR,
           PLUSHP,
           PLUSSMI,
           PLUSSTR,
           PLUSHP]
SKICKLIGLISTA=[PLUSSMI,
               Bonus('Läkekonst', plusformaga,(3,'Läkekonst')),
               PLUSSNA,
               PLUSHP,
               Bonus('Förmåga-Strategi',plusformaga,(1,'Strategi')),
               PLUSSMI,
               PLUSHP,
               PLUSSTR,
               Bonus('Bedömning',plusformaga,(3,'Bedömning')),
               PLUSSMI,
               PLUSPRI,
               PLUSEVA,
               PLUSHP,
               Bonus('Skattletande',plusformaga,(3,'Skattletande')),
               PLUSSTR,
               PLUSSMI,
               PLUSHP,
               Bonus('Läkekonst 2', plusformaga,(3,'Läkekonst 2')),
               PLUSSMI,
               PLUSHP,
               PLUSSTR,
               PLUSHP,
               Bonus('Magi-Snabbhet',plusformaga,(2,'Snabbhet',2)),
               PLUSSMI,
               PLUSHP,
               Bonus('Skattletande 2',plusformaga,(3,'Skattletande 2')),
               PLUSSTR,
               PLUSSMI,
               PLUSHP]
TROLLDOMSLISTA=[PLUSMKR,
                Bonus('Magi-Hypnos',plusformaga,(2,'Hypnos',1)),
                PLUSSMI,
                Bonus('Magi-Lindring',plusformaga,(2,'Lindring',1)),
                PLUSMKR,
                PLUSHP,
                Bonus('Magi-Kyla',plusformaga,(2,'Kyla',2)),
                PLUSHP,
                Bonus('Förmåga-Mystisk kraft',plusformaga,(1,'Mystisk kraft')),
                PLUSHP,
                Bonus('Magi-Trollstyrka',plusformaga,(2,'Trollstyrka',1)),
                PLUSMKR,
                PLUSSMI,
                Bonus('Magi-Helning',plusformaga,(2,'Helning',1)),
                PLUSMKR,
                Bonus('Magi-Sömnighet',plusformaga,(2,'Sömnighet',3)),
                PLUSHP,
                PLUSMKR,
                PLUSSMI,
                Bonus('Magi-Upplyftning',plusformaga,(2,'Upplyftning',3)),
                PLUSHP,
                PLUSMKR,
                Bonus('Magi-Smärta',plusformaga,(2,'Smärta',3)),
                PLUSEVA,
                PLUSMKR,
                PLUSSKY,
                Bonus('Magi-Beskydd',plusformaga,(2,'Beskydd',3)),
                PLUSHP,
                PLUSMKR,
                PLUSSMI,
                PLUSMKR,
                PLUSHP,
                PLUSMKR,
                PLUSSMI]
DUNKELLISTA=[Bonus('Magi-Se framtiden',plusformaga,(2,'Se framtiden',1)),
             PLUSSTR,
             PLUSHP,
             PLUSMKR,
             Bonus('Magi-Mörk attack',plusformaga,(2,'Mörk attack',1)),
             PLUSSKY,
             PLUSHP,
             PLUSSTR,
             PLUSHP,
             PLUSMKR,
             PLUSSMI,
             Bonus('Magi-Förvrida framtiden',plusformaga,(2,'Förvrida framtiden',2)),
             PLUSHP,
             PLUSSKY,
             PLUSMKR,
             Bonus('Magi-Kyla',plusformaga,(2,'Kyla',2)),
             PLUSSTR,
             PLUSHP,
             PLUSMKR,
             PLUSSMI,
             PLUSHP,
             Bonus('Förmåga-Projicera själ',plusformaga,(1,'Projicera själ')),
             PLUSSTR,
             PLUSHP,
             PLUSHP,
             Bonus('Magi-Ändra framtiden',plusformaga,(2,'Ändra framtiden',3)),
             PLUSSTR,
             PLUSHP,
             PLUSMKR,
             PLUSSKY,
             PLUSHP,
             PLUSSTR,
             PLUSHP,
             PLUSSMI,
             PLUSMKR,
             PLUSSTR,
             PLUSHP,
             PLUSMKR,
             Bonus('Magi-Förtärande mörker',plusformaga,(2,'Förtärande mörker',4)),
             PLUSSKY,
             PLUSHP,
             PLUSSTR,
             PLUSHP,
             PLUSSMI,
             PLUSMKR]
SJALLISTA=[PLUSHP,
           PLUSSMI,
           PLUSMKR,
           Bonus('Förmåga-Fågel',plusformaga,(1,'Fågel')),
           PLUSHP,
           PLUSSTR,
           PLUSSMI,
           PLUSHP,
           PLUSMKR,
           PLUSSTR,
           PLUSHP,
           PLUSSMI,
           PLUSMKR,
           Bonus('Förmåga-Gorilla',plusformaga,(1,'Gorilla')),
           PLUSHP,
           PLUSSTR,
           PLUSSMI,
           PLUSHP,
           PLUSMKR,
           PLUSSTR,
           PLUSHP,
           PLUSSMI,
           PLUSMKR,
           PLUSHP,
           PLUSSTR,
           PLUSSMI,
           PLUSHP,
           PLUSMKR,
           Bonus('Förmåga-Älva',plusformaga,(1,'Älva')),
           PLUSSTR,
           PLUSHP,
           PLUSSMI,
           PLUSMKR,
           PLUSHP,
           PLUSSTR,
           PLUSSMI,
           PLUSHP,
           PLUSMKR,
           PLUSSTR]
HEMLIGLISTA=[Bonus('Förmåga-Mystisk kraft',plusformaga,(1,'Mystisk kraft')),
             PLUSMKR,
             PLUSHP,
             Bonus('Magi-Eld', plusformaga,(2,'Eld',3)),
             PLUSNONE,
             Bonus('Magi-Helning',plusformaga,(2,'Helning',1)),
             PLUSHP,
             PLUSSMI,
             PLUSNONE,
             Bonus('Lyckoträff', plusformaga,(3,'Lyckoträff')),
             Bonus('Mystisk attack', plusformaga,(2,'Mystisk attack',3)),
             PLUSNONE,
             PLUSMKR,
             Bonus('Magi-Livskraft', plusformaga,(2,'Livskraft',4)),
             Bonus('Förmåga-Urkraft',plusformaga,(1,'Urkraft'))]
UTLISTA=[Bonus('Förmåga-Uthållighet',plusformaga,(1,'Uthållighet')),
        PLUSSTR,
        PLUSHP,
        PLUSSMI,
        PLUSHP,
        PLUSMKR,
        Bonus('Förmåga-Djärv attack',plusformaga,(1,'Djärv attack')),
        PLUSHP,
        PLUSSTR,
        PLUSHP,
        PLUSSMI,
        PLUSSTR,
        PLUSMKR,
        PLUSHP,
        PLUSSTR,
        Bonus('Magi-Återställning',plusformaga,(2,'Återställning',2)),
        PLUSHP,
        PLUSSMI,
        PLUSHP,
        PLUSMKR,
        PLUSHP,
        PLUSSTR,
        PLUSHP,
        PLUSSMI,
        PLUSSTR,
        PLUSMKR,
        PLUSHP,
        Bonus('Lura döden',plusformaga,(3,'Lura döden'))]
        

LEVELUP={'Kamp':KAMPLISTA, 'Trolldom':TROLLDOMSLISTA, 'Dunkel konst':DUNKELLISTA, 'Uthållighet': UTLISTA,
         'Skicklighet':SKICKLIGLISTA, 'Själskunskap':SJALLISTA, 'Hemlig lära':HEMLIGLISTA}
