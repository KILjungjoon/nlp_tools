from tools import GramTools
import csv

def get_csv_content(csvfile, column_name):
    with open(csvfile, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        contents = [row[column_name] for row in reader]
        contents = '\n'.join(contents)
    return contents

csvfile     = './sample_csv.csv'
column_name = 'comment'

contents = get_csv_content(csvfile, column_name)
g = GramTools(contents, remove_symbles='')
uni_gram = g.get_n_gram_freq(1)
g.save('./result_csv_uni_gram.json', uni_gram)
