#! /usr/bin/python
# -*- coding: utf-8 -*-

import wget
import html2text
import justext
import os
import requests
import urllib2
from urllib import urlopen
import django.utils.encoding
from django.utils.encoding import smart_str
import subprocess as sub
import datetime
import json
import nltk
from pprint import pprint
#import test_api.py
import random
from urlparse import urlparse

import boilerpipe
from boilerpipe.extract import Extractor

# chaines de caracteres frequements utilisees
exception_url = 'La page demande n\'est pas accessible pour le moment : '
corpus_perso_directory = './corpus_perso/'
corpus_daniel_directory= './corpus_daniel/corpus_multi/'

# lit un fichier json
def read_json(jsonstring):
    json_data = open(jsonstring)
    data = json.load(json_data)
    return data


# permet de recuprer les donnees desirees du json et les mets dans un tuple
# retourne une liste de tuple
def create_listeOfTuple(data):
    listeOfTuple = []
    for key, value in data.iteritems():

        id = key
        url = ''
        lang = ''
        path = ''
        for key2, value in value.iteritems():
            if key2 == 'langue':
                lang = str(value)
            if key2 == 'url':
                url = str(value)
            if key2 == 'path':
                path = str(value)
        tuple = (key, lang, url, path)
        listeOfTuple.append(tuple)

    return listeOfTuple


# transforme un contenu web en txt en utilisant html2text
# retourne le text
def toHtml2text(webContent):
    print 'Entree dans toHtml2text'

    txt=''
    h = html2text.HTML2Text()
    h.ignore_links = True
    txt = h.handle(webContent).encode('utf-8')
    return txt

# transforme un contenu web en txt en utilisant justText
# retourne le text
def toJustText(webContent):
    print 'Entree dans toJustText'

    txt=''
    paragraphs = justext.justext(webContent, justext.get_stoplist("English"))
    for paragraph in paragraphs:
        #if not paragraph.is_boilerplate:
        txt+= smart_str(paragraph.text.encode('utf-8'))
    return txt

# transforme un contenu web en txt en utilisant BoilerPipe
# retourne le text
def toBoilerPipe(myURL):
    extractor = Extractor(extractor='ArticleExtractor', url=myURL)
    txt = extractor.getText().encode('utf-8')
    return txt


# Permet d'appeler la fonction qui transforme le contenu web en fonction de l'outil desire
def webContentToText(webContent, tool, url):
    if tool == "html2text":
        txt = toHtml2text(webContent)
    if tool == "justText":
        txt = toJustText(webContent)
    if tool == "boilerpipe":
        txt = toBoilerPipe(url)
    return txt


# Creer des dossiers au chemin passe en parametre
def create_folder(folderPath):
    if not os.path.exists(folderPath):
        os.makedirs(folderPath)

#Lister les dossiers contenus dans un répertoire
def list_directories(path):
    langues = ''
    for path, dirs, files in os.walk(path):
        langues = dirs
        break
    return langues

# retoune le domaine d'une url donnee
def get_domains(url):
    parsed_uri = urlparse(url)
    domain = '{uri.netloc}'.format(uri=parsed_uri)
    return domain

# sauvegarde un contenu text dans un fichier a l'adresse fournie
def save_file(filepath, text):
    f = open(filepath, 'w')
    f.write(text)
    f.close


