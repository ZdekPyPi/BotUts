from functools import wraps
from time import sleep
import threading
import functools

def retry(attempts=3, delay=2, skip_on_errors=None):
   """
   attempts: Número máximo de execuções.
   delay: Tempo de espera em segundos entre as tentativas.
   skip_on_errors: Lista de classes de exceção que NÃO devem disparar o retry.
   """
   # Converte para tupla para o isinstance funcionar corretamente
   skip_errors = () if skip_on_errors is None else tuple(skip_on_errors)
    
   def decorator(func):
      @wraps(func)
      def wrapper(*args, **kwargs):
         last_exception = None
         for tentativa in range(1, attempts + 1):
            try:
               return func(*args, **kwargs)
            except skip_errors as e: raise e
            except Exception as e:
               last_exception = e
               if tentativa == attempts:
                  raise last_exception
               sleep(delay)
         return None
      return wrapper
   return decorator


def timeout(segundos):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Cria uma thread para executar a função
            res = []
            def target():
                try:
                    res.append(func(*args, **kwargs))
                except Exception as e:
                    res.append(e)

            thread = threading.Thread(target=target)
            thread.start()
            thread.join(segundos) # Espera o tempo definido

            if thread.is_alive():
                # A thread ainda está rodando, então houve timeout
                raise TimeoutError(f"A função '{func.__name__}' excedeu o tempo de {segundos}s.")
            
            if res and isinstance(res[0], Exception):
                raise res[0]
            return res[0] if res else None
        return wrapper
    return decorator