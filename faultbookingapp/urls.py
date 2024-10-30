
from django.contrib import admin
from django.urls import path
from bookfault import views as v1

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', v1.loginhome),                            #homepage view
    path('home/', v1.home),                            #homepage view
    path('bookfault/', v1.OfcFaultView),          #OFC fault booking Page

    path('faultrestore/', v1.FaultRestoredView),  #Display Form for Fetch particular fault on the basis of id
    path('display/', v1.displayrec),              #Display particular fault Details of fetched faults on the basis of id
    path('displayall/', v1.displayallfaults),     #display all the faults present in database and you can download the excel
    path('displaydaily/', v1.displaydailyfaults), #Display daily fault record and download its excel
    path('displaymonthly/', v1.displaymonthlyfaults), #Display monthly record and you can download its excel
    path('displaynotrestored/', v1.displaynotrestored), #Display those records which fault is not restored, and you can download its excel
    path('update/<int:id>', v1.updaterec),        #Update record by the FRT team
    path('updateadmin/<int:id>', v1.updateadmin), #Update any record form the display tab by admin
    path('deletefault/<int:id>', v1.deletefault), #Delete any record from the database by the admin

    path('login/', v1.user_login, name='login'),
    path('logout/', v1.user_logout, name='logout'),
    path('register/', v1.register, name='register'),

]
