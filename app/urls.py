from django.urls import path,include
from rest_framework.routers import DefaultRouter
from app import views

router=DefaultRouter()
router.register('signup',views.SignUpViewSet),
router.register('bus',views.Bus_ViewSet)
router.register('route',views.Route_ViewSet)
router.register('schedule',views.Schedule_ViewSet)
router.register('ticket',views.Ticket_ViewSet)



urlpatterns = [
    path('',include(router.urls) ),

]