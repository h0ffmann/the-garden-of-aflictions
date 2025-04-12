# Prompt de Análise de Tom (Português)

## Objetivo
Analisar estilo retórico e tom em textos em português, com atenção às características específicas da língua.

## Análise Específica para Português
1. **Níveis de Formalidade**:
   - Uso de pronomes (você/tu)
   - Conjugações verbais formais/informais
   - Registro linguístico

2. **Variações Regionais**:
   - Diferenças entre PT-BR e PT-PT
   - Regionalismos e expressões locais

3. **Referências Culturais**:
   - Identificar expressões idiomáticas
   - Analisar uso de diminutivos
   - Referências culturais específicas

4. **Dispositivos Retóricos**:
   - Padrões retóricos em português
   - Figuras de linguagem comuns

## Variáveis do Template
- `{text}`: (Obrigatório) Texto para análise
- `{lang}`: (Opcional) Código de língua (pt)
- `{options}`: (Opcional) Opções de análise em JSON

## Exemplo de Uso
```python
from obsidian_analyzer.prompt_loader import load_prompt

prompt = load_prompt("analyze_tone_pt", {
    "text": texto_exemplo,
    "lang": "pt"
})
```

## Estrutura de Saída
```markdown
### Avaliação de Tom
**Tom Dominante**: [Descrição]
**Características Linguísticas**:
- Formalidade: [Nível]
- Características Regionais: [Notas]
- Referências Culturais: [Se presentes]

### Características Principais
- [Característica]: [Exemplo] → [Análise]
- [Observação específica]: [Detalhes]

### Recomendações
- Para Tradução: [Notas sobre preservação de tom]
- Para Análise: [Abordagens para português]
```

**Diretrizes de Análise**:
1. Primeiro identificar a variedade regional (PT-BR/PT-PT)
2. Identificar marcadores de formalidade
3. Notar referências culturais ou expressões idiomáticas
4. Analisar como o tom é criado através de dispositivos linguísticos
