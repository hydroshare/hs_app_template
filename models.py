from django.contrib.contenttypes import generic
from django.contrib.auth.models import User, Group
from django.db import models
from mezzanine.pages.models import Page, RichText
from mezzanine.core.models import Ownable
from hs_core.models import AbstractResource, resource_processor
from .forms import InputForm
from mezzanine.pages.page_processors import processor_for
#
# To create a new resource, use these three super-classes. 
#

class InstResource(Page, RichText, AbstractResource):
    class Meta:
        verbose_name = 'REHESsys Instance Resource'
    name = models.CharField(max_length=50)
    git_repo = models.URLField()
    git_username = models.CharField(max_length=50)
    # later change it to use Jeff's password encode function with django SECRET_KEY
    git_password = models.CharField(max_length=50)
    commit_id = models.CharField(max_length=50)
    model_desc = models.CharField(max_length=500)
    git_branch = models.CharField(max_length=50)
    study_area_bbox = models.CharField(max_length = 50)
    model_command_line_parameters = models.CharField(max_length=50)

    def can_add(self, request):
        return AbstractResource.can_add(self, request)

    def can_change(self, request):
        return AbstractResource.can_change(self, request)

    def can_delete(self, request):
        return AbstractResource.can_delete(self, request)

    def can_view(self, request):
        return AbstractResource.can_view(self, request)


processor_for(InstResource)(resource_processor)

@processor_for(InstResource)
def main_page(request, page):
    if(request.method == 'POST'):
        form = InputForm(request.POST)
        if(form.is_valid()):
            content_model = page.get_content_model()
            content_model.name=form.cleaned_data['name']
            content_model.model_desc = form.cleaned_data['model_desc']
            content_model.study_area_bbox = form.cleaned_data['study_area_bbox']
            content_model.git_repo = form.cleaned_data['git_repo']
            content_model.git_username = form.cleaned_data['git_username']
            content_model.git_password = form.cleaned_data['git_password']
            content_model.commit_id = form.cleaned_data['commit_id']
            content_model.git_branch = form.cleaned_data['git_branch']
            content_model.model_command_line_parameters = form.cleaned_data['model_command_line_parameters']
            content_model.save()
    else:
        form = InputForm()

    return  {'form': form}