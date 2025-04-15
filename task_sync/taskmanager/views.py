from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from django.http import HttpResponseForbidden
from .models import Project, Task, Document, ProjectCollaborator
from .forms import SignUpForm, ProjectForm, TaskForm, DocumentForm, CollaboratorForm

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})

@login_required
def dashboard(request):
    user_projects = Project.objects.filter(
        Q(created_by=request.user) |
        Q(collaborators__user=request.user)
    ).distinct()
    user_tasks = Task.objects.filter(assignee=request.user)

    context = {
        'user_projects': user_projects,
        'user_tasks': user_tasks,
    }
    return render(request, 'taskmanager/dashboard.html', context)

@login_required
def project_list(request):
    projects = Project.objects.filter(
        Q(created_by=request.user) |
        Q(collaborators__user=request.user)
    ).distinct()
    return render(request, 'taskmanager/project_list.html', {'projects': projects})

@login_required
def project_create(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.created_by = request.user
            project.save()
            return redirect('project_detail', pk=project.pk)
    else:
        form = ProjectForm()
    return render(request, 'taskmanager/project_form.html', {'form': form})

def has_project_permission(user, project, required_permission=None):
    # Project creator has all permissions
    if project.created_by == user:
        return True

    # Check collaborator permissions
    try:
        collaborator = ProjectCollaborator.objects.get(project=project, user=user)
        if required_permission:
            if required_permission == 'admin' and collaborator.permission == 'admin':
                return True
            elif required_permission == 'editor' and collaborator.permission in ['editor', 'admin']:
                return True
            elif required_permission == 'viewer':
                return True
            return False
        return True
    except ProjectCollaborator.DoesNotExist:
        pass

    # Give editor permission to task assignees
    if required_permission in ['editor', 'viewer'] and Task.objects.filter(project=project, assignee=user).exists():
        return True

    return False

@login_required
def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk)

    if not has_project_permission(request.user, project):
        return HttpResponseForbidden("You don't have access to this project.")

    tasks = project.tasks.all()
    documents = project.documents.all()

    task_counts = {
        'todo': tasks.filter(status='todo').count(),
        'in_progress': tasks.filter(status='in_progress').count(),
        'review': tasks.filter(status='review').count(),
        'done': tasks.filter(status='done').count(),
    }

    context = {
        'project': project,
        'tasks': tasks,
        'documents': documents,
        'task_counts': task_counts,
        'can_edit': has_project_permission(request.user, project, 'editor'),
        'is_admin': has_project_permission(request.user, project, 'admin'),
    }
    return render(request, 'taskmanager/project_detail.html', context)

@login_required
def task_create(request, project_id):
    project = get_object_or_404(Project, id=project_id)

    if not has_project_permission(request.user, project, 'editor'):
        return HttpResponseForbidden("You don't have permission to create tasks.")

    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.project = project
            task.assigned_by = request.user
            task.save()
            return redirect('project_detail', pk=project.id)
    else:
        form = TaskForm()

    return render(request, 'taskmanager/task_form.html', {'form': form, 'project': project})

@login_required
def task_update(request, pk):
    task = get_object_or_404(Task, pk=pk)

    if not has_project_permission(request.user, task.project, 'editor'):
        return HttpResponseForbidden("You don't have permission to update this task.")

    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('project_detail', pk=task.project.id)
    else:
        form = TaskForm(instance=task)

    return render(request, 'taskmanager/task_form.html', {'form': form, 'project': task.project, 'task': task})

@login_required
def document_upload(request, project_id):
    project = get_object_or_404(Project, id=project_id)

    if not has_project_permission(request.user, project, 'editor'):
        return HttpResponseForbidden("You don't have permission to upload documents.")

    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            document = form.save(commit=False)
            document.project = project
            document.uploaded_by = request.user
            document.save()
            return redirect('project_detail', pk=project.id)
    else:
        form = DocumentForm()

    return render(request, 'taskmanager/document_form.html', {'form': form, 'project': project})

@login_required
def add_collaborator(request, project_id):
    project = get_object_or_404(Project, id=project_id)

    if not (project.created_by == request.user or
            has_project_permission(request.user, project, 'admin')):
        return HttpResponseForbidden("You don't have permission to manage collaborators.")

    if request.method == 'POST':
        form = CollaboratorForm(request.POST)
        if form.is_valid():
            collaborator = form.save(commit=False)
            collaborator.project = project
            # Check if collaboration already exists
            if not ProjectCollaborator.objects.filter(project=project, user=collaborator.user).exists():
                collaborator.save()
            return redirect('project_detail', pk=project.id)
    else:
        form = CollaboratorForm()

    return render(request, 'taskmanager/collaborator_form.html', {'form': form, 'project': project})

@login_required
def edit_collaborator(request, project_id, collaborator_id):
    project = get_object_or_404(Project, id=project_id)
    collaborator = get_object_or_404(ProjectCollaborator, id=collaborator_id, project=project)

    # Check if user has admin permission
    if not (project.created_by == request.user or
            has_project_permission(request.user, project, 'admin')):
        return HttpResponseForbidden("You don't have permission to edit collaborators.")

    if request.method == 'POST':
        form = CollaboratorForm(request.POST, instance=collaborator)
        if form.is_valid():
            form.save()
            return redirect('project_detail', pk=project.id)
    else:
        form = CollaboratorForm(instance=collaborator)

    return render(request, 'taskmanager/collaborator_form.html',
                 {'form': form, 'project': project, 'edit_mode': True})

def notifications_view(request):
    from .utils import get_due_today_notifications
    if request.user.is_authenticated:
        notifications = get_due_today_notifications(request.user)
        return render(request, 'taskmanager/notifications.html', {'notifications': notifications})
    return render(request, 'taskmanager/notifications.html', {'notifications': []})