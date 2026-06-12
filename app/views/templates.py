def success_page(email: str) -> str:
    """Retorna a página HTML de sucesso (glassmorphism + confetti)."""
    return f"""\
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Vinculação Confirmada</title>
    <link rel="preconnect" href="https://fonts.googleapis.com" />
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet" />
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}

        body {{
            font-family: 'Inter', sans-serif;
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
            overflow: hidden;
            position: relative;
        }}

        .orb {{
            position: fixed;
            border-radius: 50%;
            filter: blur(80px);
            opacity: 0.4;
            animation: float 8s ease-in-out infinite;
        }}
        .orb-1 {{ width: 400px; height: 400px; background: #6366f1; top: -100px; left: -100px; animation-delay: 0s; }}
        .orb-2 {{ width: 300px; height: 300px; background: #8b5cf6; bottom: -80px; right: -80px; animation-delay: 2s; }}
        .orb-3 {{ width: 200px; height: 200px; background: #a78bfa; top: 50%; left: 60%; animation-delay: 4s; }}

        @keyframes float {{
            0%, 100% {{ transform: translateY(0) scale(1); }}
            50% {{ transform: translateY(-30px) scale(1.05); }}
        }}

        .card {{
            position: relative;
            z-index: 1;
            background: rgba(255, 255, 255, 0.06);
            backdrop-filter: blur(24px);
            -webkit-backdrop-filter: blur(24px);
            border: 1px solid rgba(255, 255, 255, 0.12);
            border-radius: 24px;
            padding: 48px 40px;
            max-width: 460px;
            width: 90%;
            text-align: center;
            box-shadow: 0 8px 40px rgba(0, 0, 0, 0.3);
            animation: slideUp 0.6s cubic-bezier(0.16, 1, 0.3, 1) forwards;
            opacity: 0;
            transform: translateY(30px);
        }}

        @keyframes slideUp {{
            to {{ opacity: 1; transform: translateY(0); }}
        }}

        .icon-circle {{
            width: 80px;
            height: 80px;
            margin: 0 auto 24px;
            border-radius: 50%;
            background: linear-gradient(135deg, #22c55e, #16a34a);
            display: flex;
            align-items: center;
            justify-content: center;
            box-shadow: 0 0 30px rgba(34, 197, 94, 0.4);
            animation: pulse 2s ease-in-out infinite;
        }}

        @keyframes pulse {{
            0%, 100% {{ box-shadow: 0 0 30px rgba(34, 197, 94, 0.4); }}
            50% {{ box-shadow: 0 0 50px rgba(34, 197, 94, 0.6); }}
        }}

        .icon-circle svg {{
            width: 40px;
            height: 40px;
            stroke: #fff;
            stroke-width: 3;
            fill: none;
            stroke-linecap: round;
            stroke-linejoin: round;
            animation: drawCheck 0.6s 0.4s ease forwards;
            stroke-dasharray: 60;
            stroke-dashoffset: 60;
        }}

        @keyframes drawCheck {{
            to {{ stroke-dashoffset: 0; }}
        }}

        h1 {{
            color: #f1f5f9;
            font-size: 26px;
            font-weight: 700;
            margin-bottom: 12px;
        }}

        .subtitle {{
            color: #94a3b8;
            font-size: 15px;
            line-height: 1.6;
            margin-bottom: 8px;
        }}

        .email-badge {{
            display: inline-block;
            background: rgba(99, 102, 241, 0.2);
            border: 1px solid rgba(99, 102, 241, 0.3);
            color: #a5b4fc;
            padding: 6px 16px;
            border-radius: 20px;
            font-size: 14px;
            font-weight: 500;
            margin-top: 16px;
            letter-spacing: 0.3px;
        }}

        .footer-text {{
            margin-top: 32px;
            font-size: 12px;
            color: #64748b;
        }}

        .confetti {{
            position: fixed;
            width: 8px;
            height: 8px;
            border-radius: 2px;
            opacity: 0;
            z-index: 10;
            animation: confettiFall 3s ease-in forwards;
        }}

        @keyframes confettiFall {{
            0% {{ opacity: 1; transform: translateY(-100vh) rotate(0deg); }}
            100% {{ opacity: 0; transform: translateY(100vh) rotate(720deg); }}
        }}
    </style>
</head>
<body>
    <div class="orb orb-1"></div>
    <div class="orb orb-2"></div>
    <div class="orb orb-3"></div>

    <div class="card">
        <div class="icon-circle">
            <svg viewBox="0 0 24 24">
                <polyline points="20 6 9 17 4 12"></polyline>
            </svg>
        </div>
        <h1>Conexão Confirmada!</h1>
        <p class="subtitle">
            Seu número de celular foi vinculado com sucesso à sua conta Phiz.
            Agora você pode fechar esta página.
        </p>
        <div class="email-badge">{email}</div>
        <p class="footer-text">Phiz &mdash; Instituto Germinare</p>
    </div>

    <script>
        const colors = ['#6366f1', '#8b5cf6', '#22c55e', '#f59e0b', '#ec4899', '#06b6d4'];
        for (let i = 0; i < 40; i++) {{
            const c = document.createElement('div');
            c.className = 'confetti';
            c.style.left = Math.random() * 100 + 'vw';
            c.style.background = colors[Math.floor(Math.random() * colors.length)];
            c.style.animationDelay = (Math.random() * 2) + 's';
            c.style.animationDuration = (2 + Math.random() * 2) + 's';
            c.style.width = (5 + Math.random() * 6) + 'px';
            c.style.height = (5 + Math.random() * 6) + 'px';
            document.body.appendChild(c);
        }}
    </script>
</body>
</html>
"""


