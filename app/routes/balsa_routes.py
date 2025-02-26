from flask import Blueprint, render_template, request, redirect, url_for, flash
from ..services.balsa_service import BalsaService

balsa_bp = Blueprint('balsa', __name__)

@balsa_bp.route('/balsas/cadastrar', methods=['GET', 'POST'])
def cadastrar_balsa():
    if request.method == 'POST':
        nome = request.form['nome']
        capacidade_maxima = request.form['capacidade_maxima']
        BalsaService.create_balsa({'nome': nome, 'capacidade_maxima': capacidade_maxima})
        flash('Balsa cadastrada com sucesso!', 'success')
        return redirect(url_for('balsa.cadastrar_balsa'))
    
    balsas = BalsaService.get_all_balsas()
    return render_template('cadastrar_balsa.html', balsas=balsas)

@balsa_bp.route('/balsas/editar/<int:id>', methods=['GET', 'POST'])
def editar_balsa(id):
    balsa = BalsaService.get_balsa_by_id(id)
    if request.method == 'POST':
        nome = request.form['nome']
        capacidade_maxima = request.form['capacidade_maxima']
        BalsaService.update_balsa(id, {'nome': nome, 'capacidade_maxima': capacidade_maxima})
        flash('Balsa atualizada com sucesso!', 'success')
        return redirect(url_for('balsa.cadastrar_balsa'))
    
    return render_template('editar_balsa.html', balsa=balsa)

@balsa_bp.route('/balsas/excluir/<int:id>', methods=['POST'])
def excluir_balsa(id):
    BalsaService.delete_balsa(id)
    flash('Balsa excluída com sucesso!', 'success')
    return redirect(url_for('balsa.cadastrar_balsa'))