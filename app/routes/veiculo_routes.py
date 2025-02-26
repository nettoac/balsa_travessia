from flask import Blueprint, render_template, request, redirect, url_for, flash
from ..services.veiculo_service import VeiculoService

veiculo_bp = Blueprint('veiculo', __name__)

@veiculo_bp.route('/veiculos/cadastrar', methods=['GET', 'POST'])
def cadastrar_veiculo():
    if request.method == 'POST':
        tipo = request.form['tipo']
        peso_medio = request.form['peso_medio']
        VeiculoService.create_veiculo({'tipo': tipo, 'peso_medio': peso_medio})
        flash('Veículo cadastrado com sucesso!', 'success')
        return redirect(url_for('veiculo.cadastrar_veiculo'))
    
    veiculos = VeiculoService.get_all_veiculos()
    return render_template('cadastrar_veiculo.html', veiculos=veiculos)

@veiculo_bp.route('/veiculos/editar/<int:id>', methods=['GET', 'POST'])
def editar_veiculo(id):
    veiculo = VeiculoService.get_veiculo_by_id(id)
    if request.method == 'POST':
        tipo = request.form['tipo']
        peso_medio = request.form['peso_medio']
        VeiculoService.update_veiculo(id, {'tipo': tipo, 'peso_medio': peso_medio})
        flash('Veículo atualizado com sucesso!', 'success')
        return redirect(url_for('veiculo.cadastrar_veiculo'))
    
    return render_template('editar_veiculo.html', veiculo=veiculo)

@veiculo_bp.route('/veiculos/excluir/<int:id>', methods=['POST'])
def excluir_veiculo(id):
    VeiculoService.delete_veiculo(id)
    flash('Veículo excluído com sucesso!', 'success')
    return redirect(url_for('veiculo.cadastrar_veiculo'))