# Design System

## Paleta de Cores

### Cores Primárias
- **Azul Escuro**: `#1e3a8a` (blue-900)
- **Verde Avai**: `#22c55e` (green-500)
- **Branco**: `#ffffff`

### Cores de Fundo
- **Gradiente Principal**: `bg-gradient-to-br from-gray-900 to-gray-800`
- **Fundo Escuro**: `bg-gray-900`
- **Fundo Secundário**: `bg-gray-800`
- **Fundo de Cards**: `bg-gray-700`

### Cores de Texto
- **Texto Principal**: `text-white`
- **Texto Secundário**: `text-gray-300`
- **Texto Muted**: `text-gray-400`

## Componentes

### Botões

#### Botão Primário
```html
<button class="bg-blue-600 hover:bg-blue-700 text-white rounded-lg px-4 py-2 transition-colors">
    Botão Primário
</button>
```

#### Botão Secundário
```html
<button class="bg-gray-600 hover:bg-gray-700 text-white rounded-lg px-4 py-2 transition-colors">
    Botão Secundário
</button>
```

#### Botão Sucesso
```html
<button class="bg-green-600 hover:bg-green-700 text-white rounded-lg px-4 py-2 transition-colors">
    Botão Sucesso
</button>
```

#### Botão Perigo
```html
<button class="bg-red-600 hover:bg-red-700 text-white rounded-lg px-4 py-2 transition-colors">
    Botão Perigo
</button>
```

### Inputs

#### Input de Texto
```html
<input type="text" 
       class="border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500 bg-gray-800 text-white w-full"
       placeholder="Digite aqui...">
```

#### Textarea
```html
<textarea 
    class="border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500 bg-gray-800 text-white w-full"
    rows="4"
    placeholder="Digite aqui..."></textarea>
```

#### Select
```html
<select class="border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500 bg-gray-800 text-white w-full">
    <option>Opção 1</option>
    <option>Opção 2</option>
</select>
```

### Forms

#### Estrutura de Form
```html
<form class="space-y-4">
    <div>
        <label class="block text-gray-300 mb-2">Label do Campo</label>
        <input type="text" class="border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500 bg-gray-800 text-white w-full">
    </div>
    
    <div>
        <button type="submit" class="bg-blue-600 hover:bg-blue-700 text-white rounded-lg px-4 py-2">
            Enviar
        </button>
    </div>
</form>
```

### Cards

```html
<div class="bg-gray-800 rounded-lg p-6 shadow-lg">
    <h3 class="text-xl font-semibold text-white mb-4">Título do Card</h3>
    <p class="text-gray-300">Conteúdo do card...</p>
</div>
```

### Tabelas

```html
<div class="overflow-x-auto">
    <table class="w-full text-left">
        <thead class="bg-gray-700">
            <tr>
                <th class="px-4 py-3 text-gray-300">Coluna 1</th>
                <th class="px-4 py-3 text-gray-300">Coluna 2</th>
            </tr>
        </thead>
        <tbody>
            <tr class="border-b border-gray-700 hover:bg-gray-700">
                <td class="px-4 py-3 text-white">Dado 1</td>
                <td class="px-4 py-3 text-white">Dado 2</td>
            </tr>
        </tbody>
    </table>
</div>
```

## Layout

### Grid Responsivo
```html
<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
    <!-- Itens -->
</div>
```

### Container
```html
<div class="container mx-auto px-4">
    <!-- Conteúdo -->
</div>
```

### Espaçamento
- **Gap entre elementos**: `gap-4` (1rem)
- **Padding interno**: `px-4 py-2` ou `p-4`
- **Margin**: `mb-4`, `mt-4`, etc.

## Tipografia

### Fontes
- **Família**: `font-sans` (Tailwind default: system-ui, sans-serif)

### Tamanhos
- **Título Principal**: `text-3xl font-bold`
- **Título Secundário**: `text-2xl font-semibold`
- **Título Terciário**: `text-xl font-semibold`
- **Corpo de Texto**: `text-base`
- **Texto Pequeno**: `text-sm`

### Exemplos
```html
<h1 class="text-3xl font-bold text-white mb-6">Título Principal</h1>
<h2 class="text-2xl font-semibold text-white mb-4">Título Secundário</h2>
<p class="text-base text-gray-300">Parágrafo de texto...</p>
```

## Menu/Navegação

```html
<nav class="bg-gray-800 text-white">
    <ul class="flex space-x-4">
        <li>
            <a href="#" class="hover:bg-gray-700 px-4 py-2 rounded transition-colors">
                Link 1
            </a>
        </li>
        <li>
            <a href="#" class="hover:bg-gray-700 px-4 py-2 rounded transition-colors">
                Link 2
            </a>
        </li>
    </ul>
</nav>
```

## Responsividade

### Breakpoints Tailwind
- **sm**: 640px
- **md**: 768px
- **lg**: 1024px
- **xl**: 1280px

### Exemplo de Uso
```html
<div class="text-sm md:text-base lg:text-lg">
    Texto responsivo
</div>
```

## Princípios de Design

- **Mobile First**: Sempre desenvolver pensando em mobile primeiro
- **Consistência**: Usar os mesmos componentes em todo o sistema
- **Acessibilidade**: Garantir contraste adequado e navegação por teclado
- **Performance**: Usar TailwindCSS via CDN para simplicidade
