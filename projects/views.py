from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Project,Tag
from .forms import ProjectForm, ReviewForm
from django.contrib import messages
from .utils import searchProjects,paginateProjects
from .models import Project, Review


def projects(request):

    projects, search_query = searchProjects(request)
    custom_range,projects =  paginateProjects(request,projects,6)



    context = {'projects': projects, 'search_query': search_query, 'custom_range': custom_range}
    return render(request, 'projects/projects.html', context)



def project(request,pk):
    projectObj = Project.objects.get(id=pk)
    form = ReviewForm()

    if request.method =='POST':
        form = ReviewForm(request.POST)
        review = form.save(commit=False)
        review.project = projectObj
        review.owner = request.user.profile
        review.save()

        

        messages.success(request, 'your review was successfully submitted')
        return redirect('project', pk=projectObj.id)


    
    return render(request, 'projects/single-projects.html',{'project':projectObj,'form':form})




@login_required(login_url="login")
def upvote_project(request, pk):
    project = Project.objects.get(id=pk)
    Review.upvote(project, request.user.profile)
    project.update_vote_count()  # Recalculate the vote count
    return redirect('project', pk=pk)



@login_required(login_url="login")
def createproject(request):
    profile = request.user.profile
    form = ProjectForm()

    if request.method =='POST':
        form = ProjectForm(request.POST,request.FILES)
        if form.is_valid():
            project = form.save(commit= False)
            project.owner =profile
            project.save()
            return redirect('account')

        

    context = {'form': form}
    return render(request,"projects/project_form.html",context)

@login_required(login_url="login")
def updateproject(request,pk):
    profile = request.user.profile
    project=profile.project_set.get(id=pk)
    form = ProjectForm(instance=project)

    if request.method =='POST':
        form = ProjectForm(request.POST,request.FILES,instance=project)
        if form.is_valid():
            form.save()
            return redirect('account')

        

    context = {'form': form}
    return render(request,"projects/project_form.html",context)

@login_required(login_url="login")
def deleteproject(request,pk):
    profile = request.user.profile
    project=profile.project_set.get(id=pk)
    if request.method =='POST':
        project.delete()
        return  redirect('account') 
    context={'object':project}
    return render(request, 'delete_template.html',context)