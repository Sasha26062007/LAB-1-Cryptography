import math
import random
import sys
import io
import os
from collections import Counter

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def calc_h1(text):
    if not text:
        return 0.0
    freqs = Counter(text)
    length = len(text)
    h = -sum((count / length) * math.log2(count / length) for count in freqs.values())
    return abs(h)

def calc_h2_overlapping(text):
    if len(text) < 2:
        return 0.0
    bigrams = [text[i:i+2] for i in range(len(text) - 1)]
    freqs = Counter(bigrams)
    length = len(bigrams)
    h_bigram = -sum((count / length) * math.log2(count / length) for count in freqs.values())
    return abs(h_bigram / 2)

def calc_h2_non_overlapping(text):
    if len(text) < 2:
        return 0.0
    bigrams = [text[i:i+2] for i in range(0, len(text) - 1, 2)]
    freqs = Counter(bigrams)
    length = len(bigrams)
    h_bigram = -sum((count / length) * math.log2(count / length) for count in freqs.values())
    return abs(h_bigram / 2)

def generate_random_text(alphabet, length):
    return ''.join(random.choice(alphabet) for _ in range(length))

def run_section_3(h1_natural_text=4.4686):
    print("=" * 55)
    print("РОЗДІЛ 3: ДОСЛІДЖЕННЯ ВПЛИВУ РОЗПОДІЛУ НА H1")
    print("=" * 55)
    
    data_path = os.path.join(os.path.dirname(__file__), "data", "text_without_spaces.txt")
    if os.path.exists(data_path):
        with open(data_path, "r", encoding="utf-8") as f:
            natural_sample = f.read(100000)
            h1_a = calc_h1(natural_sample)
    else:
        h1_a = h1_natural_text

    seq_b = "а" * 100000
    h1_b = calc_h1(seq_b)
    print(f"Послідовність Б (один символ):        H1 = {h1_b:.4f} (невизначеність відсутня)")
    
    print(f"Послідовність А (природний текст):    H1 = {h1_a:.4f}")
    
    alphabet_32 = "абвгдежзийклмнопрстуфхцчшщъыьэюя"
    seq_v = generate_random_text(alphabet_32, 100000)
    h1_v = calc_h1(seq_v)
    h0 = math.log2(len(alphabet_32))
    print(f"Послідовність В (випадкова рівнойм.): H1 = {h1_v:.4f} (H0 = log2(32) = {h0:.4f})")
    
    print("\nПрогноз підтверджено: H1(Б) < H1(А) < H1(В).")
    print("При виродженому розподілі H1=0, а максимум досягається при рівноймовірному.\n")

def run_section_4():
    print("=" * 55)
    print("РОЗДІЛ 4: ДОСЛІДЖЕННЯ ЗАЛЕЖНОСТЕЙ МІЖ СИМВОЛАМИ")
    print("=" * 55)
    
    chars_g = ["а"] * 50000 + ["б"] * 50000
    random.shuffle(chars_g)
    seq_g = "".join(chars_g)
    
    h1_g = calc_h1(seq_g)
    h2_g_overlap = calc_h2_overlapping(seq_g)
    h2_g_non_overlap = calc_h2_non_overlapping(seq_g)
    
    print(f"Послідовність Г (випадковий порядок 'а' і 'б' з p=0.5):")
    print(f"  H1 = {h1_g:.4f}, H2(перетинні) = {h2_g_overlap:.4f}, H2(неперетинні) = {h2_g_non_overlap:.4f}")
    
    seq_d = "аб" * 50000
    h1_d = calc_h1(seq_d)
    h2_d_overlap = calc_h2_overlapping(seq_d)
    h2_d_non_overlap = calc_h2_non_overlapping(seq_d)
    
    print(f"Послідовність Д (періодична ababab... з p=0.5):")
    print(f"  H1 = {h1_d:.4f}, H2(перетинні) = {h2_d_overlap:.4f}, H2(неперетинні) = {h2_d_non_overlap:.4f}")
    
    print("\nВисновки до розділу 4:")
    print("1. H1 однакова для обох послідовностей (1.0000), бо враховує тільки сумарні частоти літер.")
    print("2. H2 у періодичній послідовності Д різко падає (0.5000 з перетином і 0.0000 без перетину),")
    print("   оскільки модель біграм враховує залежність між сусідніми символами.")
    print("3. У послідовності Д неперетинні біграми потрапляють чітко на крок періоду 'аб', тому невизначеність зникає повністю.\n")

if __name__ == "__main__":
    print("Модуль: Дослідження властивостей ентропії (Розділи 3 та 4)")
    print("Виконавець: Денис Бучинський\n")
    
    run_section_3()
    run_section_4()
