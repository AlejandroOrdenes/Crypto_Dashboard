import json
import requests
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .models import Portfolio

from django.http import JsonResponse


# Create your views here.
def home(request):
    return render(request, "home.html")


def logIn(request):
    if request.method == "GET":
        return render(request, "login.html")
    else:
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)
        if user is None:
            return render(
                request, "logIn.html", {"error": "Username or password are incorrect!!"}
            )
        else:
            login(request, user)
            return redirect("dashboard")


def signIn(request):
    if request.method == "GET":
        return render(request, "signIn.html")
    else:
        username = request.POST.get("username")
        pass1 = request.POST.get("password")
        pass2 = request.POST.get("repeatPassword")

        if username == "" or pass1 == "" or pass2 == "":
            return render(request, "signIn.html", {"error": "Enter all info!!"})

        if pass1 == pass2:
            try:
                user = User.objects.create_user(
                    username=username,
                    password=pass1,
                )
                user.save()
                login(request, user)
                return redirect("dashboard")
            except IntegrityError as err:
                print(err)
                return render(
                    request, "signIn.html", {"error": "Username already exist"}
                )
        return render(request, "signIn.html", {"error": "The passwords do not match!"})


def signout(request):
    logout(request)
    return redirect("logIn")


def dashboardCrypto(request):
    if request.method == "GET":
        # Hacemos una petición GET a la API de coingecko
        response = requests.get(
            "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=99999999&page=1&sparkline=false"
        )

        # Si la petición fue exitosa, devolvemos los datos en formato JSON
        if response.status_code == 200:
            cryptos = response.json()
            return render(request, "dashboard.html", {"data": cryptos})
        else:
            # Si la petición no fue exitosa, devolvemos un mensaje de error
            return JsonResponse(
                {"error": "Error to get data"}, status=response.status_code
            )
    else:
        # Si la petición no fue exitosa, devolvemos un mensaje de error
        return JsonResponse({"error": "Error to get data"}, status=response.status_code)


def portfolio(request):
    userId = request.user.id
    portafolios = getPortafolioByUserId(userId)
    print(portafolios)
    if not portafolios.exists():
        print("vacio")
        return render(request, "portfolio.html", {"error": "You Dont have Portfolios!"})
    else:
        return render(request, "portfolio.html", {"data": portafolios})


def newPortfolio(request):
    if request.method == "GET":
        return render(request, "portfolio.html")
    else:
        portfolioName = request.POST.get("portfolioName")
        userId = request.user.id
        print("Creando nuevo portfolio!!!")
        nuevoPortfolio = Portfolio(user=request.user, name=portfolioName)
        nuevoPortfolio.save()

        portafolios = getPortafolioByUserId(userId)
        print(portafolios)
        return render(request, "portfolio.html", {"data": portafolios})


def deletePortfolio(request, portfolioId):
    portById = Portfolio.objects.get(id=portfolioId)
    userId = request.user.id
    print("Eliminando portfolio!!!")
    print(portById)
    portById.delete()

    portafolios = getPortafolioByUserId(userId)
    if not portafolios.exists():
        print("vacio")
        return render(request, "portfolio.html", {"error": "You Dont have Portfolios!"})
    else:
        return render(request, "portfolio.html", {"data": portafolios})


def getPortafolioByUserId(userId):
    portafolio = Portfolio.objects.filter(user_id=userId)
    return portafolio


def getPortfolioById(portfolioId):
    portafolio = Portfolio.objects.get(id=portfolioId)
    return portafolio


def createTable(request, portfolioId):
    response = requests.get(
        "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=999999&page=1&sparkline=false"
    )

    portfolio = getPortafolioByUserId(request.user.id)
    portafolio = Portfolio.objects.filter(id=portfolioId)
    porta = Portfolio.objects.get(id=portfolioId)

    print(portafolio)
    json_string = json.dumps(porta.cryptoIds)
    json_data = json.loads(json_string)
    data = []
    print(json_data)
    if response.status_code == 200:
        cryptos = response.json()
        if json_data == None:
            json_data = []
        for d in json_data:
            for c in cryptos:
                if c["id"] == d:
                    data.append(c)
                else:
                    continue
        return render(
                        request,
                        "portfolio.html",
                        {
                            "portfolios": portafolio,
                            "data": portfolio,
                            "data2": data,
                        },
                    )
    return render(
        request,
        "portfolio.html",
        {"portfolios": portafolio, "data": portfolio, "data2": json_data},
    )


def searchOnModal(request):
    response = requests.get(
        "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=999999&page=1&sparkline=false"
    )
    if response.status_code == 200:
        cryptos = response.json()
        return JsonResponse(cryptos, safe=False)
    else:
        pass


def searchCrypto(request):
    dataCrypto = request.POST.get("searchCripto")
    response = requests.get(
        "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=999999&page=1&sparkline=false"
    )

    response2 = requests.get(
        f"https://api.coingecko.com/api/v3/search?query={dataCrypto}"
    )
    cryptos_found = []
    if dataCrypto == "":
        return render(request, "dashboard.html", {"error": "Not data found!"})
    else:
        # Si la petición fue exitosa, devolvemos los datos en formato JSON
        if response2.status_code == 200 and response.status_code == 200:
            cryptos = response.json()
            cryptos2 = response2.json()

            for id in cryptos2["coins"]:
                for id2 in cryptos:
                    if id["symbol"].lower() == id2["symbol"].lower():
                        cryptos_found.append(id2)

            if cryptos_found == []:
                return render(request, "dashboard.html", {"error": "Not data found!"})
            return render(request, "dashboard.html", {"data": cryptos_found})

        else:
            # Si la petición no fue exitosa, devolvemos un mensaje de error
            return JsonResponse(
                {"error": "Error to get data"}, status=response.status_code
            )


def addCrypto(request, portfolioId, cryptoId):
    portfolio = getPortfolioById(portfolioId)
    response = requests.get(
        "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=999999&page=1&sparkline=false"
    )
    if response.status_code == 200:
        cryptos = response.json()

        for c in cryptos:
            if c["id"] == cryptoId:
                print("Se econtro")
                print(c)
                cryptoInPortfolio = portfolio.cryptoIds
                if cryptoInPortfolio is None:
                    print("Is none!!")
                    cryptoInPortfolio = []
                    cryptoInPortfolio.append(cryptoId)
                    portfolio.cryptoIds = cryptoInPortfolio
                    portfolio.save()
                    break
                exist = False
                for i in cryptoInPortfolio:
                    if i == cryptoId:
                        print("ya existe!!")
                        exist = True
                        break
                if exist == False:
                    cryptoInPortfolio.append(cryptoId)
                    portfolio.cryptoIds = cryptoInPortfolio
                    portfolio.save()
                    print(cryptoInPortfolio)

            else:
                print("ERROR AL GUARDAR CRYPTO ID")

    else:
        return JsonResponse({"error": "Error to get data"}, status=response.status_code)
    return render(request, "dashboard.html")

def deleteCrypto(request, portfolioId, cryptoId ):
    portfolio = getPortfolioById(portfolioId)
    json_string = json.dumps(portfolio.cryptoIds)
    json_data = json.loads(json_string)
    print("delete coin!!")
    print(portfolioId)
    
    for d in json_data:
        if cryptoId == d:
            print(d)
            index = json_data.index(d)
            portfolio.deleteCoin(index)
            
    return createTable(request, portfolioId)
    