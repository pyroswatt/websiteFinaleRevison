#-*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.shortcuts import redirect, render
from datetime import datetime
import MySQLdb
from blog.models import *
import json
import time
from .forms import LampeForm, SpectrophotometerForm
from datetime import datetime, timedelta
from django.db import connection,transaction


PERIODE_MONITORING = 'jour'

class user:
    def __init__(self):
        self.login = ''
        self.password = ''
        self.equipment = []

def home(request):
    """ Exemple de page HTML, non valide pour que l'exemple soit concis """
    text = """<h1>Bienvenue sur mon blog !</h1>
              <p>Les crêpes bretonnes ça tue des mouettes en plein vol !</p>"""
    return HttpResponse(text)

def call_principe(request):
    return render(request, 'blog/principe.html')

def call_services(request):
    return render(request, 'blog/services.html')

def call_clients(request):
    return render(request, 'blog/clients.html')

def call_recordCredentialsUser(request):
    login = 'Identifiant non cohérent'
    pathHtml = 'blog/plateformeUser.html'
    if 'identifiant' in request.GET and 'password' in request.GET and 'confirmPassword' in request.GET and 'mail' in request.GET and request.GET['identifiant'] != '' :

        login = 'Identifiant erroné: réencoder vos données.'
        password = ''
        confirmPassword = ''
        mail = ''
        telemetryAddress = ''
        try:
            db = MySQLdb.connect(host="mysql-watersense.alwaysdata.net",  # your host, usually localhost
                                 user="146622",  # your username
                                 passwd="Android92",  # your password
                                 db="watersense_db")  # name of the data base
            cur = db.cursor()

            # Use all the SQL you like
            cur.execute("SELECT login FROM userCredentials where login like '%s' "%(request.GET['identifiant']))
            login = request.GET['identifiant']
            password = request.GET['password']
            # print all the first cell of all the rows

            for row in cur.fetchall():
                login = row[0]
            if cur.rowcount ==0:
                login = "Bonjour %s , connexion acceptée"%login
                if (request.GET['password'] == request.GET['confirmPassword']) and request.GET['mail'] != '' and request.GET['telemetryAddress'] != '':
                    #Password match
                    login = 'Compte créé avec succès !'
                    cur.execute("INSERT INTO userCredentials(login, password, mail, devAddress) VALUES ('%s','%s','%s','%s')" % (
                        request.GET['identifiant'], request.GET['password'], request.GET['mail'], request.GET['telemetryAddress']))
                    # force INSERT || UPDATE records into database
                    db.commit()
                    pathHtml = 'blog/plateforme.html'
                    request.session['login'] = request.GET['identifiant']
                else:
                    login = "Champ non-conforme (mot de passe non identique et/ou un champ est vide."
            else:
                login = 'Identifiant existant déjà !'
                pathHtml = 'blog/plateformeUser.html'
        except Exception as e:
            print("Exception raised: %s"%str(e))
        finally:
            db.close()
    return render(request, pathHtml, {'user':login})

def call_plateformeUserRecord(request):
    pathHtml = 'blog/plateformeUser.html'
    return render(request, pathHtml)