# permet de faire le traitement global
def get_html_file(listeOfTuples, tool):
    print tool
    i = 0

    html_eval = '<!DOCTYPE html> <html> <head> <title> Resultat global </title> </head> <body>'
    html_eval+= '<table><tr><th>Fichier</th><th>Langue</th><th>Domaine</th><th>Gold Standard</th><th>JusText</th><th>BoilerPipe</th></tr>'

    while i < len(listeOfTuples):

        print i
        mon_tuple = listeOfTuples[i]
        lang = mon_tuple[1]
        url = mon_tuple[2]
        path = mon_tuple[3]

        try:
            ####################
            # tri par langue
            ####################
            #  repertoire ou sera stocke le fichier html telecharge
            htmlfilepath = corpus_perso_directory+'langues/'+lang+'/html/'
            # si le repertoire n'existe pas, on le cree
            create_folder(htmlfilepath)

            # repertoire ou sera stocke le fichier text genere par l'outil teste
            textfilepath = corpus_perso_directory+'langues/'+lang+'/text/'
            # si le repertoire n'existe pas, on le cree
            create_folder(textfilepath)

            # on rajoute path qui correspond au nom du fichier (dans le json c'est l'attribut path)
            htmlfilepath+=path
            textfilepath+=path

            # on affiche l'url qui va etre traitee
            print 'url : '+ url


            ####################
            #  tri par nom de domaine
            ####################

            # on "determine le nom de domaine de l'url"
            domain = get_domains(url)
            # repertoire ou sera stocke le fichier html telecharge
            domainhtmlfilepath = corpus_perso_directory+'domains/'+domain+'/html/'
            # si le repertoire n'existe pas on le cree
            create_folder(domainhtmlfilepath)

            # repertoire ou sera stocke le fichier text genere par l'outil teste
            domaintextfilepath = corpus_perso_directory+'domains/'+domain+'/text/'
            create_folder(domaintextfilepath)

            # chemin ou seront stocke les fichiers
            domainhtmlfilepath+=path
            domaintextfilepath+=path

            # on cree aussi un repertoire dans lequel on met tous les html sans distinction de langue ou nom de domaine
            allhtmlfilepath = corpus_perso_directory+'all/html/'
            create_folder(allhtmlfilepath)

            # on cree aussi un repertoire dans lequel on met tous les text sans distinction de langue ou nom de domaine
            alltextfilepath = corpus_perso_directory+'all/text/'
            create_folder(alltextfilepath)


            allhtmlfilepath+=path
            alltextfilepath+=path

            # on fait la requete et si le status est 200, on poursuit le traitement
            response = requests.get(url)
            if response.status_code == 200:
                webContent = response.content
                webContent = webContentToText(webContent,tool,url)
            else:
                print exception_url + url

            webContentBoilerPipe = webContentToText(webContent,'boilerpipe',url)

            # on sauvegarde tous les fichers au bon endroit (dans all + tri par langue + tri par domaine)
            save_file(htmlfilepath,webContent)
            save_file(textfilepath,webContent)

            save_file(domainhtmlfilepath,webContent)
            save_file(domaintextfilepath,webContent)

            save_file(allhtmlfilepath,webContent)
            save_file(alltextfilepath,webContent)

            gold=''

            goldPath=corpus_daniel_directory+lang+'/gold/'+path
            f = open(goldPath, 'r')
            gold = f.read()
            f.close()

            res = evaluation_extrinseque(gold, webContent)
            res2 = evaluation_extrinseque(gold,webContentBoilerPipe)

            html_eval += '<tr><td>' + path + '</td><td>' + lang + '</td><td>' + domain + '</td><td>' + res[0]
            html_eval += '</td><td>' + res[1] + '</td><td>'+res[1]+'</td></tr>'

        except Exception as ex:
            print str(ex) + ' ' + url
        i+=1
    html_eval+='</table></body></html>'
    create_folder('./resultats/evaluation_extrinseque/')
    save_file('./resultats/evaluation_extrinseque/out.html', html_eval)

# permet de faire l'evaluation de l'efficacite de l'outil
def evaluation():
    p = os.popen('python cleaneval.py ./corpus_daniel/files/ ./corpus_perso/all/text/').read()
    create_folder('./resultats/'+'out.txt')
    save_file('./resultats/out.txt',p)




#Evalutaion par nom de domaine : on note que cleaneval ne gere pas les cas où il y a des divisions par 0
def evaluation_domaines():
    listeOfMyOutput = []
    listeOfVtOutput = []

    path = corpus_perso_directory+'domains/'
    domaines = list_directories(path)

    for domaine in domaines:
        dom = path+domaine
        listeOfMyOutput.append(dom)

    path = './corpus_daniel/domains/'
    domaines = list_directories(path)

    for domaine in domaines:
        dom = './corpus_daniel/domains/'+domaine+'/'
        listeOfVtOutput.append(dom)

    i = 0

    for langue in listeOfMyOutput:
        command_line = 'python cleaneval.py '+listeOfVtOutput[i] + ' '+listeOfMyOutput[i]
        command_line_t = 'python cleaneval.py -t '+listeOfVtOutput[i] + ' '+listeOfMyOutput[i]

        print command_line

        p = os.popen(command_line).read()
        p_t = os.popen(command_line_t).read()

        file_domaine = domaines[i]

        # on ecrit les resultats dans un dossier resultat / langue ....
        create_folder('./resultats/domains/'+file_domaine)

        fichier_resultat_detaille = './resultats/domains/'+file_domaine+'/out.txt'
        save_file(fichier_resultat_detaille,p)
        from_text_to_html_tab(fichier_resultat_detaille)

        # il y a aussi un fichier "global" contenant une seule ligne
        fichier_resultat_global = './resultats/domains/'+file_domaine+'/global_out.txt'
        save_file(fichier_resultat_global,p_t)
        from_text_to_html_tab(fichier_resultat_global)
        i+=1

