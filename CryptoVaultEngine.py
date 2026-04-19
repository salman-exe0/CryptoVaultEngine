import os
import json
import heapq
import hashlib


class HuffmanNode:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq


class FileHandler:
    def __init__(self):
        self.vault_extension = ".salman"
        self.header_size_bytes = 4
        self.valid_formats = [".txt", ".py", ".md", ".cpp"]
        self.encoding = "utf-8"

    def readTextFile(self, filePath):
        try:
            with open(filePath, mode="r", encoding="utf-8") as myFile:
                fileData = myFile.read()
                return fileData
        except FileNotFoundError:
            print("File Not Found!..")
            return None

    def writeVaultFile(self, file_path, header, tree_data, encrypted_payload):
        base = os.path.splitext(file_path)[0]
        vaultPath = base + self.vault_extension
        vaultData = {
            "header": header,
            "tree": tree_data,
            "payload": list(encrypted_payload),
        }
        with open(vaultPath, mode="w", encoding=self.encoding) as vaultFile:
            vaultFile.write(json.dumps(vaultData))
            return vaultPath

    def read_vault_file(self, file_path):
        try:
            with open(file_path, mode="r", encoding=self.encoding) as file:
                vaultData = json.loads(file.read())
                header = vaultData["header"]
                treeData = vaultData["tree"]
                payload = bytes(vaultData["payload"])
                return header, treeData, payload
        except FileNotFoundError:
            print("Vault File Not Found")
            return None, None, None

    def write_decoded_file(self, file_path, original_text):
        with open(file_path, mode="w", encoding=self.encoding) as decodedFile:
            decodedFile.write(original_text)
            print(f"File Saved: {file_path}")


class DataCompressor:
    def build_frequency_table(self, text):
        freq = {}
        for char in text:
            if char in freq:
                freq[char] += 1
            else:
                freq[char] = 1
        return freq

    def build_huffman_tree(self, freq_table):
        heap = []
        for char, freq in freq_table.items():
            node = HuffmanNode(char, freq)
            heapq.heappush(heap, node)
        while len(heap) > 1:
            left = heapq.heappop(heap)
            right = heapq.heappop(heap)
            parent = HuffmanNode(None, left.freq + right.freq)
            parent.left = left
            parent.right = right
            heapq.heappush(heap, parent)
        return heap[0]

    def build_codes(self, root):
        codes = {}

        def _generate(node, current_code):
            if node is None:
                return
            if node.char is not None:  # leaf node
                codes[node.char] = current_code
                return
            _generate(node.left, current_code + "0")
            _generate(node.right, current_code + "1")

        _generate(root, "")
        return codes

    def compress(self, text):
        freq = self.build_frequency_table(text)
        root = self.build_huffman_tree(freq)
        codes = self.build_codes(root)
        binary_str = ""
        for char in text:
            binary_str += codes[char]
        padding = 8 - (len(binary_str) % 8)
        if padding == 8:
            padding = 0
        binary_str += "0" * padding
        compressed_bytes = bytearray()
        for i in range(0, len(binary_str), 8):
            byte = binary_str[i : i + 8]
            compressed_bytes.append(int(byte, 2))
        return bytes(compressed_bytes), padding, codes

    def decompress(self, compressed_bytes, padding, codes):
        binary_str = ""
        for byte in compressed_bytes:
            binary_str += format(byte, "08b")
        if padding > 0:
            binary_str = binary_str[:-padding]
        reverse_codes = {v: k for k, v in codes.items()}
        text = ""
        current = ""
        for bit in binary_str:
            current += bit
            if current in reverse_codes:
                text += reverse_codes[current]
                current = ""
        return text


class SecurityEngine:
    def hash_password(self, password):
        hashed = hashlib.sha256(password.encode("utf-8")).hexdigest()
        return hashed

    def verify_password(self, password, stored_hash):
        return self.hash_password(password) == stored_hash

    def encrypt(self, data_bytes, key_hash):
        key = key_hash.encode("utf-8")
        encrypted = bytearray()
        for i, byte in enumerate(data_bytes):
            encrypted_byte = byte ^ key[i % len(key)]
            encrypted.append(encrypted_byte)
        return bytes(encrypted)

    def decrypt(self, encrypted_bytes, key_hash):
        return self.encrypt(encrypted_bytes, key_hash)


class VaultController:
    def __init__(self):
        self.file_handler = FileHandler()
        self.compressor = DataCompressor()
        self.security_engine = SecurityEngine()

    def lock(self, file_path, password):
        text = self.file_handler.readTextFile(file_path)
        if text is None:
            return
        comp_bytes, padding, codes = self.compressor.compress(text)
        key_hash = self.security_engine.hash_password(password)
        encrypted = self.security_engine.encrypt(comp_bytes, key_hash)
        original_extension = os.path.splitext(file_path)[1]
        header = {"padding": padding, "pass_check": key_hash[:16], "original_extension": original_extension}
        vault_path = self.file_handler.writeVaultFile(
            file_path, header, codes, encrypted
        )
        print(f"File Locked: {vault_path}")

    def unlock(self, vault_path, password):
        header, codes, payload = self.file_handler.read_vault_file(vault_path)
        if header is None:
            return
        key_hash = self.security_engine.hash_password(password)
        if key_hash[:16] != header["pass_check"]:
            print("File Unlocked")
            return
        decrypted = self.security_engine.decrypt(payload, key_hash)
        original_text = self.compressor.decompress(decrypted, header["padding"], codes)
        original_extension = header.get("original_extension", ".txt")  # fallback to .txt if not found
        output_path = vault_path.replace(self.file_handler.vault_extension, original_extension)
        self.file_handler.write_decoded_file(output_path, original_text)
        print(f"File Unlocked: {output_path}")

    def run(self):
        print("=== CryptoVault Engine ===")
        while True:
            print("\n[1] Lock File")
            print("[2] Unlock File")
            print("[3] Exit")
            choice = input("Choice: ").strip()
            if choice == "1":
                path = input("File path: ").strip()
                pwd = input("Password: ").strip()
                self.lock(path, pwd)
            elif choice == "2":
                path = input("Vault file path: ").strip()
                pwd = input("Password: ").strip()
                self.unlock(path, pwd)
            elif choice == "3":
                print("Good Bye!")
                break
            else:
                print("Wrong choice!")


if __name__ == "__main__":
    vault = VaultController()
    vault.run()
