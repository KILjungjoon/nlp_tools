import json

class GramTools:
    def __init__(self, text, remove_symbles=''):
        self.text = text
        for symble in remove_symbles:
            self.text = self.text.replace(symble, '')
        self.lines = self.text.split('\n')

    def get_gram_by_line(self, line, n=1):
        gram_list = line.split()
        return [' '.join(gram_list[i:i+n]) for i in range(len(gram_list)-n+1)]

    def get_gram_by_lines(self, n=1, lines=[]):
        lines = lines if lines else self.lines
        n_gram = []
        for line in lines:
            n_gram.extend(self.get_gram_by_line(line, n))
        return n_gram

    def get_freq(self, n_gram):
        freq = {}
        for item in n_gram:
            if (item in freq):
                freq[item] += 1
            else:
                freq[item] = 1
        return freq

    def get_n_gram_freq(self, n):
        n_gram      = self.get_gram_by_lines(n=n)
        n_gram_freq = self.get_freq(n_gram)
        return dict(sorted(n_gram_freq.items(), key=lambda item: item[1], reverse=True))

    def save(self, path, content, indent=4):
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(content, f, indent=indent, ensure_ascii=False)

if __name__=='__main__':
    with open('./simple_comtent.txt', 'r', encoding='utf-8') as f:
        text = f.read()
    g = GramTools(text, '.?')
    uni_gram = g.get_n_gram_freq(1)
    # bi_gram  = g.get_n_gram_freq(2)
    # tri_gram = g.get_n_gram_freq(3)

    g.save('./result_uni_gram.json', uni_gram)
    # g.save('./result_bi_gram.json', bi_gram)
    # g.save('./result_thi_gram.json', tri_gram)
