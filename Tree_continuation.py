__author__ = 'aldazj'


def readfile(filename, type):
    """
    Lire un ficher et crée une liste avec les mots
    :param filename: nom du fichier
    :param type: verbe ou suffixe
    :return: liste avec tous les mots
    """
    list = []
    file = open(filename, 'r')
    if file:
        if type == "verbes":
            list = [line.strip() for line in file]
        elif type == "suffixes":
            list = [line.strip().split('\t') for line in file]
    return list


def analyse_suffixe(word, tree_suffixe):
    """
    Analyse les suffixe d'un arbre
    :param word: le suffixe
    :param tree_suffixe: arbre des suffixes
    :return: la description du suffixe
    """
    pointer_dico = tree_suffixe
    description = None
    for i in range(len(word)):
        if word[i] in pointer_dico.keys():
            pointer_dico = pointer_dico[word[i]]
        else:
            return description
    if 'end' in pointer_dico.keys():
        description = pointer_dico['end']
    return description


def analyse(word, tree_v, tree_ir, tree_er):
    """
    Cherche la description d'un verbe conjugué s'il existe
    :param word: verbe conjugué
    :param tree_v: arbre des verbes
    :param tree_ir: arbre des suffixes ir
    :param tree_er: arbre des suffixes er
    :return: la description du verbe conjugué
    """
    pointer_dico = tree_v
    description_verbe = []
    for i in range(len(word)):
        try:
            a = word[i]
            if word[i] in pointer_dico.keys():
                pointer_dico = pointer_dico[word[i]]
            else:
                break
            if 'end' in pointer_dico.keys():
                suffixes = pointer_dico['end'].split(';')
                if suffixes[0] == 'er':
                    tmp_desc_verbe = analyse_suffixe(word[i+1:], tree_er)
                    if tmp_desc_verbe is not None:
                        description_verbe.append(word[0:i+1]+'er')
                        description_verbe.append(tmp_desc_verbe)
                else:
                    tmp_desc_verbe = analyse_suffixe(word[i+1:], tree_ir)
                    if tmp_desc_verbe is not None:
                        description_verbe.append(word[0:i+1]+'ir')
                        description_verbe.append(tmp_desc_verbe)
                if len(suffixes) > 1:
                    if suffixes[1] == 'er':
                        tmp_desc_verbe = analyse_suffixe(word[i+1:], tree_er)
                        if tmp_desc_verbe is not None:
                            description_verbe.append(word[0:i+1]+'er')
                            description_verbe.append(tmp_desc_verbe)
                    else:
                        tmp_desc_verbe = analyse_suffixe(word[i+1:], tree_ir)
                        if tmp_desc_verbe is not None:
                            description_verbe.append(word[0:i+1]+'ir')
                            description_verbe.append(tmp_desc_verbe)
                # pointer_dico = pointer_dico[word[i+1]]
        except KeyError:
            break
    return description_verbe


def insert_tree(word, tree, end):
    """
    Creation d'un arbre à lettre
    :param word: le mot
    :param tree: l'arbre
    :param end: la terminaison
    :return:
    """
    pointer_dico = tree
    for i in range(len(word)):
        if not word[i] in pointer_dico.keys():
                pointer_dico[word[i]] = dict()
        pointer_dico = pointer_dico[word[i]]
        if i == len(word)-1 and end not in pointer_dico.values():
            if 'end' not in pointer_dico.keys():
                pointer_dico['end'] = end
            else:
                pointer_dico['end'] = pointer_dico['end']+";"+end


def build_tree(tree, list, type):
    """
    Construction des arbres
    :param tree: arbre
    :param list: liste des mots
    :param type: type d'arbre
    :return:
    """
    for word in list:
        if type == 'verbes':
            insert_tree(word[0:-2], tree, word[-2:])
        else:
            insert_tree(word[0], tree, word[1])


treeV = dict()
treeEr = dict()
treeIr = dict()
build_tree(treeV, sorted(readfile('verbes-er.txt', 'verbes')+readfile('verbes-ir.txt', 'verbes')), 'verbes')
build_tree(treeEr, readfile('suffixes-er.txt', 'suffixes'), 'suffixes')
build_tree(treeIr, readfile('suffixes-ir.txt', 'suffixes'), 'suffixes')
while True:
    myword = input('Entrez un verbe conjugué ou entrez le numero 0 pour arrêter:\n')
    if myword == '0':
        break
    response = analyse(myword, treeV, treeIr, treeEr)
    if response:
        if len(response) < 3:
            verb = response[0]
            conjugated_verbs = response[1].split(';')
            for conjugated_verb in conjugated_verbs:
                print(myword.ljust(10)+"==>"+" ".format(' '*2)+verb.ljust(10)+"/"+" ".format(' '*2)+conjugated_verb)
        else:
            for i in range(0, len(response), 2):
                print(myword.ljust(10)+"==>"+" ".format(' '*2)+response[i].ljust(10)+"/"+" ".format(' '*2)+response[i+1])
    else:
        print('Le mot \''+myword+'\' n\'existe pas dans la langue française ou n\'est pas enregistré dans ce programme!')
