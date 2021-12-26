from django.shortcuts import render
from django.views import View
from .basa import *
from django.http import HttpResponseRedirect
from django.utils import timezone
from datetime import datetime
from dateutil.relativedelta import relativedelta


class MainPage(View):
    def get(self, request):
        try:
            #print(datetime.now() + relativedelta(months=int(1)),"eto data")
            personal_area = request.session.get("personal_area")
            if personal_area is None:
                print(personal_area)
                return HttpResponseRedirect('page_log_in.html')

            context = {

            }

            return render(request, 'main.html', context=context)
        except:
            return HttpResponseRedirect('page_log_in.html')




class Order_Page(View):
    def get(self, request):

        try:
            personal_area = request.session.get("personal_area")
            if personal_area is None:
                print(personal_area)
                return HttpResponseRedirect('../page_log_in.html')
            a = check_orders()
            context = {
                'building': get_building(1)
            }
            return render(request, 'order_page.html', context=context)
        except:
            return HttpResponseRedirect('page_log_in.html')

class Order_Page_2(View):
    def get(self, request):
        try:
            personal_area = request.session.get("personal_area")
            if personal_area is None:
                print(personal_area)
                return HttpResponseRedirect('../page_log_in.html')
            check_orders()
            context = {
                'building': get_building(2)
            }
            return render(request, 'order_page_2.html', context=context)
        except:
            return HttpResponseRedirect('page_log_in.html')

class Personal_area(View):
    def get(self, request):
        try:
            #print(datetime.now() + relativedelta(months=int(1)),"eto data")
            personal_area = request.session.get("personal_area")
            print(personal_area)
            order, name_user = get_order_user(personal_area)
            context = {
                    'data_table' : order,
                    'name_user': name_user,

            }
            return render(request, 'personal_area.html', context=context)
        except:
            return HttpResponseRedirect('page_log_in.html')

    def post(self, request):
        del request.session['user']
        del request.session['personal_area']
        return HttpResponseRedirect('page_log_in.html')
class Page_registr(View):
    def get(self, request):
        context = {

        }
        return render(request, 'page_registr.html', context=context)

    def post(self, request):
        entered_login = request.POST.get("enter_login")
        entered_passw = request.POST.get("enter_password")
        if len(entered_login) <= 0 or len(entered_passw) <= 0:
            context = {
                'error_message': 'Заполните все поля'
            }
            return render(request, 'page_registr.html', context=context)
        elif len(entered_login) > 25:
            context = {
                'error_message': 'Логин не должен быть больше 25 символов'
            }
            return render(request, 'page_registr.html', context=context)
        elif len(entered_passw) > 10:
            context = {
                'error_message': 'Пароль не должен быть больше 10 символов'
            }
            return render(request, 'page_registr.html', context=context)

        elif check_login_user(entered_login):
            context = {
                'error_message': 'Пользователь с таким именнем уже существует'
            }
            return render(request, 'page_registr.html', context=context)

        elif entered_login.find(' ') != -1 or entered_passw.find(' ') != -1:
            context = {
                'error_message': 'Нельзя использовать пробельные символы'
            }
            return render(request, 'page_registr.html', context=context)
        else:
            create_account(entered_login, entered_passw)

            return HttpResponseRedirect('page_log_in.html')
        #users = autoriz(entered_login, entered_passw)
        #if not users:
        #    context = {
        #        "message": "Введен неверный логин или пароль"
        #    }

class Page_login(View):
    def get(self, request):
        context = {

        }
        return render(request, 'page_log_in.html', context=context)

    def post(self, request):
        entered_login = request.POST.get("log_login")
        entered_passw = request.POST.get("log_pass")
        if not check_login_user(entered_login):
            context = {
                'error_message': 'Пользователя с таким именнем не существует'
            }
            return render(request, 'page_log_in.html', context=context)
        else:
            if not check_pass(entered_login, entered_passw):
                context = {
                    'error_message': 'Не правильный ввод данных'
                }
                return render(request, 'page_log_in.html', context=context)
            else:
                user, personal_area = get_info_user(entered_login)
                request.session['user'] = user.pk
                request.session['personal_area'] = personal_area.pk
                print("adasdasdasdaddsdas")
                return HttpResponseRedirect('personal_area.html')


