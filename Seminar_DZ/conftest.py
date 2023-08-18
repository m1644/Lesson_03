import pytest
from checkers import checkout
import random, string
import yaml
from datetime import datetime


with open('config.yaml') as f:
    data = yaml.safe_load(f)


@pytest.fixture()
def make_folders():
    return checkout("mkdir {} {} {} {}".format(data["folder_in"], data["folder_in"], data["folder_ext"], data["folder_ext2"]), "")


@pytest.fixture()
def clear_folders():
    return checkout("rm -rf {}/* {}/* {}/* {}/*".format(data["folder_in"], data["folder_in"], data["folder_ext"], data["folder_ext2"]), "")


@pytest.fixture()
def make_files():
    list_of_files = []
    for i in range(data["count"]):
        filename = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
        if checkout("cd {}; dd if=/dev/urandom of={} bs={} count=1 iflag=fullblock".format(data["folder_in"], filename, data["bs"]), ""):
            list_of_files.append(filename)
    return list_of_files


@pytest.fixture()
def make_subfolder():
    testfilename = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    subfoldername = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    if not checkout("cd {}; mkdir {}".format(data["folder_in"], subfoldername), ""):
        return None, None
    if not checkout("cd {}/{}; dd if=/dev/urandom of={} bs=1M count=1 iflag=fullblock".format(data["folder_in"], subfoldername, testfilename), ""):
        return subfoldername, None
    else:
        return subfoldername, testfilename


@pytest.fixture(autouse=True)
def print_time():
    print("Start: {}".format(datetime.now().strftime("%H:%M:%S.%f")))
    yield
    print("Finish: {}".format(datetime.now().strftime("%H:%M:%S.%f")))


@pytest.fixture(autouse=True)
def write_stat(request):
    # Создаем файл для записи статистики
    stat_file = open("stat.txt", "a")
    # Выполняем тест
    yield
    # Получаем информацию для записи
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
    file_count = data["count"]
    file_size = data["bs"]
    # Читаем статистику загрузки процессора из файла /proc/loadavg
    with open('/proc/loadavg', 'r') as loadavg_file:
        loadavg_stats = loadavg_file.read()
    # Формируем строку для записи
    stat_line = f"{current_time}, Files: {file_count}, Size: {file_size}, Loadavg: {loadavg_stats}\n"
    # Записываем строку в файл
    stat_file.write(stat_line)
    # Закрываем файл
    stat_file.close()


@pytest.fixture
def archive_type():
    return data["archive_type"]
