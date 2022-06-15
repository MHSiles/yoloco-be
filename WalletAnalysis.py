import requests
import json
import tkinter as tk
from tkinter import simpledialog
import pdfrw
import json

ROOT = tk.Tk()

ROOT.withdraw()
# the input dialog
USER_INP = simpledialog.askstring(title="Wallet Info",
                                  prompt="Please Enter your Wallet ID:")

APIKEY = '43044ac0170dc40fa60cfd249ef3307b64edbab8'
BASE = 'https://rest.cryptoapis.io/v2'
BLOCKCHAIN = 'bitcoin'
NETWORK = 'mainnet'
WALLETID = USER_INP
print(USER_INP)

#used if we are looking for data on a particular transaction 
# myTestNetWallet - 62a8e61a25a05500079dda90
# random MainnetWallet - 3R2UHDGKLQkPmAjBGbdzpET95xYV59hkyw
#TID = '4b66461bf88b61e1e4326356534c135129defb504c7acb2fd6c92697d79eb250'

#blockchain-data/bitcoin/testnet/addresses/mzYijhgmzZrmuB7wBDazRKirnChKyow4M3?


#get Bitcoin amount from wallet
with requests.Session() as session:
    h = {'Content-Type': 'application/json',
         'X-API-KEY': APIKEY}
    r = session.get(f'https://rest.cryptoapis.io/v2/wallet-as-a-service/wallets/{WALLETID}/bitcoin/testnet',headers=h)
    r.raise_for_status()
    qdata = r.json()
    bitCoinAmount = qdata['data']['item']['confirmedBalance']['amount']
    
#get Ethereum amount from wallet
with requests.Session() as session:
    h1 = {'Content-Type': 'application/json',
         'X-API-KEY': APIKEY}
    r1 = session.get(f'https://rest.cryptoapis.io/v2/wallet-as-a-service/wallets/{WALLETID}/ethereum/ropsten',headers=h1)
    r1.raise_for_status()
    qdata1 = r1.json()
    ethereumAmount = qdata1['data']['item']['confirmedBalance']['amount']   
    


# #test for a wallet on the chain
# #blockchain-data/bitcoin/testnet/addresses/mzYijhgmzZrmuB7wBDazRKirnChKyow4M3?
# with requests.Session() as session:
#     h = {'Content-Type': 'application/json',
#          'X-API-KEY': APIKEY}
#     r = session.get(f'https://rest.cryptoapis.io/v2/blockchain-data/bitcoin/testnet/addresses/{WALLETID}', headers=h)
#     r.raise_for_status()
#     print(json.dumps(r.json(), indent=4, sort_keys=True))

import os
#directory = os.getcwd()
#print(os.path.abspath("AtomicTest.pdf"))

#pdf_template = "/Users/adityabora/Desktop/AtomicTest.pdf"
pdf_template = "./PortfolioAnalysisV2.pdf"
pdf_output = "output7.pdf"


#template_pdf = pdfrw.PdfReader(pdf_template)  # create a pdfrw object from our template.pdf
print(os.path.exists(pdf_template))
template_pdf = pdfrw.PdfReader(pdf_template)

ANNOT_KEY = '/Annots'
ANNOT_FIELD_KEY = '/T'
ANNOT_VAL_KEY = '/V'
ANNOT_RECT_KEY = '/Rect'
SUBTYPE_KEY = '/Subtype'
WIDGET_SUBTYPE_KEY = '/Widget'

for page in template_pdf.pages:
    annotations = page[ANNOT_KEY]
    for annotation in annotations:
        if annotation[SUBTYPE_KEY] == WIDGET_SUBTYPE_KEY:
            if annotation[ANNOT_FIELD_KEY]:
                key = annotation[ANNOT_FIELD_KEY][1:-1]
                print(key)

from datetime import date

data_dict = {
    'Risk': '3.8',
    'BitcoinAmount':  bitCoinAmount,
    'EthAmount':    ethereumAmount,
    'USDCAmount': '30',
    'RiskGPA': '3.7'
}

def fill_pdf(input_pdf_path, output_pdf_path, data_dict):
    template_pdf = pdfrw.PdfReader(input_pdf_path)
    for page in template_pdf.pages:
        annotations = page[ANNOT_KEY]
        for annotation in annotations:
            if annotation[SUBTYPE_KEY] == WIDGET_SUBTYPE_KEY:
                if annotation[ANNOT_FIELD_KEY]:
                    key = annotation[ANNOT_FIELD_KEY][1:-1]
                    if key in data_dict.keys():
                        if type(data_dict[key]) == bool:
                            if data_dict[key] == True:
                                annotation.update(pdfrw.PdfDict(
                                    AS=pdfrw.PdfName('Yes')))
                        else:
                            annotation.update(
                                pdfrw.PdfDict(V='{}'.format(data_dict[key]))
                            )
                            annotation.update(pdfrw.PdfDict(AP=''))
    pdfrw.PdfWriter().write(output_pdf_path, template_pdf)

template_pdf.Root.AcroForm.update(pdfrw.PdfDict(NeedAppearances=pdfrw.PdfObject('true')))  # NEW
fill_pdf(pdf_template, pdf_output, data_dict)
