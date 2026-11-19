"""Simula o estado de um fluxo CAPTCHA sem abrir navegador ou acessar o Lattes."""

import json
import sys
import time


STEPS = (
    ("preparando", "Lote autorizado carregado", "aprovado"),
    ("navegando", "Abrindo o curriculo autorizado", "em_execucao"),
    ("desafio_detectado", "CAPTCHA ou MFA encontrado", "aguardando_usuario"),
    ("takeover_humano", "Usuario resolve na live preview", "aguardando_confirmacao"),
    ("confirmado", "Sessao e dominio confirmados", "em_execucao"),
    ("continuando", "Retomando somente o lote autorizado", "concluido"),
)


def main() -> int:
    events = []
    for estado, descricao, status in STEPS:
        event = {
            "estado": estado,
            "descricao": descricao,
            "status": status,
            "navegador_aberto": False,
            "dados_reais_enviados": False,
        }
        events.append(event)
        print(json.dumps(event, ensure_ascii=False))
        if estado in {"desafio_detectado", "takeover_humano"}:
            print(json.dumps({
                "acao": "Pausar",
                "motivo": "Nao tentar resolver, inferir ou contornar o desafio",
            }, ensure_ascii=False))
        time.sleep(0.05)
    print(json.dumps({"resultado": "simulacao_segura", "eventos": len(events)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
