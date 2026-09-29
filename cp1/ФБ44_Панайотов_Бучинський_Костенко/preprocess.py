import os
import re

RUS_ALPHABET = "абвгдежзийклмнопрстуфхцчшщъыьэюя"
ALLOWED_CHARS = set(RUS_ALPHABET)


def clean_text(text: str, keep_spaces: bool = True) -> str:
    """
    Правила попередньої обробки тексту:
    1. Переведення всіх літер до нижнього регістру.
    2. Заміна літери 'ё' на 'е'.
    3. Заміна всіх символів, що не належать до алфавіту, на пробіли.
    4. Зведення послідовностей пробілів до одного пробілу та обрізання країв.
    5. За необхідності (keep_spaces=False) — повне вилучення всіх пробілів.
    """
    text = text.lower().replace("ё", "е")

    chars = []
    for ch in text:
        if ch in ALLOWED_CHARS:
            chars.append(ch)
        else:
            chars.append(" ")

    normalized = " ".join("".join(chars).split())

    if not keep_spaces:
        normalized = normalized.replace(" ", "")

    return normalized


def prepare_datasets(input_path: str, output_dir: str):
    with open(input_path, "r", encoding="utf-8") as f:
        raw_text = f.read()

    os.makedirs(output_dir, exist_ok=True)

    text_sp = clean_text(raw_text, keep_spaces=True)
    text_nosp = clean_text(raw_text, keep_spaces=False)

    path_sp = os.path.join(output_dir, "text_with_spaces.txt")
    path_nosp = os.path.join(output_dir, "text_without_spaces.txt")

    with open(path_sp, "w", encoding="utf-8") as f:
        f.write(text_sp)

    with open(path_nosp, "w", encoding="utf-8") as f:
        f.write(text_nosp)

    return {
        "raw_length": len(raw_text),
        "with_spaces_len": len(text_sp),
        "without_spaces_len": len(text_nosp),
        "chars_with_spaces": len(set(text_sp)),
        "chars_without_spaces": len(set(text_nosp)),
    }


if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.abspath(__file__))
    raw_path = os.path.join(base_dir, "data", "raw_text.txt")
    out_dir = os.path.join(base_dir, "data")

    stats = prepare_datasets(raw_path, out_dir)
    print("Результати нормалізації:")
    print(f"  Вхідний текст: {stats['raw_length']} символів")
    print(f"  Текст з пробілами: {stats['with_spaces_len']} символів (алфавіт: {stats['chars_with_spaces']})")
    print(f"  Текст без пробілів: {stats['without_spaces_len']} символів (алфавіт: {stats['chars_without_spaces']})")
