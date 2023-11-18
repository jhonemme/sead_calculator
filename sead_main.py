import streamlit as st
from datetime import datetime, timedelta

# Funzione per il calcolo del tempo di soppressione
@st.cache_data()
def calcola_tempo_soppressione(velocita_aereo, distanza_minaccia, raggio_minaccia, tot_obiettivo, tof_colpo):
    try:
        # Converti TOT in un oggetto datetime
        tot_obiettivo_oggetto = datetime.strptime(tot_obiettivo, "%H:%M:%S")

        # Calcolo del tempo di attraversamento considerando il raggio della minaccia
        tempo_di_through = ((distanza_minaccia - raggio_minaccia) / velocita_aereo) * 60  # Converti in minuti

        # Calcolo del tempo in cui l'aereo entra nell'area della minaccia e inizia la soppressione
        tempo_ingresso_minaccia = tot_obiettivo_oggetto - timedelta(minutes=(tempo_di_through / 60 + tof_colpo / 60 + 0.5))  # Aggiungi 30 secondi e converte in minuti

        # Calcolo del tempo di inizio della soppressione ogni 30 secondi
        tempo_soppressione = tempo_ingresso_minaccia - timedelta(seconds=30)

        # Calcolo del tempo di fine della soppressione ogni 30 secondi
        tempo_fine_soppressione = tempo_ingresso_minaccia + timedelta(seconds=30)

        # Calcolo del tempo di uscita dall'area di minaccia
        tempo_uscita_minaccia = tempo_ingresso_minaccia + timedelta(minutes=(tempo_di_through / 60 + tof_colpo / 60))
        # Calcolo del tempo di fine soppressione per coprire l'aereo durante l'uscita dalla minaccia
        tempo_fine_soppressione = tempo_ingresso_minaccia + timedelta(minutes=(tempo_di_through / 60 + tof_colpo / 60))
        # Ritorna i risultati
        risultati = {
            "tempo_ingresso_minaccia": tempo_ingresso_minaccia.strftime('%H:%M:%S'),
            "tempo_soppressione": tempo_soppressione.strftime('%H:%M:%S'),
            "tempo_fine_soppressione": tempo_fine_soppressione.strftime('%H:%M:%S'),
            "tempo_uscita_minaccia": tempo_uscita_minaccia.strftime('%H:%M:%S'),
            "tempo_fine_soppressione_uscita": tempo_fine_soppressione_uscita.strftime('%H:%M:%S')
        }

        return risultati

    except ValueError:
        return None

# Interfaccia Streamlit
st.title("Calcolatore di Tempo di Soppressione")

# Input manuale
velocita_aereo = st.number_input("Velocità dell'aereo in nodi", min_value=0.0, step=1.0)
distanza_minaccia = st.number_input("Distanza tra il punto di partenza e l'obiettivo in nm", min_value=0.0, step=1.0)
raggio_minaccia = st.number_input("Raggio dell'area di minaccia in nm", min_value=0.0, step=1.0)
tot_obiettivo = st.text_input("Tempo di obiettivo (TOT) nel formato HH:MM:SS ")
tof_colpo = st.number_input("Time of Flight (TOF) del colpo di soppressione in secondi", min_value=0.0, step=1.0)

# Calcola il tempo di soppressione solo se il pulsante è stato premuto
if st.button("Calcola"):
    risultati = calcola_tempo_soppressione(velocita_aereo, distanza_minaccia, raggio_minaccia, tot_obiettivo, tof_colpo)
    if risultati is not None:
        # Visualizza i risultati
        st.header("Risultati:")
        st.write(f"L'aereo entra nell'area della minaccia circa alle {risultati['tempo_ingresso_minaccia']}.")
        st.write(f"Inizia la soppressione ogni 30 secondi a partire da {risultati['tempo_soppressione']} fino all'uscita dell'aereo dall'area di minaccia alle {risultati['tempo_uscita_minaccia']}.")
    else:
        st.error("Si è verificato un errore durante il calcolo del tempo di soppressione.")
