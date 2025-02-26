from flask import Blueprint, render_template
from ..services.viagem_service import ViagemService
from ..services.balsa_service import BalsaService
from ..services.veiculo_service import VeiculoService
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from openpyxl import Workbook
from io import BytesIO
from flask import request, send_file
import base64
import tempfile
from PIL import Image


relatorio_bp = Blueprint('relatorio', __name__)

@relatorio_bp.route('/relatorios/gerar')
def gerar_relatorio():
    viagens = ViagemService.get_all_viagens()
    balsas = BalsaService.get_all_balsas()
    veiculos = VeiculoService.get_all_veiculos()

    # Dados para os gráficos
    balsas_labels = [balsa.nome for balsa in balsas]
    balsas_data = [sum(viagem.quantidade_veiculos for viagem in viagens if viagem.balsa_id == balsa.id) for balsa in balsas]

    veiculos_labels = [veiculo.tipo for veiculo in veiculos]
    veiculos_data = [sum(registro.quantidade for viagem in viagens for registro in viagem.registros if registro.veiculo_id == veiculo.id) for veiculo in veiculos]

    viagens_labels = [f"{viagem.data_hora} - {viagem.balsa.nome}" for viagem in viagens]
    viagens_data = [viagem.quantidade_veiculos for viagem in viagens]

    return render_template('gerar_relatorio.html', 
                          viagens=viagens, 
                          balsas_labels=balsas_labels, 
                          balsas_data=balsas_data, 
                          veiculos_labels=veiculos_labels, 
                          veiculos_data=veiculos_data, 
                          viagens_labels=viagens_labels, 
                          viagens_data=viagens_data)


@relatorio_bp.route('/relatorios/exportar_excel')
def exportar_excel():
    viagens = ViagemService.get_all_viagens()

    # Cria um arquivo Excel
    wb = Workbook()
    ws = wb.active
    ws.title = "Viagens"

    # Cabeçalho
    ws.append(["ID", "Balsa", "Data e Hora", "Veículos", "Total de Veículos"])

    # Dados
    for viagem in viagens:
        veiculos = ", ".join([f"{registro.veiculo.tipo}: {registro.quantidade}" for registro in viagem.registros])
        ws.append([viagem.id, viagem.balsa.nome, viagem.data_hora, veiculos, viagem.quantidade_veiculos])

    # Salva o arquivo em memória
    buffer = BytesIO()
    wb.save(buffer)
    buffer.seek(0)

    return send_file(buffer, as_attachment=True, download_name="relatorio_viagens.xlsx", mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")


@relatorio_bp.route('/relatorios/exportar_pdf', methods=['POST'])
def exportar_pdf():
    data = request.json
    balsa_img = data.get('balsaImg')
    veiculo_img = data.get('veiculoImg')
    viagens_img = data.get('viagensImg')

    # Decodifica as imagens
    balsa_img_data = base64.b64decode(balsa_img.split(',')[1])
    veiculo_img_data = base64.b64decode(veiculo_img.split(',')[1])
    viagens_img_data = base64.b64decode(viagens_img.split(',')[1])

    # Salva as imagens em arquivos temporários
    with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as tmp_balsa:
        tmp_balsa.write(balsa_img_data)
        tmp_balsa_path = tmp_balsa.name

    with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as tmp_veiculo:
        tmp_veiculo.write(veiculo_img_data)
        tmp_veiculo_path = tmp_veiculo.name

    with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as tmp_viagens:
        tmp_viagens.write(viagens_img_data)
        tmp_viagens_path = tmp_viagens.name

    # Cria o PDF
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)

    # Adiciona o título
    p.setFont("Helvetica-Bold", 16)
    p.drawString(50, 750, "RELATÓRIO DE TRAVESSIAS")

    # Adiciona os gráficos lado a lado
    p.setFont("Helvetica", 12)
    y = 720  # Posição inicial após o título

    # Gráfico de Quantidades por Balsa
    p.drawString(50, y, "Quantidades por Balsa")
    p.drawImage(tmp_balsa_path, 50, y - 120, width=150, height=120)  # Ajuste a posição e o tamanho

    # Gráfico de Viagens por Veículos
    p.drawString(250, y, "Viagens por Veículos")
    p.drawImage(tmp_veiculo_path, 250, y - 120, width=150, height=120)

    # Gráfico de Viagens por Data / Balsa / Veículos
    p.drawString(450, y, "Viagens por Data / Balsa / Veículos")
    p.drawImage(tmp_viagens_path, 450, y - 120, width=150, height=120)

    y -= 140  # Espaçamento após os gráficos

    # Adiciona a linha consolidada por Ano e Mês
    p.setFont("Helvetica-Bold", 14)
    p.drawString(50, y, "Consolidado por Ano e Mês")
    y -= 20  # Espaçamento após o título consolidado

    p.setFont("Helvetica", 12)
    viagens = ViagemService.get_all_viagens()

    # Agrupa viagens por Ano e Mês
    consolidado = {}
    for viagem in viagens:
        ano_mes = viagem.data_hora.strftime('%Y-%m')
        if ano_mes not in consolidado:
            consolidado[ano_mes] = {
                'quantidade_veiculos': 0,
                'viagens': []
            }
        consolidado[ano_mes]['quantidade_veiculos'] += viagem.quantidade_veiculos
        consolidado[ano_mes]['viagens'].append(viagem)

    # Exibe o consolidado
    for ano_mes, dados in consolidado.items():
        p.drawString(50, y, f"{ano_mes}: {dados['quantidade_veiculos']} veículos transportados")
        y -= 20  # Espaçamento entre os consolidados

    # Adiciona a listagem de viagens
    p.setFont("Helvetica-Bold", 14)
    p.drawString(50, y, "Listagem de Viagens")
    y -= 20  # Espaçamento após o título da listagem

    p.setFont("Helvetica", 12)
    for viagem in viagens:
        p.drawString(50, y, f"ID: {viagem.id}")
        p.drawString(50, y - 20, f"Balsa: {viagem.balsa.nome}")
        p.drawString(50, y - 40, f"Data e Hora: {viagem.data_hora}")
        p.drawString(50, y - 60, f"Veículos: {', '.join([f'{registro.veiculo.tipo}: {registro.quantidade}' for registro in viagem.registros])}")
        p.drawString(50, y - 80, f"Total de Veículos: {viagem.quantidade_veiculos}")
        y -= 100  # Espaçamento entre viagens

        # Verifica se a página está cheia e cria uma nova página
        if y < 50:
            p.showPage()
            y = 750  # Reinicia a posição Y no topo da nova página
            p.setFont("Helvetica", 12)

    p.showPage()
    p.save()
    buffer.seek(0)

    return send_file(buffer, as_attachment=True, download_name="relatorio_viagens.pdf", mimetype="application/pdf")