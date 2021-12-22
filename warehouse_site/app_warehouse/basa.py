from .models import *
from django.utils import timezone
from datetime import datetime


def get_user():
    users = Building.objects.filter(floor_number=1)
    list_skils = []
    for i in users:
        list_skils.append(i)
    return list_skils[0], list_skils[1], list_skils[2]
   # for i in users:
    #    print(type(i.pk))
def get_building(floor):
    building = Building.objects.filter(floor_number=floor)
    return building

def get_order_user(id_personal_area):
    orders_users = Orders.objects.filter(personal_area_idpersonal_area=id_personal_area)
    name_user = PersonalArea.objects.filter(pk=id_personal_area)

    return orders_users, name_user[0]


def check_login_user(login_user):
    login = Users.objects.filter(login=login_user)
    if len(login) > 0:
        return True
    else:
        return False


def create_account(entered_login, entered_passw):
    new_user = Users(login=entered_login, password=entered_passw)
    new_user.save()
    new_personal_area = PersonalArea(user_id_user=new_user)
    new_personal_area.save()


def check_pass(login, password):
    get_user_pass = Users.objects.filter(login=login)
    if get_user_pass[0].password == password:
        return True
    else:
        return False

def get_info_user(login):
    user = Users.objects.filter(login=login)
    personal_area = PersonalArea.objects.filter(user_id_user=user[0].pk)
    print(personal_area[0])
    return user[0], personal_area[0]


def check_warehouse(id, id_user):
    ger_role = Users.objects.filter(pk=id_user)
    get_warehouse = Building.objects.filter(pk=id)
    if get_warehouse[0].status_warehouse == 'Active' and ger_role[0].role != 'admin':
        return True
    else:
        return False


def get_status(id):
    get_warehouse = Building.objects.filter(pk=id)
    return get_warehouse[0].status_warehouse


def get_info_build(personal_area):
    get_warehouse = Building.objects.filter(pk=personal_area)
    return get_warehouse[0]

def get_recive(id):
    get_recive = Review.objects.filter(building_idbuilding=id)
    return get_recive

def deactivate_warehouse(id):
    print("eti id ", id)
    close_warehouse = Building.objects.get(id=id)
    close_warehouse.status_warehouse = "Active"
    close_warehouse.save()


def activate_warehouse(id):
    print("eti id ", id)
    close_warehouse = Building.objects.get(id=id)
    close_warehouse.status_warehouse = "Not active"
    close_warehouse.save()


def add_rewiew(id_user, id_build, text_rew):
    build = Building.objects.filter(pk=id_build)
    user = Users.objects.filter(pk=id_user)
    new_review = Review(text_review=text_rew, user_iduser=user[0], building_idbuilding=build[0])
    new_review.save()

def get_role(id_user):
    role_user = Users.objects.filter(pk=id_user)
    if role_user[0].role == 'admin':
        return True
    else:
        return False

def get_sum(id):
    build = Building.objects.filter(pk=id)
    return build[0].cost_per_month


def create_order(summ, date_start, date_end, id_user, id_build):
    personal = PersonalArea.objects.filter(pk=id_user)
    build = Building.objects.filter(pk=id_build)
    new_order = Orders(OrderSum=summ, LeaseStartDate=date_start, LeaseEndDate=date_end, personal_area_idpersonal_area=personal[0], building_idbuilding=build[0])
    new_order.save()

def check_orders():
    orders = Orders.objects.all()
    date_now = datetime.now()
    for i in orders:
        if i.LeaseEndDate < date_now.date() and i.building_idbuilding.status_warehouse == "Not active":
            open_warehouse = Building.objects.get(pk=i.building_idbuilding.pk)
            open_warehouse.status_warehouse = "Not active"
            open_warehouse.save()


def update_price(id, price):
    warehouse = Building.objects.get(id=id)
    warehouse.cost_per_month = price
    warehouse.save()


def get_login(id_user):
    login_user = Users.objects.get(id=id_user)
    return login_user.login

def del_ref(id_rew):
    rew = Review.objects.get(id=id_rew).delete()