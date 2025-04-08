from abe import *


def intérieur(ch):
    return ch[1 : len(ch) - 1]


def suivant(ch):
    return ch[1:]


def découpage(ch, i):
    return (ch[:i], ch[i], ch[i + 1 :])


assert intérieur("(2+3)") == "2+3"

assert suivant("-(2+3)") == "(2+3)"

assert découpage("(2+3)*(4+5)", 5) == ("(2+3)", "*", "(4+5)")


# Exo 2:


def suppression_espaces(ch):
    r = ""
    for c in ch:
        if c != " ":
            r += c
    return r


assert suppression_espaces("( 2+ 3) * ( 4 + 7) ") == "(2+3)*(4+7)"


def remplacement_négatif(ch):
    r = ""
    prev = ch[0]
    if prev == "-":
        r += "_"
    else:
        r += ch[0]

    for c in ch[1:]:
        if c == "-" and prev in "(+-*/^<=>&|~":
            r += "_"
        else:
            r += c
        prev = c
    return r


assert remplacement_négatif("1+-3") == "1+_3"

assert remplacement_négatif("1-3") == "1-3"

assert remplacement_négatif("-1-3") == "_1-3"

assert remplacement_négatif("-(1+2)--5") == "_(1+2)-_5"


# Exo 03

op_prio = {
    "+": ")))+(((",
    "-": ")))-(((",
    "*": "))*((",
    "/": "))/((",
    "^": ")^(",
    "=": "))))=((((",
    "<": "))))<((((",
    ">": "))))>((((",
    "&": ")))))&(((((",
    "|": ")))))|(((((",
    "~": ")))))~(((((",
    ")": "))))))",
    "(": "((((((",
}


def parenthèsage(formule):
    formule = "(" + formule + ")"
    formule = suppression_espaces(formule)
    print(formule)
    formule = remplacement_négatif(formule)

    r = ""
    for c in formule:
        if c in op_prio:
            r += op_prio[c]
        else:
            r += c
    return r


assert parenthèsage("-1+2 *3") == "((((((_1)))+(((2))*((3))))))"

# Exo 5:


def indice_racine(ch):
    niveau = 0
    for i in range(len(ch) - 1, -1, -1):
        if ch[i] == ")":
            niveau += 1
        elif ch[i] == "(":
            niveau -= 1
        elif ch[i] in "+-*/^<=>|&~" and niveau == 0:
            return i


# print(indice_racine("(3*5)"))


def découpage_formule(ch):

    idx_racine = indice_racine(ch)
    if idx_racine is None:
        return None
    else:
        return découpage(ch, idx_racine)


assert découpage_formule("1-5+2-(3*5)") == ("1-5+2", "-", "(3*5)")


def arboriser_propre(ch):
    r = découpage_formule(ch)
    if r is None:
        if ch == "":
            return None
        if ch.isnumeric():
            return int(ch)
        elif ch.isalpha():
            return ch
        elif ch[0] == "(":

            return arboriser_propre(intérieur(ch))
        elif ch[0] == "_":
            return arbre("-", 0, arboriser_propre(suivant(ch)))

    else:
        if r[0] == "~":
            return arbre(None, "~", arboriser_propre(r[2]))
        else:
            return arbre(r[1], arboriser_propre(r[0]), arboriser_propre(r[2]))


def arboriser(ch):
    ch = parenthèsage(ch)
    return arboriser_propre(ch)


# assert arboriser("1-5+2-(3*5)") == ('-', ('+', ('-', 1, 5), 2), ('*', 3, 5))


# print(arboriser("~(a&b)"))


def est_arithmétique(A):
    if est_feuille(A):
        return isinstance(A, int)
    return est_arithmétique(fg(A)) and est_arithmétique(fd(A))


def calculer_arbre(A):
    if not est_arithmétique(A):
        raise ValueError("Tree is not arethmetic")
    if est_feuille(A):
        return A
    else:
        op = racine(A)
        Ag = calculer_arbre(fg(A))
        Ad = calculer_arbre(fd(A))
        if op == "+":
            return Ag + Ad
        elif op == "-":
            return Ag - Ad
        elif op == "*":
            return Ag * Ad
        elif op == "/":
            if Ad == 0:
                raise ValueError("Can't devide by zero")
            return Ag / Ad
        elif op == "^":
            return Ag**Ad


