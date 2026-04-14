"""Utility functions for string operations."""


def reverse_string(s):
    return s[::-1]


def count_vowels(s):
    vowels = "aeiouAEIOU"
    return sum(1 for char in s if char in vowels)


def is_palindrome(s):
    cleaned = s.lower().replace(" ", "")
    return cleaned == cleaned[::-1]


def capitalize_words(s):
    return " ".join(word.capitalize() for word in s.split())


if __name__ == "__main__":
    print("String Utils Demo")
    print(f"Reverse 'hello': {reverse_string('hello')}")
    print(f"Vowels in 'hello world': {count_vowels('hello world')}")
    print(f"Is 'racecar' palindrome: {is_palindrome('racecar')}")
    print(f"Capitalize 'hello world': {capitalize_words('hello world')}")
