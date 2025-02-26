from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for, flash
from ..services.viagem_service import ViagemService
from ..services.balsa_service import BalsaService
from ..services.veiculo_service import VeiculoService
from ..services.registro_service import RegistroService
from .. import db

viagem_bp = Blueprint('viagem', __name__)

@viagem_bp.route('/viagens/iniciar', methods=['GET', 'POST'])
def iniciar_viagem():
    if request.method == 'POST':
        balsa_id = request.form['balsa_id']
        data_hora_str = request.form['data_hora']
        
        # Converte a string para um objeto datetime
        data_hora = datetime.strptime(data_hora_str, '%Y-%m-%dT%H:%M')
        
        # Processar os veículos e suas quantidades
        veiculos = VeiculoService.get_all_veiculos()
        quantidade_total = 0  # Inicializa a quantidade total de veículos
        for veiculo in veiculos:
            quantidade = int(request.form.get(f'veiculo_{veiculo.id}', 0))
            quantidade_total += quantidade  # Soma as quantidades

        # Criar a viagem com a quantidade total de veículos
        viagem = ViagemService.create_viagem({
            'balsa_id': balsa_id,
            'data_hora': data_hora,
            'quantidade_veiculos': quantidade_total  # Passa a quantidade total
        })

        # Criar os registros de travessia para cada veículo
        for veiculo in veiculos:
            quantidade = int(request.form.get(f'veiculo_{veiculo.id}', 0))
            if quantidade > 0:
                RegistroService.create_registro({
                    'viagem_id': viagem.id,
                    'veiculo_id': veiculo.id,
                    'quantidade': quantidade
                })

        flash('Viagem iniciada com sucesso!', 'success')
        return redirect(url_for('viagem.iniciar_viagem'))

    # Carregar balsas, veículos e viagens para o formulário
    balsas = BalsaService.get_all_balsas()
    veiculos = VeiculoService.get_all_veiculos()
    viagens = ViagemService.get_all_viagens()
    return render_template('iniciar_viagem.html', balsas=balsas, veiculos=veiculos, viagens=viagens)

@viagem_bp.route('/viagens/editar/<int:id>', methods=['GET', 'POST'])
def editar_viagem(id):
    viagem = ViagemService.get_viagem_by_id(id)
    veiculos = VeiculoService.get_all_veiculos()

    if request.method == 'POST':
        # Atualizar a data e hora da viagem
        data_hora_str = request.form['data_hora']
        data_hora = datetime.strptime(data_hora_str, '%Y-%m-%dT%H:%M')
        viagem.data_hora = data_hora

        # Atualizar as quantidades dos veículos
        quantidade_total = 0
        for veiculo in veiculos:
            quantidade = int(request.form.get(f'veiculo_{veiculo.id}', 0))
            quantidade_total += quantidade

            # Atualizar ou criar o registro de travessia
            registro = RegistroService.get_registro_by_viagem_e_veiculo(viagem.id, veiculo.id)
            if registro:
                registro.quantidade = quantidade
            else:
                RegistroService.create_registro({
                    'viagem_id': viagem.id,
                    'veiculo_id': veiculo.id,
                    'quantidade': quantidade
                })

        # Atualizar a quantidade total de veículos
        viagem.quantidade_veiculos = quantidade_total
        db.session.commit()

        flash('Viagem atualizada com sucesso!', 'success')
        return redirect(url_for('viagem.iniciar_viagem'))

    return render_template('editar_viagem.html', viagem=viagem, veiculos=veiculos)

@viagem_bp.route('/viagens/excluir/<int:id>', methods=['POST'])
def excluir_viagem(id):
    ViagemService.delete_viagem(id)
    flash('Viagem excluída com sucesso!', 'success')
    return redirect(url_for('viagem.iniciar_viagem'))