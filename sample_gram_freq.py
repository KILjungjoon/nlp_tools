from tools import GramTools

with open('./sample_comtent.txt', 'r', encoding='utf-8') as f:
    text = f.read()
g = GramTools(text, remove_symbles='.?')
uni_gram = g.get_n_gram_freq(1)
g.save('./result_uni_gram.json', uni_gram)
