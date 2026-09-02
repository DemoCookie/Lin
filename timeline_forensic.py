#-------------------------------
#Forensic Data Visualization — iPhone Activity Timeline
#Copyright (c) 2026 [https://github.com/DemoCookie]
#Ce programme est mis à disposition selon les termes de la Licence Creative
#Commons Attribution - Pas d'Utilisation Commerciale 4.0 International (CC BY-NC 4.0).
#https://creativecommons.org/licenses/by-nc/4.0/
#Vous êtes libre de :
# - Partager : copier, distribuer et communiquer le matériel par tous moyens.
# - Adapter : remixer, transformer et composer d'après le matériel.
#
#Selon les conditions suivantes :
#  - Attribution : Vous devez créditer l'œuvre originale (mention de l'auteur).
#  - Pas d'Utilisation Commerciale : Vous n'êtes pas autorisé à faire un usage
#    commercial de tout ou partie de ce matériel.
#---------------------------------

import sys
import datetime as dt

import pandas as pd
import plotly.graph_objects as go

# ----------------------------------------------------------------------
# 1) CONFIGURATION — à adapter à ton fichier
# ----------------------------------------------------------------------

SHEET_NAME = "Log Data"          # nom de l'onglet à lire
TIMESTAMP_COL = "Timestamp (UTC-5)"
CATEGORY_COL = "Category"
DIRECTION_COL = "Direction / Count"
PARTICIPANTS_COL = "Participants / Direction Info"
DETAILS_COL = "Details / Content"
DOC_COL = "document"
IDX_COL = "#"

# Ordre des lignes (axe Y) et mapping Catégorie brute -> Groupe fonctionnel.
# Modifie librement pour coller à tes propres catégories.
GROUP_ORDER = [
    "Logs Système (WAN/Apps)",
    "Réseau Wi-Fi",
    "Capteurs Santé (Health)",
    "Navigation Web & Searches",
    "Photos & Géoloc",
    "Messages (SMS/iMessage)",
    "Appels & Agenda",
]

GROUP_MAP = {
    "Log Entries": "Logs Système (WAN/Apps)",
    "Wireless Networks": "Réseau Wi-Fi",
    "Activity Sensor Data": "Capteurs Santé (Health)",
    "Web History": "Navigation Web & Searches",
    "Cookies": "Navigation Web & Searches",
    "Searched Items": "Navigation Web & Searches",
    "Image: Location": "Photos & Géoloc",
    "Image Location": "Photos & Géoloc",
    "Images": "Photos & Géoloc",
    "Locations": "Photos & Géoloc",
    "Instant Messages": "Messages (SMS/iMessage)",
    "Call Log": "Appels & Agenda",
    "Calendar": "Appels & Agenda",
}

COLORS = {
    "Logs Système (WAN/Apps)": "#8a8d91",
    "Réseau Wi-Fi": "#17becf",
    "Capteurs Santé (Health)": "#e74c3c",
    "Navigation Web & Searches": "#3498db",
    "Photos & Géoloc": "#2ecc71",
    "Messages (SMS/iMessage)": "#9b59b6",
    "Appels & Agenda": "#f39c12",
}

# ----------------------------------------------------------------------
# 2) LECTURE + NETTOYAGE
# ----------------------------------------------------------------------

# Toutes les données du fichier se situent sur une seule journée.
# Une date factice sert uniquement de support pour l'axe X (Plotly a besoin
# d'un datetime, pas juste d'une heure).
SINGLE_DAY = dt.date(2023, 1, 23)


def parse_timestamp(v):
    """Le fichier source mélange parfois datetime.time et str '\\nHH:MM:SS'."""
    if isinstance(v, dt.time):
        return v
    if isinstance(v, dt.datetime):
        return v.time()
    if isinstance(v, str):
        v = v.strip()
        return dt.datetime.strptime(v, "%H:%M:%S").time()
    return None


def clean_details(txt):
    """Supprime les lignes 'Source file: ...' (chemins bruts, peu lisibles en hover)."""
    if not isinstance(txt, str) or not txt:
        return ""
    lines = [l for l in txt.split("\n") if not l.strip().startswith("Source file:")]
    return "<br>".join(lines)


