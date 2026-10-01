import os
import math
import csv

# --------------------------------------------------------------------------------------
# РОЗДІЛ 5: ЕКСПЕРИМЕНТАЛЬНІ ДАНІ 50 ДОСЛІДІВ ВГАДУВАННЯ ЛІТЕР ЗА МЕТОДОМ ШЕННОНА
# Виконавець: Володимир Костенко (група ФБ-44)
# --------------------------------------------------------------------------------------

# Розподіл кількості спроб для 50 дослідів при довжинах контексту n = 10, 20, 30:
# Індекс масиву + 1 відповідає номеру спроби (1-а спроба, 2-а спроба, ...).
SHANNON_TRIALS = {
    10: {
        # n = 10 символів (передісторія 9 символів):
        # 1-ша спроба: 29 разів, 2-га: 9, 3-тя: 5, 4-та: 3, 5-та: 2, 6-та: 1, 7-ма: 1. Разом = 50.
        "attempts_counts": [29, 9, 5, 3, 2, 1, 1],
        "total_trials": 50,
        "n_length": 10,
    },
    20: {
        # n = 20 символів (передісторія 19 символів):
        # 1-ша спроба: 35 разів, 2-га: 7, 3-тя: 4, 4-та: 2, 5-та: 1, 6-та: 1. Разом = 50.
        "attempts_counts": [35, 7, 4, 2, 1, 1],
        "total_trials": 50,
        "n_length": 20,
    },
    30: {
        # n = 30 символів (передісторія 29 символів):
        # 1-ша спроба: 39 разів, 2-га: 6, 3-тя: 3, 4-та: 1, 5-та: 1. Разом = 50.
        "attempts_counts": [39, 6, 3, 1, 1],
        "total_trials": 50,
        "n_length": 30,
    },
}


def calc_shannon_bounds(counts_list, total_trials=50, alphabet_size=32):
    """
    Обчислення меж Шеннона F_L та F_R за емпіричним розподілом спроб вгадування.
    
    q_i - емпірична ймовірність вгадування літери з i-ї спроби (q_i = k_i / N).
    
    Верхня межа (ентропія розподілу спроб):
        F_R = - sum(q_i * log2(q_i))
        
    Нижня межа Шеннона:
        F_L = sum_{i=1}^m i * (q_i - q_{i+1}) * log2(i)
            = sum_{i=1}^m q_i * [i * log2(i) - (i - 1) * log2(i - 1)] (з 0*log2(0) = 0)
    """
    # Створюємо повний вектор частот до розміру алфавіту m
    counts = list(counts_list) + [0] * (alphabet_size - len(counts_list))
    total = float(total_trials)
    
    q = [c / total for c in counts]
    
    # 1. Верхня межа F_R
    f_r = 0.0
    for prob in q:
        if prob > 0:
            f_r -= prob * math.log2(prob)
            
    # 2. Нижня межа F_L
    f_l = 0.0
    for i in range(1, alphabet_size + 1):
        prob = q[i - 1]
        if prob > 0:
            term_curr = i * math.log2(i) if i > 0 else 0.0
            term_prev = (i - 1) * math.log2(i - 1) if (i - 1) > 0 else 0.0
            coeff = term_curr - term_prev
            f_l += prob * coeff
            
    return {
        "F_L": f_l,
        "F_R": f_r,
        "q": q,
        "counts": counts_list,
        "total_trials": total_trials,
    }


def calc_redundancy(h_value, h0_value):
    """
    Розрахунок надлишковості джерела:
        R = 1 - (H / H0)
    """
    if h0_value <= 0:
        return 0.0
    return max(0.0, 1.0 - (h_value / h0_value))


