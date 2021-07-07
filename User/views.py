from django.contrib.auth.models import User
from django.core import serializers
from django.db.models.query_utils import Q
from .models import MyUser, UserProfile
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from Core.response import response_gen
from math import ceil
# @require_http_methods(["*"])


def check_method(*methods):
    def inner(func):
        def wrapper(request, *args, **kargs):
            if str(request.method).upper() not in methods:
                return response_gen(
                    message="method not allow",
                    status=403
                )
            return func(request, *args, **kargs)
        return wrapper
    return inner


@check_method("POST")
def create_user(request, *args, **kargs):

    data = request.POST.dict()

    required_field = ["username", "full_name", "email", "password"]

    for key in required_field:
        if not key in data.keys():
            return response_gen(
                message=f"missing field {key}",
                status=403
            )

    try:
        user: MyUser = MyUser.objects.create_user(
            **{key: data[key] for key in required_field})
    except Exception as err:
        return response_gen(
            message=str(err)
        )

    return response_gen(
        data=user.to_json(),
        message="succesffuly created"
    )

# Create your views here.


@check_method("POST", "GET")
def get_user(request, *args, **kargs):
    # print(request.method)
    if request.method == "GET":

        id = request.GET.get("id")

    else:

        id = request.POST.get("id")

    try:

        user = MyUser.objects.get(id=id)

    except Exception as err:

        return response_gen(
            data={},
            message="user not found",
            status=404
        )

    return response_gen(
        data=user.to_json(),
        message="user founded"
    )


@check_method("POST")
def update_user(request, *args, **kargs):
    # valid_key = ["username", "email", "password", "bio", "company_name", "job"]
    try:
        id = request.POST.get("id")
        user: MyUser = MyUser.objects.get(id=id)

    except Exception as err:

        return response_gen(
            data={},
            message="user not found",
            status=404
        )

    account_key = [*user.to_json().keys(), "password"]
    profile_key = [*user.to_json().get("user_profile").keys()]
    profile_key.remove("id")
    valid_key = account_key + profile_key

    for key in request.POST.keys():
        if key in account_key:
            user.__setattr__(key, request.POST.get(key))

        elif key in profile_key:
            user.user_profile.__setattr__(key, request.POST.get(key))

    if request.FILES.get("avatar"):
        # user.user_profile.update(avatar= request.FILES["avatar"])
        user.user_profile.avatar = request.FILES["avatar"]

    user.save()
    user.user_profile.save()
    return response_gen(
        data=user.to_json(),
        message="user updated"
    )


@check_method("GET", "POST")
def delete_user(request, *args, **kargs):
    if request.method == "GET":
        id = request.GET.get("id")

    else:
        id = request.POST.get("id")

    try:

        user = MyUser.objects.get(id=id)

    except Exception as err:

        return response_gen(
            data={},
            message="user not found",
            status=404
        )

    user.delete()
    return response_gen(
        message="user deleted",
    )


@check_method("POST", "GET")
def list_user(request, *args, **kargs):
    query: dict = {}
    if request.method == "GET":
        # quefor key in request.GET.keys():
        query = request.GET.dict()

    else:
        print(request.POST)
        print(request.GET)
        query = {**request.GET.dict(),**request.POST.dict()}
        # return response_gen(
        #         message="paging need both page number and page size and both must be integers larger than 0"
        #     )





    page_size = 0
    if query.get("page"):
        try:
            page_number = int(query.get("page"))
            page_size = int(query.get("page_size"))
            if not page_number or not page_size:
                raise Exception("")
        except Exception as err:
            return response_gen(
                message="paging need both page number and page size and both must be integers larger than 0"
            )

    account_key = MyUser.fields_name
    profile_key = UserProfile.field_names

    qs = MyUser.objects

    q = None
    for key, value in query.items():

        if key in profile_key:
            new_q = Q(**{f"user_profile__{key}__icontains": value})
            q = q & new_q if q else new_q

        if key in account_key:

            if key in ["email", "username"]:
                new_q = Q(**{f"{key}": value})

            else:
                new_q = Q(**{f"{key}__icontains": value})

            q = q & new_q if q else new_q

    
    qs = qs.filter(q) if q else qs.filter()

    if page_size:
        data = {}
        data["total_pages"] = ceil(len(qs)/page_size)
        data["total_rows"] = len(qs)
        
        if page_number > data["total_pages"]:
            return response_gen(status=404, message="page number out of range")

        data["current_page"] = page_number
        data["page_size"] = page_size


        begin = (page_number-1)*page_size
        end = (begin + page_size) if (begin +
                                      page_size <= len(qs)) else len(qs)

        data["content"] = list(map(
            lambda query: query.to_json(),
            qs[begin:end]
        ))

    else:
        data = list(map(
            lambda query: query.to_json(),
            qs
        ))

    return response_gen(
        data=data
        # message
    )


@check_method("POST", "GET")
def get_profile(request, *args, **kargs):...

@check_method("POST")
def update_profile(request, *args, **kargs):
    ...
    try:
        print(kargs)
        id = kargs.get("user_id")
        user: MyUser = MyUser.objects.get(id=id)

    except Exception as err:

        return response_gen(
            data={},
            message="user not found",
            status=404
        )

    profile_key = [*user.to_json().get("user_profile").keys()]
    valid_key = [*profile_key]
    valid_key.remove("id")

    for key in request.POST.keys():
        if key in valid_key:
            user.user_profile.__setattr__(key, request.POST.get(key))

    if request.FILES.get("avatar"):
        # user.user_profile.update(avatar= request.FILES["avatar"])
        user.user_profile.avatar = request.FILES["avatar"]

    # user.save()
    user.user_profile.save()
    return response_gen(
        data=user.to_json(),
        message="user updated"
    )


@check_method("POST","GET")
def test(request,*args,**kargs):
    print(kargs)
    return response_gen()