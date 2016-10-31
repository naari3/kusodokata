# coding: utf-8
import random
import MeCab

class MarkovChainer(object):
    """docstring for MarkovChainer."""
    def __init__(self, n, sentences=None):
        self.n = n
        self.tagger = MeCab.Tagger('-d /usr/local/lib/mecab/dic/ipadic')
        self.morphed = None
        self.grammed = None
        self.chain_dic = None
        if sentences:
            self.morphed = [self.parse_to_morph(s) for s in sentences]
            self.grammed = [self.n_gram(m) for m in self.morphed]
            self.regist_chain_dict(self.grammed)
    def parse_to_morph(self, sentence):
        mecabed = self.tagger.parse(sentence).splitlines()
        morphed = [m.split("\t")[0] for m in mecabed]
        morphed.insert(0, "BOS")
        return morphed
    def n_gram(self, arg):
        grammed = []
        for i in range(len(arg)):
            grammed.append(arg[i:i+self.n])
        return grammed
    def regist_chain_dict(self, grammeds):
        chain_dic = {}
        length = len(grammeds[0][0])
        for grs in grammeds:
            for word in grs:
                if word[0] != "EOS" and not("".join(word[1:]) in chain_dic.get(word[0],["EOS"])):
                    chain_dic.setdefault("".join(word[0:length-1]), []).append(word[1:])
        self.chain_dic = chain_dic
        return chain_dic
    def make_sentence(self, dic=None):
        if not dic:
            dic = self.chain_dic
        sentence = []
        length = len(list(dic.items())[0])
        first_word = "BOS"
        wordstr = random.choice([l for l in list(dic.keys()) if first_word in l])
        sentence.append(wordstr[3:])
        while True:
            word_list = dic.get(wordstr, [["EOS"]])
            words = random.choice(word_list)
            sentence.append("".join(words[1-length:]))
            wordstr = "".join(words)
            if words[-1] == "EOS":
                break
        return "".join(sentence).replace("EOS","")

with open("kuso.txt") as f:
    text = f.read()
    txts = text.split("\n")
mc = MarkovChainer(3, txts)
print(mc.make_sentence())
