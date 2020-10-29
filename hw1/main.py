class Shingling():

    shingles = []

    def k_shingle(self, text, k: int) -> list:
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

    def compare(self, set1: list, set2: list) -> float:
        intersection = len(list(set(set1).intersection(set2)))
        union = len(list(dict.fromkeys(set(set1 + set2))))
        jaccard_similarity =  intersection / union
        return jaccard_similarity

    def __init__(self, set1: list, set2: list) -> None:
        self.jaccard_similarity = self.compare(set1, set2)


class MinHashing():
    """
    Builds a minHash signature (in the form of a vector or a set) of a given
    length n from a given set of integers (a set of hashed shingles).
    """

    signature = None

    def get_signature(self, n, shingles):
        import hashlib

        def hashWith(alg, i):
            return int(hashlib.new(alg, str(i).encode('UTF-8')).hexdigest(), 16)

        algorithms = ['sha3_224', 'sha3_256', 'sha1', 'sha512', 'sha3_384',
          'sha3_512', 'sha256', 'md5', 'sha224', 'blake2b', 'blake2s', 'sha384']
        print(len(algorithms))
        
        # iterate over hash functions and compute h_min(s) for the set.
        signature = [min(hashWith(alg, i) for i in shingles) for alg in algorithms[0:n]]
        print(len(signature))
        return signature

    def __init__(self, n: int, shingles) -> None:
        self.signature = self.get_signature(n, shingles)


class CompareSignatures():
    """
    A class CompareSignatures that estimates similarity of two integer vectors –
    minhash signatures – as a fraction of components, in which they agree.
    """
    jaccard_similarity = -1

    def compare(self, set1: list, set2: list) -> float:
        intersection = len(list(set(set1).intersection(set2)))
        union = len(list(dict.fromkeys(set(set1 + set2))))
        jaccard_similarity =  intersection / union
        return jaccard_similarity

    def __init__(self, set1: list, set2: list) -> None:
        self.jaccard_similarity = self.compare(set1, set2)


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
    c = CompareSets(s1.shingles, s2.shingles)
    print(c.jaccard_similarity)
    print()

    # print('Testing MinHashing')
    # # n can be between 1 and 12
    # mh = MinHashing(10, x.shingles)
    # print(mh.signature)
    # print()

    print('Testing ComparingSignatures')
    s1 = Shingling('1 2 3 4 5 6 7', 3)
    s2 = Shingling('3 4 5 6 7 8 9', 3)
    c = CompareSignatures(s1.shingles, s2.shingles)
    print(c.jaccard_similarity)
main()