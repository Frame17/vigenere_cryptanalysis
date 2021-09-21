from collections import Counter
from statistics import mean

MAX_KEY_LENGTH = 8
ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
ENGLISH_FREQUENCIES = [
    0.08167, 0.01492, 0.02782, 0.04253, 0.12702, 0.02228, 0.02015,
    0.06094, 0.06966, 0.00153, 0.00772, 0.04025, 0.02406, 0.06749,
    0.07507, 0.01929, 0.00095, 0.05987, 0.06327, 0.09056, 0.02758,
    0.00978, 0.02360, 0.00150, 0.01974, 0.00074
]


class VigenereCracker:
    def __index_of_coincidence(self, text):
        N = len(text)
        letters_in_text_frequencies = Counter(text)
        sum = 0.0

        for c in ALPHABET:
            f_i = letters_in_text_frequencies[c]
            sum += f_i * (f_i - 1)
        return sum / (N * (N - 1))

    def __determine_key_length(self, cypher):
        key_len_probability = (0, 0.0)
        for i in range(2, MAX_KEY_LENGTH):
            pieces = [[] for _ in range(i)]
            for j, c in enumerate(cypher):
                pieces[j % i].append(c)

            avg_ioc = mean(list(map(lambda piece: self.__index_of_coincidence(''.join(piece)), pieces)))
            if avg_ioc > key_len_probability[1]:
                key_len_probability = (i, avg_ioc)

        return key_len_probability[0]

    def __caesar_decrypt(self, cypher, key):
        result = ''
        for c in cypher:
            shift = ord(c) - key
            if shift < ord('A'):
                shift += ord('Z') - ord('A') + 1

            result += chr(shift)

        return result

    def __chi_squared(self, text):
        N = len(text)
        letters_in_text_frequencies = Counter(text)
        result = 0.0

        for i, c in enumerate(ALPHABET):
            c_i = letters_in_text_frequencies[c]
            e_i = ENGLISH_FREQUENCIES[i]

            result += ((c_i - N * e_i) ** 2) / (N * e_i)

        return result

    def crack(self, cypher):
        key_len = self.__determine_key_length(cypher)

        caesar_pieces = [[] for _ in range(key_len)]
        for i, c in enumerate(cypher):
            caesar_pieces[i % key_len].append(c)

        key = ''
        for piece in caesar_pieces:
            key_char_probability = ('A', self.__chi_squared(self.__caesar_decrypt(piece, 1)))
            for i in range(2, 26):
                caesar = self.__caesar_decrypt(piece, i)
                chi_2 = self.__chi_squared(caesar)
                if chi_2 < key_char_probability[1]:
                    key_char_probability = (ALPHABET[i], chi_2)
            key += key_char_probability[0]

        return key


def vigenere_decrypt(cypher, key):
    i = 0
    N = len(key)
    result = ''

    for c in cypher:
        shift = ord(c) - (ord(key[i % N]) - ord('A'))
        if shift < ord('A'):
            shift += ord('Z') - ord('A') + 1

        result += chr(shift)
        i += 1

    return result


if __name__ == '__main__':
    cracker = VigenereCracker()

    # cypher = 'JSGFCCIHWBFWMGFTKZARYXIOFESNIVWHMBNATQBTTRQOCAXTOGDXAFROERSJELUBTDEZREPXGFAPHFVRXJDCZLNECAPRMPYPHQBQASUBGHLQBEPUGSFEIPMBFEXGBSEHSFZQQAHEEFWARJGBPEMABFELMHNWPAKLZYFCNOHMBQZTFWBYEXZLFRFWYYSIRRWIFSRIMEHVYKQJRYXETBCXTWFLWEWTYQQBGJSGKVWPMRQLYFVRYXUQNEMABFZXTOGLPXCSELQSIPRFGNCIFWROXACAPEZRBYPKCAPYESEELMHHDIDAHDXNSYZKSSQTRFCFPIFVRTVQJRYXEHUTWYSNYWKCHHMXZPCIMHRLVQUVDXDOGTSZTBCQMZBRMZTBCQMBQDIZRNYHDSPPMHSFPWEWBYGACXTIEKUTPQWGTWFSZAXUBTESGGRELQPHTPFWAFWQFPWEEGVYTKHUZRMHYPEEHBELQFYLRSINRIEVNGIEWZTPMFSLGUZVEMQGSZVFVVDEEGVRRYSAECAIJTPXPRCSXZVYKKCHCZQFLZAZOHELQBGTGMHVZRUTNAIDGBYMEBBEPAUTPHUBGSIKKVWPNSBQJQFROEXCTTREQEPIZOAOMRHUPCMFRYSFFRRMEHRCIPMBFAUZYAVAJVOIMKNJJAFGSIYHBDMSBHAAUHUELQWEZAZQUZWQBHDIDBNXIMBQAEEGJZVPPRNEGGRJSGFRIMEHVYKPOGLMEBBEEFHNNLQRGZEGGRCCAIJTPXBRPHFCPCIMHRLYESEQSDMBFVESYQEZRGSIZAVRVMHRELQSKTWFWARHMHNZZQFGZMFAVRVMHVYKPOGLMEDNCXATGSIMGFTKZARYXECLZYIWYWRQSQESPSZZREHELXQQBOIFVNEHASFELQAVRVMHVZRMZBYKIWGSEIFVEXQBFEVMHRRCRCESSIWGTWGGRO'
    cypher = 'vptnvffuntshtarptymjwzirappljmhhqvsubwlzzygvtyitarptyiougxiuydtgzhhvvmumshwkzgstfmekvmpkswdgbilvjljmglmjfqwioiivknulvvfemioiemojtywdsajtwmtcgluysdsumfbieugmvalvxkjduetukatymvkqzhvqvgvptytjwwldyeevquhlulwpkt'.upper()
    key = cracker.crack(cypher)
    print(f'Key: {key}')
    print(f'Message: {vigenere_decrypt(cypher, key)}')
