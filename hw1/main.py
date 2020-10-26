class Shingling():

    shingles = []

    def k_shingle(self, text: str, k: int) -> list:
        import string
        import hashlib

        # shingles = set()
        shingles = []

        text = text.translate(str.maketrans('', '', string.punctuation)).split(' ')

        for index in range(len(text)-k+1):
            # shingles.add(' '.join([text[index+i] for i in range(k)]))
            shingle = ' '.join([text[index+i] for i in range(k)])
            bytes_shingle = bytes(shingle, encoding='utf-8')
            hashed = hashlib.md5(bytes_shingle).hexdigest()
            shingles.append(hashed)

        return list(dict.fromkeys(shingles))
    

    def __init__(self, text: str) -> None:
        self.shingles = self.k_shingle(text, 5)

x = Shingling('Hey, I got this stupid text that I wrote!')
print(x.shingles)

# hashing tutorial: https://www.pythoncentral.io/hashing-strings-with-python/

class CompareSets():

    jaccard_similarity = -1

    def compare(set1: Shingling, set2: Shingling) -> int:
        jaccard_similarity = -1
        return jaccard_similarity

    def __init__(self, set1: Shingling, set2: Shingling) -> None:
        self.jaccard_similarity = self.compare(set1, set2)