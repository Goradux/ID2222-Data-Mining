class Shingling():

    shingles = []

    def k_shingle(self, text: str, k: int) -> list:
        import string
        import hashlib

        # shingles = set()
        shingles = []

        # strip away punctuation
        text = text.translate(str.maketrans('', '', string.punctuation)).split(' ')

        for index in range(len(text)-k+1):
            # shingles.add(' '.join([text[index+i] for i in range(k)]))
            shingle = ' '.join([text[index+i] for i in range(k)])
            # bytes_shingle = bytes(shingle, encoding='utf-8')
            # hashed = hashlib.md5(bytes_shingle).hexdigest()
            # shingles.append(hashed)
            shingles.append(int(hashlib.sha1(shingle.encode('utf-8')).hexdigest(), 16) % (10 ** 8))

        return list(dict.fromkeys(shingles))
    

    def __init__(self, text: str, k: int) -> None:
        self.shingles = self.k_shingle(text, k)


class CompareSets():

    jaccard_similarity = -1

    def compare(self, set1: Shingling, set2: Shingling) -> int:
        intersection = len(list(set(set1.shingles).intersection(set2.shingles)))
        union = len(list(dict.fromkeys(set(set1.shingles + set2.shingles))))
        jaccard_similarity =  intersection / union
        return jaccard_similarity

    def __init__(self, set1: Shingling, set2: Shingling) -> None:
        self.jaccard_similarity = self.compare(set1, set2)


class MinHashing():
    """
    Builds a minHash signature (in the form of a vector or a set) of a given
    length n from a given set of integers (a set of hashed shingles).
    """

    singature = None

    def get_signature(self):
        pass

    def __init__(self, n: int, shingles) -> None:
        self.singature = self.get_signature()



def main():    
    print('Testing Shingling')
    x = Shingling('Hey, I got this stupid text that I wrote!', 5)
    print(x.shingles)
    print()

    # hashing tutorial: https://www.pythoncentral.io/hashing-strings-with-python/
    # https://stackoverflow.com/questions/16008670/how-to-hash-a-string-into-8-digits

    print('Testing CompareSets')
    s1 = Shingling('1 2 3 4 5 6 7', 3)
    s2 = Shingling('3 4 5 6 7 8 9', 3)
    c = CompareSets(s1, s2)
    print(c.jaccard_similarity)
main()