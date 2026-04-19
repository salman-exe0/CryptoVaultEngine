# CryptoVault Engine

A Python-based file encryption and compression utility that combines **Huffman Coding** for data compression with **XOR encryption** for security. Lock your sensitive files with a password and store them in a compact `.salman` vault format.

## Features

✨ **Data Compression**
- Implements Huffman Coding algorithm for optimal text compression
- Reduces file size before encryption for faster processing

🔐 **File Encryption**
- SHA-256 password hashing for secure authentication
- XOR-based encryption using password hash as key
- Password verification before file decryption

📦 **Vault Format**
- Custom `.salman` file extension for encrypted files
- Stores header data (padding, password check), Huffman tree, and encrypted payload
- JSON-based storage for easy portability

⚡ **Simple Interface**
- Interactive menu-driven command-line interface
- Support for multiple file formats (.txt, .py, .md, .cpp)
- UTF-8 encoding support

## How It Works

### Lock (Encryption) Process
1. **Read** the source file
2. **Compress** using Huffman Coding algorithm
   - Analyze character frequency
   - Build binary tree with shortest codes for frequent characters
3. **Encrypt** compressed data using XOR cipher with password hash
4. **Store** in `.salman` vault file with metadata

### Unlock (Decryption) Process
1. **Read** the vault file
2. **Verify** password using stored password hash
3. **Decrypt** using XOR cipher (symmetric operation)
4. **Decompress** using stored Huffman tree
5. **Save** original text to output file

## Installation

### Requirements
- Python 3.7 or higher
- No external dependencies (uses only Python standard library)

### Setup
```bash
# Clone or download the repository
git clone https://github.com/yourusername/CryptoVaultEngine.git
cd CryptoVaultEngine

# Run the application
python CryptoVaultEngine.py
```

## Usage

### Running the Application

```bash
python CryptoVaultEngine.py
```

### Menu Options

```
=== CryptoVault Engine ===

[1] Lock Filw      - Encrypt and compress a file
[2] Unlock File    - Decrypt and decompress a vault file
[3] Exit                - Exit the application
```

### Example: Lock a File

```
Choice: 1
File path: myfile.txt
Password: mysecurepassword
File Locked: myfile.salman
```

### Example: Unlock a File

```
Choice: 2
Vault file path: myfile.salman
Password: mysecurepassword
File Unlocked: myfile.txt
```

## Project Structure

```
CryptoVaultEngine/
├── CryptoVaultEngine.py      # Main application file
└── README.md                 # This file
```

## Core Components

### 1. **HuffmanNode**
Represents a node in the Huffman binary tree for compression hierarchy.

### 2. **FileHandler**
Manages file I/O operations:
- Read plain text files
- Write encrypted vault files
- Read encrypted vault files
- Write decrypted output files

### 3. **DataCompressor**
Implements Huffman compression algorithm:
- `build_frequency_table()` - Analyze character frequencies
- `build_huffman_tree()` - Construct optimal binary tree
- `build_codes()` - Generate variable-length binary codes
- `compress()` - Compress text data
- `decompress()` - Decompress compressed data

### 4. **SecurityEngine**
Handles encryption and authentication:
- `hash_password()` - SHA-256 password hashing
- `verify_password()` - Compare passwords
- `encrypt()` - XOR-based encryption
- `decrypt()` - XOR-based decryption

### 5. **VaultController**
Main controller orchestrating the encryption/decryption workflow:
- `lock()` - Encrypt a file
- `unlock()` - Decrypt a vault file
- `run()` - Interactive menu interface

## Vault File Format

The `.salman` vault file is JSON-formatted with the following structure:

```json
{
  "header": {
    "padding": 6,
    "pass_check": "abcdef1234567890"
  },
  "tree": {
    "char": null,
    "freq": 42,
    "left": {...},
    "right": {...}
  },
  "payload": [26, 192, ...]
}
```

## Supported File Types

- `.txt` - Text files
- `.py` - Python source code
- `.md` - Markdown documentation
- `.cpp` - C++ source code
- *Other text formats can be added*

## Algorithm Details

### Huffman Coding
- **Compression Ratio**: 40-60% reduction for typical text
- **Time Complexity**: O(n log n) where n = number of unique characters
- **Space Complexity**: O(n)

### XOR Encryption
- **Security Level**: Basic encryption (suitable for non-critical data)
- **Key Derivation**: SHA-256 hash of password
- **Block Mode**: Keystream repeats across entire data

## Limitations

⚠️ **Important Security Notes:**
- XOR encryption is basic; not suitable for highly sensitive data
- Password stored as hash check (first 16 chars) - vulnerable to rainbow tables
- No salt used in password hashing - use strong passwords
- For production use, consider AES encryption instead

## Testing

The `huffmanPractice.py` file includes test cases for:
- Binary encoding/decoding
- Huffman compression example
- Padding and byte conversion

Run tests:
```bash
python huffmanPractice.py
```

Expected output:
```
0001101011
Padded Binary:  0001101011000000
Extra Bits:  6
Bytes:  b'\x1a\xc0'
Binary Back:  0001101011000000
After Removing Padding:  0001101011
 Decoded Text:  hello
```

## Future Enhancements

- [ ] Support for binary files (images, videos, etc.)
- [ ] AES encryption instead of XOR
- [ ] Salted password hashing (bcrypt/scrypt)
- [ ] Progress bar for large files
- [ ] Batch file processing
- [ ] GUI interface (tkinter/PyQt)
- [ ] Archive support (.zip integration)

## Contributing

Contributions are welcome! Please feel free to:
1. Fork the repository
2. Create a feature branch
3. Submit a pull request

## License

This project is open source and available under the MIT License.

## Disclaimer

This is an educational project designed to demonstrate encryption and compression concepts. For production use with sensitive data, consider using established cryptographic libraries like `cryptography` or `pycryptodome`.

## Author

Created as a learning project for cryptography and data compression algorithms.

---
