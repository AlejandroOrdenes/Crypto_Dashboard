from django.urls import path
from . import views


urlpatterns = [
    path("", views.dashboardCrypto, name="dashboard"),
    path("logIn/", views.logIn, name="logIn"),
    path("signIn/", views.signIn, name="signIn"),
    path("signout/", views.signout, name="signout"),
    path("dashboard/", views.dashboardCrypto, name="dashboard"),
    path("portfolio/", views.portfolio, name="portfolio"),
    path("searchCrypto/", views.searchCrypto, name="search"),
    path("searchOnModal/", views.searchOnModal, name="searchOnModal"),
    path("newPortfolio/", views.newPortfolio, name="newPortfolio"),
    path("deletePortfolio/<int:portfolioId>", views.deletePortfolio, name='deletePortfolio'),
    path("portfolio/<int:portfolioId>", views.createTable, name='createTable'),
    path("addCrypto/<int:portfolioId>/<str:cryptoId>", views.addCrypto, name='addCrypto'),
    path("deleteCrypto/<int:portfolioId>/<str:cryptoId>", views.deleteCrypto, name='deleteCrypto'),
    path("addTransaction/<int:portfolioId>/<str:cryptoId>", views.addTransaction, name='addTransaction'),
]
