#!/usr/bin/env python3
"""
Script para criar vídeo de demonstração do Sistema de Votação Avaí FC
Usa Playwright para gravar navegação automatizada pelo sistema
"""

from playwright.sync_api import sync_playwright
import time

def run_demo(playwright):
    # Configurar browser com gravação de vídeo
    browser = playwright.chromium.launch(
        headless=False,  # Mostrar navegador
        slow_mo=1000,  # Slow motion para melhor visualização
    )

    # Criar contexto com gravação de vídeo
    context = browser.new_context(
        viewport={'width': 1920, 'height': 1080},
        record_video_dir='videos/',
        record_video_size={'width': 1920, 'height': 1080}
    )

    page = context.new_page()

    try:
        print('🎬 Iniciando gravação da demonstração...')

        # 1. PÁGINA INICIAL
        print('📍 Navegando para página inicial...')
        page.goto('http://localhost:8000')
        page.wait_for_timeout(3000)

        # 2. LOGIN
        print('🔐 Fazendo login...')
        page.click('text=Fazer Login')
        page.wait_for_timeout(2000)

        # Se já estiver logado, vai direto pro dashboard
        # Se não, preenche o formulário
        if 'login' in page.url:
            page.fill('input[name="username"]', 'demo_admin')
            page.fill('input[name="password"]', 'demo123')
            page.click('button:has-text("Entrar")')
            page.wait_for_timeout(2000)

        # 3. DASHBOARD ADMINISTRATIVO
        print('📊 Mostrando dashboard...')
        page.wait_for_timeout(3000)

        # Navegar para Admin Dashboard completo
        page.click('text=Admin Dashboard')
        page.wait_for_timeout(4000)

        # Scroll para ver votantes mais ativos
        page.evaluate('window.scrollTo(0, document.body.scrollHeight / 2)')
        page.wait_for_timeout(2000)
        page.evaluate('window.scrollTo(0, 0)')
        page.wait_for_timeout(1000)

        # 4. MARCAR PRESENÇA
        print('✅ Demonstrando marcação de presença...')
        page.click('text=Marcar Presença')
        page.wait_for_timeout(3000)

        # Marcar presença de 3 usuários
        print('   Marcando presença de usuários...')
        for i in range(3):
            buttons = page.query_selector_all('button:has-text("Ausente")')
            if buttons and len(buttons) > i:
                buttons[i].click()
                page.wait_for_timeout(1500)

        page.wait_for_timeout(2000)

        # 5. VOTAÇÕES
        print('🗳️ Navegando para votações...')
        page.click('a:has-text("Votações")')
        page.wait_for_timeout(3000)

        # 6. VER RESULTADOS DE UMA VOTAÇÃO
        print('📈 Visualizando resultados...')
        page.click('a[href*="/business/admin-dashboard/"]')
        page.wait_for_timeout(2000)

        # Clicar no primeiro resultado
        page.click('a:has-text("Resultados")>> nth=0')
        page.wait_for_timeout(4000)

        # Scroll para ver todos os resultados
        page.evaluate('window.scrollTo(0, document.body.scrollHeight / 2)')
        page.wait_for_timeout(2000)
        page.evaluate('window.scrollTo(0, 0)')
        page.wait_for_timeout(2000)

        # 7. VOLTAR PARA DASHBOARD
        print('🏠 Voltando ao dashboard...')
        page.click('text=Dashboard')
        page.wait_for_timeout(3000)

        # 8. PÁGINA INICIAL FINAL
        print('👋 Finalizando...')
        page.click('text=Sistema de Votação')
        page.wait_for_timeout(3000)

        print('✅ Demonstração completa!')

    finally:
        # Fechar e salvar vídeo
        print('💾 Salvando vídeo...')
        context.close()
        browser.close()
        print('✅ Vídeo salvo em videos/')

def main():
    print('='*60)
    print('🎥 GRAVAÇÃO DE DEMONSTRAÇÃO - SISTEMA DE VOTAÇÃO AVAÍ FC')
    print('='*60)
    print()
    print('📋 Pré-requisitos:')
    print('  1. Servidor Django rodando em http://localhost:8000')
    print('  2. Usuário demo_admin com senha demo123 criado')
    print('  3. Playwright instalado: pip install playwright')
    print('  4. Navegadores instalados: playwright install')
    print()
    print('⏳ Iniciando gravação em 3 segundos...')
    time.sleep(3)

    with sync_playwright() as playwright:
        run_demo(playwright)

    print()
    print('='*60)
    print('🎉 CONCLUÍDO!')
    print('='*60)
    print()
    print('📂 O vídeo foi salvo na pasta "videos/"')
    print('📝 Para converter para formato comum, use:')
    print('   ffmpeg -i videos/*.webm demo_sistema_votacao.mp4')
    print()

if __name__ == '__main__':
    main()
