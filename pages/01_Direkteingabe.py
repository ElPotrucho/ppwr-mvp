import streamlit as st
import pandas as pd
from pathlib import Path

st.set_page_config(page_title="Direkteingabe – Verpackungsdaten", layout="centered")
st.title("Direkteingabe – Verpackungsdaten (Schritt 1 von 2)")

st.markdown("""
**Was ist das?**  
Tragen Sie hier die wichtigsten Verpackungen Ihres Unternehmens ein.  
Schon **wenige Angaben** genügen, um im nächsten Schritt eine erste **Risikoeinschätzung** und eine **unverbindliche Kostenschätzung** zu erhalten.
""")

# --- Hilfstexte ---
HELP_RAM = "Retail = Endkundeneinheit • Aggregation = Um-/Trays • Mobility = Transportverpackung"
HELP_REUSE = "Ja = Mehrweg / Rückführungssystem vorhanden • Nein = Einweg • Unsicher = Tool schlägt Default vor"
HELP_GEWICHT = "Sie können Gewichte in g oder kg eingeben – wir rechnen automatisch um."

# --- Defaultliste aus CSV (optional) ---
default_csv_path = Path("RAM_Defaultwerte.csv")
default_types = []
if default_csv_path.exists():
    try:
        defaults_df = pd.read_csv(default_csv_path)
        default_types = sorted(defaults_df["Verpackungstyp"].dropna().unique().tolist())
    except Exception:
        default_types = []
else:
    default_types = []

# --- Session State vorbereiten ---
if "eingaben" not in st.session_state:
    st.session_state.eingaben = []  # Liste von Dicts

with st.form("eingabe_form"):
    col1, col2 = st.columns([2, 1])
    with col1:
        verpackungstyp = st.selectbox(
            "Verpackungstyp",
            options=["(Bitte wählen)"] + default_types if default_types else ["(Bitte wählen)", "Topseal-Schale", "EPS-Kiste", "IFCO-Kiste", "Glas (Konfitüre)", "Edelstahlcontainer"],
            help="Auto-Suggest aus Defaultliste. Sie können später weitere Typen ergänzen."
        )
    with col2:
        ram = st.selectbox("RAM-Kategorie", options=["Retail", "Aggregation", "Mobility"], help=HELP_RAM)

    col3, col4 = st.columns([1, 1])
    with col3:
        gewicht = st.number_input("Gewicht", min_value=0.0, step=0.1, help=HELP_GEWICHT)
    with col4:
        einheit = st.selectbox("Einheit", options=["g", "kg"])

    menge = st.number_input("Menge (Stück/Jahr)", min_value=0, step=1, help="Jährliche Stückzahl (grobe Schätzung reicht).")

    col5, col6 = st.columns([1, 1])
    with col5:
        material = st.selectbox("Material", options=["Kunststoff", "Glas", "Metall", "Papier/Pappe", "Holz", "Sonstiges"], help="Material-Hauptklasse.")
    with col6:
        reuse = st.selectbox("Reuse-geeignet?", options=["ja", "nein", "unsicher"], help=HELP_REUSE)

    geschaetzt = st.checkbox("Gewichtsdaten geschätzt", help="Markieren, wenn die Gewichtsangabe nicht exakt ist (wirken auf Datenqualitätsbewertung).")

    add = st.form_submit_button("➕ Verpackung hinzufügen")

if add:
    if verpackungstyp == "(Bitte wählen)":
        st.warning("Bitte wählen Sie einen Verpackungstyp.")
    else:
        # in g normalisieren
        gewicht_g = gewicht * 1000 if einheit == "kg" else gewicht
        st.session_state.eingaben.append({
            "Verpackungstyp": verpackungstyp,
            "RAM-Kategorie": ram,
            "Material": material,
            "Gewicht (g)": round(float(gewicht_g), 3),
            "Menge (Stück/Jahr)": int(menge),
            "Reuse-geeignet": reuse,
            "Gewichtsdaten geschätzt": "ja" if geschaetzt else "nein"
        })
        st.success(f"'{verpackungstyp}' hinzugefügt.")

st.markdown("### Übersicht Ihrer Eingaben")
if st.session_state.eingaben:
    df = pd.DataFrame(st.session_state.eingaben)
    st.dataframe(df, use_container_width=True)

    # Entfernen-Funktion
    idx_to_remove = st.number_input("Index zum Entfernen (optional)", min_value=0, step=1, value=0, help="Zeilennummer in der Tabelle (beginnend bei 0).")
    colA, colB = st.columns([1, 2])
    with colA:
        if st.button("❌ Ausgewählte Zeile entfernen"):
            if 0 <= idx_to_remove < len(st.session_state.eingaben):
                removed = st.session_state.eingaben.pop(int(idx_to_remove))
                st.info(f"Entfernt: {removed.get('Verpackungstyp')}")
            else:
                st.warning("Ungültiger Index.")

    # Weiter zur Analyse
    st.markdown("---")
    st.markdown("**Nächster Schritt:** Daten prüfen und Analyse starten (Schritt 2).")
    if st.button("✅ Analyse vorbereiten (Schritt 2)"):
        # Daten für nächsten Schritt speichern
        st.session_state.eingaben_df = pd.DataFrame(st.session_state.eingaben)
        st.success("Daten gespeichert. Öffnen Sie jetzt die Seite 'Direkteingabe – Übersicht & Analyse (Schritt 2)'.")
        st.caption("Tipp: In der linken Seitenleiste die nächste Seite auswählen.")
else:
    st.info("Noch keine Einträge vorhanden. Fügen Sie oben Ihre erste Verpackung hinzu.")