def evaluate_shannon_experiments(alphabet_size=32):
    h0 = math.log2(alphabet_size)
    shannon_results = {}
    
    for n_len, data in SHANNON_TRIALS.items():
        bounds = calc_shannon_bounds(data["attempts_counts"], data["total_trials"], alphabet_size)
        
        # Межі надлишковості R_L та R_R:
        # Оскільки F_L <= H <= F_R, то (1 - F_R/H0) <= R <= (1 - F_L/H0)
        r_lower = calc_redundancy(bounds["F_R"], h0)
        r_upper = calc_redundancy(bounds["F_L"], h0)
        
        shannon_results[n_len] = {
            **bounds,
            "H0": h0,
            "R_lower": r_lower,
            "R_upper": r_upper,
        }
        
    return shannon_results


def save_shannon_results_csv(shannon_res, output_csv_path):
    os.makedirs(os.path.dirname(output_csv_path), exist_ok=True)
    with open(output_csv_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["n_symbols", "F_L_lower_bound", "F_R_upper_bound", "R_lower_pct", "R_upper_pct", "distribution_q1_to_q5"])
        for n_len, res in shannon_res.items():
            q_str = "; ".join(f"q{i+1}={res['q'][i]:.2f}" for i in range(min(5, len(res['counts']))))
            writer.writerow([
                n_len,
                f"{res['F_L']:.4f}",
                f"{res['F_R']:.4f}",
                f"{res['R_lower'] * 100:.2f}%",
                f"{res['R_upper'] * 100:.2f}%",
                q_str
            ])


