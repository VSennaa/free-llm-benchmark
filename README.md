<a name="readme-top"></a>

<!-- PROJECT SHIELDS -->
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]

<!-- PROJECT LOGO -->
<br />
<div align="center">
  <h3 align="center">Free LLM Benchmark</h3>

  <p align="center">
    Um benchmark holístico, adaptado da metodologia de Fábio Akita, focado em avaliar a real musculatura neural de LLMs Gratuitos e Previews em cenários de Zero-Shot Coding!
    <br />
    <a href="https://github.com/VSennaa/free-llm-benchmark"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/VSennaa/free-llm-benchmark/issues/new?labels=bug&template=bug-report---.md">Report Bug</a>
    ·
    <a href="https://github.com/VSennaa/free-llm-benchmark/issues/new?labels=enhancement&template=feature-request---.md">Request Feature</a>
  </p>
</div>

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Sumário</summary>
  <ol>
    <li><a href="#tldr">TL;DR (Resumo Rápido)</a></li>
    <li><a href="#sobre-o-projeto">Sobre o Projeto</a></li>
    <li><a href="#metodologia">Metodologia (Akita Adaptada)</a></li>
    <li><a href="#ranking-completo">Ranking Completo (Corrida 2.0)</a></li>
    <li><a href="#análise-por-família-de-modelos">Análise por Família</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
  </ol>
</details>

---

## 🚀 TL;DR

O **Free LLM Benchmark** testou 30 modelos gratuitos e previews (Google, Nvidia, DeepSeek, Liquid, etc.) na criação de uma classe complexa de Thread-Safe LRU Cache com TTL, exigindo precisão total de sintaxe de primeira (Zero-Shot).

**O Pódio:**
1. 🥇 **DeepSeek V4 Flash Free**: Venceu pelo "Reasoning" limpo! O código gerado foi o mais eficiente do campeonato consumindo apenas `0.04 KB` de RAM e compilando perfeitamente de primeira.
2. 🥈 **Laguna XS 2.1 (Free)**: Empate técnico em eficiência com o DeepSeek.
3. 🥉 **Gemma 4 31B (Free)**: O gigante livre do Google obteve a mesmíssima métrica de eficiência.

**A Grande Decepção:**
A família **Google Pro (Gemini 2.5 Pro / 3.1 Pro Prev)** falhou em Zero-Shot, gerando códigos "verbosos" demais, com dependências alucinadas ou lógicas que quebraram na inicialização (`Erro_Execucao`).

**A Parede Invisível do Zero-Shot:**
NENHUM modelo conseguiu passar de `0/10` nos testes pesados de Semântica e *Race Conditions* em concorrência. Conclusão: Sem *agentic loops* ou iteratividade, bater testes rígidos de Thread-Locks ainda é impossível para modelos rápidos no primeiro tiro.

---

## 🎯 Sobre o Projeto

O objetivo deste repositório é testar a pura fundação (Zero-Shot) de diferentes Large Language Models gratuitos e APIs abertas. 
A arquitetura do repositório está dividida em abordagens de benchmark:
* `/logic`: (Atual) Teste rígido onde o modelo cospe código puro em stdout, com ferramentas de OS desabilitadas, sendo testado por um validador local de complexidade em memória e testes unitários.
* `/agentic`: (Em Breve) Teste com liberdade de ferramentas, onde os modelos poderão auto-corrigir o código iterativamente rodando os testes localmente.

---

## 📏 Metodologia

Adotamos e adaptamos a metodologia holística do Fábio Akita para classificar não apenas o "passou no teste", mas a qualidade computacional do código.

A nota (escala de 0 a 100) é composta por:
1. **Corretude Sintática (Até 40 pts):** O código gera erro de importação? Possui bugs que impedem a classe de ser instanciada?
2. **Qualidade Semântica / Testes (Até 40 pts):** Roda de forma thread-safe? Trata edge-cases (TTL negativo, Eviction)? (Cada teste vale 4 pts).
3. **Eficiência (Até 20 pts):** Uso do `tracemalloc` e `time.perf_counter` para medir o pico de alocação de memória (KB) e a latência (ms) na inicialização e run inicial da classe.

**Nota:** Modelos que utilizam _Agentic Tools_ (escrever no disco proativamente ao invés de stdout) foram contidos via System Prompt para manter a justiça do teste Zero-Shot e não inflar o timer computacional.

---

## 🏆 Ranking Completo (Corrida 2.0)

