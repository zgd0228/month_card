from django.urls import reverse

def memory(request,name,*args,**kwargs):

    url = reverse(name,args=args,kwargs=kwargs)
    origin_params = request.GET.get('filter')
    if origin_params:
        url = '%s?%s' % (url, origin_params)
    return url