class Page_warehouses(View):
    def get(self, request, id):
        context = {
                'id_ware': id
        }
        if request.method == "GET" and 'deactivate' in request.GET:
            print("I am deactivate")
            deactivate_warehouse(id)
        elif request.method == "GET" and 'activate' in request.GET:
            activate_warehouse(id)
        #if 1==1:
        try:
            personal_area = request.session.get("personal_area")
            if not check_warehouse(id, request.session.get("user")):
                print(id)
                context = {
                    'build': get_info_build(id),
                    'recive': get_recive(id),
                    'role': get_role(request.session.get("user")),
                    'status': get_status(id),
                    'login': get_login(request.session.get("user"))
                }
                return render(request, 'page_warehouses.html', context=context)
            else:
                return HttpResponseRedirect('../')
        except:
            return HttpResponseRedirect('../page_log_in.html')

    def post(self, request, id):
        if request.method == "POST" and 'textarea' in request.POST:
            print("Privet Egor and Kirill")
            if len(request.POST.get("textarea")) <= 0:
                return HttpResponseRedirect('../')
            else:
                add_rewiew(request.session.get("user"), id, request.POST.get("textarea"))
                return HttpResponseRedirect('../page_warehouses.html/' + str(id))
        elif request.method == "POST" and 'number_month' in request.POST:
            try:
                if int(request.POST.get("number_month")) <= 0:
                    return HttpResponseRedirect('../page_warehouses.html/' + str(id))
                sum_order = int(request.POST.get("number_month")) * get_sum(id)
                request.session['sum_order'] = sum_order
                request.session['number_month'] = request.POST.get("number_month")
                return HttpResponseRedirect('../page_payback.html/' + str(id))
            except:
                return HttpResponseRedirect('../page_warehouses.html/' + str(id))
        elif request.method == "POST" and 'upd_submit' in request.POST:

            try:
                price = float(request.POST.get("upd_price"))
                if price <= 0:
                    return HttpResponseRedirect('../page_warehouses.html/' + str(id))
                print(price + 4)
                update_price(id, price)
                return HttpResponseRedirect('../page_warehouses.html/' + str(id))
            except:
                return HttpResponseRedirect('../page_warehouses.html/' + str(id))
        elif request.method == "POST" and 'del_rew' in request.POST:
            del_ref(request.POST.get("id_rew"))
            return HttpResponseRedirect('../page_warehouses.html/' + str(id))

class Page_payback(View):
    def get(self, request, id):
        context = {
            'summ': round(request.session.get("sum_order"),2)
        }
        return render(request, 'page_payback.html', context=context)

    def post(self, request, id):
        card_detail = str(request.POST.get("number_card"))
        if len(card_detail) <= 0:
            context = {
                'error_message': 'Заполните поле',
                'summ': round(request.session.get("sum_order"), 2)
            }
            return render(request, 'page_payback.html', context=context)
        elif card_detail.find('-') != -1 or card_detail.find('.') != -1:
            context = {
                'error_message': 'Введите корректные данные',
                'summ': round(request.session.get("sum_order"), 2)
            }
            return render(request, 'page_payback.html', context=context)
        elif len(card_detail) > 16:
            context = {
                'error_message': 'Длина карты не может быть больше 16 символов',
                'summ': round(request.session.get("sum_order"), 2)
            }
            return render(request, 'page_payback.html', context=context)
        elif len(card_detail) < 16:
            context = {
                'error_message': 'Длина карты не может быть меньше 16 символов',
                'summ': round(request.session.get("sum_order"), 2)
            }
            return render(request, 'page_payback.html', context=context)
        else:


            date_start = datetime.now().strftime("%Y-%m-%d")
            date_now = datetime.now()
            date_end = date_now + relativedelta(months=int(request.session.get("number_month")))
            create_order(round(request.session.get("sum_order"),2), date_start, date_end.strftime("%Y-%m-%d"), request.session.get("personal_area"), id)
            deactivate_warehouse(id)
            del request.session['sum_order']
            del request.session['number_month']
            return HttpResponseRedirect('../personal_area.html')