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

    def get_signature(self, n, shingles, a: list, b: list):
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
        self.signature = self.get_signature(n, shingles, a, b)


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


class LSH():
    """
    A class LSH that implements the LSH technique: given a collection of minhash
    signatures (integer vectors) and a similarity threshold t, the LSH class
    (using banding and hashing) finds all candidate pairs of signatures that
    agree on at least fraction t of their components.
    """
    
    candidate_pairs = []

    def locality_sensitive_hashing(self, sets: list, similarity: float, num_bands: int, num_rows: int):
        # num_bands * num_rows = num_hashes
        # initialize empty buckets for each band
        import collections
        buckets = [[] for _ in range(num_bands)]
        
        for index, signature in enumerate(sets):
            for i in range(0, num_bands):
                # concatenate and hash into a bucket
                chunk = ''.join([str(x) for x in signature[i*num_rows:i*num_rows+num_rows]])
                bucket = hash(chunk) % num_bands
                # document #:
                buckets[bucket].append('Doc #{}'.format(index+1))
        
        # remove duplicates from the buckets
        for i in range(len(buckets)):
            buckets[i] = list(dict.fromkeys(buckets[i]))
        # get rid of buckets that don't have two or more elements
        buckets = [i for i in buckets if len(i) > 1]

        from itertools import combinations
        candidate_candidate_pairs = []
        # construct all of the possible pairs
        for bucket in buckets:
            pairs = [i for i in combinations(bucket, 2)]
            candidate_candidate_pairs += pairs

        # count occurences
        c = collections.Counter(candidate_candidate_pairs)
        indices = []
        for index, value in enumerate(c.values()):
            # print(index, value)
            if (value/(num_bands-1)) >= similarity:
                indices.append(index)
        candidate_pairs = []
        for index, pair in enumerate(c.keys()):
            if index in indices:
                candidate_pairs.append(pair)

        return candidate_pairs


    def __init__(self, sets: list, similarity: float, num_bands: int, num_rows: int) -> None:
        self.candidate_pairs = self.locality_sensitive_hashing(sets, similarity, num_bands, num_rows)


def main():    
    # Simple demo
    print('Testing Shingling')
    num_words = 500
    k_shingle = 9
    s1 = Shingling(' '.join([str(i) for i in range(num_words)]), k_shingle)
    s2 = Shingling(' '.join([str(round(i+num_words/2)) for i in range(num_words)]), k_shingle)      # ~33% JS with s1
    s3 = Shingling(' '.join([str(round(i+num_words/10)) for i in range(num_words)]), k_shingle)     # ~80% JS with s1
    s4 = Shingling(' '.join([str(round(i+num_words*0.8)) for i in range(num_words)]), k_shingle)    # ~10% JS with s1
    # print(s1.shingles)
    # print(s2.shingles)
    print()

    print('Testing CompareSets')
    c12 = CompareSets(s1.shingles, s2.shingles)
    c13 = CompareSets(s1.shingles, s3.shingles)
    c14 = CompareSets(s1.shingles, s4.shingles)
    print('Jaccard similarity of s1 and s2:', c12.jaccard_similarity)
    print('Jaccard similarity of s1 and s3:', c13.jaccard_similarity)
    print('Jaccard similarity of s1 and s4:', c14.jaccard_similarity)
    print()

    print('Testing MinHashing')
    n = 75                                          # number of hash functions
    a = generate_random_coefficients(n)             # init coeff for hash funcs
    b = generate_random_coefficients(n)
    mh1 = MinHashing(n, s1.shingles, a, b)
    mh2 = MinHashing(n, s2.shingles, a, b)
    mh3 = MinHashing(n, s3.shingles, a, b)
    mh4 = MinHashing(n, s4.shingles, a, b)
    # print(mh1.signature)
    # print(mh2.signature)
    print()

    print('Testing ComparingSignatures')
    c12 = CompareSignatures(mh1.signature, mh2.signature, n)
    c13 = CompareSignatures(mh1.signature, mh3.signature, n)
    c14 = CompareSignatures(mh1.signature, mh4.signature, n)
    print('Jaccard similarity estimation of s1 and s2:', c12.estimation)
    print('Jaccard similarity estimation of s1 and s3:', c13.estimation)
    print('Jaccard similarity estimation of s1 and s4:', c14.estimation)
    print()

    print('Testing LSH')
    data_set = [mh1.signature, mh2.signature, mh3.signature, mh4.signature]
    # b*r = n, t = (1/b)^(1/r)
    l = LSH(data_set, 0.6, 15, 5)
    print('Candidate pairs:', l.candidate_pairs)

    
    ############
    # Execution time demo

    # print()
    # print('------------------')
    # print('EXUCITON TIME DEMO')
    # print('------------------')
    # print()
    # import time
    # import glob
    # threshold = 0.8
    # k_shingle = 4
    # num_docs = 300
    # print('For {} documents the execution times are:'.format(num_docs))
    # num_docs_read = 0
    # data = []
    # for f_path in glob.glob('./data/*.txt'):
    #     if num_docs_read >= num_docs:
    #         break
    #     with open(f_path, 'r') as f:
    #         d = f.read().replace('\n', '')
    #         data.append(d)
    #     num_docs_read += 1

    # print('Testing shingles')
    # docs = []
    # start = time.time()
    # for i in range(num_docs):
    #     docs.append(Shingling(data[i], k_shingle))
    # for i in range(len(docs)-1):
    #     for j in range(i+1, len(docs)):
    #         similarity = CompareSets(docs[i].shingles, docs[j].shingles).jaccard_similarity
    #         # if similarity > threshold:
    #             # print('Doc {} is similar to doc {} with JS = {}'.format(i, j, similarity))
    # end = time.time()
    # print('Shingling execution time: {} seconds'.format(round(end-start, 3)))
    # print()

    # print('Testing MinHashing')
    # start = time.time()
    # num_hash_f = 30
    # a = generate_random_coefficients(num_hash_f)             # init coeff for hash funcs
    # b = generate_random_coefficients(num_hash_f)
    # docs_minhash = []
    # for i in range(num_docs):
    #     docs_minhash.append(MinHashing(num_hash_f, docs[i].shingles, a, b))
    # for i in range(len(docs_minhash)-1):
    #     for j in range(i+1, len(docs_minhash)):
    #         similarity = CompareSignatures(docs_minhash[i].signature, docs_minhash[j].signature, num_hash_f).estimation
    #         # if similarity > threshold:
    #             # print('Doc {} is similar to doc {} with JS = {}'.format(i, j, similarity))
    # end = time.time()
    # print('MinHashing execution time: {} seconds'.format(round(end-start, 3)))
    # print()

    # print('Testing LSH')
    # start = time.time()
    # lsh = LSH([i.signature for i in docs_minhash], 0.8, 10, 3)
    # end = time.time()
    # print('MinHashing execution time: {} seconds'.format(round(end-start, 3)))

main()