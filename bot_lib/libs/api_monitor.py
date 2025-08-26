from urllib.parse import urlparse
from functools import wraps
from httplib2 import Http
from requests import api
import requests as rq
import bot_lib
from bot_lib.database.orm import ApiMonitor
import inspect
import urllib3
import os
import time


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)



#============================================================ REQUESTS
def default_manager(url,req,*args, **kwargs):
    curframe  = inspect.currentframe()
    calframe  = inspect.getouterframes(curframe, 2)
    caller    = calframe[2][3]
    path      = calframe[2][1]
    line      = calframe[2][2]
    file_name = os.path.basename(path)

    if bot_lib.IN_PRD:
        ApiMonitor(
                method      = req.request.method,
                function    = caller,
                url         = req.url,
                host        = '{uri.scheme}://{uri.netloc}/'.format(uri=urlparse(req.url)),
                url_path    = url.replace('{uri.scheme}://{uri.netloc}/'.format(uri=urlparse(req.url)),""),
                time_exec   = req.elapsed.microseconds,
                status_code = req.status_code,
                file        = file_name,
                module      = os.path.dirname(os.path.abspath(path)),
                path        = path,
                line        = line,
                message     = req.text.replace("\x00","")
                ).save()


def get_manager(url,params=None,*args, **kwargs):
    req = api.get(url,params,*args, **kwargs)
    default_manager(url,req,*args, **kwargs)
    return req

def options_manager(url,*args, **kwargs):
    req = api.options(url,*args, **kwargs)
    default_manager(url,req,*args, **kwargs)
    return req

def post_manager(url,data=None,json=None,*args, **kwargs):
    req = api.post(url,data,json,*args, **kwargs)
    default_manager(url,req,*args, **kwargs)
    return req

def put_manager(url,data=None,*args, **kwargs):
    req = api.put(url,data,*args, **kwargs)
    default_manager(url,req,*args, **kwargs)
    return req

def patch_manager(url,data=None,*args, **kwargs):
    req = api.patch(url,data,*args, **kwargs)
    default_manager(url,req,*args, **kwargs)
    return req

def delete_manager(url,*args, **kwargs):
    req = api.delete(url,*args, **kwargs)
    default_manager(url,req,*args, **kwargs)
    return req

rq.get     = get_manager
rq.options = options_manager
rq.post    = post_manager
rq.patch   = patch_manager
rq.delete  = delete_manager
rq.put     = put_manager

#=============================================================== HTTPLIB2

def default_manager_httplib2(method,url,data,elapsed_time_microseconds):
    curframe  = inspect.currentframe()
    calframe  = inspect.getouterframes(curframe, 2)
    caller    = calframe[2][3]
    path      = calframe[2][1]
    line      = calframe[2][2]
    file_name = os.path.basename(path)

    if bot_lib.IN_PRD:
        ApiMonitor(
                method      = method,
                function    = caller,
                url         = url,
                host        = '{uri.scheme}://{uri.netloc}/'.format(uri=urlparse(url)),
                url_path    = url.replace('{uri.scheme}://{uri.netloc}/'.format(uri=urlparse(url)),""),
                time_exec   = int(elapsed_time_microseconds),
                status_code = data[0].status,
                file        = file_name,
                module      = os.path.dirname(os.path.abspath(path)),
                path        = path,
                line        = line,
                message     = data[1].decode('utf-8')
                ).save()



def httplib_intercept(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        
        data = function(*args, **kwargs)
        
        elapsed_time_microseconds = (time.perf_counter() - start_time) * 1_000_000
        method = kwargs.get("method") or args[2] 
        default_manager_httplib2(method=method,url=args[1],data=data,elapsed_time_microseconds=elapsed_time_microseconds)
        return data
    return wrapper

setattr(Http, "request", httplib_intercept(getattr(Http, "request")))

# def testeChamada():
#     a = get_manager("https://www.google.com/asdasdasd/asd",verify=False)

# testeChamada()
# get_manager("https://www.google.com/asdasdasd/asd",verify=False)

# pass

