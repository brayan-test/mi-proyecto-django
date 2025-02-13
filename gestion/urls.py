from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('ciclos/',views.listar_ciclos,name='listar_ciclos'),
    path('ciclos/crear',views.crear_ciclo,name='crear_ciclos'),
    path('ciclos/editar/<int:ciclo_id>',views.editar_ciclo,name='editar_ciclo'),
    path('ciclos/eliminar/<int:ciclo_id>',views.eliminar_ciclo,name='eliminar_ciclo'),
   
    path('aportes/',views.listar_aportes,name='listar_aportes'),
    path('aportes/crear',views.listar_aportes,name='listar_aportes'),

    path('',views.inicio,name='inicio'),

    #path('login/',auth_views.LoginView.as_view(),name='login'),
    path('login/',auth_views.LoginView.as_view(template_name = 'silva/login.html'),name='login'),
    path('logout/',auth_views.LoginView.as_view(template_name = 'gestion/logout.html'),name='logout'),
    #path('logout/',auth_views.LoginView.as_view(),name='logout'),

]
