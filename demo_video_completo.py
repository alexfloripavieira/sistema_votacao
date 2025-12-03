#!/usr/bin/env python3
"""
Script para criar vídeo de demonstração COMPLETA do Sistema de Votação Avaí FC
Fluxo: Admin → Inicia Sessão → Cria Votação → Marca Presença → Usuário Vota → Encerra → Relatório
"""

from playwright.sync_api import sync_playwright
import time

def run_demo(playwright):
    # Configurar browser com gravação de vídeo
    browser = playwright.chromium.launch(
        headless=False,
        slow_mo=800,  # Slow motion para melhor visualização
    )

    context = browser.new_context(
        viewport={'width': 1920, 'height': 1080},
        record_video_dir='videos/',
        record_video_size={'width': 1920, 'height': 1080}
    )

    page = context.new_page()

    try:
        print('🎬 Iniciando gravação da demonstração completa...')
        print()

        # ============================================================
        # PARTE 1: ADMIN - PREPARAÇÃO DO SISTEMA
        # ============================================================

        print('👤 ADMIN: Fazendo login...')
        page.goto('http://localhost:8000')
        page.wait_for_timeout(2000)

        page.click('text=Fazer Login')
        page.wait_for_timeout(2000)

        page.fill('input[name="username"]', 'demo_admin')
        page.fill('input[name="password"]', 'demo123')
        page.click('button:has-text("Entrar")')
        page.wait_for_timeout(3000)

        # ============================================================
        # PARTE 2: INICIAR SESSÃO/REUNIÃO
        # ============================================================

        print('📅 ADMIN: Iniciando nova sessão/reunião...')
        page.goto('http://localhost:8000/business/presence/admin/')
        page.wait_for_timeout(2000)

        # Verificar se há botão para iniciar reunião
        start_meeting_button = page.query_selector('button:has-text("Iniciar Reunião")')
        if start_meeting_button:
            print('   Iniciando nova reunião...')
            start_meeting_button.click()
            page.wait_for_timeout(3000)
            print('   ✅ Reunião iniciada!')
        else:
            print('   ℹ️  Reunião já está ativa')

        page.wait_for_timeout(2000)

        # ============================================================
        # PARTE 3: CRIAR VOTAÇÃO
        # ============================================================

        print('🗳️ ADMIN: Criando nova votação...')
        page.goto('http://localhost:8000/business/voting/create/')
        page.wait_for_timeout(2000)

        # Preencher formulário de criação de votação
        page.fill('input[name="title"]', 'Contratação do Novo Técnico')
        page.fill('textarea[name="description"]', 'Votação para decidir se devemos contratar o novo técnico proposto pela diretoria.')

        # Opções da votação (existem 2 opções padrão: A e B)
        option_texts = page.query_selector_all('input[name="option_texts[]"]')
        if len(option_texts) >= 2:
            option_texts[0].fill('Aprovar Contratação')
            option_texts[1].fill('Rejeitar Contratação')

        # Marcar como requer presença
        page.check('input[name="requires_presence"]')

        # Definir datas (hoje e daqui a 7 dias)
        from datetime import datetime, timedelta
        start_date = datetime.now().strftime('%Y-%m-%dT%H:%M')
        end_date = (datetime.now() + timedelta(days=7)).strftime('%Y-%m-%dT%H:%M')

        page.fill('input[name="start_date"]', start_date)
        page.fill('input[name="end_date"]', end_date)

        page.wait_for_timeout(2000)

        # Submeter formulário
        page.click('button:has-text("Criar Votação")')
        page.wait_for_timeout(3000)

        print('   ✅ Votação criada com sucesso!')

        # ============================================================
        # PARTE 4: MARCAR PRESENÇA DE USUÁRIO
        # ============================================================

        print('✅ ADMIN: Marcando presença de usuário comum...')
        page.goto('http://localhost:8000/business/presence/admin/')
        page.wait_for_timeout(2000)

        # Procurar por usuário comum (não admin)
        # Marcar presença do primeiro usuário "Ausente" que não for admin
        print('   Procurando usuário para marcar presença...')
        buttons = page.query_selector_all('button:has-text("Ausente")')
        if buttons and len(buttons) > 0:
            print(f'   Encontrado {len(buttons)} usuário(s) ausente(s)')
            buttons[0].click()
            page.wait_for_timeout(2000)
            print('   ✅ Presença marcada!')
        else:
            print('   ⚠️ Nenhum usuário ausente encontrado')

        page.wait_for_timeout(2000)

        # ============================================================
        # PARTE 5: LOGOUT DO ADMIN
        # ============================================================

        print('🚪 ADMIN: Fazendo logout...')
        page.click('text=Sair')
        page.wait_for_timeout(3000)

        # ============================================================
        # PARTE 6: USUÁRIO COMUM - LOGIN
        # ============================================================

        print()
        print('👤 USUÁRIO: Fazendo login...')
        page.click('text=Fazer Login')
        page.wait_for_timeout(2000)

        # Login com usuário comum (precisa existir no sistema)
        page.fill('input[name="username"]', 'demo_user')
        page.fill('input[name="password"]', 'demo123')
        page.click('button:has-text("Entrar")')
        page.wait_for_timeout(3000)

        # ============================================================
        # PARTE 7: USUÁRIO VOTA
        # ============================================================

        print('🗳️ USUÁRIO: Visualizando votações disponíveis...')
        page.goto('http://localhost:8000/dashboard/')
        page.wait_for_timeout(2000)

        # Clicar na votação criada (procurar pelo link)
        voting_link = page.query_selector('a:has-text("Contratação do Novo Técnico")')
        if voting_link:
            voting_link.click()
            page.wait_for_timeout(3000)
        else:
            print('   ⚠️ Votação não encontrada no dashboard, tentando pela lista...')
            page.goto('http://localhost:8000/business/voting/')
            page.wait_for_timeout(2000)
            voting_link = page.query_selector('a:has-text("Contratação do Novo Técnico")')
            if voting_link:
                voting_link.click()
                page.wait_for_timeout(3000)

        print('📝 USUÁRIO: Votando...')
        # Selecionar primeira opção disponível (pelo nome do campo)
        first_option = page.query_selector('input[name="option_id"]')
        if first_option:
            first_option.click()
            page.wait_for_timeout(1500)

            # Configurar para aceitar o dialog de confirmação
            page.on('dialog', lambda dialog: dialog.accept())

            # Confirmar voto
            page.click('button:has-text("Confirmar Voto")')
            page.wait_for_timeout(3000)

            print('   ✅ Voto registrado com sucesso!')
        else:
            print('   ⚠️ Opções de voto não encontradas')

        # ============================================================
        # PARTE 8: LOGOUT DO USUÁRIO
        # ============================================================

        print('🚪 USUÁRIO: Fazendo logout...')
        page.click('text=Sair')
        page.wait_for_timeout(3000)

        # ============================================================
        # PARTE 9: ADMIN - LOGIN NOVAMENTE
        # ============================================================

        print()
        print('👤 ADMIN: Fazendo login novamente...')
        page.click('text=Fazer Login')
        page.wait_for_timeout(2000)

        page.fill('input[name="username"]', 'demo_admin')
        page.fill('input[name="password"]', 'demo123')
        page.click('button:has-text("Entrar")')
        page.wait_for_timeout(3000)

        # ============================================================
        # PARTE 10: VISUALIZAR RESULTADOS
        # ============================================================

        print('📊 ADMIN: Visualizando resultados da votação...')
        page.goto('http://localhost:8000/business/voting/')
        page.wait_for_timeout(2000)

        # Clicar na votação para ver detalhes
        voting_link = page.query_selector('a:has-text("Contratação do Novo Técnico")')
        if voting_link:
            voting_link.click()
            page.wait_for_timeout(2000)

            # Ver resultados
            results_link = page.query_selector('a:has-text("Resultados")')
            if results_link:
                results_link.click()
                page.wait_for_timeout(4000)

                # Scroll para ver todos os detalhes
                page.evaluate('window.scrollTo(0, document.body.scrollHeight / 2)')
                page.wait_for_timeout(2000)
                page.evaluate('window.scrollTo(0, 0)')
                page.wait_for_timeout(2000)

                print('   ✅ Resultados exibidos!')
            else:
                print('   ⚠️ Link de resultados não encontrado')
        else:
            print('   ⚠️ Votação não encontrada')

        # ============================================================
        # PARTE 11: DASHBOARD FINAL
        # ============================================================

        print('📊 ADMIN: Retornando ao dashboard...')
        page.click('text=Dashboard')
        page.wait_for_timeout(3000)

        # Scroll no dashboard para mostrar estatísticas
        page.evaluate('window.scrollTo(0, document.body.scrollHeight / 3)')
        page.wait_for_timeout(2000)
        page.evaluate('window.scrollTo(0, 0)')
        page.wait_for_timeout(2000)

        print()
        print('✅ Demonstração completa finalizada!')

    except Exception as e:
        print(f'❌ Erro durante a execução: {e}')
        import traceback
        traceback.print_exc()

    finally:
        # Fechar e salvar vídeo
        print()
        print('💾 Salvando vídeo...')
        context.close()
        browser.close()
        print('✅ Vídeo salvo em videos/')