assert est_arithmétique(arboriser("1-5+2-(3*5)")) == True
# print(calculer_arbre(arboriser("1-5+2-(3*5)")))


def évaluer(ch):
    A = arboriser(ch)
    return calculer_arbre(A)


assert évaluer("1-5+2-(3*5)") == -17


def variables(A):

    def variables_helper(A):
        if A is None:
            return []
        if est_feuille(A):
            if isinstance(A, str):
                return [A]
            else:
                return []
        return variables_helper(fg(A)) + variables_helper(fd(A))

    return list(set(variables_helper(A)))


print(variables(arboriser("~(a&b)")))


def évaluer_environnement(A, env):
    if A is None:
        return
    if est_feuille(A):
        if A in env:
            return env[A]
        else:
            return A
    else:
        op = racine(A)
        Ag = évaluer_environnement(fg(A), env)
        Ad = évaluer_environnement(fd(A), env)
        if op == "+":
            return Ag + Ad
        elif op == "-":
            return Ag - Ad
        elif op == "*":
            return Ag * Ad
        elif op == "/":
            if Ad == 0:
                raise ValueError("Can't devide by zero")
            return Ag / Ad
        elif op == "^":
            return Ag**Ad

        # Logique
        elif op == "&":
            return Ag and Ad
        elif op == "|":
            return Ag or Ad
        elif op == "~":
            return not Ad
        elif op == "=":
            return Ag == Ad
        elif op == ">":
            return Ag > Ad
        elif op == "<":
            return Ag < Ad


variables_env = {"a": 5, "b": 2}
A1 = arboriser("1-5+b-(3*a)")

print(évaluer_environnement(A1, variables_env))

A2 = arboriser("~(a&b)")
variables_logic = {"a": True, "b": False}
print(évaluer_environnement(A2, variables_logic))


def combinaisons(variables):
    """
    Fonction D'aide qui génère une list de dictionnaires ou chaque dictionnaire contient une combinaison différente de
    valeurs bolleans de nos variables logiques.
    donc pour deux variables : on aura 4 combinaisons possible 2^2,
    et pour n variables on aura 2^n combinaisons possibles
    a = {a : T}, {a : F}
    a, b = {a : T, b : T}, {a : T, b: F}, {a: F, b : T}, {a: F, b : F}
    """
    if len(variables) == 1:
        return [{variables[0]: True}, {variables[0]: False}]
    else:
        rest_combinations = combinaisons(variables[1:])
        result = []
        for comb in rest_combinations:
            result.append({**comb, variables[0]: True})
            result.append({**comb, variables[0]: False})
        return result


def table_de_vérité(formule):
    r = ""
    A = arboriser(formule)
    print(A)
    variables_formule = variables(A)
    print(variables_formule)
    combinaisons_formule = combinaisons(variables_formule)

    for comb in combinaisons_formule:
        for value in comb.values():
            r += str(value) + " "
            # print(value, end=" ")
        eval_res = évaluer_environnement(A, comb)
        # print(eval_res)
        r += str(eval_res) + "\n"

    print(r)
    return r


# print(table_de_vérité("~(a&b)|(c&d)"))


def tautologie(formule):
    A = arboriser(formule)
    variables_formule = variables(A)
    combinaisons_formule = combinaisons(variables_formule)
    for comb in combinaisons_formule:
        if not évaluer_environnement(A, comb):
            return False
    return True


assert tautologie("a|(~a)") == True


def contradiction(formule):
    A = arboriser(formule)

    variables_formule = variables(A)
    combinaisons_formule = combinaisons(variables_formule)
    for comb in combinaisons_formule:
        if évaluer_environnement(A, comb):
            return False
    return True


assert contradiction("a&(~a)") == True


def équivalence(formule1, formule2):
    return table_de_vérité(formule1) == table_de_vérité(formule2)


assert équivalence("a&b", "c&d") == True

assert équivalence("a & b", "b & a")
assert équivalence("a | b", "b | a")
assert équivalence("~(a & b)", "(~a) | (~b)")
assert équivalence("~(a | b)", "(~a) & (~b)")
assert équivalence("(a & b) | ((~a) & (~b))", "a = b")

assert not équivalence("a & b", "a | b")
assert not équivalence("a", "~a")


def afficher(arbre):
    if arbre is None:
        return ""
    if est_feuille(arbre):
        return arbre
    else:
        return f"{afficher(fg(arbre))} {racine(arbre)} {afficher(fd(arbre))}"
