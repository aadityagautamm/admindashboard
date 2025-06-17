from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .forms import *
from django.utils.timezone import now
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import AdminPasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.http import JsonResponse
from .models import DAYS_OF_WEEK


# Create your views here.


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        # Authenticate the user
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user) 
            return redirect('dashboard')  
        else:
            messages.error(request, 'Invalid username or password')
    
    return render(request, 'dashboard/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')  
def dashboard(request):
    business = Business.objects.first()  

    if business:
        total_menu_items = business.menu_items.count()  
        total_photos_uploaded = business.gallery_images.count()  

       
        profile_fields = [
            business.brand_name, business.slogan, business.image,
            business.description, business.email, business.phone,
            business.website, business.facebook, business.instagram,
            business.twitter, business.linkedin, business.latitude,
            business.longitude
        ]
        filled_fields = sum(1 for field in profile_fields if field)  
        total_fields = len(profile_fields)
        profile_completion = int((filled_fields / total_fields) * 100)

        
        last_image = business.gallery_images.order_by('-uploaded_at').first()
        last_update = (now() - last_image.uploaded_at).days if last_image else None
    else:
        total_menu_items = 0
        total_photos_uploaded = 0
        profile_completion = 0
        last_update = None

    return render(request, 'dashboard/base.html', {
        'business': business,
        'total_menu_items': total_menu_items,
        'total_photos_uploaded': total_photos_uploaded,
        'profile_completion': profile_completion,
        'last_update': last_update,
    })

def business_profile(request):
    # Get the first Business object (you can adjust this logic as needed)
    business = Business.objects.first()

    if request.method == 'POST':
        form = BusinessProfileForm(request.POST, request.FILES, instance=business)
        if form.is_valid():
            form.save()
            return redirect('dashboard')  # Or wherever you want to go
    else:
        form = BusinessProfileForm(instance=business)

    return render(request, 'dashboard/business_profile.html', {'form': form})



def social_links(request):
    business = Business.objects.first()

    if request.method == 'POST':
        form = SocialLinksForm(request.POST, instance=business)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = SocialLinksForm()

    return render(request, 'dashboard/business_profile.html', {'form': form})

def add_menu_item(request):
    business = Business.objects.first()

    if request.method == 'POST':
        form = MenuItemForm(request.POST, request.FILES)
        if form.is_valid():
            menu_item = form.save(commit=False)
            menu_item.business = business
            menu_item.save()
            return redirect('dashboard')
    else:
        form = MenuItemForm()

    return render(request, 'dashboard/add_menu_item.html', {'form': form})

def get_items_by_category(request):
    category_id = request.GET.get('category_id')
    items = MenuItem.objects.filter(category_id=category_id).values('name')
    return JsonResponse(list(items), safe=False)


def is_superuser(user):
    return user.is_superuser
@login_required
@user_passes_test(is_superuser)
def change_password(request):
    if request.method == 'POST':
        form = AdminPasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Keeps the user logged in
            messages.success(request, 'Your password was successfully updated!')
            return redirect('dashboard')  # or wherever you want
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = AdminPasswordChangeForm(user=request.user)

    return render(request, 'dashboard/change_password.html', {'form': form})



def manage_business_hours(request):
    business = Business.objects.first()

    if request.method == 'POST':
        for day, _ in DAYS_OF_WEEK:
            is_open = request.POST.get(f'{day}_open') == 'on'
            from_time = request.POST.get(f'{day}_from') if is_open else None
            to_time = request.POST.get(f'{day}_to') if is_open else None

            BusinessHour.objects.update_or_create(
                business=business,
                day=day,
                defaults={
                    'from_time': from_time or None,
                    'to_time': to_time or None,
                    'is_closed': not is_open,
                }
            )

        messages.success(request, "Business hours updated successfully.")
        return redirect('manage_business_hours')

    existing_hours = {
        hour.day: hour for hour in BusinessHour.objects.filter(business=business)
    }

  
    return render(request, 'dashboard/business_hours.html', {
        'days': DAYS_OF_WEEK,
        'existing_hours': existing_hours,
    })


def admin_balance_dashboard(request):
    # Admin user
    user = request.user

    # Get or create the balance object
    balance, created = Balance.objects.get_or_create(user=user)
    aok_point, created = AOKPoint.objects.get_or_create(user=user)

    context = {
        'balance_from_sales': balance.balance_from_sales,
        'balance_from_tips': balance.balance_from_tips,
        'current_balance': balance.current_balance,
        'aok_points': aok_point.points,
    }

    return render(request, 'dashboard/admin_balance.html', context)