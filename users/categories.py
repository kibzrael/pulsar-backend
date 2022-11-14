from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt

from users.category import Category
from pulsar.decorators.jwt_required import jwt_required


@csrf_exempt
def create_category(request, **kwargs):
    if request.method != "POST":
        return JsonResponse(
            status=405, data={"message": "The method you're calling is invalid"}
        )

    name = request.POST.get("name", "Personal Account")
    user = request.POST.get("user", "Personal Account")
    users = request.POST.get("users", "Personal Account")
    parent = request.POST.get("parent")

    parent_category = None

    if parent:
        try:
            parent_category = Category.objects.get(name=parent)
        except ObjectDoesNotExist:
            pass

    try:
        Category.objects.get(name=name)
    except ObjectDoesNotExist:
        category = Category(name=name, user=user, users=users, parent=parent_category)
        category.save()
    except:
        return JsonResponse(status=500, data={"message": "Failed to create category"})
    else:
        return JsonResponse(status=200, data={"message": "The category already exists"})

    return JsonResponse(
        status=200, data={"message": "You've succesfully created a category."}
    )


@jwt_required()
def get_categories(request, **kwargs):
    categories = Category.objects.filter(parent__isnull=True).values()

    for category in categories:
        sub_categories = Category.objects.filter(parent=category.get("id")).values()
        category["subCategories"] = list(sub_categories)

    return JsonResponse(status=200, data={"categories": list(categories)})
