##############################################################
##                                                          ##
##  Module pour manipuler des arbres binaire dâ€™expression   ##
##                                                          ##
##############################################################



def arbre(r, Ag, Ad):
    """
    Construit un arbre Ã  partir dâ€™une racine et de deux arbres.
    """
    return (r, Ag, Ad)


def est_feuille(A):
    """
    Regarde si lâ€™arbre A est composÃ© ou sâ€™il est une simple feuille.
    Une feuille est soit un entier soit une chaÃ®ne de caractÃ¨re.
    """
    return type(A) == int or type(A) == str


def racine(A):
    """
    Renvoie la racine de lâ€™arbre A
    A doit Ãªtre un arbre composÃ© et non une feuiile
    """
    if est_feuille(A):
        raise ValueError("une feuille nâ€™a pas de racine")
    return A[0]


def fg(A):
    """
    Renvoie le fils gauche de lâ€™arbre A
    A doit Ãªtre un arbre composÃ© et non une feuiile
    """
    if est_feuille(A):
        raise ValueError("une feuille nâ€™a pas de fils gauche")
    return A[1]


def fd(A):
    """
    Renvoie le fils droit de lâ€™arbre A
    A doit Ãªtre un arbre composÃ© et non une feuiile
    """
    if est_feuille(A):
        raise ValueError('une feuille nâ€™a pas de fils droit')
    return A[2]