def main():
    print('='*70)
    print('🎥 DEMONSTRAÇÃO COMPLETA - SISTEMA DE VOTAÇÃO AVAÍ FC')
    print('='*70)
    print()
    print('📋 Fluxo da Demonstração:')
    print('  1. Admin faz login')
    print('  2. Admin inicia sessão/reunião')
    print('  3. Admin cria nova votação')
    print('  4. Admin marca presença de usuário')
    print('  5. Admin faz logout')
    print('  6. Usuário comum faz login')
    print('  7. Usuário vota na votação')
    print('  8. Usuário faz logout')
    print('  9. Admin faz login novamente')
    print(' 10. Admin visualiza resultados')
    print(' 11. Admin visualiza dashboard')
    print()
    print('📋 Pré-requisitos:')
    print('  1. Servidor Django rodando em http://localhost:8000')
    print('  2. Usuário demo_admin com senha demo123 (admin)')
    print('  3. Usuário demo_user com senha demo123 (usuário comum)')
    print('  4. Playwright instalado: pip install playwright')
    print('  5. Navegadores instalados: playwright install')
    print()
    print('⏳ Iniciando gravação em 3 segundos...')
    time.sleep(3)

    with sync_playwright() as playwright:
        run_demo(playwright)

    print()
    print('='*70)
    print('🎉 CONCLUÍDO!')
    print('='*70)
    print()
    print('📂 O vídeo foi salvo na pasta "videos/"')
    print('📝 Para converter para formato comum, use:')
    print('   ffmpeg -i videos/*.webm demo_completo_sistema_votacao.mp4')
    print()

if __name__ == '__main__':
    main()
