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
            # shingles.append(int(hashlib.sha1(shingle.encode('utf-8')).hexdigest(), 16) % (10 ** 8))
            # shingles.append(int(hashlib.sha1(shingle.encode('utf-8')).hexdigest(), 16))
            shingles.append(hash(shingle))

        return list(dict.fromkeys(shingles))
    

    def __init__(self, text: str, k: int) -> None:
        self.shingles = self.k_shingle(text, k)


class CompareSets():

    jaccard_similarity = -1

    def compare(self, set1: list, set2: list) -> float:
        intersection = len(list(set(set1).intersection(set2)))
        union = len(list(dict.fromkeys(set(set1 + set2))))
        jaccard_similarity =  intersection / union
        return round(jaccard_similarity, 3)

    def __init__(self, set1: list, set2: list) -> None:
        self.jaccard_similarity = self.compare(set1, set2)


def generate_random_coefficients(k):
    import random
    # 2^32 can be the max id
    max_shingle_id = 2**32 - 1
    rand_list = []
    while k > 0:
        rand_index = random.randint(0, max_shingle_id)
        while rand_index in rand_list:
            rand_index = random.randint(0, max_shingle_id)
        rand_list.append(rand_index)
        k -= 1
    return rand_list


class MinHashing():
    """
    Builds a minHash signature (in the form of a vector or a set) of a given
    length n from a given set of integers (a set of hashed shingles).
    """

    signature = None

    def get_signature2(self, n, shingles, a: list, b: list):
        # c constant should be a prime greater than max_shingle_id so no collisions occur
        big_prime = 4294967311

        # hash function h(x) = (a*x + b) % c like in the book
        
        # the result (should be returned)
        signature = []

        for i in range(0, n):
            min_hash_code = big_prime + 1

            for shingle in shingles:
                hash_code = (a[i] * shingle + b[i]) % big_prime
            
                if hash_code < min_hash_code:
                    min_hash_code = hash_code
            
            signature.append(min_hash_code)

        return signature


    def __init__(self, n: int, shingles, a: list, b: list) -> None:
        # self.signature = self.get_signature(n, shingles)
        self.signature = self.get_signature2(n, shingles, a, b)


class CompareSignatures():
    """
    A class CompareSignatures that estimates similarity of two integer vectors –
    minhash signatures – as a fraction of components, in which they agree.
    """
    estimation = -1

    def compare(self, set1: list, set2: list, n) -> float:
        count = 0
        # count the number of positions in the minhash signature which are equal.

        for k in range(0, n):
            count = count + (set1[k] == set2[k])

        return count/n

    def __init__(self, set1: list, set2: list, n: int) -> None:
        self.estimation = self.compare(set1, set2, n)


def main():    
    # hashing tutorial: https://www.pythoncentral.io/hashing-strings-with-python/
    # https://stackoverflow.com/questions/16008670/how-to-hash-a-string-into-8-digits

    print('Testing Shingling')
    num_words = 50
    k_shingle = 4
    s1 = Shingling(' '.join([str(i) for i in range(num_words)]), k_shingle)
    s2 = Shingling(' '.join([str(round(i+num_words/2)) for i in range(num_words)]), k_shingle)
    # print(s1.shingles)
    # print(s2.shingles)
    print('Amount of shingles in s1 and s2:', len(s1.shingles))
    print()

    print('Testing CompareSets')
    c = CompareSets(s1.shingles, s2.shingles)
    print('Jaccard similarity:', c.jaccard_similarity)
    print()

    print('Testing MinHashing')
    n = 20                                          # number of hash functions
    a = generate_random_coefficients(n)             # init coeff for hash funcs
    b = generate_random_coefficients(n)
    mh1 = MinHashing(n, s1.shingles, a, b)
    mh2 = MinHashing(n, s2.shingles, a, b)
    print(mh1.signature)
    print(mh2.signature)
    print()

    print('Testing ComparingSignatures')
    c = CompareSignatures(mh1.signature, mh2.signature, n)
    print('Jaccard similarity estimation:', c.estimation)
main()