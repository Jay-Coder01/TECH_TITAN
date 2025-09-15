from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login as auth_login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .models import Scholarship, ForumTopic, ForumReply, StudentProfile, ScholarshipRecommendation, Signup
from .forms import SignupForm, LoginForm
from .recommendation_engine.utils import get_recommendations_for_user, refresh_recommendations_for_student, ensure_recommendations_exist
from decimal import Decimal
import json


def frontend_login_required(view_func):
    def wrapper(request, *args, **kwargs):
        if 'user_id' not in request.session:
            messages.error(request, "Please login to access this page.")
            return redirect('login')
        return view_func(request, *args, **kwargs)
    return wrapper


def home(request):
    if 'user_id' in request.session:
        try:
            user = Signup.objects.get(id=request.session['user_id'])
            profile = StudentProfile.objects.get(user=user)
            recommendations = get_recommendations_for_user(user, 3)
        except (StudentProfile.DoesNotExist, Signup.DoesNotExist):
            recommendations = []
    else:
        recommendations = []
    
    context = {
        'recommendations': recommendations,
    }
    return render(request, 'home.html', context)

@frontend_login_required
def scholarships(request):
    all_scholarships = Scholarship.objects.all().order_by('-deadline')
    
    # Get recommendations for the user
    user = Signup.objects.get(id=request.session['user_id'])
    try:
        profile = StudentProfile.objects.get(user=user)
        recommendations = get_recommendations_for_user(user)
        recommended_ids = [rec.scholarship.id for rec in recommendations]
    except StudentProfile.DoesNotExist:
        recommendations = []
        recommended_ids = []
    
    context = {
        'scholarships': all_scholarships,
        'recommended_ids': recommended_ids,
    }
    return render(request, 'scholarships.html', context)

@frontend_login_required
def profile(request):
    user = Signup.objects.get(id=request.session['user_id'])
    try:
        profile = StudentProfile.objects.get(user=user)
    except StudentProfile.DoesNotExist:
        profile = None
    
    # Define choices for checkbox groups
    extracurricular_choices = [
        {'value': 'sports', 'label': 'Sports'},
        {'value': 'arts', 'label': 'Arts & Music'},
        {'value': 'debate', 'label': 'Debate & Public Speaking'},
        {'value': 'volunteering', 'label': 'Volunteering & Community Service'},
        {'value': 'stem_clubs', 'label': 'STEM Clubs'},
        {'value': 'cultural', 'label': 'Cultural Activities'},
        {'value': 'leadership', 'label': 'Leadership Roles'},
    ]
    
    achievement_choices = [
        {'value': 'academic_awards', 'label': 'Academic Awards'},
        {'value': 'sports_awards', 'label': 'Sports Awards'},
        {'value': 'arts_awards', 'label': 'Arts & Music Awards'},
        {'value': 'competition_wins', 'label': 'Competition Wins'},
        {'value': 'research_publications', 'label': 'Research Publications'},
        {'value': 'patents', 'label': 'Patents'},
    ]
    
    minority_choices = [
        {'value': 'sc_st', 'label': 'SC/ST'},
        {'value': 'obc', 'label': 'OBC'},
        {'value': 'ews', 'label': 'EWS'},
        {'value': 'women_in_stem', 'label': 'Women in STEM'},
        {'value': 'first_generation', 'label': 'First Generation College Student'},
        {'value': 'rural_background', 'label': 'Rural Background'},
    ]
    
    disability_choices = [
        {'value': 'physical', 'label': 'Physical Disability'},
        {'value': 'visual', 'label': 'Visual Impairment'},
        {'value': 'hearing', 'label': 'Hearing Impairment'},
        {'value': 'learning', 'label': 'Learning Disability'},
        {'value': 'autism', 'label': 'Autism Spectrum'},
    ]
    
    if request.method == 'POST':
        if not profile:
            # Use the frontend user (Signup instance) instead of request.user
            profile = StudentProfile(user=user)
        
        # Update basic info
        profile.date_of_birth = request.POST.get('date_of_birth')
        profile.gender = request.POST.get('gender')
        profile.nationality = request.POST.get('nationality')
        profile.citizenship = request.POST.get('citizenship')
        
        # Update academic info - handle decimal conversion
        profile.education_level = request.POST.get('education_level')
        profile.field_of_study = request.POST.get('field_of_study')
        
        # Convert CGPA to Decimal safely
        cgpa_value = request.POST.get('cgpa')
        if cgpa_value:
            try:
                profile.cgpa = Decimal(cgpa_value)
            except (TypeError, ValueError):
                profile.cgpa = None
        else:
            profile.cgpa = None
        
        # Convert graduation year to integer safely
        grad_year = request.POST.get('graduation_year')
        if grad_year:
            try:
                profile.graduation_year = int(grad_year)
            except (TypeError, ValueError):
                profile.graduation_year = None
        else:
            profile.graduation_year = None
        
        # Convert family income to Decimal safely
        income_value = request.POST.get('family_income')
        if income_value:
            try:
                profile.family_income = Decimal(income_value)
            except (TypeError, ValueError):
                profile.family_income = None
        else:
            profile.family_income = None
            
        profile.financial_aid_needed = 'financial_aid_needed' in request.POST
        
        # Update additional criteria (stored as JSON)
        extracurriculars = request.POST.getlist('extracurriculars')
        profile.extracurriculars = json.dumps(extracurriculars) if extracurriculars else '[]'
        
        achievements = request.POST.getlist('achievements')
        profile.achievements = json.dumps(achievements) if achievements else '[]'
        
        disabilities = request.POST.getlist('disabilities')
        profile.disabilities = json.dumps(disabilities) if disabilities else '[]'
        
        minority_groups = request.POST.getlist('minority_groups')
        profile.minority_groups = json.dumps(minority_groups) if minority_groups else '[]'
        
        profile.save()
        
        # Refresh recommendations
        count = refresh_recommendations_for_student(profile)
        
        # Ensure at least some recommendations exist
        final_count = ensure_recommendations_exist(profile)
        
        messages.success(request, f'Profile updated successfully! Found {final_count} scholarship recommendations.')
        return redirect('profile')
    
    context = {
        'profile': profile,
        'education_levels': StudentProfile._meta.get_field('education_level').choices,
        'extracurricular_choices': extracurricular_choices,
        'achievement_choices': achievement_choices,
        'minority_choices': minority_choices,
        'disability_choices': disability_choices,
    }
    return render(request, 'profile.html', context)

