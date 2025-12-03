#!/usr/bin/env python3
"""
Script SIMPLIFICADO para vídeo de demonstração - mais robusto
"""

from playwright.sync_api import sync_playwright
import time

def run_demo(playwright):
    browser = playwright.chromium.launch(
        headless=False,
        slow_mo=800,
    )

    context = browser.new_context(
        viewport={'width': 1920, 'height': 1080},
        record_video_dir='videos/',
        record_video_size={'width': 1920, 'height': 1080}
    )

    page = context.new_page()

    # Configurar para aceitar todos os dialogs automaticamente
    page.on('dialog', lambda dialog: dialog.accept())

    try:
        print('🎬 Iniciando demonstração...\n')

        # 1. ADMIN LOGIN
        print('1️⃣ Admin fazendo login...')
        page.goto('http://localhost:8000/accounts/login/')
        page.wait_for_timeout(2000)
        page.fill('input[name="username"]', 'demo_admin')
        page.fill('input[name="password"]', 'demo123')
        page.click('button[type="submit"]')
        page.wait_for_timeout(3000)
        print('   ✅ Login realizado\n')

        # 2. DASHBOARD ADMIN
        print('2️⃣ Visualizando dashboard administrativo...')
        page.goto('http://localhost:8000/business/admin-dashboard/')
        page.wait_for_timeout(3000)
        page.evaluate('window.scrollTo(0, document.body.scrollHeight / 2)')
        page.wait_for_timeout(2000)
        page.evaluate('window.scrollTo(0, 0)')
        page.wait_for_timeout(2000)
        print('   ✅ Dashboard visualizado\n')

        # 3. MARCAR PRESENÇA - procurar especificamente demo_user
        print('3️⃣ Marcando presença do usuário demo_user...')
        page.goto('http://localhost:8000/business/presence/admin/')
        page.wait_for_timeout(2000)

        # Procurar campo de busca e filtrar por demo_user
        search_input = page.query_selector('input[type="search"], input[placeholder*="Buscar"], input[placeholder*="pesquisar"]')
        if search_input:
            search_input.fill('demo_user')
            page.wait_for_timeout(1500)

        # Usar script JavaScript para encontrar e clicar no botão certo
        clicked = page.evaluate('''() => {
            const rows = document.querySelectorAll('tr, div.user-row, div[class*="user"]');
            for (const row of rows) {
                const text = row.textContent.toLowerCase();
                if (text.includes('demo_user') || text.includes('joão') || text.includes('joao')) {
                    const buttons = row.querySelectorAll('button');
                    for (const button of buttons) {
                        if (button.textContent.includes('Ausente') && !button.classList.contains('bg-avai-green')) {
                            button.click();
                            return true;
                        }
                    }
                }
            }
            return false;
        }''')

        page.wait_for_timeout(3000)

        if clicked:
            print('   ✅ Presença do demo_user marcada com sucesso!\n')
        else:
            print('   ⚠️ Tentativa de marcar presença (pode já estar marcada)\n')

        # 4. CRIAR VOTAÇÃO
        print('4️⃣ Criando nova votação...')
        page.goto('http://localhost:8000/business/voting/create/')
        page.wait_for_timeout(2000)

        page.fill('input[name="title"]', 'Contratação do Novo Técnico')
        page.fill('textarea[name="description"]', 'Votação para aprovar a contratação do novo técnico.')

        # Preencher opções
        page.evaluate('''
            document.querySelectorAll('input[name="option_texts[]"]')[0].value = 'Aprovar Contratação';
            document.querySelectorAll('input[name="option_texts[]"]')[1].value = 'Rejeitar Contratação';
        ''')

        # Definir datas - 1 hora no passado até 7 dias no futuro
        from datetime import datetime, timedelta
        start_date = (datetime.now() - timedelta(hours=1)).strftime('%Y-%m-%dT%H:%M')
        end_date = (datetime.now() + timedelta(days=7)).strftime('%Y-%m-%dT%H:%M')

        page.fill('input[name="start_date"]', start_date)
        page.fill('input[name="end_date"]', end_date)

        page.wait_for_timeout(2000)
        page.click('button[type="submit"]')
        page.wait_for_timeout(3000)
        print('   ✅ Votação criada\n')

        # 5. ADMIN LOGOUT
        print('5️⃣ Admin fazendo logout...')
        page.goto('http://localhost:8000/accounts/logout/')
        page.wait_for_timeout(3000)
        print('   ✅ Logout realizado\n')

        # 6. USER LOGIN
        print('6️⃣ Usuário demo_user fazendo login...')
        page.goto('http://localhost:8000/accounts/login/')
        page.wait_for_timeout(2000)
        page.fill('input[name="username"]', 'demo_user')
        page.fill('input[name="password"]', 'demo123')
        page.click('button[type="submit"]')
        page.wait_for_timeout(3000)
        print('   ✅ Login realizado\n')

        # 7. VISUALIZAR E VOTAR
        print('7️⃣ Visualizando votações disponíveis...')
        # Ir direto para lista de votações
        page.goto('http://localhost:8000/business/voting/')
        page.wait_for_timeout(3000)

        # Procurar link da votação
        voting_link = page.query_selector('a:has-text("Contratação do Novo Técnico")')
        if voting_link:
            print('   📋 Votação encontrada! Acessando...')
            voting_link.click()
            page.wait_for_timeout(3000)

            # Verificar se pode votar
            can_vote = page.query_selector('button:has-text("Confirmar Voto")')
            if can_vote:
                print('   ✅ Usuário tem permissão para votar!')

                # Votar
                first_radio = page.query_selector('input[name="option_id"]')
                if first_radio:
                    first_radio.click()
                    page.wait_for_timeout(1500)

                    print('   📝 Confirmando voto...')
                    page.click('button:has-text("Confirmar Voto")')
                    page.wait_for_timeout(3000)
                    print('   ✅ Voto registrado com sucesso!\n')
                else:
                    print('   ⚠️ Opções de voto não encontradas\n')
            else:
                print('   ⚠️ Usuário não tem permissão para votar (presença não marcada?)\n')
        else:
            print('   ⚠️ Votação não encontrada na lista\n')

        # 8. USER LOGOUT
        print('8️⃣ Usuário fazendo logout...')
        page.goto('http://localhost:8000/accounts/logout/')
        page.wait_for_timeout(3000)
        print('   ✅ Logout realizado\n')

        # 9. ADMIN LOGIN NOVAMENTE
        print('9️⃣ Admin fazendo login novamente...')
        page.goto('http://localhost:8000/accounts/login/')
        page.wait_for_timeout(2000)
        page.fill('input[name="username"]', 'demo_admin')
        page.fill('input[name="password"]', 'demo123')
        page.click('button[type="submit"]')
        page.wait_for_timeout(3000)
        print('   ✅ Login realizado\n')

        # 10. VER RESULTADOS
        print('🔟 Visualizando resultados...')
        page.goto('http://localhost:8000/business/voting/')
        page.wait_for_timeout(2000)

        # Clicar na votação
        voting_link = page.query_selector('a:has-text("Contratação do Novo Técnico")')
        if voting_link:
            voting_link.click()
            page.wait_for_timeout(3000)

            # Ver resultados detalhados se disponível
            results_btn = page.query_selector('a:has-text("Resultados")')
            if results_btn:
                results_btn.click()
                page.wait_for_timeout(4000)
                page.evaluate('window.scrollTo(0, document.body.scrollHeight / 2)')
                page.wait_for_timeout(2000)
                page.evaluate('window.scrollTo(0, 0)')
                page.wait_for_timeout(2000)
                print('   ✅ Resultados exibidos\n')

        # 11. DASHBOARD FINAL
        print('1️⃣1️⃣ Retornando ao dashboard...')
        page.goto('http://localhost:8000/business/admin-dashboard/')
        page.wait_for_timeout(3000)
        page.evaluate('window.scrollTo(0, document.body.scrollHeight / 3)')
        page.wait_for_timeout(2000)
        page.evaluate('window.scrollTo(0, 0)')
        page.wait_for_timeout(3000)
        print('   ✅ Dashboard exibido\n')

        print('✅ DEMONSTRAÇÃO COMPLETA!\n')

    except Exception as e:
        print(f'\n❌ Erro: {e}\n')
        import traceback
        traceback.print_exc()

    finally:
        print('💾 Salvando vídeo...')
        context.close()
        browser.close()
        print('✅ Vídeo salvo!\n')

def main():
    print('='*70)
    print('🎥 DEMONSTRAÇÃO - SISTEMA DE VOTAÇÃO AVAÍ FC')
    print('='*70)
    print()
    print('⏳ Iniciando em 3 segundos...\n')
    time.sleep(3)

    with sync_playwright() as playwright:
        run_demo(playwright)

    print('='*70)
    print('🎉 CONCLUÍDO!')
    print('='*70)
    print('\n📂 Vídeo salvo em: videos/')
    print('📝 Converter para MP4: ffmpeg -i videos/*.webm demo_final.mp4\n')

if __name__ == '__main__':
    main()
