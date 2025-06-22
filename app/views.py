from django.shortcuts import redirect, render
from django.views import View
from app.forms import UserRegistrationForm, CustomerRegistrationForm, AgentRegistrationForm
from django.contrib.auth.decorators import login_required
from app.models import AbstractUser, Cutomer
from django.utils.decorators import method_decorator
from django.db.models import Q
from django.db.models import Count
from django.contrib import messages
# Create your views here.


class SearchView(View):
    def get(self, request):
        context = {}
        search = request.GET.get('s', '').strip()
        user = AbstractUser.objects.filter(user=request.user)
        user_categories = " ".join([u.category for u in user])
        customer = Cutomer.objects.none()

        if user_categories == "agent":
            agent_instance = user.first()
            customer = Cutomer.objects.filter(agent=agent_instance)
        elif user_categories == "builder":
            customer = Cutomer.objects.all()

        if search:
            customer = customer.filter(
                Q(name__icontains=search) |
                Q(location__icontains=search) |
                Q(agent__user__username__icontains=search) |
                Q(property_type__icontains=search) |
                Q(status__icontains=search)
            )
            agent = user.filter(
                Q(user__username__icontains=search)
            )

            # Add customer_count as an extra field to each agent
            agent = agent.annotate(customer_count=Count('cutomer'))
            context["agent"] = agent

        context.update({
            "user_categories": user_categories,
            "customer": customer,
            "agent": agent
        })
        return render(request, 'searchpage.html', context)


@method_decorator(login_required, name='dispatch')
class HomeView(View):
    def get(self, request):
        context = {}
        CustomerForm = CustomerRegistrationForm()
        user = AbstractUser.objects.filter(user=request.user)
        user_categories = " ".join([u.category for u in user])

        if user_categories == "agent":
            agent_instance = user.first()  # get the first user instance
            customer = Cutomer.objects.filter(agent=agent_instance)
            context["customer"] = customer
        else:
            customer = Cutomer.objects.all()
            agents = AbstractUser.objects.filter(
                category="agent"
            ).annotate(
                customer_count=Count('cutomer')
            ).order_by('-customer_count')[:4]
            UserForm = UserRegistrationForm()
            context.update({
                'agent': agents,
                "customer": customer,
                "UserForm": UserForm,
            })

        context.update({
            "CustomerForm": CustomerForm,
            "user_categories": user_categories,
        })
        return render(request, "home.html", context)

    def post(self, request, *args, **kwargs):
        if 'customer_submit' in request.POST:
            user = AbstractUser.objects.get(
                user=request.user, category="agent")
            customer_form = CustomerRegistrationForm(request.POST)
            if customer_form.is_valid():
                customer = customer_form.save(commit=False)
                customer.agent = user
                customer.status = "pending"
                customer.save()
                messages.success(request, "Customer create successfully")
                return redirect(request.path)
            else:
                messages.error(
                    request, "Customer creation failed. Please check the form and try again.")
                return redirect(request.path)

        elif 'agent_submit' in request.POST:
            agent_form = UserRegistrationForm(request.POST)
            if agent_form.is_valid():
                agent = agent_form.save(commit=False)
                agent.set_password(agent_form.cleaned_data.get('password'))
                agent.save()
                user_agent = AbstractUser.objects.create(
                    user=agent,
                    category="agent",
                    phone_number=agent_form.cleaned_data.get('phone_number')
                )
                user_agent.save()
                messages.success(request, "Agent create successfully")
                return redirect(request.path)
            else:
                messages.error(
                    request, "Agent creation failed. Please check the form and try again.")
                return redirect(request.path)

        return redirect(request.path)


@method_decorator(login_required, name='dispatch')
class AgentView(View):
    def get(self, request, agent_id=None):
        user = AbstractUser.objects.filter(user=request.user)
        user_categories = " ".join([u.category for u in user])
        if agent_id:
            agent = AbstractUser.objects.get(user__id=agent_id)
            # Get customers assigned to this agent
            customers = Cutomer.objects.filter(agent=agent)
            context = {
                "agent_id": agent,
                "customers": customers
            }
        else:
            agents = AbstractUser.objects.filter(
                category="agent"
            ).annotate(
                customer_count=Count('cutomer')
            ).order_by('-customer_count')
            context = {
                "agent": agents
            }
        context['user_categories'] = user_categories
        return render(request, "agents.html", context)


@method_decorator(login_required, name='dispatch')
class CustomerView(View):
    def get(self, request, customer_id=None):
        context = {}
        customer_form = CustomerRegistrationForm()
        user_qs = AbstractUser.objects.filter(user=request.user)
        user_categories = " ".join([u.category for u in user_qs])
        filter_status = request.GET.get('q')

        if customer_id:
            customer_qs = Cutomer.objects.get(id=customer_id)
        else:
            # Determine customer queryset based on user category and filter
            if user_categories == "agent":
                agent_instance = user_qs.first()
                customer_qs = Cutomer.objects.filter(agent=agent_instance)
            else:
                customer_qs = Cutomer.objects.all()
                context["UserForm"] = UserRegistrationForm()

            if filter_status:
                customer_qs = customer_qs.filter(status=filter_status)

        context.update({
            "customer_id": customer_id,
            "CustomerForm": customer_form,
            "user_categories": user_categories,
            "customer": customer_qs
        })
        return render(request, "customer.html", context)

    def post(self, request, customer_id):
        if "customer_update" in request.POST:
            customer_instance = Cutomer.objects.get(id=customer_id)
            customer_form = CustomerRegistrationForm(
                request.POST, instance=customer_instance)
            if customer_form.is_valid():
                customer_form.save()
                messages.success(request, "Customer updated successfully")
            return redirect(f"/customer/{customer_id}")
        elif "status" in request.POST:
            customer_instance = Cutomer.objects.get(id=customer_id)
            status = request.POST.get("status")
            if status:
                customer_instance.status = status
                customer_instance.save()
                messages.success(
                    request, "Customer status updated successfully")
            else:
                messages.error(request, "No status provided.")
            return redirect(f"/customer/{customer_id}")
        else:
            messages.error(
                request, "Failed to update customer.Please check the form and try again.")
            return redirect(f"/customer/{customer_id}")
