import os
import datetime
import zipfile

archives = ('U:\\Users\\mrogozhyn\\Desktop\\Logs backups',
            'Q:\\01_Backup\\Logs backups')

logs = (('0103-00-000.00', 'W:\\03_Workspace\\0103-00-000.00_Книга учета времени.ods'),
        ('0104-00-000.00', 'W:\\03_Workspace Pavalex\\0104-00-000.00_Книга учета времени.ods')
        )

year_string = datetime.date.today().strftime("%Y")
month_string = datetime.date.today().strftime("%Y-%m")
date_string = datetime.date.today().strftime("%Y-%m-%d")

for log in logs:
    for path in archives:
        dir_path = os.path.join(path, log[0], year_string, month_string)
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        zip_file_path = os.path.join(dir_path, date_string + '.zip')
        zip_file = zipfile.ZipFile(str(zip_file_path), 'w')
        zip_file.write(str(log[1]))