def call_fillChart(request):
    '''
    Add devAddress --to retrieve data
    :param request:
    :return:
    '''
    periode = request.session.get("periodeMonitoring")
    equipment = request.session.get('items')
    dataa ={}
    data = {'dates': [], 'stateLampe': [], 'temperatureTesteur': [], 'temperatureLampe': [], 'stateLampe': [], 'pH': [], 'NO2': [], 'NO3': [] }
    query = ""


    if periode == 'jour':
        periodeAnalysis = datetime.now() - timedelta(days=1)
    elif periode == 'semaine':
        periodeAnalysis = datetime.now() - timedelta(days=7)
    else:
        periodeAnalysis = datetime.now() - timedelta(days=31)

    if equipment == 'lampe':
        query = "SELECT stateLampe, temperatureTesteur, temperatureLampe, TimeStamp FROM dataLora where TimeStamp > '%s'"%(str(periodeAnalysis.strftime('%Y-%m-%d %H:%M:%S')))
    elif equipment == 'spectrophotomètre':
        query = "SELECT pH, NO2, NO3, TimeStamp FROM dataLora where TimeStamp > '%s'" % (str(periodeAnalysis.strftime('%Y-%m-%d %H:%M:%S')))

    try:
        db = MySQLdb.connect(host="mysql-watersense.alwaysdata.net",  # your host, usually localhost
                             user="146622",  # your username
                             passwd="Android92",  # your password
                             db="watersense_db")  # name of the data base
        cur = db.cursor()
        #2017-12-12 12:00:00.strftime()
        cur.execute(query)
        if cur.rowcount != 0:
            for row in cur.fetchall():
                try:
                    if equipment == 'spectrophotomètre':
                        data['pH'].append(int(row[0]))
                        data['NO2'].append(int(row[1]))
                        data['NO3'].append(int(row[2]))
                        #print('spectro')
                    elif equipment == 'lampe':
                        data['stateLampe'].append(int(row[0]))
                        data['temperatureTesteur'].append(int(row[1]))
                        data['temperatureLampe'].append(int(row[2]))
                        #print('lampe')
                    data['dates'].append(str(row[-1]))
                except Exception as e:
                    pass

                #print("DEBUG " + str(row[0]))
    except Exception as e:
        print("Exception raised: %s" % str(e))
    finally:
        db.close()

    dataa['chart_data'] = data
    return HttpResponse(json.dumps(dataa), content_type = 'application/json' )


def call_plateforme(request):
    row =['test']
    login = ''
    pathHtml = 'blog/plateforme.html'

    if 'identifiant' in request.GET and 'password' in request.GET:


        login = 'Identifiant erroné: réencoder vos données.'
        password = ''

        try:
            db = MySQLdb.connect(host="mysql-watersense.alwaysdata.net",  # your host, usually localhost
                                 user="146622",  # your username
                                 passwd="Android92",  # your password
                                 db="watersense_db")  # name of the data base
            cur = db.cursor()

            # Use all the SQL you like
            cur.execute("SELECT login,password FROM userCredentials where login like '%s' and password like '%s'"%(request.GET['identifiant'], request.GET['password']))
            login = request.GET['identifiant']
            password = request.GET['password']
            # print all the first cell of all the rows

            for row in cur.fetchall():
                login = row[0]
            if cur.rowcount !=0:
                login = "Bonjour %s , connexion acceptée"%login
                pathHtml = 'blog/configurationPlateforme.html'
                request.session['login'] = request.GET['identifiant']
            else:
                login = 'Identifiant et/ou mot de passe incorrectes'
                pathHtml = 'blog/plateforme.html'
        except Exception as e:
            print("Exception raised: %s"%str(e))
        finally:
            db.close()
    return render(request, pathHtml, {'user':login})

def call_configurationPlateforme(request):
    pathHtml = 'blog/configurationPlateforme.html'
    info = "Equipement en attente d'ajout"
    lstEqp =[]
    if request.GET['itemPlateforme'] != '0':
        try:
            db = MySQLdb.connect(host="mysql-watersense.alwaysdata.net",  # your host, usually localhost
                                 user="146622",  # your username
                                 passwd="Android92",  # your password
                                 db="watersense_db")  # name of the data base
            cur = db.cursor()
            cur.execute("SELECT equipment FROM equipment where user like '%s' and equipment like '%s'" % (
                request.session.get('login', None), request.GET['itemPlateforme']))
            if cur.rowcount == 0:
                info = 'Insertion %s effectué avec succès !'%(request.GET['itemPlateforme'])
                cur.execute("INSERT INTO equipment(user, equipment) VALUES ('%s','%s')"%(request.session.get('login', None), request.GET['itemPlateforme']))
                # force INSERT || UPDATE records into database
                db.commit()
            else:
                info = 'Equipement déjà ajouté !'

        except Exception as e:
            print("Exception raised: %s"%str(e))
        finally:
            db.close()

    return render(request, pathHtml, {'user':info})

def call_statusPlateforme(request):
    pathHtml = 'blog/statusPlateforme.html'
    return render(request, pathHtml)