@frontend_login_required
def recommendations(request):
    user = Signup.objects.get(id=request.session['user_id'])
    try:
        profile = StudentProfile.objects.get(user=user)
        recommendations = get_recommendations_for_user(user)
        
        # If no recommendations, try to create some
        if not recommendations:
            ensure_recommendations_exist(profile)
            recommendations = get_recommendations_for_user(user)
            
    except StudentProfile.DoesNotExist:
        recommendations = []
        messages.error(request, 'Please complete your profile first to get recommendations.')
    
    context = {
        'recommendations': recommendations,
    }
    return render(request, 'recommendations.html', context)

@frontend_login_required
def refresh_recommendations(request):
    try:
        user = Signup.objects.get(id=request.session['user_id'])
        profile = StudentProfile.objects.get(user=user)
        count = refresh_recommendations_for_student(profile)
        messages.success(request, f'Recommendations refreshed! Found {count} matching scholarships.')
    except StudentProfile.DoesNotExist:
        messages.error(request, 'Please complete your profile first to get recommendations.')
    
    return redirect('recommendations')

def forum(request):
    topics = ForumTopic.objects.all().order_by('-created_at')
    return render(request, 'forum.html', {'topics': topics})

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')

def login_view(request):
    # If user is already logged in, redirect to home
    if 'user_id' in request.session:
        return redirect('home')
    
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            
            try:
                # Check if user exists in Signup model (frontend user)
                user = Signup.objects.get(email=email)
                if user.password == password:  # Simple password check
                    # Set session for frontend user
                    request.session['user_id'] = user.id
                    request.session['user_name'] = user.name
                    request.session['user_email'] = user.email
                    
                    messages.success(request, "Logged in successfully!")
                    return redirect('home')
                else:
                    messages.error(request, "Invalid email or password.")
            except Signup.DoesNotExist:
                messages.error(request, "Invalid email or password.")
    else:
        form = LoginForm()
    
    return render(request, 'login.html', {'form': form})

def register(request):
    # If user is already logged in, redirect to home
    if 'user_id' in request.session:
        return redirect('home')
    
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            
            # Check if user already exists
            if Signup.objects.filter(email=email).exists():
                messages.error(request, "Email already exists. Please use a different one.")
            else:
                user = form.save()
                # Auto-login after registration
                request.session['user_id'] = user.id
                request.session['user_name'] = user.name
                request.session['user_email'] = user.email
                
                messages.success(request, "Account created successfully!")
                return redirect('profile')  # Redirect to profile to complete setup
        else:
            messages.error(request, "Signup failed. Please check your details.")
    else:
        form = SignupForm()
    
    return render(request, 'register.html', {'form': form})


def logout_view(request):
    # Clear frontend user session
    if 'user_id' in request.session:
        del request.session['user_id']
    if 'user_name' in request.session:
        del request.session['user_name']
    if 'user_email' in request.session:
        del request.session['user_email']
    
    messages.success(request, 'Logged out successfully!')
    return redirect('home')

def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = Signup.objects.get(email=email)
            # Here you would typically send a password reset email
            messages.success(request, "Password reset instructions have been sent to your email.")
            return redirect('login')
        except Signup.DoesNotExist:
            messages.error(request, "No account found with that email address.")
    
    return render(request, 'forgot-password.html')

def api_scholarships(request):
    scholarships = Scholarship.objects.all().values('title', 'provider', 'amount', 'deadline', 'description')
    return JsonResponse(list(scholarships), safe=False)