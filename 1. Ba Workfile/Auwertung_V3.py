import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# ====== Style: gut lesbar für BA ======
plt.rcParams.update({
    "font.size": 20,
    "axes.titlesize": 26,
    "axes.labelsize": 22,
    "xtick.labelsize": 18,
    "ytick.labelsize": 18,
    "legend.fontsize": 18
})

# ====== Rohdaten (wie aus deinen Tabellen) ======
raw = pd.DataFrame([
    # Szenario, Frage, Median, Hauptanteil, Streuung
    ("S1", "Tiefenwahrnehmung klar erkennbar", 6, 7.00, 1.72),
    ("S1", "Verzerrungen beim Bewegen",       6, 7.00, 2.53),
    ("S1", "Tiefenwirkung realistisch",       4, 2.00, 1.98),
    ("S1", "Szene läuft flüssig",             7, 7.00, 2.25),

    ("S2", "Tiefenwahrnehmung klar erkennbar", 6, 7.00, 1.32),
    ("S2", "Verzerrungen beim Bewegen",       2, 1.00, 1.46),
    ("S2", "Tiefenwirkung realistisch",       5, 7.00, 1.85),
    ("S2", "Szene läuft flüssig",             7, 7.00, 2.25),

    ("S3", "Tiefenwahrnehmung klar erkennbar", 7, 7.00, 0.81),
    ("S3", "Verzerrungen beim Bewegen",       1, 1.00, 1.84),
    ("S3", "Tiefenwirkung realistisch",       6, 7.00, 1.50),
    ("S3", "Szene läuft flüssig",             7, 7.00, 2.43),
], columns=["Szenario_raw", "Frage", "Median", "Hauptanteil", "Streuung"])

# ====== WICHTIG: Umcodierung (Umfrage -> technisch) ======
# Du: S1 ist eigentlich S2, S2 ist eigentlich S3, S3 ist eigentlich S1
scenario_map = {
    "S1": "S2 (Depth Map)",
    "S2": "S3 (Low-Poly)",
    "S3": "S1 (Baseline)"
}
order = ["S2 (Depth Map)", "S3 (Low-Poly)", "S1 (Baseline)"]

raw["Szenario"] = raw["Szenario_raw"].map(scenario_map)
raw["Szenario"] = pd.Categorical(raw["Szenario"], categories=order, ordered=True)

# Sortieren für saubere Balkenreihenfolge
raw = raw.sort_values(["Frage", "Szenario"])

# ====== Plot-Funktion: gruppierte Balken pro Frage ======
def plot_grouped(metric: str, title: str, ylabel: str, ylim=None, filename=None):
    df = raw.pivot(index="Frage", columns="Szenario", values=metric).loc[:, order]

    questions = df.index.tolist()
    x = np.arange(len(questions))
    width = 0.25

    fig, ax = plt.subplots(figsize=(16, 8))

    # Farben: gleiche Logik wie bei deinen anderen Plots (grün/lila/dunkel)
    colors = {
        "S2 (Depth Map)": "#9381ff",  # lila
        "S3 (Low-Poly)":  "#272727",  # dunkel
        "S1 (Baseline)":  "#628b48",  # grün
    }

    for i, scen in enumerate(order):
        ax.bar(x + (i - 1) * width, df[scen].values, width, label=scen, color=colors[scen])

    ax.set_title(title)
    ax.set_ylabel(ylabel)
    ax.set_xticks(x)
    ax.set_xticklabels(questions, rotation=20, ha="right")

    if ylim is not None:
        ax.set_ylim(*ylim)

    ax.legend(loc="upper right")
    ax.grid(axis="y", linestyle="--", alpha=0.35)

    plt.tight_layout()

    if filename:
        plt.savefig(filename, dpi=300, bbox_inches="tight")

    plt.show()

# ====== 3 Grafiken ======
plot_grouped(
    metric="Median",
    title="Subjektive Einschätzungen (P2) – Median",
    ylabel="Likert-Skala (1–7)",
    ylim=(1, 7),
    filename="Subjektiv_P2_Median.png"
)

plot_grouped(
    metric="Hauptanteil",
    title="Subjektive Einschätzungen (P2) – Hauptanteil (Modus)",
    ylabel="Likert-Skala (1–7)",
    ylim=(1, 7),
    filename="Subjektiv_P2_Hauptanteil.png"
)

plot_grouped(
    metric="Streuung",
    title="Subjektive Einschätzungen (P2) – Streuung (Standardabweichung)",
    ylabel="Standardabweichung",
    ylim=None,
    filename="Subjektiv_P2_Streuung.png"
)
