from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, FormView
from .models import Animal, Adoption
from django.db.models import Q
from .forms import AdoptionForm
from django.http import HttpResponse


class AnimalListView(ListView):
    model = Animal
    template_name = "animal_list.html"
    context_object_name = "animals"

    def get_queryset(self):
        queryset = Animal.objects.filter(enabled=True)

        # Filter by search query
        search_query = self.request.GET.get("search_term", "")
        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query)
                | Q(breed__icontains=search_query)
                | Q(species__icontains=search_query)
                | Q(age__icontains=search_query)
                | Q(health_history__icontains=search_query),
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Include the search query in the context
        context["search_query"] = self.request.GET.get("search_term", "")
        return context


class AdoptionRequestView(FormView):
    template_name = 'adoption_form.html' 
    form_class = AdoptionForm

    def form_valid(self, form):
        
        animal_id = self.kwargs['animal_id']
        animal = get_object_or_404(Animal, id=animal_id)

        
        adoption = form.save(commit=False)
        adoption.animal = animal  
        adoption.save()  

        return HttpResponse("Adoção solicitada com sucesso! Aguardando aprovação.")

    def get_context_data(self, **kwargs):
        
        context = super().get_context_data(**kwargs)
        animal_id = self.kwargs['animal_id']
        animal = get_object_or_404(Animal, id=animal_id)
        context['animal'] = animal
        return context