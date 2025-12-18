# arbre (pas forcément binaire)
from typing import Union, TypeAlias
from data import data
ArbreVide: TypeAlias = tuple[()]
Arbre: TypeAlias = Union[ArbreVide, tuple[str, list['Arbre']]]

a_pref_rec: Arbre = ("a", 
              [
                ("ad", 
                   [
                       ("adroit", []),
                       ("adhésif",[])
                    ]),
                ("ab",
                    [
                        ("abruti", []),
                        ("abri", [
                            ("abri", []),
                            ("abricot", [])
                            ]
                        )
                    ])
                ])
            


def tete(x):
    return x[:1]

def queue(x):
    return x[1:]

def plus_long_prefique_commun(s1: str, s2: str) -> str:
    """Renvoie la plus longue chaine commune entre s1 et s2
    """
    match tete(s1):
        case '':
            return ''
        case _:
            if tete(s1) == tete(s2):
                return tete(s1) + plus_long_prefique_commun(queue(s1), queue(s2))
            else:
                return ''
            
assert plus_long_prefique_commun("abrupt", "abricot") == "abr"


def ajouter(x: str, a: Arbre) -> Arbre:
    match a:
        case ():
            return (x, [])
        case (r, enfants):
            if plus_long_prefique_commun(x, r) == r:
                if all([plus_long_prefique_commun(x, e[0]) == r for e in enfants]): #Si x ne correspond à aucun enfant
                    return (r, enfants + [(x, [])])
                else:
                    rendu = []
                    for k in enfants:
                        k_racine = k[0]
                        if plus_long_prefique_commun(x, k_racine) != r:
                            rendu.append(ajouter(x, k))
                        else:
                            rendu.append(k)
                    return (r, rendu)
            else:
                return (plus_long_prefique_commun(x, r), [a, (x, [])])
                
                

def prediction(x: str, a: Arbre) -> list[str] | str:
    match a:
        case ():
            return "Pas possible"

        case (racine, enfants):
            if racine == x:
                if enfants == []:
                    return "Pas possible"
                else:
                    return [k[0] for k in enfants]

            correct = []
            for k in enfants:
                if plus_long_prefique_commun(x, k[0]) == x:
                    correct.append(k[0])

            if correct != []:
                return correct

            else:
                for k in enfants:
                    rendu = prediction(x, k)
                    if rendu != "ya pas":
                        return rendu
                    
                return "ya pas"


assert prediction("abr", a_pref_rec) == ["abruti", "abri"]

##########################################################################

arb: Arbre = ()
for i, mot in enumerate(data):
    arb = ajouter(mot, arb)
    if i % 200 == 0:
        print(f"{i} mots ajoutés")
