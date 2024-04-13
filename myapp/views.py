from django.shortcuts import redirect, render

from .forms import ExpenseForm
from .models import Expense


# Create your views here.
def index(request):
    form = ExpenseForm()
    if request.method == "POST":
        form = ExpenseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("index")

    expenses = Expense.objects.all()
    context = {"form": form, "expenses": expenses}
    return render(request, "myapp/index.html", context)


def edit(request, pk=None):
    expense = Expense.objects.get(pk=pk)
    if request.method == "POST":
        form = ExpenseForm(request.POST, instance=expense)
        if form.is_valid():
            form.save()
            return redirect("index")
        return render(request, "myapp/edit.html", {"form": form})

    form = ExpenseForm(instance=expense)
    return render(request, "myapp/edit.html", {"form": form})


def delete(request, pk=None):
    if request.method == "POST":
        expense = Expense.objects.get(pk=pk)
        expense.delete()
    return redirect("index")
