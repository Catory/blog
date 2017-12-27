
import logging
from django.core.cache import cache

logger = logging.getLogger('inf')

def getip(func):
    def wrap(request,*args):

        ip = request.META['REMOTE_ADDR']
        logger.info('{ip}  {}'.format(ip=ip,*args))
        return func(request,*args)
    return wrap

def page_cache(timeout):
    def article_cache(func):
        def wrap(request,*args,**kwargs):
            key = 'url_%s'%request.get_full_path()
            response = cache.get(key)
            if response is None:
                print('execute...')
                response = func(request,*args,**kwargs)
                cache.set(key,response,timeout)
            return response
        return wrap
    return article_cache