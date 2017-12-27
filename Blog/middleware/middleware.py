from django.utils.deprecation import MiddlewareMixin

class MyMiddleware(MiddlewareMixin):
    pass
    # def process_request(self,request):
    #     ip = request.META['REMOTE_ADDR']
    #     server = request.META['HTTP_HOST']
    #     print(ip,'111111111',server)
    #     if int(ip[-1])%2 == 1:
    #         raise AttributeError('你以为你想访问就访问啊')