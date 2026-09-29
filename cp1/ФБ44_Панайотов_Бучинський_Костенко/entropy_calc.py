import os
import math
import csv
from collections import Counter


def calc_monograms(text: str):
    total = len(text)
    counts = Counter(text)
    freqs = {}
    h1 = 0.0

    for ch, count in counts.items():
        p = count / total
        freqs[ch] = {
            "count": count,
            "probability": p,
        }
        h1 -= p * math.log2(p)

    return h1, freqs


def calc_bigrams(text: str, step: int):
    # step=1: перетинні біграми (overlapping)
    # step=2: неперетинні біграми (non-overlapping)
    bigrams = [text[i:i+2] for i in range(0, len(text) - 1, step) if len(text[i:i+2]) == 2]
    total = len(bigrams)
    counts = Counter(bigrams)
    freqs = {}
    h2_sum = 0.0

    for bg, count in counts.items():
        p = count / total
        freqs[bg] = {
            "count": count,
            "probability": p,
        }
        h2_sum -= p * math.log2(p)

    # Питома ентропія на один символ H2 = H(bigram) / 2
    h2 = h2_sum / 2.0
    return h2, freqs


def save_frequencies_csv(freqs: dict, filename: str, is_bigram: bool = False):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    header = ["bigram" if is_bigram else "character", "count", "probability"]
    sorted_items = sorted(freqs.items(), key=lambda x: x[1]["count"], reverse=True)

    with open(filename, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        for key, info in sorted_items:
            # Для пробілу вказуємо позначення [SPACE], щоб у CSV було зручно читати
            disp_key = "[SPACE]" if key == " " else key
            if is_bigram:
                disp_key = disp_key.replace(" ", "[SPACE]")
            writer.writerow([disp_key, info["count"], f"{info['probability']:.6f}"])


def run_full_entropy_analysis(text_sp: str, text_nosp: str, results_dir: str):
    os.makedirs(results_dir, exist_ok=True)

    # 1. Текст з пробілами
    h1_sp, f1_sp = calc_monograms(text_sp)
    h2_sp_ov, f2_sp_ov = calc_bigrams(text_sp, step=1)
    h2_sp_nov, f2_sp_nov = calc_bigrams(text_sp, step=2)

    save_frequencies_csv(f1_sp, os.path.join(results_dir, "letters_with_spaces.csv"), False)
    save_frequencies_csv(f2_sp_ov, os.path.join(results_dir, "bigrams_with_spaces_overlapping.csv"), True)
    save_frequencies_csv(f2_sp_nov, os.path.join(results_dir, "bigrams_with_spaces_non_overlapping.csv"), True)

    # 2. Текст без пробілів
    h1_nosp, f1_nosp = calc_monograms(text_nosp)
    h2_nosp_ov, f2_nosp_ov = calc_bigrams(text_nosp, step=1)
    h2_nosp_nov, f2_nosp_nov = calc_bigrams(text_nosp, step=2)

    save_frequencies_csv(f1_nosp, os.path.join(results_dir, "letters_without_spaces.csv"), False)
    save_frequencies_csv(f2_nosp_ov, os.path.join(results_dir, "bigrams_without_spaces_overlapping.csv"), True)
    save_frequencies_csv(f2_nosp_nov, os.path.join(results_dir, "bigrams_without_spaces_non_overlapping.csv"), True)

    # Топ-5 допоміжна функція
    def get_top5(freqs: dict):
        return sorted(freqs.items(), key=lambda x: x[1]["probability"], reverse=True)[:5]

    return {
        "with_spaces": {
            "H1": h1_sp,
            "H2_overlapping": h2_sp_ov,
            "H2_non_overlapping": h2_sp_nov,
            "top5_letters": get_top5(f1_sp),
            "top5_bigrams_ov": get_top5(f2_sp_ov),
            "top5_bigrams_nov": get_top5(f2_sp_nov),
            "total_chars": len(text_sp),
            "alphabet_size": len(f1_sp),
        },
        "without_spaces": {
            "H1": h1_nosp,
            "H2_overlapping": h2_nosp_ov,
            "H2_non_overlapping": h2_nosp_nov,
            "top5_letters": get_top5(f1_nosp),
            "top5_bigrams_ov": get_top5(f2_nosp_ov),
            "top5_bigrams_nov": get_top5(f2_nosp_nov),
            "total_chars": len(text_nosp),
            "alphabet_size": len(f1_nosp),
        },
    }


if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.abspath(__file__))
    sp_file = os.path.join(base_dir, "data", "text_with_spaces.txt")
    nosp_file = os.path.join(base_dir, "data", "text_without_spaces.txt")
    res_dir = os.path.join(base_dir, "results")

    with open(sp_file, "r", encoding="utf-8") as f:
        text_sp = f.read()
    with open(nosp_file, "r", encoding="utf-8") as f:
        text_nosp = f.read()

    res = run_full_entropy_analysis(text_sp, text_nosp, res_dir)

    print("=== ТЕКСТ З ПРОБІЛАМИ ===")
    print(f"H1: {res['with_spaces']['H1']:.4f} біт/символ")
    print(f"H2 (перетинні, крок 1): {res['with_spaces']['H2_overlapping']:.4f} біт/символ")
    print(f"H2 (неперетинні, крок 2): {res['with_spaces']['H2_non_overlapping']:.4f} біт/символ")
    print("Топ-5 символів:")
    for ch, d in res['with_spaces']['top5_letters']:
        name = "[пробіл]" if ch == " " else f"'{ch}'"
        print(f"  {name}: count={d['count']}, p={d['probability']:.4f}")

    print("\n=== ТЕКСТ БЕЗ ПРОБІЛІВ ===")
    print(f"H1: {res['without_spaces']['H1']:.4f} біт/символ")
    print(f"H2 (перетинні, крок 1): {res['without_spaces']['H2_overlapping']:.4f} біт/символ")
    print(f"H2 (неперетинні, крок 2): {res['without_spaces']['H2_non_overlapping']:.4f} біт/символ")
    print("Топ-5 символів:")
    for ch, d in res['without_spaces']['top5_letters']:
        print(f"  '{ch}': count={d['count']}, p={d['probability']:.4f}")
