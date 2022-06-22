from flask import Flask, request
import requests
import pdfrw
from flask_cors import CORS
import io
import base64
from random import randint

app = Flask(__name__)
CORS(app)

bitcoinAmount = 0
ethereumAmount = 0

async def getWalletInformation(api_key, wallet, type):
    with requests.Session() as session:
        h = {'Content-Type': 'application/json',
            'X-API-KEY': api_key}
        r = session.get(f'https://rest.cryptoapis.io/v2/wallet-as-a-service/wallets/{wallet}/{type}',headers=h)
        r.raise_for_status()
        qdata = r.json()
        return float(qdata['data']['item']['confirmedBalance']['amount'])


@app.route("/", methods=['GET', 'POST'])
async def get_crypto_score():

    API_KEY = '43044ac0170dc40fa60cfd249ef3307b64edbab8'
    BASE = 'https://rest.cryptoapis.io/v2'
    BLOCKCHAIN = 'bitcoin'
    NETWORK = 'mainnet'
    WALLET_LIST = request.form['listOfWallets'].split(',')

    #used if we are looking for data on a particular transaction 
    # myTestNetWallet - 62a8e61a25a05500079dda90
    # random MainnetWallet - 3R2UHDGKLQkPmAjBGbdzpET95xYV59hkyw
    #TID = '4b66461bf88b61e1e4326356534c135129defb504c7acb2fd6c92697d79eb250'

    #blockchain-data/bitcoin/testnet/addresses/mzYijhgmzZrmuB7wBDazRKirnChKyow4M3?

    for wallet in WALLET_LIST:
        print(wallet)
        global bitcoinAmount
        global ethereumAmount
        bitcoinAmount += await getWalletInformation(API_KEY, wallet, 'bitcoin/testnet')
        ethereumAmount += await getWalletInformation(API_KEY, wallet, 'ethereum/ropsten')

    # #test for a wallet on the chain
    # #blockchain-data/bitcoin/testnet/addresses/mzYijhgmzZrmuB7wBDazRKirnChKyow4M3?
    # with requests.Session() as session:
    #     h = {'Content-Type': 'application/json',
    #          'X-API-KEY': API_KEY}
    #     r = session.get(f'https://rest.cryptoapis.io/v2/blockchain-data/bitcoin/testnet/addresses/{WALLET_LIST}', headers=h)
    #     r.raise_for_status()
    #     print(json.dumps(r.json(), indent=4, sort_keys=True))

    import os
    #directory = os.getcwd()
    #print(os.path.abspath("AtomicTest.pdf"))

    #pdf_template = "/Users/adityabora/Desktop/AtomicTest.pdf"
    pdf_template = "./PortfolioAnalysisV3.pdf"
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

    from datetime import date

    data_dict = {
        'Risk': randint(0,100),
        'BitcoinAmount':  bitcoinAmount,
        'EthAmount':    ethereumAmount,
        'USDCAmount': randint(0, 10),
        'RiskGPA': '3.7'
    }

    def fill_pdf(input_pdf_path, data_dict):
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
        # pdfrw.PdfWriter().write(output_pdf_path, template_pdf)
        buf = io.BytesIO()
        pdfrw.PdfWriter().write(buf, template_pdf)
        buf.seek(0)
        return base64.encodebytes(buf.read()).decode()

    data = fill_pdf(pdf_template, data_dict)

    bitcoinAmount = 0
    ethereumAmount = 0

    return data

