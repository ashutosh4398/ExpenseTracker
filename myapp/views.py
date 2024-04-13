import datetime
from django.shortcuts import redirect, render
from django.db.models import Sum

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
    # logic to calculate 365 days expenses
    get_date = lambda x: datetime.date.today() - datetime.timedelta(days=x)

    daily_sums = (
        Expense.objects.filter()
        .values("date_created__date")
        .order_by("date_created__date")
        .annotate(sum=Sum("amount"))
    )

    categorical_expenses = (
        Expense.objects
        .values("category")
        .order_by("category")
        .annotate(amount=Sum('amount'))
    )
    print(daily_sums)
    print(categorical_expenses)
    context = {
        "form": form,
        "expenses": expenses,
        "agg": expenses.aggregate(sum=Sum("amount")),
        "yearly_sum": expenses.filter(date_created__date__gte=get_date(365)).aggregate(
            sum=Sum("amount")
        )["sum"],
        "monthlys_sum": expenses.filter(date_created__date__gte=get_date(30)).aggregate(
            sum=Sum("amount")
        )["sum"],
        "weekly_sum": expenses.filter(date_created__date__gte=get_date(7)).aggregate(
            sum=Sum("amount")
        )["sum"],
    }
    print(context)
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
