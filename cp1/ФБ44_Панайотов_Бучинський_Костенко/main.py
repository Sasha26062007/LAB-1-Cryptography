import os
from preprocess import prepare_datasets
from entropy_calc import run_full_entropy_analysis


def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(base_dir, "data")
    res_dir = os.path.join(base_dir, "results")
    raw_path = os.path.join(data_dir, "raw_text.txt")
    sp_path = os.path.join(data_dir, "text_with_spaces.txt")
    nosp_path = os.path.join(data_dir, "text_without_spaces.txt")

    print("=" * 65)
    print("КОМП'ЮТЕРНИЙ ПРАКТИКУМ №1: ЧАСТИНА 1 ТА 2 (ОЛЕКСАНДР ПАНАЙОТОВ)")
    print("=" * 65)

    # 1. Попередня обробка тексту (Розділ 1)
    if not (os.path.exists(sp_path) and os.path.exists(nosp_path)):
        print("\n[1] Обробка та нормалізація тексту...")
        stats = prepare_datasets(raw_path, data_dir)
    else:
        print("\n[1] Файли даних знайдено:")

    with open(sp_path, "r", encoding="utf-8") as f:
        text_sp = f.read()
    with open(nosp_path, "r", encoding="utf-8") as f:
        text_nosp = f.read()

    print(f"  • Текст із пробілами: {len(text_sp)} символів (потужність алфавіту: {len(set(text_sp))})")
    print(f"  • Текст без пробілів: {len(text_nosp)} символів (потужність алфавіту: {len(set(text_nosp))})")

    # 2. Розрахунок H1 та H2 (Розділ 2)
    print("\n[2] Розрахунок монограм, біграм та ентропій...")
    res = run_full_entropy_analysis(text_sp, text_nosp, res_dir)

    print("\n" + "-" * 65)
    print(f"{'Параметр':<30} | {'З пробілами':<15} | {'Без пробілів':<15}")
    print("-" * 65)
    print(f"{'H1 (монограми)':<30} | {res['with_spaces']['H1']:<15.4f} | {res['without_spaces']['H1']:<15.4f}")
    print(f"{'H2 (перетинні, крок 1)':<30} | {res['with_spaces']['H2_overlapping']:<15.4f} | {res['without_spaces']['H2_overlapping']:<15.4f}")
    print(f"{'H2 (неперетинні, крок 2)':<30} | {res['with_spaces']['H2_non_overlapping']:<15.4f} | {res['without_spaces']['H2_non_overlapping']:<15.4f}")
    print("-" * 65)

    print("\nТоп-5 символів:")
    print("  З пробілами:   " + ", ".join(f"'{'[SPACE]' if ch==' ' else ch}' ({d['probability']:.4f})" for ch, d in res['with_spaces']['top5_letters']))
    print("  Без пробілів: " + ", ".join(f"'{ch}' ({d['probability']:.4f})" for ch, d in res['without_spaces']['top5_letters']))

    print("\nТоп-5 біграм:")
    print("  З пробілами (перетинні):   " + ", ".join(f"'{bg.replace(' ', '_')}' ({d['probability']:.4f})" for bg, d in res['with_spaces']['top5_bigrams_ov']))
    print("  З пробілами (неперетинні): " + ", ".join(f"'{bg.replace(' ', '_')}' ({d['probability']:.4f})" for bg, d in res['with_spaces']['top5_bigrams_nov']))
    print("  Без пробілів (перетинні):  " + ", ".join(f"'{bg}' ({d['probability']:.4f})" for bg, d in res['without_spaces']['top5_bigrams_ov']))
    print("  Без пробілів (неперетинні):" + ", ".join(f"'{bg}' ({d['probability']:.4f})" for bg, d in res['without_spaces']['top5_bigrams_nov']))

    print(f"\nПовні CSV-таблиці частот збережено у папку: {res_dir}")


if __name__ == "__main__":
    main()
