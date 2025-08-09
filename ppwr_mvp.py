import streamlit as st
import pandas as pd

st.set_page_config(page_title="PPWR & EPR Quick Check", layout="centered")

st.title("PPWR & EPR Quick Check")
st.markdown(
    """
    Willkommen zu Ihrem **PPWR & EPR Quick Check**  
    Dieses Tool hilft Ihnen, Ihre Verpackungsdaten in Bezug auf die EU-Verpackungsverordnung (PPWR) einzuordnen.  
    **Ziel:** Ermittlung Ihres Compliance-Risikos und einer unverbindlichen Kostenschätzung bei Non-Compliance.
    """
)

choice = st.radio("Wählen Sie Ihren Einstieg:", ["Excel-Upload starten", "Direkteingabe starten"])

if choice == "Excel-Upload starten":
    st.subheader("Excel-Upload: Ihre Verpackungsdaten")
    st.markdown(
        """
        Bitte laden Sie hier Ihr Verpackungsdatenblatt hoch.  
        Falls keine exakten Gewichte vorliegen, können Defaultwerte genutzt werden.  
        Ziel: Eine erste **Risikoeinschätzung** und eine **unverbindliche Kostenschätzung** für Non-Compliance.
        """
    )
    uploaded_file = st.file_uploader("Drag & Drop oder Datei auswählen (Excel/CSV)", type=["xlsx", "csv"])
    st.checkbox("Eigene Gewichtsdaten vorhanden – Defaults nur nutzen, falls keine Angaben verfügbar")
    st.info("💡 Tipp: Nutzen Sie unser Musterformular, um sicherzustellen, dass alle relevanten Felder enthalten sind.")
    st.caption("Hinweis: Sie können Gewichte in Gramm oder Kilogramm angeben – wir rechnen automatisch um.")
    
    if uploaded_file:
        st.success("Datei erfolgreich hochgeladen! (Analyse-Logik folgt im nächsten Schritt.)")
        st.button("Analyse starten")

if choice == "Direkteingabe starten":
    st.subheader("Direkteingabe (In Arbeit)")
    st.markdown("Hier wird in der nächsten Iteration die manuelle Eingabe-Maske verfügbar sein.")