import json
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist

from users.category import Category


@csrf_exempt
def load_categories(request):
    import_file, import_data = request.FILES.get("json"), None
    if import_file:
        import_data = json.loads(import_file.read().decode("utf-8"))

        for category in import_data:
            data = import_data[category]
            parent_category = None
            try:
                parent_category = Category.objects.get(name=category)
            except ObjectDoesNotExist:
                parent_category = Category(
                    name=category, user=data.get("user"), users=data.get("users")
                )
                parent_category.save()
            for subcategory in data["subcategories"]:
                subcategory_data = data["subcategories"][subcategory]
                try:
                    Category.objects.get(name=subcategory)
                except ObjectDoesNotExist:
                    subcategory_obj = Category(
                        name=subcategory,
                        user=subcategory_data.get("user", data.get("user")),
                        users=subcategory_data.get("users", data.get("users")),
                        parent=parent_category,
                    )
                    subcategory_obj.save()
    return JsonResponse(status=200, data={"message": "Categories created successfuly."})