def call_monitoringPlateforme(request):
    pathHtml = 'blog/statusPlateforme.html'
    lstEqp = []
    parameterTester = []
    #datetime.now().strftime('%Y-%m-%d %H:%M:%S')


    try:
        db = MySQLdb.connect(host="mysql-watersense.alwaysdata.net",  # your host, usually localhost
                             user="146622",  # your username
                             passwd="Android92",  # your password
                             db="watersense_db")  # name of the data base
        cur = db.cursor()
        cur.execute("SELECT parameter FROM parameterTester where tester like '%s' " % (
            request.GET['items']))


        if cur.rowcount != 0:
            for parameter in cur.fetchall():
                parameterTester.append(parameter)
                print(parameter)
        else:
            info = 'Aucun equipement ajouté !'

    except Exception as e:
        print("Exception raised: %s" % str(e))
    finally:
        db.close()

    try:
        db = MySQLdb.connect(host="mysql-watersense.alwaysdata.net",  # your host, usually localhost
                             user="146622",  # your username
                             passwd="Android92",  # your password
                             db="watersense_db")  # name of the data base
        cur = db.cursor()
        cur.execute("SELECT equipment FROM equipment where user like '%s' " % (
            request.session.get('login', None)))

        if cur.rowcount != 0:
            for eqp in cur.fetchall():
                lstEqp.append(eqp)
        else:
            info = 'Aucun equipement ajouté !'

    except Exception as e:
        print("Exception raised: %s" % str(e))
    finally:
        db.close()

    try:
        db = MySQLdb.connect(host="mysql-watersense.alwaysdata.net",  # your host, usually localhost
                             user="146622",  # your username
                             passwd="Android92",  # your password
                             db="watersense_db")  # name of the data base
        cur = db.cursor()
        cur.execute("SELECT DataBrut,DevAddress FROM dataLora ORDER BY  `dataLora`.`TimeStamp` DESC LIMIT 0 , 1 " )


        if cur.rowcount != 0:
            for row in cur.fetchall():
                print(row[0])


    except Exception as e:
        print("Exception raised: %s" % str(e))
    finally:
        db.close()

    if request.method == 'POST':
        if 'lampe' in lstEqp:
            form = LampeForm(request.POST)
        else:
            form = SpectrophotometerForm(request.POST)
    else:
        if 'lampe' in lstEqp:
            form = LampeForm()
        else:
            form = SpectrophotometerForm()
    request.session['periodeMonitoring'] = request.GET['periodeMonitoring']
    try:
        request.session['items'] = request.GET['items']
    except Exception as e:
        print(e)
    lstEqp = [str(x).strip("()',´") for x in lstEqp]
    parameterTester = [str(x).strip("()',´") for x in parameterTester]
    return render(request, pathHtml, {'temperature': row[0], 'user':'Sélectionner un appareil et la fréquence de mesure', 'temperatureUV':row[1], 'items':lstEqp, 'parameters':parameterTester, 'form': form})

def accueil(request):
    """ Afficher tous les articles de notre blog"""

    db = MySQLdb.connect(host="mysql-watersense.alwaysdata.net",  # your host, usually localhost
                         user="146622",  # your username
                         passwd="Android92",  # your password
                         db="watersense_db")  # name of the data base

    # you must create a Cursor object. It will let
    #  you execute all the queries you need
    cur = db.cursor()

    # Use all the SQL you like
    cur.execute("SELECT * FROM eventLora")

    # print all the first cell of all the rows
    for row in cur.fetchall():
        print
        row[0]

    db.close()
    return render(request, 'blog/Untitled.html', {'date': row[0]})
    #return render(request, 'blog/accueil.html', {'derniers_articles': articles})





def view_redirection(request):
    return HttpResponse("Vous avez été redirigé.")

def list_articles(request, year, month):
    # Il veut des articles ? Soyons fourbe et redirigeons-le vers djangoproject.com
    return redirect("https://www.djangoproject.com")

def date_actuelle(request):
    return render(request, 'blog/Date.html', {'date': datetime.now()})

def addition(request, nombre1, nombre2):
    total = int(nombre1) + int(nombre2)

    # Retourne nombre1, nombre2 et la somme des deux au tpl
    #{"total": 8, "nombre1": 5, "nombre2": 3, "request": <WSGIRequest ...>}
    #clé du dictionnaire = total, nb1, nb2 ... & valeur des clés sont la valeur des variables
    return render(request, 'blog/addition.html', locals())