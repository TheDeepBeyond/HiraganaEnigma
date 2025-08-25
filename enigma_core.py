BASE = list("あいうえおかきくけこさしすせそたちつてとなにぬねのはひふへほまみむめもやゆよらりるれろわをんがぎぐげござじずぜぞだぢづでどばびぶべぼぱぴぷぺぽぁぃぅぇぉゃゅょっ")

class Enigma:
    def __init__(self, wiring=None, position=0):
        self.wiring = wiring if wiring else self._generate_wiring()
        self.position = position
        self.N = len(BASE)

    def _generate_wiring(self):
        import random
        shuffled = BASE[:]
        random.shuffle(shuffled)
        return shuffled

    def encrypt(self, plain_text):
        result = ""
        pos = self.position
        for char in plain_text:
            try:
                idx = BASE.index(char)
            except ValueError:
                continue
            cipher_idx = (idx + pos) % self.N
            result += self.wiring[cipher_idx]
            pos = (pos + 1) % self.N
        return result

    def decrypt(self, cipher_text):
        result = ""
        pos = self.position
        for char in cipher_text:
            try:
                idx = self.wiring.index(char)
            except ValueError:
                continue
            original_idx = (idx - pos) % self.N
            result += BASE[original_idx]
            pos = (pos + 1) % self.N
        return result

    def export_key(self):
        return {
            "wiring": self.wiring,
            "position": self.position
        }

    @staticmethod
    def import_key(key_data):
        return Enigma(wiring=key_data["wiring"], position=key_data["position"])

    @classmethod
    def max_position(cls):
        return len(BASE) - 1