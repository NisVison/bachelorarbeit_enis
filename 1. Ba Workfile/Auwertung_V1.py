import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams.update({
    "font.size": 22,
    "axes.titlesize": 26,
    "axes.labelsize": 24,
    "xtick.labelsize": 22,
    "ytick.labelsize": 22,
    "legend.fontsize": 20
})

data = [
    # Umfrage S1_P2  → technisch S2 (Depth Map)
    ("S2 (Depth Map)", "Tiefenwahrnehmung klar erkennbar", 6, 1.72),
    ("S2 (Depth Map)", "Verzerrungen beim Bewegen",        6, 2.53),
    ("S2 (Depth Map)", "Tiefenwirkung realistisch",        4, 1.98),
    ("S2 (Depth Map)", "Szene läuft flüssig",              7, 2.25),

    # Umfrage S2_P2 → technisch S3 (Low-Poly)
    ("S3 (Low-Poly)", "Tiefenwahrnehmung klar erkennbar", 6, 1.32),
    ("S3 (Low-Poly)", "Verzerrungen beim Bewegen",        2, 1.46),
    ("S3 (Low-Poly)", "Tiefenwirkung realistisch",        5, 1.85),
    ("S3 (Low-Poly)", "Szene läuft flüssig",              7, 2.25),

    # Umfrage S3_P2 → technisch S1 (Baseline)
    ("S1 (Baseline)", "Tiefenwahrnehmung klar erkennbar", 7, 0.81),
    ("S1 (Baseline)", "Verzerrungen beim Bewegen",        1, 1.84),
    ("S1 (Baseline)", "Tiefenwirkung realistisch",        6, 1.50),
    ("S1 (Baseline)", "Szene läuft flüssig",              7, 2.43),
]

df = pd.DataFrame(
    data,
    columns=["Szenario", "Frage", "Median", "Streuung"]
)

order = ["S1 (Baseline)", "S2 (Depth Map)", "S3 (Low-Poly)"]
df["Szenario"] = pd.Categorical(df["Szenario"], categories=order, ordered=True)


for frage in df["Frage"].unique():
    sub = df[df["Frage"] == frage].sort_values("Szenario")

    fig, ax = plt.subplots(figsize=(10, 6))

    ax.errorbar(
        sub["Szenario"],
        sub["Median"],
        yerr=sub["Streuung"],
        fmt="o",
        capsize=8,
        markersize=10,
        linewidth=2,
        color="#628b48"
    )

    ax.set_ylim(1, 7)
    ax.set_ylabel("Likert-Skala (1–7)")
    ax.set_title(frage)
    ax.grid(axis="y", linestyle="--", alpha=0.5)

    plt.tight_layout()
    plt.savefig(f"subjektiv_{frage.replace(' ', '_')}.pdf", bbox_inches="tight")
    plt.show()


"""# Temporär auskommentiert: ganze Datei deaktiviert
plt.rcParams.update({
    "font.size": 22,
    "axes.titlesize": 26,
    "axes.labelsize": 26,
    "xtick.labelsize": 26,
    "ytick.labelsize": 26,
    "legend.fontsize": 22
})

data = {
    "Szenario": ["S1 P1", "S2 P1", "S3 P1"],
    "Korrekt":  [86, 64, 84],
    "Falsch":   [14, 33, 16],
    "Unsicher": [ 0,  3,  0],
}

df = pd.DataFrame(data)


df["Szenario"] = df["Szenario"].map({
    "S1 P1": "S2 (Depth Map)",
    "S2 P1": "S3 (Low-Poly)",
    "S3 P1": "S1 (Baseline)",
})

# feste Reihenfolge im Plot
order = ["S2 (Depth Map)", "S3 (Low-Poly)", "S1 (Baseline)"]
df["Szenario"] = pd.Categorical(df["Szenario"], categories=order, ordered=True)
df = df.sort_values("Szenario")

COLOR_KORREKT  = "#628b48"
COLOR_FALSCH   = "#9381ff"
COLOR_UNSICHER = "#272727"

fig, ax = plt.subplots(figsize=(10, 6))

ax.bar(df["Szenario"], df["Korrekt"], label="Korrekte Ordnung", color=COLOR_KORREKT)
ax.bar(
    df["Szenario"],
    df["Falsch"],
    bottom=df["Korrekt"],
    label="Falsche Ordnung",
    color=COLOR_FALSCH
)
ax.bar(
    df["Szenario"],
    df["Unsicher"],
    bottom=df["Korrekt"] + df["Falsch"],
    label="Unsicher",
    color=COLOR_UNSICHER
)

ax.set_ylim(0, 100)
ax.set_ylabel("Anteil in %")
ax.set_title("Relative Tiefenschätzung (korrekt / falsch / unsicher)")
ax.legend()

plt.tight_layout()
plt.show()
"""