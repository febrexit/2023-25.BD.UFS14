import requests
import bs4

def sito(url):
    risposta = requests.get(url)
    # Usa risposta.content per ottenere i byte del file
    contenuto = risposta.content
    return contenuto  # Ora stai restituendo il contenuto effettivo

def test_snapshot(snapshot):
    snapshot.snapshot_dir = 'snapshots' 
    contenuto = sito("https://cir-reports.cir-safety.org/view-attachment/?id=0334b6a1-8c74-ec11-8943-0022482f06a6")
    # Confronta il contenuto del sito con il file 'contenuto.txt'
    snapshot.assert_match(contenuto, 'contenuto.txt')  # Assicurati che il contenuto.txt contenga dati binari
