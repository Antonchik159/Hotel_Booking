from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import logout, authenticate, login
from .models import Hostel, Booking, Client, Room
from .forms import ClientForm, EmailPasswordForm, BookingForm, UserForm, BookingApprovalForm
from django.contrib import messages
from django.contrib.auth.models import User

def request_login(request):
    if request.method == 'POST':
        form = EmailPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            # Проверяем клиента
            try:
                user = Client.objects.get(email=email)
                if user.check_password(password):
                    login(request, user)
                    user.update_last_login()  # Обновление времени последнего входа
                    request.session['client_name'] = user.fullname
                    messages.success(request, 'Ви успішно увійшли!')
                    return redirect('home')
                else:
                    messages.error(request, 'Невірний пароль!')
                    return redirect('request_login')
            except Client.DoesNotExist:
                pass  # Если клиент не найден, переходим к проверке администратора

            # Проверяем администратора
            try:
                admin = User.objects.get(email=email)
                if admin.check_password(password):
                    login(request, admin)
                    request.session['username'] = admin.username
                    messages.success(request, 'Ви успішно увійшли як адмін!')
                    return redirect('home')
                else:
                    messages.error(request, 'Невірний пароль!')
                    return redirect('request_login')
            except User.DoesNotExist:  # Исправлено с Client.DoesNotExist
                messages.error(request, 'Користувач або адмін з таким email не знайдено.')
                return redirect('request_login')

    else:
        form = EmailPasswordForm()
    return render(request, 'booking/request_login.html', {'form': form})

# Create your views here.
def index(request):
    return render(request, 'booking/index.html')

def hostel(request):
    hostels = Hostel.objects.all()
    return render(request, 'booking/hostels.html', {'hostel': hostels})

def show_det_hostel(request, item_id):
    hostel = get_object_or_404(Hostel, id=item_id)
    rooms = hostel.get_room()
    return render(request, 'booking/detail_hostel.html', {'hostels': hostel, 'room': rooms})

def client(request):
    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            client = form.save(commit=False)
            password = client.password
            client.set_password(password)
            client.save()
            request.session['client_name'] = client.fullname
            return redirect('hostels')
        else:
            messages.error(request, 'Користувач з такою поштою вже зареєстрований. Бажаєте увійти?')
            return redirect('client')

        
    form = ClientForm()
    context = {'form': form}
    return render(request, 'booking/client.html', context)

def logout_view(request):
    logout(request)
    return redirect('home')

def booking(request, item_id):
    room = get_object_or_404(Room, id=item_id)
    room_price = room.price
    client_name = request.session.get('client_name', None)

    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            start_date = form.cleaned_data['start_date']
            last_date = form.cleaned_data['last_date']

            # Проверка на пересечение промежутков дат
            conflicting_bookings = Booking.objects.filter(
                room=room,
                start_date__lt=last_date,
                last_date__gt=start_date
            )

            if conflicting_bookings.exists():
                messages.error(request, 'Ця дата вже заброньована')
            else:
                form.save()
                return redirect('hostels')
        else:
            return redirect('home')

    if client_name:
        client = get_object_or_404(Client, fullname=client_name)
        form = BookingForm(initial={'room': room, 'client': client, 'price': room_price})
        form.fields['client'].widget.attrs['readonly'] = 'readonly'
        form.fields['room'].widget.attrs['style'] = 'pointer-events: none;'
        form.fields['client'].widget.attrs['style'] = 'pointer-events: none;'
        return render(request, 'booking/book.html', {'form': form, 'room': room, 'client': client, 'price': room_price})
    else:
        form = BookingForm(initial={'room': room, 'price': room_price})
        form.fields['room'].widget.attrs['style'] = 'pointer-events: none;'
        return render(request, 'booking/book.html', {'form': form, 'room': room, 'price': room_price})
    
def account(request):
    # Клієнт
    client_name = request.session.get('client_name', None)
    if client_name:
        try:
            client = get_object_or_404(Client, fullname=client_name)
            book = Booking.objects.filter(client=client)
            return render(request, 'booking/my_account.html', {'book': book})
        except Client.DoesNotExist:
            messages.error(request, 'Клієнта не знайдено.')
            return redirect('home')

    # Адмін
    admin_username = request.session.get('username', None)
    if admin_username:
        try:
            admin = get_object_or_404(User, username=admin_username)
            bookings = Booking.objects.filter(room__hostel__admin=admin)

            if request.method == 'POST':
                booking_id = request.POST.get('booking_id')
                booking = get_object_or_404(Booking, id=booking_id)
                form = BookingApprovalForm(request.POST, instance=booking)
                if form.is_valid():
                    form.save()
                    messages.success(request, 'Статус оновлено.')
                    return redirect('account')

            return render(request, 'booking/admin_account.html', {'bookings': bookings, 'form': BookingApprovalForm()})
        except User.DoesNotExist:
            messages.error(request, 'Адміна не знайдено!.')
            return redirect('home')

    messages.error(request, 'Ви не авторизовані. Будь ласка, увійдіть в систему.')
    return redirect('request_login')


def detail_booking(request, item_id):
    item = get_object_or_404(Booking, id=item_id)
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            item.client = form.cleaned_data['client']
            item.room = form.cleaned_data['room']
            item.price = form.cleaned_data['price']
            item.start_date = form.cleaned_data['start_date']
            item.last_date = form.cleaned_data['last_date']
            item.save()
        return redirect('account')
    if request.method == 'GET':
        form = BookingForm()
        return render(request, 'booking/bron_detail.html', {'form': form, 'item': item})
    
def add_admin(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save()
            request.session['username'] = user.username
            return redirect('hostels')
        else:
            messages.error(request, 'Користувач з такою поштою вже зареєстрований. Бажаєте увійти?')
            return redirect('home')
    else:
        form = UserForm()
    return render(request, 'booking/create_adm.html', {'form': form})