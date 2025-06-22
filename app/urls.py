from django.urls import path
from app.views import HomeView,AgentView,CustomerView,SearchView

urlpatterns = [
    path('', HomeView.as_view(), name="home"),
    # agent page
    path("agent/", AgentView.as_view(), name="agentpage"),
    path("agent/<int:agent_id>/", AgentView.as_view(), name='agentview'),

    # customer page
    path("customer/", CustomerView.as_view(), name="customerpage"),
    path("customer/<int:customer_id>", CustomerView.as_view(), name="customerview"),
    # search 
    path("q/", SearchView.as_view(), name='search'),
]
