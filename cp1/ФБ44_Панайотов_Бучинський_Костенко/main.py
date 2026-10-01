import os
from preprocess import prepare_datasets
from entropy_calc import run_full_entropy_analysis
from experiments import run_section_3, run_section_4
from shannon_entropy import run_section_5_and_6


def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(base_dir, "data")
    res_dir = os.path.join(base_dir, "results")
    raw_path = os.path.join(data_dir, "raw_text.txt")
    sp_path = os.path.join(data_dir, "text_with_spaces.txt")
    nosp_path = os.path.join(data_dir, "text_without_spaces.txt")

    print("=" * 65)
    print("КОМП'ЮТЕРНИЙ ПРАКТИКУМ №1: ОЦІНКА ЕНТРОПІЇ ВІДКРИТОГО ТЕКСТУ")
    print("Бригада: Панайотов Олександр, Бучинський Денис, Костенко Володимир")
    print("=" * 65)

    # 1. Попередня обробка тексту (Олександр Панайотов)
    if not (os.path.exists(sp_path) and os.path.exists(nosp_path)):
        print("\n[1] Обробка та нормалізація тексту...")
        prepare_datasets(raw_path, data_dir)
    else:
        print("\n[1] Файли даних знайдено:")

    with open(sp_path, "r", encoding="utf-8") as f:
        text_sp = f.read()
    with open(nosp_path, "r", encoding="utf-8") as f:
        text_nosp = f.read()

    print(f"  • Текст із пробілами: {len(text_sp)} символів (потужність алфавіту: {len(set(text_sp))})")
    print(f"  • Текст без пробілів: {len(text_nosp)} символів (потужність алфавіту: {len(set(text_nosp))})")

    # 2. Розрахунок H1 та H2 (Олександр Панайотов)
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

    # 3 & 4. Експерименти над розподілами та періодичністю (Денис Бучинський)
    print("\n" + "=" * 65)
    print("[3 & 4] Експерименти над моделями та періодичністю (Денис Бучинський)")
    run_section_3(h1_natural_text=res['without_spaces']['H1'])
    run_section_4()

    # 5 & 6. Оцінка Шеннона та надлишковість (Володимир Костенко)
    print("\n" + "=" * 65)
    print("[5 & 6] Оцінка за методом Шеннона та розрахунок надлишковості R (Володимир Костенко)")
    run_section_5_and_6(entropy_analysis_res=res, results_dir=res_dir)

    print(f"\n[OK] Усі обчислення завершено. Результати CSV експортовано у: {res_dir}")


if __name__ == "__main__":
    main()
