"""Versão funcional, enviando para os email conforme extração do arquivo .CSV"""

import pandas as pd
from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import TA_LEFT
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

# Ler o arquivo CSV
csv_file = 'templatecorrecaoprova.csv'
data = pd.read_csv(csv_file)

# Encontrar índices das colunas 'Nome Completo' e 'Email'
nome_index = data.columns.get_loc('Nome Completo')
email_index = data.columns.get_loc('Email')

# Percorrer as linhas e gerar PDF e enviar email
for index, row in data.iterrows():
    nome = row[nome_index]
    email = row[email_index]


    # Gerar PDF
    pdf_file = f'{nome}_dados.pdf'
    doc = SimpleDocTemplate(pdf_file, pagesize=landscape(letter), rightMargin=72)

    elements = []
    style = getSampleStyleSheet()["Normal"]
    style.alignment = TA_LEFT

    for column, value in row.items():
        if "■■" in str(value):
            value = value.replace("■■", "<br/>")  # Quebrar linha onde "■■" é encontrado
        elif "RESPOSTA" in str(value) or "COMENTARIO" in str(value):
            value = "<br/><br/>" + value  # Quebrar duas linhas para baixo quando "RESPOSTA" ou "COMENTARIO" é encontrado
        p = Paragraph(f"<b>{column}:</b> {value}", style)
        elements.append(p)

    doc.build(elements)


    # Enviar email
    subject = 'Seus dados'
    body = f'Olá {nome},\n\nSegue em anexo seus dados em PDF.'
    sender_email = 'mathpcv@gmail.com'
    sender_password = 'zdyupvdyvvsoewhv'
    receiver_email = email

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    with open(pdf_file, 'rb') as f:
        attach = MIMEApplication(f.read(), _subtype="pdf")
        attach.add_header('Content-Disposition', f'attachment; filename= {pdf_file}')
        msg.attach(attach)

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender_email, sender_password)
    server.sendmail(sender_email, receiver_email, msg.as_string())
    server.quit()

    print(f'Email enviado para {nome} ({email}) com sucesso!')

"""##Versão abaixo é de testes para implementação da função do envio por WhatsApp!

"""

import pandas as pd
import time
from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import TA_LEFT
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


# Ler o arquivo CSV
csv_file = 'templatecorrecaoprova.csv'
data = pd.read_csv(csv_file)

# Encontrar índices das colunas 'Nome' e 'Email'
nome_index = data.columns.get_loc('Nome Completo')
email_index = data.columns.get_loc('Email')
celular_index = data.columns.get_loc('celular')

# Percorrer as linhas e gerar PDF e enviar email
for index, row in data.iterrows():
    nome = row[nome_index]
    email = row[email_index]
    celular = row[celular_index]

    # Gerar PDF
    pdf_file = f'{nome}_dados.pdf'
    doc = SimpleDocTemplate(pdf_file, pagesize=landscape(letter), rightMargin=72)

    elements = []
    style = getSampleStyleSheet()["Normal"]
    style.alignment = TA_LEFT

    for column, value in row.items():
        if "■■" in str(value):
            value = value.replace("■■", "<br/>")  # Quebrar linha onde "■■" é encontrado
        elif "RESPOSTA" in str(value) or "COMENTARIO" in str(value):
            value = "<br/><br/>" + value  # Quebrar duas linhas para baixo quando "RESPOSTA" ou "COMENTARIO" é encontrado
        p = Paragraph(f"<b>{column}:</b> {value}", style)
        elements.append(p)

    doc.build(elements)

   # Enviar mensagem do WhatsApp
   #Necessário ter chromedriver no webdriver
    message = f"Olá {nome}, segue em anexo seus dados em PDF."

    driver = webdriver.Chrome()
    driver.get("https://web.whatsapp.com/")
    time.sleep(10)  # Aguardar a página carregar

    search_box = driver.find_element_by_xpath("//div[@contenteditable='true']")
    search_box.send_keys(celular + Keys.ENTER)
    time.sleep(3)  # Aguardar a conversa ser aberta

    message_box = driver.find_element_by_xpath("//div[@contenteditable='true'][@data-tab='1']")
    message_box.send_keys(message + Keys.ENTER)
    time.sleep(3)  # Aguardar a mensagem ser enviada

    print(f'Mensagem enviada para {nome} ({email}) no WhatsApp com sucesso!')

    # Enviar email
    subject = 'Seus dados'
    body = f'Olá {nome},\n\nSegue em anexo seus dados em PDF.'
    sender_email = 'mathpcv@gmail.com'
    sender_password = 'zdyupvdyvvsoewhv'
    receiver_email = email

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    with open(pdf_file, 'rb') as f:
        attach = MIMEApplication(f.read(), _subtype="pdf")
        attach.add_header('Content-Disposition', f'attachment; filename= {pdf_file}')
        msg.attach(attach)

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender_email, sender_password)
    server.sendmail(sender_email, receiver_email, msg.as_string())
    server.quit()

    print(f'Email enviado para {nome} ({email}) com sucesso!')