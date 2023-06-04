import os
import datetime
import zipfile

archives = ('D:\\Users\\Mykhailo Rogozhyn\\Desktop\\Logs backups',
            'Q:\\01_Backup\\Logs backups',
            'Q:\\02_Google drive\\03_imihanick\\ФОП Рогожин\\02_Logs backups')

logs = (('0103-00-000.00', 'W:\\03_Workspace', '0103-00-000.00_Книга учета времени.ods'),
        ('0104-00-000.00', 'W:\\03_Workspace Pavalex', '0104-00-000.00_Книга учета времени.ods'),
        ('Spending and income', 'W:\\01_General\\03_Management\\03_Бухучет', 'Учет расходов и доходов.ods'),
        )

year_string = datetime.date.today().strftime("%Y")
month_string = datetime.date.today().strftime("%Y-%m")
date_string = datetime.date.today().strftime("%Y-%m-%d")

for log in logs:
    os.chdir(log[1])
    for path in archives:
        dir_path = os.path.join(path, log[0], year_string, month_string)
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        zip_file_path = os.path.join(dir_path, date_string + '.zip')
        zip_file = zipfile.ZipFile(str(zip_file_path), 'w')
        zip_file.write(str(log[2]))
