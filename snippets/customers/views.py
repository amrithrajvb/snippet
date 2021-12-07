from django.shortcuts import render

# Create your views here.

from customers.models import MyUser,SnippetTitle,SnippetSheetDetails
from customers.serializers import UserCreationSerializer,SignInSerializer,AddingSnippetTitleSerializer,AddingSnippetDescriptionsSerializer
from rest_framework import mixins,generics
from rest_framework.views import APIView
from django.contrib.auth import authenticate,login,logout
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status

class UserCreationView(generics.GenericAPIView,mixins.CreateModelMixin,mixins.ListModelMixin):
    model=MyUser
    serializer_class = UserCreationSerializer
    queryset = model.objects.all()

    def post(self,request,*args,**kwargs):
        print("created successfully")
        return self.create(request,*args,**kwargs)

    def get(self,request,*args,**kwargs):
        return self.list(request,*args,**kwargs)

class SignInView(APIView):
   serializer_class=SignInSerializer

   def post(self,request,*args,**kwargs):
       serializer=self.serializer_class(data=request.data)
       if serializer.is_valid():
           email=serializer.validated_data["email"]
           password=serializer.validated_data["password"]
           user=authenticate(request,email=email,password=password)
           if user:
               login(request, user)
               token, create = Token.objects.get_or_create(user=user)
               return Response({"token":token.key},status=status.HTTP_200_OK)
           else:
               return Response({"message":"Invalid User"},status=status.HTTP_400_BAD_REQUEST)
       else:
           return Response(serializer.errors)




class AddingSnippetTitleView(generics.GenericAPIView,mixins.CreateModelMixin
                             ,mixins.ListModelMixin):

    model=SnippetTitle
    serializer_class =AddingSnippetTitleSerializer
    queryset = model.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]


    def get(self,request,*args,**kwargs):
        queryset = self.model.objects.all()
        count = len(queryset)
        print(count)
        # if count:
        #     return Response({"count":count},status=status.HTTP_200_OK)

        return self.list(request,*args,**kwargs)

    def post(self,request,*args,**kwargs):
        serializer=self.serializer_class(data=request.data)
        if serializer.is_valid():
            title=serializer.validated_data["title"]
            checking=SnippetTitle.objects.filter(title=title)
            if checking:
                return Response({"message":"snippet title with this title already exists"},status=status.HTTP_400_BAD_REQUEST)
            else:
                return self.create(request,*args,**kwargs)
        else:
            return Response(serializer.errors)






class SnippetTitleDetailsView(generics.GenericAPIView,mixins.RetrieveModelMixin,
                          mixins.UpdateModelMixin,mixins.DestroyModelMixin):
    model = SnippetTitle
    serializer_class = AddingSnippetTitleSerializer
    queryset = model.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    lookup_field = "id"

    def get(self, request, *args, **kwargs):
        queryset = self.model.objects.all()
        count = len(queryset)
        print(count)
        if request.user.is_authenticated:
            return self.retrieve(request, *args, **kwargs)
        else:
            return Response({"message": "user must login"}, status=status.HTTP_400_BAD_REQUEST)

    def put(self,request, *args, **kwargs):
        if request.user.is_authenticated:
            return self.update(request, *args, **kwargs)
        else:
            return Response({"message": "user must login"}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request,*args,**kwargs):
        return self.destroy(request,*args,**kwargs)





class AddingSnippetDescriptionView(generics.GenericAPIView,mixins.CreateModelMixin
                               ,mixins.ListModelMixin):

    model=SnippetSheetDetails
    serializer_class=AddingSnippetDescriptionsSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = model.objects.all()

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(user=user)

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return self.create(request, *args, **kwargs)
        else:
            return Response({"msg": "user must login"}, status=status.HTTP_400_BAD_REQUEST)

    def get(self,request,*args,**kwargs):
        if request.user.is_authenticated:
            return self.list(request,*args,**kwargs)
        else:
            return Response({"message":"user must login"},status=status.HTTP_400_BAD_REQUEST)


class SnippetDescriptionDetailView(generics.GenericAPIView,mixins.RetrieveModelMixin,
                          mixins.UpdateModelMixin,mixins.DestroyModelMixin):
    model = SnippetSheetDetails
    serializer_class = AddingSnippetDescriptionsSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = model.objects.all()

    lookup_field = "id"

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return self.retrieve(request, *args, **kwargs)
        else:
            return Response({"message": "user must login"}, status=status.HTTP_400_BAD_REQUEST)

    def put(self,request, *args, **kwargs):
        if request.user.is_authenticated:
            return self.update(request, *args, **kwargs)
        else:
            return Response({"message": "user must login"}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request,*args,**kwargs):
        return self.destroy(request,*args,**kwargs)







