import json
from functools import wraps
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import User

def body(request):
    try: return json.loads(request.body or '{}')
    except json.JSONDecodeError: return {}

def public_user(user):
    return {'id': user.id, 'name': user.get_full_name() or user.username, 'email': user.email, 'mobile': user.mobile, 'role': user.role}

def api(view):
    @wraps(view)
    def wrapped(request, *args, **kwargs):
        if request.method != 'POST': return JsonResponse({'ok': False, 'message': 'POST required.'}, status=405)
        return view(request, *args, **kwargs)
    return wrapped

@csrf_exempt
@api
def signup(request):
    data = body(request)
    name = str(data.get('fullName', '')).strip()
    email = str(data.get('email', '')).strip().lower()
    mobile = str(data.get('mobile', '')).strip()
    password = str(data.get('password', ''))
    role = data.get('role', 'citizen')
    if not name or not email or len(password) < 6 or role not in ('citizen', 'admin'):
        return JsonResponse({'ok': False, 'message': 'Please provide valid signup details.'}, status=400)
    if User.objects.filter(email=email).exists():
        return JsonResponse({'ok': False, 'message': 'An account with this email already exists.'}, status=409)
    first, *last = name.split()
    user = User.objects.create_user(username=email, email=email, password=password, first_name=first, last_name=' '.join(last), mobile=mobile, role=role)
    return JsonResponse({'ok': True, 'message': 'Account created successfully.', 'user': public_user(user)})

@csrf_exempt
@api
def login_api(request):
    data = body(request); email = str(data.get('email', '')).strip().lower(); password = str(data.get('password', ''))
    user = authenticate(request, username=email, password=password)
    if not user or not user.is_active:
        return JsonResponse({'ok': False, 'message': 'Invalid email or password.'}, status=401)
    login(request, user)
    return JsonResponse({'ok': True, 'user': public_user(user)})

@csrf_exempt
@api
def reset_password(request):
    data = body(request); email = str(data.get('email', '')).strip().lower(); new_password = str(data.get('newPassword', ''))
    if len(new_password) < 6: return JsonResponse({'ok': False, 'message': 'Password must contain at least 6 characters.'}, status=400)
    try: user = User.objects.get(email=email)
    except User.DoesNotExist: return JsonResponse({'ok': False, 'message': 'No account was found for this email.'}, status=404)
    user.password = make_password(new_password); user.save(update_fields=['password'])
    return JsonResponse({'ok': True, 'message': 'Password reset successfully.'})

@csrf_exempt
@api
def logout_api(request):
    logout(request); return JsonResponse({'ok': True})

def me(request):
    if not request.user.is_authenticated: return JsonResponse({'authenticated': False}, status=401)
    return JsonResponse({'authenticated': True, 'user': public_user(request.user)})
