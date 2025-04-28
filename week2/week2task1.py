def encode_message(message, shift):
    encoded = ""
    for char in message:
        if char.isalpha():
            shift_base = ord('A') if char.isupper() else ord('a')
            new_char = chr((ord(char) - shift_base + shift) % 26 + shift_base)
            encoded += new_char
        else:
            encoded += char
    return encoded

def decode_message(message, shift):
    return encode_message(message, -shift)

def get_user_choice():
    print("\n--- Secret Code Generator ---")
    print("1. Encode a message")
    print("2. Decode a message")
    print("3. Exit")
    choice = input("Enter your choice (1/2/3): ")
    return choice

def get_message_and_shift():
    message = input("Enter your message: ")
    while True:
        try:
            shift = int(input("Enter shift number (integer): "))
            break
        except ValueError:
            print("Invalid input. Please enter an integer for the shift.")
    return message, shift

def main():
    while True:
        choice = get_user_choice()

        if choice == '1':
            message, shift = get_message_and_shift()
            encoded = encode_message(message, shift)
            print(f"Encoded Message: {encoded}")
        elif choice == '2':
            message, shift = get_message_and_shift()
            decoded = decode_message(message, shift)
            print(f"Decoded Message: {decoded}")
        elif choice == '3':
            print("Exiting the program. Goodbye!")
            break
        else:
            print("Invalid choice. Please select 1, 2, or 3.")

if __name__ == "__main__":
    main()
