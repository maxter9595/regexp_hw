import re
import csv


""" Список функций

1. open_csv - открытие csv файла
    ввод: path - путь к файлу, encoding - кодировка
    вывод: contacts_list - список контактных данных

2. modify_name - заполнение столбцов lastname, firstname, surname
    ввод: contacts_list - текущий список контактных данных
    вывод: измененный список контактных данных
    
3. modify_telephone - корректировка телефонных данных
    ввод: contacts_list - текущий список контактных данных
    вывод: измененный список контактных данных

4. correct_similar_name - учет одинаковых ФИО
    ввод: contacts_list - текущий список контактных данных
    вывод: измененный список контактных данных

5. write_csv - запись данных
    ввод: path - путь к файлу, contacts_list - список контактных данных,
    encoding - кодировка

"""

def open_csv(path:str, encoding:str="utf-8") -> list:
    with open(path, encoding=encoding) as f:
        rows = csv.reader(f, delimiter=",")
        contacts_list = list(rows)
    return contacts_list

def modify_name(contacts_list:list) -> list:
    for i, contact_list in enumerate(contacts_list[1:], start=1):
        name_str = contact_list[:3]
        name_list = " ".join(name_str).strip(" ").split()
        name_list.extend([""]*(len(name_str)-len(name_list)))
        contacts_list[i] = name_list+contact_list[3:]
    return contacts_list

def modify_telephone(contacts_list:list) -> list:
    pattern=r"(\+7|8)?(\s*|\s*\()?(\d{3})(\)\s*|\s*|-)?(\d{3})(\s*|-)?"\
            "(\d{2})(\s*|-)?(\d{2})\s*(\w+.|\(\w+.)?\s*(\d+)?(\))?"
    for contact_list in contacts_list[1:]:
        telephone = contact_list[5]
        result = re.sub(pattern,r"+7(\3)\5-\7-\9 доб.\11",telephone)
        if result:
            idx_loc = result.index('доб.')
            if result[idx_loc:] == 'доб.':
                contact_list[5] = result[:idx_loc-1]
            else:
                contact_list[5] = result
        else:
            contact_list[5] = ''
    return contacts_list

def correct_similar_name(contacts_list:list) -> list:
    dict_data, col_list = {}, contacts_list[0]
    for contact_list in contacts_list[1:]:
        name = ' '.join(contact_list[:3])
        similarity_list = [n for n in dict_data.keys() 
                            if name in n or n in name]
        if similarity_list:
            for my_col, val in zip(col_list, contact_list):
                if val:
                    dict_data[similarity_list[0]][my_col] = val
        else:
            dict_data[name] = dict(zip(col_list, contact_list))
    return [col_list] + [list(dict_data.get(k).values()) 
                        for k in dict_data.keys()]

def write_csv(path:str, contacts_list:list, encoding:str="utf-8"):
    with open(path, "w", encoding=encoding) as f:
        datawriter = csv.writer(f, delimiter=',')
        datawriter.writerows(contacts_list)


if __name__ == '__main__':
    contacts_list = open_csv("phonebook_raw.csv")
    contacts_list = modify_name(contacts_list)
    contacts_list = modify_telephone(contacts_list)
    contacts_list = correct_similar_name(contacts_list)
    write_csv("phonebook.csv",contacts_list)