def error_page(title: str, message: str) -> str:
    """Retorna a página HTML de erro."""
    return f"""\
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>{title}</title>
    <link rel="preconnect" href="https://fonts.googleapis.com" />
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet" />
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}

        body {{
            font-family: 'Inter', sans-serif;
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
            overflow: hidden;
            position: relative;
        }}

        .orb {{
            position: fixed;
            border-radius: 50%;
            filter: blur(80px);
            opacity: 0.35;
            animation: float 8s ease-in-out infinite;
        }}
        .orb-1 {{ width: 400px; height: 400px; background: #ef4444; top: -100px; left: -100px; }}
        .orb-2 {{ width: 300px; height: 300px; background: #dc2626; bottom: -80px; right: -80px; animation-delay: 2s; }}

        @keyframes float {{
            0%, 100% {{ transform: translateY(0) scale(1); }}
            50% {{ transform: translateY(-30px) scale(1.05); }}
        }}

        .card {{
            position: relative;
            z-index: 1;
            background: rgba(255, 255, 255, 0.06);
            backdrop-filter: blur(24px);
            -webkit-backdrop-filter: blur(24px);
            border: 1px solid rgba(255, 255, 255, 0.12);
            border-radius: 24px;
            padding: 48px 40px;
            max-width: 460px;
            width: 90%;
            text-align: center;
            box-shadow: 0 8px 40px rgba(0, 0, 0, 0.3);
            animation: slideUp 0.6s cubic-bezier(0.16, 1, 0.3, 1) forwards;
            opacity: 0;
            transform: translateY(30px);
        }}

        @keyframes slideUp {{
            to {{ opacity: 1; transform: translateY(0); }}
        }}

        .icon-circle {{
            width: 80px;
            height: 80px;
            margin: 0 auto 24px;
            border-radius: 50%;
            background: linear-gradient(135deg, #ef4444, #dc2626);
            display: flex;
            align-items: center;
            justify-content: center;
            box-shadow: 0 0 30px rgba(239, 68, 68, 0.4);
        }}

        .icon-circle svg {{
            width: 40px;
            height: 40px;
            stroke: #fff;
            stroke-width: 3;
            fill: none;
            stroke-linecap: round;
            stroke-linejoin: round;
        }}

        h1 {{
            color: #f1f5f9;
            font-size: 26px;
            font-weight: 700;
            margin-bottom: 12px;
        }}

        .subtitle {{
            color: #94a3b8;
            font-size: 15px;
            line-height: 1.6;
        }}

        .footer-text {{
            margin-top: 32px;
            font-size: 12px;
            color: #64748b;
        }}
    </style>
</head>
<body>
    <div class="orb orb-1"></div>
    <div class="orb orb-2"></div>

    <div class="card">
        <div class="icon-circle">
            <svg viewBox="0 0 24 24">
                <line x1="18" y1="6" x2="6" y2="18"></line>
                <line x1="6" y1="6" x2="18" y2="18"></line>
            </svg>
        </div>
        <h1>{title}</h1>
        <p class="subtitle">{message}</p>
        <p class="footer-text">Phiz &mdash; Instituto Germinare</p>
    </div>
</body>
</html>
"""
