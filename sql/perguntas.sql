-- Optional initial question bank: execute once only if the table is empty.
-- Sources are listed in fontes_perguntas.md.
insert into public.perguntas (enunciado, alternativa_a, alternativa_b, alternativa_c, alternativa_d, correta, dificuldade) values
('Qual é a capital do Brasil?', 'Brasília', 'Rio de Janeiro', 'São Paulo', 'Salvador', 'A', 'facil'),
('Quantos dias tem uma semana?', '5', '6', '7', '8', 'C', 'facil'),
('Qual planeta é conhecido como Planeta Vermelho?', 'Vênus', 'Marte', 'Júpiter', 'Saturno', 'B', 'facil'),
('Qual é o maior oceano da Terra?', 'Atlântico', 'Índico', 'Ártico', 'Pacífico', 'D', 'facil'),
('Qual é o idioma oficial do Brasil?', 'Português', 'Espanhol', 'Inglês', 'Francês', 'A', 'facil'),
('Qual é a unidade básica de medida de comprimento no Sistema Internacional?', 'Metro', 'Litro', 'Quilograma', 'Segundo', 'A', 'media'),
('Em que ano foi proclamada a República no Brasil?', '1822', '1889', '1930', '1964', 'B', 'media'),
('Qual órgão do corpo humano bombeia o sangue?', 'Pulmão', 'Fígado', 'Coração', 'Rim', 'C', 'media'),
('Quem escreveu Dom Casmurro?', 'José de Alencar', 'Machado de Assis', 'Carlos Drummond de Andrade', 'Jorge Amado', 'B', 'media'),
('Qual é o símbolo químico do ouro?', 'Ag', 'Au', 'Fe', 'O', 'B', 'media'),
('Qual camada da atmosfera concentra a maior parte do ozônio?', 'Troposfera', 'Estratosfera', 'Mesosfera', 'Termosfera', 'B', 'dificil'),
('Qual tratado encerrou formalmente a Primeira Guerra Mundial?', 'Tratado de Tordesilhas', 'Tratado de Versalhes', 'Tratado de Madri', 'Tratado de Utrecht', 'B', 'dificil'),
('Em uma solução de pH 3, a concentração de íons H+ é quantas vezes maior que em pH 5?', '2 vezes', '10 vezes', '100 vezes', '1.000 vezes', 'C', 'dificil'),
('Qual é a unidade de medida da resistência elétrica?', 'Volt', 'Ampere', 'Ohm', 'Watt', 'C', 'dificil'),
('Quem formulou as três leis do movimento clássico?', 'Isaac Newton', 'Albert Einstein', 'Galileu Galilei', 'Niels Bohr', 'A', 'dificil');
