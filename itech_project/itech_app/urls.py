from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('KTL_create', views.create_KTL, name="Create program KTL"),
    path('PRO_create', views.create_PRO, name="Create program PRO"),
    path('pre_create', views.select_type, name="Pre Create Program"),
    path('edit/<int:idPRM>/', views.edit, name="Edit Program"),
    path('select', views.select_all_program, name="Select All Programs"),
    path('logs', views.show_log, name="Show Logs"),
    path('line_activity', views.show_production_activity, name="Show Line Activity"),
    path('show_pack_detail', views.show_pack_detail, name="Show pack detail"),
    path('edit_pack_detail/<int:NrPRM>/', views.edit_pack_detail, name="Edit pack detail"),
    path('delete_pack_detail/<int:NrPRM>/', views.delete_pack_detail, name="Delete pack detail"),
    path('add_pack_detail', views.add_pack_detail, name="Add pack detail record"),

]

urlpatterns += staticfiles_urlpatterns()