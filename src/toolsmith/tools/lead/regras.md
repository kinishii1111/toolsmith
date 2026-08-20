# Regras ICP — lead

Critérios para `score_lead` / `tag_lead` (heurística local, sem LLM/CRM).

- **Orçamento**: menciona valor explícito (ex: "orçamento até 20k", "20k", "R$ 20000") → +30; sem orçamento → 0.
- **Urgência**: "essa semana", "urgente", "imediato", "proposta", "preciso agora" → +25.
- **Segmento**: "empresa", "funcionários", "funcionarios", "equipe de", "CNPJ", "B2B" → B2B (+25); caso contrário B2C.
- **Tamanho**: "50 funcionários" ou ">20 funcionários" → forte sinal B2B.
- **Score**: base 20 + bônus (máx 100).
- **Tag temperatura**: quente ≥70, morno 40–69, frio <40.
- **Tag segmento**: b2b|b2c (pode retornar ambos se ambíguo, mas prioriza b2b quando há "empresa").
