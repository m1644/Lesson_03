import yaml
from checkers import checkout, getout


''' Задание 2
Дополнить все тесты ключом команды 7z -t (тип архива). 
Вынести этот параметр в конфиг.
'''

# Ответ: Добавлена запись в файл config.yaml (archive_type: 7z)
# В файл conftest.py добавлена фикстура (archive_type)

with open('config.yaml') as f:
    data = yaml.safe_load(f)


class TestPositive:
    archive_type = data["archive_type"]

    def test_step1(self, make_folders, clear_folders, make_files, print_time):
        # test1
        res1 = checkout("cd {}; {} a {}/arx.{}".format(data["folder_in"], self.archive_type, data["folder_out"], self.archive_type), "Everything is Ok")
        res2 = checkout("ls {}".format(data["folder_out"]), "arx.{}".format(self.archive_type))
        assert res1 and res2, "test1 FAIL"

    def test_step2(self, clear_folders, make_files):
        # test2
        res = []
        res.append(checkout("cd {}; {} a {}/arx.{}".format(data["folder_in"], self.archive_type, data["folder_out"], self.archive_type), "Everything is Ok"))
        res.append(
            checkout("cd {}; {} e arx.{} -o{} -y".format(data["folder_out"], self.archive_type, self.archive_type, data["folder_ext"]), "Everything is Ok"))
        for item in make_files:
            res.append(checkout("ls {}".format(data["folder_ext"]), item))
        assert all(res)

    def test_step3(self):
        # test3
        assert checkout("cd {}; {} t arx.{}".format(data["folder_out"], self.archive_type, self.archive_type), "Everything is Ok"), "test3 FAIL"

    def test_step4(self):
        # test4
        assert checkout("cd {}; {} u arx2.{}".format(data["folder_in"], self.archive_type, self.archive_type), "Everything is Ok"), "test4 FAIL"

    def test_step5(self, clear_folders, make_files, archive_type):  # Добавлен аргумент archive_type
        # test5
        res = []
        res.append(checkout("cd {}; {} a {}/arx.{}".format(data["folder_in"], archive_type, data["folder_out"], archive_type), "Everything is Ok"))
        for i in make_files:
            res.append(checkout("cd {}; 7z l arx.7z".format(data["folder_out"], archive_type), i))  # Используем archive_type
        assert all(res), "test5 FAIL"

    def test_step6(self, clear_folders, make_files, make_subfolder):
        # test6
        res = []
        res.append(checkout("cd {}; {} a {}/arx.{}".format(data["folder_in"], self.archive_type, data["folder_out"], self.archive_type), "Everything is Ok"))
        res.append(
            checkout("cd {}; {} x arx.{} -o{} -y".format(data["folder_out"], self.archive_type, self.archive_type, data["folder_ext2"]), "Everything is Ok"))
        for i in make_files:
            res.append(checkout("ls {}".format(data["folder_ext2"]), i))
        res.append(checkout("ls {}".format(data["folder_ext2"]), make_subfolder[0]))
        res.append(checkout("ls {}/{}".format(data["folder_ext2"], make_subfolder[0]), make_subfolder[1]))
        assert all(res), "test6 FAIL"

    def test_step7(self):
        # test7
        assert checkout("cd {}; {} d arx.{}".format(data["folder_out"], self.archive_type, self.archive_type), "Everything is Ok"), "test7 FAIL"

    def test_step8(self, clear_folders, make_files):
        # test8
        res = []
        for i in make_files:
            res.append(checkout("cd {}; {} h {}".format(data["folder_in"], self.archive_type, i), "Everything is Ok"))
            hash = getout("cd {}; crc32 {}".format(data["folder_in"], i)).upper()
            res.append(checkout("cd {}; {} h {}".format(data["folder_in"], self.archive_type, i), hash))
        assert all(res), "test8 FAIL"


# Запуск из терминала: pytest -v test_02.py