def run_section_5_and_6(entropy_analysis_res=None, results_dir=None):
    print("\n" + "=" * 65)
    print("РОЗДІЛ 5: ЕКСПЕРИМЕНТАЛЬНА ОЦІНКА ЗА МЕТОДОМ ШЕННОНА")
    print("Виконавець: Володимир Костенко (група ФБ-44)")
    print("=" * 65)
    
    sh_res = evaluate_shannon_experiments(alphabet_size=32)
    
    print("\nРезультати 50 дослідів угадування літер за передісторією n-1 символів:")
    print("-" * 65)
    print(f"{'Довжина n':<12} | {'Розподіл успішних спроб (k_1, k_2, ...)':<32} | {'F_L (нижня)':<10} | {'F_R (верхня)':<10}")
    print("-" * 65)
    
    for n_len in [10, 20, 30]:
        r = sh_res[n_len]
        counts_str = ", ".join(f"k_{i+1}={c}" for i, c in enumerate(r['counts']))
        print(f"n = {n_len:<8} | {counts_str:<32} | {r['F_L']:<10.4f} | {r['F_R']:<10.4f}")
    print("-" * 65)
    
    print("\nОцінка інтервалу ентропії Шеннона F_L <= H^(n) <= F_R (біт/символ):")
    for n_len in [10, 20, 30]:
        r = sh_res[n_len]
        print(f"  • Для n = {n_len}:  {r['F_L']:.4f} <= H^({n_len}) <= {r['F_R']:.4f} біт/символ")
        
    print("\n" + "=" * 65)
    print("РОЗДІЛ 6: РОЗРАХУНОК НАДЛИШКОВОСТІ R ТА ПІДСУМКОВА ТАБЛИЦЯ")
    print("=" * 65)
    
    # Визначаємо H0
    h0_nosp = math.log2(32)   # 5.0000
    h0_sp = math.log2(33)     # 5.0444
    
    # Якщо передано результати попередніх розділів, беремо їх; інакше використовуємо точні розраховані
    if entropy_analysis_res:
        h1_sp = entropy_analysis_res['with_spaces']['H1']
        h2_sp_ov = entropy_analysis_res['with_spaces']['H2_overlapping']
        h2_sp_nov = entropy_analysis_res['with_spaces']['H2_non_overlapping']
        h1_nosp = entropy_analysis_res['without_spaces']['H1']
        h2_nosp_ov = entropy_analysis_res['without_spaces']['H2_overlapping']
        h2_nosp_nov = entropy_analysis_res['without_spaces']['H2_non_overlapping']
    else:
        h1_sp, h2_sp_ov, h2_sp_nov = 4.3782, 3.9677, 3.9677
        h1_nosp, h2_nosp_ov, h2_nosp_nov = 4.4686, 4.1493, 4.1497
        
    # Таблиця зведення
    print("\nПІДСУМКОВА ЗВЕДЕНА ТАБЛИЦЯ ОЦІНОК ЕНТРОПІЇ ТА НАДЛИШКОВОСТІ:")
    print("-" * 75)
    print(f"{'Модель джерела / Метод':<32} | {'Оцінка H (біт/симв)':<20} | {'Надлишковість R':<15}")
    print("-" * 75)
    print(f"{'H0 (рівноймовірна, без пробілу)':<32} | {h0_nosp:<20.4f} | {0.00:<15.2%}")
    print(f"{'H0 (рівноймовірна, з пробілом)':<32} | {h0_sp:<20.4f} | {0.00:<15.2%}")
    print("-" * 75)
    print(f"{'H1 (монограми, без пробілів)':<32} | {h1_nosp:<20.4f} | {calc_redundancy(h1_nosp, h0_nosp):<15.2%}")
    print(f"{'H1 (монограми, з пробілами)':<32} | {h1_sp:<20.4f} | {calc_redundancy(h1_sp, h0_sp):<15.2%}")
    print("-" * 75)
    print(f"{'H2 перетинні (без пробілів)':<32} | {h2_nosp_ov:<20.4f} | {calc_redundancy(h2_nosp_ov, h0_nosp):<15.2%}")
    print(f"{'H2 перетинні (з пробілами)':<32} | {h2_sp_ov:<20.4f} | {calc_redundancy(h2_sp_ov, h0_sp):<15.2%}")
    print(f"{'H2 неперетинні (без пробілів)':<32} | {h2_nosp_nov:<20.4f} | {calc_redundancy(h2_nosp_nov, h0_nosp):<15.2%}")
    print(f"{'H2 неперетинні (з пробілами)':<32} | {h2_sp_nov:<20.4f} | {calc_redundancy(h2_sp_nov, h0_sp):<15.2%}")
    print("-" * 75)
    print(f"{'Шеннон n = 10 (50 дослідів)':<32} | {sh_res[10]['F_L']:.4f} .. {sh_res[10]['F_R']:.4f}      | {sh_res[10]['R_lower']:.2%} .. {sh_res[10]['R_upper']:.2%}")
    print(f"{'Шеннон n = 20 (50 дослідів)':<32} | {sh_res[20]['F_L']:.4f} .. {sh_res[20]['F_R']:.4f}      | {sh_res[20]['R_lower']:.2%} .. {sh_res[20]['R_upper']:.2%}")
    print(f"{'Шеннон n = 30 (50 дослідів)':<32} | {sh_res[30]['F_L']:.4f} .. {sh_res[30]['F_R']:.4f}      | {sh_res[30]['R_lower']:.2%} .. {sh_res[30]['R_upper']:.2%}")
    print("-" * 75)
    
    print("\nВисновки до розділів 5 та 6:")
    print("1. Зі збільшенням довжини контексту n (від 10 до 30) ентропія на символ H^(n)")
    print("   закономірно зменшується (з ~1.14..1.89 біт до ~0.54..1.12 біт), оскільки")
    print("   людина враховує глибокі граматичні, синтаксичні та семантичні зв'язки мови.")
    print("2. Надлишковість природної мови R для n = 30 досягає 77.7% - 89.2%, що")
    print("   підтверджує високу надлишковість та передбачуваність відкритого тексту.")
    print("3. Експеримент Шеннона суттєво перевершує марковські n-грамні моделі за якістю")
    print("   оцінки істинної питомої ентропії мови H_infinity.")

    if results_dir:
        csv_path = os.path.join(results_dir, "shannon_guessing_results.csv")
        save_shannon_results_csv(sh_res, csv_path)
        print(f"\nРезультати Шеннона збережено у: {csv_path}")

    return sh_res


if __name__ == "__main__":
    run_section_5_and_6()
