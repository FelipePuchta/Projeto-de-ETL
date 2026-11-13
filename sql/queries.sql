-- Escrevi ao todo 10 consultas SQL, em que cada uma irá responder 1 dúvida sobre
-- o arquivo em que estamos trabalhando

-- 01. Quantos atendimentos e quantos pacientes diferentes temos?
SELECT
    COUNT(*) AS total_atendimentos,
    COUNT(DISTINCT id_paciente) AS total_pacientes
FROM atendimentos;

-- 02. Quais especialidades recebem mais atendimentos?
SELECT
    especialidade,
    COUNT(*) AS total_atendimentos
FROM atendimentos
GROUP BY especialidade
ORDER BY total_atendimentos DESC, especialidade;

-- 03. Quantos atendimentos temos em cada classificação de risco?
-- COALESCE mostra um nome para o grupo que está sem classificação.
-- COUNT(*) inclui também os atendimentos com classificação ausente.
SELECT
    COALESCE(classificacao_risco, 'nao informado') AS classificacao_risco,
    COUNT(*) AS total_atendimentos
FROM atendimentos
GROUP BY classificacao_risco
ORDER BY total_atendimentos DESC, classificacao_risco;

-- 04. Quantos atendimentos chegaram em cada mês?
-- STRFTIME extrai o ano e o mês da data de chegada.
SELECT
    STRFTIME('%Y-%m', data_hora_chegada) AS mes,
    COUNT(*) AS total_atendimentos
FROM atendimentos
GROUP BY STRFTIME('%Y-%m', data_hora_chegada)
ORDER BY mes;

-- 05. Quantos atendimentos chegaram em cada dia da semana?
-- No SQLite, o código do dia vai de 0 (domingo) a 6 (sábado).
-- São totais do período, sem ajuste pelo número de ocorrências de cada dia.
SELECT
    CASE STRFTIME('%w', data_hora_chegada)
        WHEN '0' THEN 'domingo'
        WHEN '1' THEN 'segunda-feira'
        WHEN '2' THEN 'terca-feira'
        WHEN '3' THEN 'quarta-feira'
        WHEN '4' THEN 'quinta-feira'
        WHEN '5' THEN 'sexta-feira'
        WHEN '6' THEN 'sabado'
    END AS dia_da_semana,
    COUNT(*) AS total_atendimentos
FROM atendimentos
GROUP BY STRFTIME('%w', data_hora_chegada)
ORDER BY STRFTIME('%w', data_hora_chegada);

-- 06. Em quais horas do dia chegam mais atendimentos?
-- A hora 14, por exemplo, reúne chegadas de 14:00:00 até 14:59:59.
SELECT
    STRFTIME('%H', data_hora_chegada) AS hora,
    COUNT(*) AS total_atendimentos
FROM atendimentos
GROUP BY STRFTIME('%H', data_hora_chegada)
ORDER BY total_atendimentos DESC, hora;

-- 07. Qual é a espera média por classificação de risco?
-- Só entram registros com cronologia válida e espera preenchida.
-- A contagem informa quantos atendimentos participaram de cada média.
SELECT
    COALESCE(classificacao_risco, 'nao informado') AS classificacao_risco,
    COUNT(*) AS atendimentos_analisados,
    ROUND(AVG(tempo_espera_min), 2) AS espera_media_minutos
FROM atendimentos
WHERE cronologia_valida = 1
    AND tempo_espera_min IS NOT NULL
GROUP BY classificacao_risco
ORDER BY espera_media_minutos DESC, classificacao_risco;

-- 08. Qual é a permanência média na unidade para cada desfecho?
-- Permanência é o tempo entre chegada e saída, incluindo a espera.
-- Não representa o tempo total de uma internação após a saída desta unidade.
SELECT
    desfecho,
    COUNT(*) AS atendimentos_analisados,
    ROUND(AVG(tempo_permanencia_min), 2) AS permanencia_media_minutos
FROM atendimentos
WHERE cronologia_valida = 1
    AND tempo_permanencia_min IS NOT NULL
GROUP BY desfecho
ORDER BY permanencia_media_minutos DESC, desfecho;

-- 09. Quantos registros apresentam problemas após o tratamento?
-- Idades inválidas já foram convertidas em NULL pelo Python.
-- As contagens podem incluir o mesmo atendimento; não devem ser somadas.
SELECT
    COUNT(*) AS total_atendimentos,
    SUM(CASE WHEN idade IS NULL THEN 1 ELSE 0 END) AS idades_ausentes,
    SUM(CASE WHEN classificacao_risco IS NULL THEN 1 ELSE 0 END) AS riscos_ausentes,
    SUM(CASE WHEN cronologia_valida = 0 THEN 1 ELSE 0 END) AS cronologias_invalidas
FROM atendimentos;

-- 10. Quais são os 10 pacientes com mais de um atendimento no período?
-- HAVING filtra os grupos depois da contagem.
-- Novas visitas não indicam, por si só, relação clínica entre os atendimentos.
SELECT
    id_paciente,
    COUNT(*) AS total_atendimentos
FROM atendimentos
GROUP BY id_paciente
HAVING COUNT(*) > 1
ORDER BY total_atendimentos DESC, id_paciente
LIMIT 10;
