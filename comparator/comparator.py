import os

#cur_path = os.getcwd()
cur_path = "C:\\Users\\mrogozhyn\\Desktop\\test folder\\folder 1\\folder 1_1"

print("Curren directory:", cur_path)
print("Curren directory files:", os.listdir(cur_path))

names_dict = {}
for name in os.listdir(cur_path):
    if os.path.isfile(os.path.join(cur_path, name)):
        names_dict[name] = {"File name": os.path.splitext(name)[0],
                            "File extension" : os.path.splitext(os.path.join(cur_path, name))[1][1:],
                            "File size" : os.path.getsize(os.path.join(cur_path, name)),
                            "File mod. time" : os.path.getmtime(os.path.join(cur_path, name))}

idw_list = []
pdf_list = []
for name in names_dict:
    if names_dict[name]["File extension"] == "idw":
        idw_list.append(names_dict[name]["File name"])
    elif names_dict[name]["File extension"] == "pdf":
        pdf_list.append(names_dict[name]["File name"])

print("idw files: ", idw_list)
print("pdf files: ", pdf_list)
input('')