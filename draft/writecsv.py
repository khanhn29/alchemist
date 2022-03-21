import csv  

header = ['name', 'area', 'country_code2', 'country_code3']
data = [['Afghanistan', 652090, 'AF', 'AFG'],
]
data2 = ['Vietnam', 121221, 'VN', 'VND']
print(type(data))
print(type(data2))
data.append(data2)

with open('countries.csv', 'w', encoding='UTF8', newline='') as f:
    writer = csv.writer(f)
    # write the header
    writer.writerow(header)
    for dt in data:
        # write the data
        writer.writerow(dt)