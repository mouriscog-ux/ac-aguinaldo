/* Read-only client: config.js contains only the public anonymous key. */
const status = document.querySelector('#status'), tbody = document.querySelector('#ranking');
const gameFilter = document.querySelector('#gameFilter'), refreshButton = document.querySelector('#refresh');
const formatMoney = n => new Intl.NumberFormat('pt-BR',{style:'currency',currency:'BRL',maximumFractionDigits:0}).format(n);
function client() {
  const c = window.SUPABASE_CONFIG;
  if (!c || !c.url || !c.anonKey || c.anonKey.includes('COLE_')) throw new Error('Credenciais públicas não configuradas. Crie site/config.js a partir de config.js.example e informe a chave anon/publicável.');
  if (!window.supabase) throw new Error('Não foi possível carregar a biblioteca do Supabase. Verifique a conexão com a internet.');
  return window.supabase.createClient(c.url, c.anonKey);
}
function setLoading(loading) { refreshButton.disabled = loading; refreshButton.textContent = loading ? 'Atualizando…' : '↻ Atualizar ranking'; }
function describeError(error) {
  if (error?.code === '42501') return 'Sem permissão para consultar o ranking. Verifique a view e as políticas RLS.';
  if (error?.message?.includes('fetch')) return 'Não foi possível conectar ao Supabase. Verifique sua internet e a URL do projeto.';
  return `Falha ao consultar o ranking: ${error?.message || 'erro desconhecido'}`;
}
async function loadGames(){
  const {data: games, error} = await client().from('jogos').select('id,nome').order('nome');
  if (error) throw error;
  gameFilter.replaceChildren(new Option('Todos os jogos', ''));
  games.forEach(g => gameFilter.add(new Option(g.nome, g.id)));
}
async function loadRanking(){
  setLoading(true); status.textContent='Carregando ranking…';tbody.innerHTML='';document.querySelector('#champion').hidden=true;document.querySelector('#empty').hidden=true;
  try {
    let request = client().from('ranking_publico').select('partida_id,jogo_id,apelido,valor_ganho,tempo_segundos,data_hora,posicao').order('valor_ganho',{ascending:false}).order('tempo_segundos').order('data_hora').order('partida_id');
    if (gameFilter.value) request = request.eq('jogo_id', gameFilter.value);
    const {data: rows, error} = await request;
    if (error) throw error;
    status.textContent='Ranking atualizado.';document.querySelector('#empty').hidden=rows.length>0;
    if(rows[0]){const c=document.querySelector('#champion');c.hidden=false;c.innerHTML=`🏆 <strong>1º ${escapeHtml(rows[0].apelido)}</strong><br>${formatMoney(rows[0].valor_ganho)} em ${Number(rows[0].tempo_segundos).toFixed(2)}s`;}
    rows.forEach(r=>{const tr=document.createElement('tr');tr.innerHTML=`<td>${r.posicao}º</td><td>${escapeHtml(r.apelido)}</td><td>${formatMoney(r.valor_ganho)}</td><td>${Number(r.tempo_segundos).toFixed(2)} s</td><td>${new Date(r.data_hora).toLocaleString('pt-BR')}</td>`;tbody.append(tr)});
  } catch(e) { status.textContent='Erro: '+describeError(e); } finally { setLoading(false); }
}
function escapeHtml(v){const d=document.createElement('div');d.textContent=v;return d.innerHTML}
document.querySelector('#refresh').onclick=loadRanking;document.querySelector('#gameFilter').onchange=loadRanking;
(async()=>{try{await loadGames()}catch(e){status.textContent='Erro: '+e.message}await loadRanking()})();
