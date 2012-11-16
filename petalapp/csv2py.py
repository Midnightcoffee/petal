

import csv
from petalapp import tools
def convertor(afile):
    """ extracts hospital_name and hospital data"""
    #TODO get area to?
    hospital_table = []
    with open(afile, 'rb') as csv_file:
        line_reader = csv.reader(csv_file, delimiter=',')
        for line in line_reader:
            hospital_row = []
            for i,v in enumerate(line):
                if (i >= 8 and i < 24) or (i==2):
                    if v == '':
                        v = 0
                    elif v.isdigit():
                        v = int(v)
                    hospital_row.append(v)
            hospital_table.append(hospital_row)
    return hospital_table


def prep(file_name, title_ext="", which_quarter=""):
    hospital_table = convertor(file_name)
    table = []
    for row in hospital_table:
        row = [title_ext] + [which_quarter] + [row[0]] + [row[1:]]
        table.append(row)
    return table

def pre_s3(file_name, title_ext="", which_quarter=""):
    hospital_table = prep(file_name, title_ext,which_quarter)
    for row in hospital_table:
        tools.upload_s3(row[0]+row[1]+row[2],row)

pre_s3("PCIbase.csv","Baseline")

