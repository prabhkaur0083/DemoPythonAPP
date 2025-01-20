from django.http import JsonResponse


def simple_view(request):
    print("this called now")
    return JsonResponse({"message": "Hello, this is a simple Django view!"})
