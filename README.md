# AXIOM Site — Estrutura do Projeto

Apresentação executiva modular, preparada para novas páginas e integrações (chatbot, leads, UnicornStudio).

## Estrutura de pastas

```
Site/
├── index.html              # Página principal (HTML sem CSS/JS inline)
├── index.html.backup       # Cópia do monólito original (referência)
├── app.py                  # API FastAPI do chatbot (opcional)
├── assets/
│   ├── css/
│   │   ├── main.css        # Entry — importa todos os módulos
│   │   ├── 00-foundation.css
│   │   ├── 03-navigation.css
│   │   └── …               # Um arquivo por área (nav, hero, chatbot…)
│   ├── js/
│   │   ├── config.js       # Config global (rotas, endpoints)
│   │   ├── main.js         # Bootstrap
│   │   ├── modules/
│   │   │   ├── scroll-ui.js
│   │   │   ├── chatbot.js
│   │   │   └── lead-form.js
│   │   └── vendors/
│   │       ├── unicorn-loader-main.js
│   │       ├── unicorn-loader-contato.js
│   │       └── img-fallback.js
│   └── images/
│       ├── logo-nav.webp
│       ├── hero-visual.jpg
│       └── profile-marcos.png
├── pages/
│   └── _template.html      # Modelo para nova página
└── scripts/
    ├── refactor_site.py
    └── extract_images.py
```

## Páginas

| Página | Arquivo | Unicorn Project ID |
|--------|---------|-------------------|
| Strategic Intelligence (home) | `index.html` | `yWZ2Tbe094Fsjgy9NRnD` |
| **Human Performance** | `pages/human-performance.html` | `UtvhDctN8AjL6tvf1yKd` (efeito alternativo) |

Troque o ID em `config.js` → `pages.humanPerformance.unicornProjectId` quando criar um projeto dedicado no UnicornStudio.

## Nova página

1. Copie `pages/_template.html` → `pages/sua-pagina.html`.
2. Registre em `assets/js/config.js` em `pages` (id, path, title, `unicornProjectId`).
3. `data-axiom-page="seu-id"` no `<body>` + `data-us-project` no background.
4. Estilos em `assets/css/pages/sua-pagina.css` (link só na página, como Human Performance).
5. Link no `<nav>` do `index.html` e da nova página.

## Chatbot (FastAPI)

No HTML, configure o endpoint no elemento do chatbot:

```html
<div id="axiom-chatbot" data-chatbot-endpoint="http://localhost:8000/chat" …>
```

Ou em `assets/js/config.js`:

```js
chatbot: { endpoint: "http://localhost:8000/chat" }
```

A API em `app.py` espera `{ "pergunta": "..." }` e retorna `{ "resposta": "..." }`. O front envia `{ "message": "..." }` — alinhe o backend ou adapte `chatbot.js` ao conectar.

## Performance

- HTML ~27 KB (antes ~1,3 MB com imagens embutidas).
- Imagens em arquivos separados (cache do navegador).
- CSS e JS em módulos (manutenção e cache).
- Removido código de debug de telemetria local.

## Restaurar versão monolítica

Use `index.html.backup` se precisar comparar ou reverter manualmente.
