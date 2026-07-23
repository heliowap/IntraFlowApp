# Intra Flow — Install (beta)

## Antes de começar

Este build é assinado com **Apple Development** (conta gratuita), **não** com Developer ID + notarização.

- Em muitos Macs o caminho abaixo basta (Gatekeeper → Abrir mesmo assim).
- Em outros, um build Development **não abre** se a máquina não estiver no perfil de provisionamento — aí não é só o aviso do Gatekeeper. Nesse caso o caminho certo é um build **notarizado** (conta Apple Developer paga), não `xattr` no Terminal.

Não use comando de Terminal para “forçar” a abertura num convite a criadores: se precisar disso, adie o contato até ter Developer ID + notarização.

## 1. Instalar

1. Baixe `IntraFlow-*.dmg` em [Releases](https://github.com/heliowap/IntraFlowApp/releases/latest).
2. Abra o DMG.
3. Arraste **IntraFlow.app** para **Applications**.

## 2. Primeira abertura (macOS Sequoia / 15+)

O beta **não é notarizado**. Na primeira abertura o macOS pode bloquear.

Caminho atual (Sequoia):

1. Tente abrir IntraFlow.app (duplo-clique) — o sistema pode recusar.
2. Abra **Ajustes do Sistema → Privacidade e Segurança**.
3. Role até a mensagem sobre IntraFlow ter sido bloqueado.
4. Clique em **Abrir mesmo assim** (pode pedir senha / Touch ID).
5. Confirme **Abrir** se o diálogo aparecer de novo.

Em versões mais antigas do macOS, às vezes ainda funciona **botão direito → Abrir** no Finder; no Sequoia o caminho confiável é **Privacidade e Segurança**.

## 3. Permissões

**Ajustes do Sistema → Privacidade e Segurança**

| Permissão | Para quê |
| --- | --- |
| **Acessibilidade** | Trigger global + inserir texto no cursor |
| **Microfone** | Capturar a voz |

Ligue Intra Flow em Acessibilidade. Aceite o microfone quando pedir.

## 4. Chave OpenAI (BYOK)

Na primeira execução, cole sua chave da API OpenAI.

- Org com **Realtime** + **Chat** habilitados.
- Guardada só na **Chaveira** do Mac.

## 5. Usar

1. Foque um campo de texto.
2. Segure **Option esquerda** (Trigger padrão) e fale.
3. Solte para injetar o texto polido no cursor.

Ícone de onda na barra de menus → Preferências, Histórico, Impacto, Mode, Trigger.

---

Feedback: [Issues](https://github.com/heliowap/IntraFlowApp/issues)
