import re
from unidecode import unidecode


def normalize_text(text):
    # Приведение текста к нижнему регистру и удаление специальных символов
    normalized_text = unidecode(text).lower()
    normalized_text = re.sub(r'\W+', '', normalized_text)
    return normalized_text


def find_similar_words(word_list, search_word):
    # Нормализация искомого слова
    normalized_search_word = normalize_text(search_word)

    # Поиск и вывод похожих слов
    similar_words = [word for word in word_list if normalized_search_word in normalize_text(word)]
    return similar_words


# Пример использования
word_list = ["Привет", "Hello", "Hola", "Bonjour!", "Ciao", "priv", "Приветик", "Héllo", "Hallo"]
search_word = "Привет"

similar_words = find_similar_words(word_list, search_word)
print("Похожие слова:", similar_words)
