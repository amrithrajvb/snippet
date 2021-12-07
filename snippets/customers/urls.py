from django.urls import path
from customers import views

urlpatterns=[
    path("users/accounts/signup", views.UserCreationView.as_view()),
    path("users/accounts/signin", views.SignInView.as_view()),
    path("users/adding/title", views.AddingSnippetTitleView.as_view()),
    path("users/adding/description",views.AddingSnippetDescriptionView.as_view()),
    path("users/adding/title/<int:id>",views.SnippetTitleDetailsView.as_view()),
    path("users/adding/description/<int:id>",views.SnippetDescriptionDetailView.as_view())
]