| Posição | Modelo | Nota (0-100) | Testes (0-10) | Memória (KB) | Tempo (ms) | Status |
|---------|--------|--------------|---------------|--------------|------------|--------|
| 1 | **DeepSeek V4 Flash Free** | 48.92 | 0 | 0.04 | 0.01 | Sucesso |
| 2 | **Laguna XS 2.1 (free)** | 48.92 | 0 | 0.04 | 0.01 | Sucesso |
| 3 | **Gemma 4 31B (free)** | 48.92 | 0 | 0.04 | 0.01 | Sucesso |
| 4 | **Gemini Flash Latest** | 48.03 | 0 | 0.04 | 0.02 | Sucesso |
| 5 | **Nemotron 3 Ultra Free** | 46.22 | 0 | 0.05 | 0.04 | Sucesso |
| 6 | **Nemotron 3 Nano 30B A3B (free)** | 22.02 | 0 | 2.93 | 0.15 | Sucesso |
| 7 | **Nemotron 3 Super (free)** | 21.76 | 0 | 2.98 | 0.15 | Sucesso |
| 8 | **Gemini 3.1 Flash Lite Preview** | 21.59 | 0 | 2.84 | 0.16 | Sucesso |
| 9 | **Nemotron 3 Nano Omni (free)** | 21.13 | 0 | 2.93 | 0.16 | Sucesso |
| 10 | **Gemini 3 Flash Preview** | 20.88 | 0 | 2.98 | 0.16 | Sucesso |
| 11 | **North Mini Code (free)** | 20.7 | 0 | 2.84 | 0.17 | Sucesso |
| 12-30 | **(Modelos com Erro de Execução)** | 0 | 0 | 0.00 | 0.00 | Erro_Execucao |

> Para ver a lista dos reprovados (`Erro_Execucao`), cheque a pasta `/logic/docs`. Entre os que falharam estão versões Pro do Google, Liquid LFM e modelos que tentaram alucinar bibliotecas.

---

## 🧠 Análise por Família de Modelos

### 🐉 DeepSeek (DeepSeek V4 Flash)
A arquitetura baseada em "Reasoning" pesou bastante. Inicialmente o modelo tentou quebrar o teste agindo como um Agente que escreve direto no disco. Uma vez contido, o raciocínio gerado em _stdout_ mostrou uma pureza absurda: o modelo gerou uma estrutura que custou míseros **0.04 KB** de memória, sendo o código mais eficiente do benchmark. Excelente fundação, embora a lógica semântica de concorrência ainda esbarre no teto do Zero-Shot.

### 🌐 Google (Gemini, Gemma)
- **Gemma 4 31B / Flash:** Foram os guerreiros resilientes da Google. Tiveram resultados brilhantes e ocuparam posições no Top 4. O Gemma 31B, em específico, mostrou a força de ser um modelo aberto gigante, batendo de frente com o DeepSeek na eficiência de memória (0.04 KB).
- **Série Pro (2.5 Pro / 3.1 Pro Preview):** O calcanhar de Aquiles do Google. Modelos muito instrucionais tentaram ser "espertos demais", supercomplicando a classe, importando `collections`, `threading` avançados que entraram em conflito, e falharam no run inicial. Zero-shot exige assertividade limpa, coisa que os "Flash" fizeram melhor.

### 🟢 Nvidia (Nemotron)
Comportamento extremamente previsível e sólido. Os modelos `Nano` e `Super` caíram certinho no meio da tabela (posições 6 a 9). Eles geram um código estável (compilação passou e memória não foi terrível, na casa dos ~2.9 KB). Fica a sensação de um baseline "Confiável, mas não excepcional" em performance pura.

### 💧 Liquid (LFM)
Modelos como `LFM2.5-1.2B-Instruct` e `LFM2.5-1.2B-Thinking` enfrentaram problemas em zero-shot no Python, possivelmente devido à janela menor e ao dataset focado. Todos eles retornaram erros de execução fatal por não respeitarem a sintaxe base ou ignorarem parâmetros exigidos da classe.

---

## 🛣️ Roadmap

- [x] Setup do script Multithread (Corrida 2.0 com 30 Modelos)
- [x] Contenção de File-Writers para Benchmark Justo (Anti-Agente)
- [x] Ranking Baseado em Memória e Tempo (Metodologia Akita)
- [ ] Implementação do diretório `/agentic` (Iterative Loop Tests)
- [ ] Adição de métricas de tokens processados por segundo.

---

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- MARKDOWN LINKS & IMAGES -->
[contributors-shield]: https://img.shields.io/github/contributors/VSennaa/free-llm-benchmark.svg?style=for-the-badge
[contributors-url]: https://github.com/VSennaa/free-llm-benchmark/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/VSennaa/free-llm-benchmark.svg?style=for-the-badge
[forks-url]: https://github.com/VSennaa/free-llm-benchmark/network/members
[stars-shield]: https://img.shields.io/github/stars/VSennaa/free-llm-benchmark.svg?style=for-the-badge
[stars-url]: https://github.com/VSennaa/free-llm-benchmark/stargazers
[issues-shield]: https://img.shields.io/github/issues/VSennaa/free-llm-benchmark.svg?style=for-the-badge
[issues-url]: https://github.com/VSennaa/free-llm-benchmark/issues
[license-shield]: https://img.shields.io/github/license/VSennaa/free-llm-benchmark.svg?style=for-the-badge
[license-url]: https://github.com/VSennaa/free-llm-benchmark/blob/master/LICENSE.txt
