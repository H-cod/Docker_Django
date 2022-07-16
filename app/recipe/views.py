import os
from email.mime.image import MIMEImage

from django.views.generic import TemplateView
from django.shortcuts import render
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings

from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Tag, Ingredient, Recipe
from recipe.serializers import (TagSerializer, IngredientSerializer,
                                RecipeSerializer, RecipeDetailSerializer)


class BaseRecipeAttrViewSet(viewsets.GenericViewSet,
                            mixins.ListModelMixin,
                            mixins.CreateModelMixin):

    """Base view-set for user owned recipe attributes"""

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """ Returns objects or the current authenticated objects only"""
        return self.queryset.filter(user=self.request.user).order_by('-name')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class TagViewSet(BaseRecipeAttrViewSet):
    """Manage tags in the database """

    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngredientViewSet(BaseRecipeAttrViewSet):
    """List of Ingredients """

    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer


class MyTemplateView(TemplateView):
    template_name = 'emails/first_email.html'

    def logo_data(self, image_name):

        with open(os.path.join(settings.STATIC_ROOT, f'images/{image_name}'),
                  'rb') as f:
            logo_data = f.read()
        logo = MIMEImage(logo_data)
        logo.add_header('Content-ID', f'<{image_name}>')
        logo.add_header('Content-Disposition', 'inline',
                        filename=image_name)
        return logo

    def css_handler(self, file):
        with open(f'{file}', 'rb') as f:
            file_data = f.read()
        # file_data.add_header('Content-ID', f'<{file_data}>')
        # file_data.add_header('Content-Disposition', 'inline',
        #                 filename=file_data)

        return file_data

    def get(self, request):
        html_message = render_to_string(self.template_name)
        email_messages = \
            EmailMultiAlternatives(subject="TestSubject",
                                   body="body on body",
                                   from_email='Nersesyan@email.com',
                                   to=['hayknersesyanaj@gmail.com',
                                        'aroavetisyan5@gmail.com',
                                        'zhora.karyan.01@gmail.com',
                                        'vahagndavtyan96@gmail.com'])
        email_messages.attach_alternative(html_message, 'text/html')
        email_messages.mixed_subtype = 'related'
        for image in os.listdir(os.path.join(settings.STATIC_ROOT, 'images')):
            email_messages.attach(self.logo_data(image))
        email_messages.attach('Content-id',
                              self.css_handler(os.path.join(settings.BASE_DIR,
                                               'static/css/email.css')
                                               )
                              )
        email_messages.send(fail_silently=False)
        # send_mail('Subject', 'Working for template',
        #           'from@mail.com', ['hayknersesyanaj@gmail.com',
        #                             'aroavetisyan5@gmail.com',
        #                             'zhora.karyan.01@gmail.com',
        #                             'vahagndavtyan96@gmail.com'],
        #           fail_silently=True,
        #           html_message=html_message
        #           )

        return render(request, self.template_name)


class RecipeViewSet(viewsets.ModelViewSet):
    """Manage recipes in the database"""

    serializer_class = RecipeSerializer
    queryset = Recipe.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """Retrieve recipes for authenticated user"""

        return self.queryset.filter(user=self.request.user)

    def get_serializer_class(self):
        """Return appropriate serializer class"""
        if self.action == "retrieve":
            return RecipeDetailSerializer

        return self.serializer_class