# permet de faire l'evalution de l'efficacite de l'outil par langue
def evaluation_par_langue_global():

    listeOfMyOutput = []
    listeOfVtOutput = []

    path = './'+corpus_perso_directory+'langues/'
    langues = list_directories(path)

    for lng in langues:
        pth = path+lng+'/text'
        listeOfMyOutput.append(pth)

    path = './corpus_daniel/corpus_multi/'
    langues = list_directories(path)

    for lng in langues:
        pth = './corpus_daniel/corpus_multi/'+lng+'/gold'
        listeOfVtOutput.append(pth)

    lang = ("en", "el", "pl", "cn", "ru")

    i = 0

    for langue in listeOfMyOutput:
        command_line = 'python cleaneval.py '+listeOfVtOutput[i+1] + ' '+listeOfMyOutput[i]
        command_line_t = 'python cleaneval.py -t '+listeOfVtOutput[i+1] + ' '+listeOfMyOutput[i]

        p = os.popen(command_line).read()
        p_t = os.popen(command_line_t).read()
        file_language = lang[i]

        # on ecrit les resultats dans un dossier resultat / langue ....
        create_folder('./resultats/langues/'+file_language)

        fichier_resultat_detaille = './resultats/langues/'+file_language+'/out.txt'
        save_file(fichier_resultat_detaille,p)
        from_text_to_html_tab(fichier_resultat_detaille)

        # il y a aussi un fichier "global" contenant une seule ligne
        fichier_resultat_global = './resultats/langues/'+file_language+'/global_out.txt'
        save_file(fichier_resultat_global,p_t)
        from_text_to_html_tab(fichier_resultat_global)

        i+=1

# transforme le fichier de resultat passe en parametre en tableau html
def from_text_to_html_tab(text_path):

    ma_liste = []
    with open(text_path) as fp:
        for line in fp:
            #print line
            ma_liste.append(line)

    str = '<!DOCTYPE html> <html> <head> <title> Resultat global </title> </head> <body>'
    str+= '<table><tr>'
    i=0
    for raw in ma_liste:
        if i == 0:
            raw = raw.split( )
            str+='<tr>'
            for r in raw:
                str+='<th>'+r+'</th>'
            str+='</tr>'
            i = 1
        else:
            raw = raw.split( )
            str+='<tr>'
            for r in raw:
                str+='<td style="border: solid 1px;">'+r+'</td>'
            str+='</tr>'

    str+='</table></body></html>'

    fichier_html = text_path+'.html'
    f = open(fichier_html, 'w')
    f.write(str)
    f.close


# effectue l'evaluation extrinseque
def evaluation_extrinseque(gold, vt):
#     goldRes = test_api.get_diagnosis(gold)
#     vtRes = test_api.get_diagnosis(gold)
    goldRes=test_api_random()
    vtRes=test_api_random()
    print goldRes, vtRes
    return goldRes,vtRes

# Simule le comportement de api_test
def test_api_random():
    diagnosis = ""
    random_number = random.random()
    print(random_number)
    if(random_number < 0.5):
        diagnosis = "Relevant"
    else:
        diagnosis = "Irrelevant"

    return diagnosis



def sort_vt_by_domain(listeOfTuple):
    #on lit le json
    #on regarde chaque objet
    #on regade la valeur de path
    #on regarde le nom de domaine
    #on la place dans un dossier correspond
    # tuple = lang url path
    for value in listeOfTuples:

        domain = get_domains(str(value[2]))


        path = './corpus_daniel/domains/'+domain
        create_folder(path)


        cmd = "cp "+corpus_daniel_directory+"all/gold/"+str(value[3])+' ' +path +"/"

        print(cmd)
        p = os.popen(cmd).read()

def evaluation_par_domain():
    pass

#############################################################
# APPEL DES FONCTIONS DANS L'ORDRE
#############################################################

# lire le fichier json
jsonFile = read_json('./corpus_daniel/daniel.json')

#creer les tuples
listeOfTuples = create_listeOfTuple(jsonFile)

# transformer en txt avec tri par langue + tri par nom de domaine
get_html_file(listeOfTuples, 'justText')
# get_html_file(listeOfTuples, 'html2text')
# get_html_file(listeOfTuples, 'boilerpipe')


# lance l'evaluation globale
evaluation()
evaluation_par_langue_global()
from_text_to_html_tab()

#evaluation par nom de domaine
sort_vt_by_domain(listeOfTuples)
evaluation_domaines()
