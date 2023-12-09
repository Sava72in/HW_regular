import csv
import re


def format_phone(phone):
    digits = re.findall(r'\d', phone)

    if len(digits) >= 10:
        print(phone)
        formatted_phone = f"+7({''.join(digits[-10:-7])}){''.join(digits[-7:-4])}-{''.join(digits[-4:])}"
        extension = re.findall(r"(.доб\. \d+.)", phone)
        if extension:
            clean = extension[0].replace('(', '').replace(')', '')
            formatted_phone += f' {clean}'
        print(formatted_phone)
        return formatted_phone
    else:
        return None


def combine_phones(phones):
    formatted_phones = []
    for phone in phones:
        formatted = format_phone(phone)
        if formatted:
            formatted_phones.append(formatted)
    return ', '.join(formatted_phones)


with open('files/phonebook_raw.csv', newline='', encoding='utf-8-sig') as csvfile:
    reader = csv.DictReader(csvfile, delimiter=';')

    unique_records = {}

    for row in reader:
        if ' ' in row['lastname'] and row['firstname'] == '' and row['surname'] == '':
            full_name = row['lastname'].split(' ')
            if len(full_name) == 3:
                row['lastname'], row['firstname'], row['surname'] = full_name
            elif len(full_name) == 2:
                row['lastname'], row['firstname'] = full_name
            elif len(full_name) == 1:
                row['lastname'] = full_name[0]

        key = row['lastname']

        if key in unique_records:
            if row['phone']:
                unique_records[key]['phone'] = combine_phones([unique_records[key]['phone'], row['phone']])

            if row['email'] and unique_records[key]['email']:
                unique_records[key]['email'] += f", {row['email']}"
            elif row['email']:
                unique_records[key]['email'] = row['email']
        else:
            unique_records[key] = row

with open('files/updated_contacts.csv', 'w', newline='', encoding='utf-8-sig') as csvfile:
    fieldnames = ['lastname', 'firstname', 'surname', 'organization', 'position', 'phone', 'email']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=';')
    writer.writeheader()

    for record in unique_records.values():
        record['phone'] = format_phone(record['phone'])
        writer.writerow(record)