def build_hover(row):
    lines = [f"<b>{row[CATEGORY_COL]}</b>"]
    if pd.notna(row.get(DIRECTION_COL)):
        lines.append(f"Direction/Count : {row[DIRECTION_COL]}")
    if pd.notna(row.get(PARTICIPANTS_COL)):
        lines.append(str(row[PARTICIPANTS_COL]).replace("\n", "<br>"))
    details = clean_details(row.get(DETAILS_COL))
    if details:
        lines.append(details)
    return "<br>".join(lines)


def load_dataframe(path):
    df = pd.read_excel(path, sheet_name=SHEET_NAME)
    df["t"] = df[TIMESTAMP_COL].apply(parse_timestamp) 
    # Toutes les données appartiennent à une seule journée. 
    # SINGLE_DAY sert uniquement de date support pour l'axe temporel Plotly. 
    df["dt"] = df["t"].apply(
         lambda t: dt.datetime.combine(SINGLE_DAY, t) if t is not None else pd.NaT 
    )

    df["groupe"] = df[CATEGORY_COL].map(GROUP_MAP)
    unmapped = sorted(df.loc[df["groupe"].isna(), CATEGORY_COL].unique())
    if unmapped:
        print(f"[!] Catégories non mappées (ignorées dans le graphique) : {unmapped}")
        print("    -> ajoute-les à GROUP_MAP en haut du script.")
    df = df.dropna(subset=["groupe"])

    df["hover"] = df.apply(build_hover, axis=1)
    return df


# ----------------------------------------------------------------------
# 3) FIGURE PLOTLY
# ----------------------------------------------------------------------

def build_figure(df):
    fig = go.Figure()

    for groupe in GROUP_ORDER:
        sub = df[df["groupe"] == groupe]
        if sub.empty:
            continue
        fig.add_trace(
            go.Scatter(
                x=sub["dt"],
                y=sub["groupe"],
                mode="markers",
                name=groupe,
                marker=dict(
                    color=COLORS.get(groupe, "#333333"), 
                    size=11, 
                    line=dict(width=1, color="white"),
                ),
                customdata=sub["hover"], 
                hovertemplate="%{customdata}<br>%{x|%H:%M:%S}<extra></extra>", 
            ) 
        )

    fig.update_yaxes(
        categoryorder="array",
        categoryarray=GROUP_ORDER[::-1],  # premier groupe en haut
        title=None,
    )
    fig.update_xaxes(
        title="Chronologie (heure)",
        tickformat="%H:%M",
        rangeslider=dict(visible=True),
    )
    
    fig.update_layout(
        title=dict(
            text="Timeline forensique — activité par catégorie",
            subtitle=dict(
                text='© 2026 <a href="https://www.tiktok.com/@panopee" target="_blank" style="color: #0366d6;">@Panopée</a> | <a href="https://github.com/DemoCookie" target="_blank" style="color: #0366d6;">DemoCookie</a> — Licence <a href="https://creativecommons.org/licenses/by-nc/4.0/" target="_blank" style="color: #0366d6;">CC BY-NC 4.0</a> (Usage non commercial)',
                font=dict(size=12, color="gray"),
            ),
        ),
        hovermode="closest",
        height=650,
        legend_title="Groupe",
        margin=dict(l=220, r=40, t=80, b=40),  # t=80 laisse de la place pour le sous-titre
        plot_bgcolor="white",
    )
    return fig


# ----------------------------------------------------------------------
# 4) MAIN
# ----------------------------------------------------------------------

def main():
    if len(sys.argv) < 2:
        print("Usage : python timeline_forensic.py fichier.xlsx")
        sys.exit(1)

    path = sys.argv[1]
    df = load_dataframe(path)
    print(f"{len(df)} entrées chargées pour une seule journée.")

    fig = build_figure(df)
    out = "timeline.html"
    fig.write_html(out, include_plotlyjs="cdn")
    print(f"-> {out} généré. Ouvre-le dans un navigateur.")


if __name__ == "__main__":
    main()
