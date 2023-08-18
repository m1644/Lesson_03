import time


######## Декораторы и фикстуры

#### Декораторы

def retry(func):
    def wrapper():
        try:
            func()
        except:
            print('Retry...')
            time.sleep(1)
            func()
    return wrapper()

@retry
def might_file():
    print('might_file')
    raise Exception

might_file()


#### Фикстуры

# См. test_01.py
