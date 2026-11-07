index.html
.

9101112131415161718192021222324252627282912345678
 <!DOCTYPE html>
<html lang="gu">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
body{font-family:Arial,sans-serif;background:#f4f6f8;margin:0;color:#202733}
header{background:#176b45;color:white;padding:18px;text-align:center}
main{max-width:1000px;margin:18px ato;padding:o 12px}
nav{display:flex;gap:8px;flex-wrap:wrap;margin-bottom:14px}

Deploy this project
button{background:#176b45;color:white;border:0;border-radius:7px;padding:10px 14px;cursor:pointer}
button.secondary{background:#526170}
.panel{background:white;padding:16px;border-radius:10px;margin-bottom:14px;box-shadow:0 1px 5px #0001}
input,select{padding:10px;border:1px solid #ccd3da;border-radius:6px;max-width:100%;box-sizing:border-box}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:10px}
table{width:100%;border-collapse:collapse;margin-top:10px}
th,td{border:1px solid #dce1e6;padding:8px;text-align:left}
th{background:#edf2ef}
.small{font-size:13px;color:#58636e}
.hidden{display:none}
.actions{display:flex;gap:8px;flex-wrap:wrap;margin-top:12px}
.status{padding:10px;border-radius:7px;background:#eef7f0;margin-top:10px}
</style>
</head>
<body>
<header><h2>શ્રી વિશ્વરથ એગ્રો સેન્ટર</h2><div>બિલ બુક અને હિસાબી સિસ્ટમ</div></header>
<main>
<nav>
<button onclick="show('bill')">નવું બિલ</button>
<button class="secondary" onclick="show('old')">જૂનાં બિલ</button>
<button class="secondary" onclick="show('ledger')">ખેડૂતનું ખાતું</button>
<button class="secondary" onclick="show('stock')">સ્ટોક</button>
</nav>
<section id="bill" class="panel">
<h3>નવું બિલ</h3>
<div class="grid">
<label>તારીખ<br><input id="date" type="date"></label>
<label>ખેડૂતનું નામ *<br><input id="farmer" placeholder="ખેડૂતનું નામ"></label>
<label>મોબાઇલ<br><input id="mobile" placeholder="મોબાઇલ નંબર"></label>
<label>જમા રકમ<br><input id="paid" type="number" min="0" value="0"></label>
</div>
<h4>વસ્તુઓ (વધુમાં વધુ 15)</h4>
<table><thead><tr><th>નં.</th><th>વસ્તુનું નામ</th><th>જથ્થો</th><th>ભાવ</th><th>રકમ</th></tr></thead><tbody id="items"></tbody></table>
<div class="actions"><button onclick="addRow()">વસ્તુ ઉમેરો</button><button onclick="save()">બિલ સાચવો</button><button class="secondary" onclick="window.print()">પ્રિન્ટ</button></div>
<p id="total">કુલ: ₹0</p><div id="billStatus" class="status hidden"></div>
</section>
<section id="old" class="panel hidden"><h3>જૂનાં બિલ</h3><button onclick="loadBills()">બિલ જુઓ</button><div id="bills"></div></section>
<section id="ledger" class="panel hidden"><h3>ખેડૂત પ્રમાણે ખાતું</h3><div class="actions"><select id="farmerList"></select><button onclick="loadLedger()">ખાતું જુઓ</button></div><div id="ledgerData"></div></section>
<section id="stock" class="panel hidden"><h3>સ્ટોક પત્રક</h3><div class="grid"><label>વસ્તુનું નામ<br><input id="stockItem"></label><label>જથ્થો ઉમેરો<br><input id="stockQty" type="number" min="0"></label><label>ભાવ<br><input id="stockRate" type="number" min="0"></label></div><div class="actions"><button onclick="addStock()">સ્ટોક ઉમેરો</button><button class="secondary" onclick="loadStock()">સ્ટોક જુઓ</button></div><div id="stockData"></div></section>
<p class="small">તમારો ડેટા Google Sheets માં સાચવાશે. પ્રથમ વખત મંજૂરી માંગવામાં આવી શકે છે.</p>
<div class="actions"><button class="secondary" onclick="openSheet()">હિસાબની Google Sheet ખોલો</button></div>
</main>
<script>
let count=0;
function show(id){['bill','old','ledger','stock'].forEach(x=>document.getElementById(x).classList.toggle('hidden',x!==id));if(id==='ledger')loadFarmers();if(id==='stock')loadStock();}
function addRow(){if(count>=15){alert('એક બિલમાં વધુમાં વધુ 15 વસ્તુ જ ઉમેરી શકો.');return;}count++;const tr=document.createElement('tr');tr.innerHTML=<td>${count}</td><td><input class="nm" placeholder="વસ્તુનું નામ"></td><td><input class="qty" type="number" min="0" step="any" value="1" oninput="calc()"></td><td><input class="rate" type="number" min="0" step="any" value="0" oninput="calc()"></td><td class="amt">0</td>;document.getElementById('items').appendChild(tr);}
function calc(){let total=0;document.querySelectorAll('#items tr').forEach(r=>{let q=Number(r.querySelector('.qty').value||0),p=Number(r.querySelector('.rate').value||0),a=q*p; r.querySelector('.amt').textContent=a.toFixed(2);total+=a;});document.getElementById('total').textContent='કુલ: ₹'+total.toFixed(2);}
function save(){const items=[...document.querySelectorAll('#items tr')].map(r=>({name:r.querySelector('.nm').value.trim(),qty:r.querySelector('.qty').value,rate:r.querySelector('.rate').value}));const data={date:document.getElementById('date').value,farmer:document.getElementById('farmer').value.trim(),mobile:document.getElementById('mobile').value.trim(),paid:document.getElementById('paid').value,items};google.script.run.withSuccessHandler(r=>{let e=document.getElementById('billStatus');e.classList.remove('hidden');e.textContent=${r.message} બિલ નંબર: ${r.billNo} | કુલ: ₹${r.total.toFixed(2)} | બાકી: ₹${r.balance.toFixed(2)};}).withFailureHandler(e=>alert(e.message)).saveBill(data);}
function table(headers,rows){return '<table><thead><tr>'+headers.map(x=>'<th>'+x+'</th>').join('')+'</tr></thead><tbody>'+rows.map(r=>'<tr>'+r.map(x=>'<td>'+x+'</td>').join('')+'</tr>').join('')+'</tbody></table>';}
function loadBills(){google.script.run.withSuccessHandler(a=>{document.getElementById('bills').innerHTML=a.length?table(['બિલ નંબર','તારીખ','ખેડૂત','કુલ','જમા','બાકી'],a.map(b=>[b.billNo,b.date,b.farmer,'₹'+b.total,'₹'+b.paid,'₹'+(b.total-b.paid)])):'હજુ કોઈ બિલ નથી.';}).getBills();}
function loadFarmers(){google.script.run.withSuccessHandler(a=>{document.getElementById('farmerList').innerHTML=a.map(x=><option>${x}</option>).join('');}).getFarmers();}
function loadLedger(){let f=document.getElementById('farmerList').value;google.script.run.withSuccessHandler(a=>{document.getElementById('ledgerData').innerHTML=a.length?table(['બિલ નંબર','તારીખ','કુલ','જમા','બાકી'],a.map(x=>[x.billNo,x.date,'₹'+x.total,'₹'+x.paid,'₹'+x.balance])):'આ ખેડૂતનું બિલ મળ્યું નથી.';}).getLedger(f);}
function loadStock(){google.script.run.withSuccessHandler(a=>{document.getElementById('stockData').innerHTML=a.length?table(['વસ્તુ','શરૂઆત','ખરીદી','વેચાણ','બાકી','ભાવ'],a.map(x=>[x.item,x.opening,x.purchased,x.sold,x.balance,'₹'+x.rate])):'સ્ટોક ખાલી છે.';}).getStock();}
function addStock(){google.script.run.withSuccessHandler(r=>{alert(r.message);loadStock();}).withFailureHandler(e=>alert(e.message)).addStock({item:document.getElementById('stockItem').value.trim(),qty:document.getElementById('stockQty').value,rate:document.getElementById('stockRate').value});}
function openSheet(){google.script.run.withSuccessHandler(u=>window.open(u,'_blank')).getSpreadsheetUrl();}
document.getElementById('date').value=new Date().toISOString().slice(0,10);
addRow();
</script>
</body></html>
const SHEET_NAME = 'Shri Vishvarath Agro Center';
const PROP_KEY = 'AGRO_SPREADSHEET_ID';

function doGet() {
  setup_();
  return HtmlService.createHtmlOutputFromFile('index')
    .setTitle('શ્રી વિશ્વરથ એગ્રો સેન્ટર')
    .setXFrameOptionsMode(HtmlService.XFrameOptionsMode.ALLOWALL);
}

function setup_() {
  const props = PropertiesService.getScriptProperties();
  let id = props.getProperty(PROP_KEY);
  let ss;
  if (id) {
    try { ss = SpreadsheetApp.openById(id); } catch (e) { ss = null; }
  }
  if (!ss) {
    ss = SpreadsheetApp.create(SHEET_NAME + ' - હિસાબ');
    props.setProperty(PROP_KEY, ss.getId());
  }
  ensureSheet_(ss, 'Bills', ['Bill No','Date','Farmer','Mobile','Item','Qty','Rate','Amount','Paid','Note']);
  ensureSheet_(ss, 'Stock', ['Item','Opening Stock','Purchased','Sold','Balance','Rate']);
  ensureSheet_(ss, 'Farmers', ['Farmer','Mobile','Address']);
  return ss;
}

function ensureSheet_(ss, name, headers) {
  let sh = ss.getSheetByName(name);
  if (!sh) sh = ss.insertSheet(name);
  if (sh.getLastRow() === 0) {
    sh.getRange(1,1,1,headers.length).setValues([headers]);
    sh.setFrozenRows(1);
  }
  return sh;
}

function saveBill(data) {
  if (!data || !data.farmer || !data.date) throw new Error('ખેડૂતનું નામ અને તારીખ જરૂરી છે.');
  const items = (data.items || []).filter(x => x.name && Number(x.qty) > 0);
  if (!items.length) throw new Error('ઓછામાં ઓછી એક વસ્તુ ઉમેરો.');
  const ss = setup_();
  const sh = ss.getSheetByName('Bills');
  const billNo = 'B' + Utilities.formatDate(new Date(), Session.getScriptTimeZone(), 'yyMMdd-HHmmss');
  const paid = Number(data.paid || 0);
  const total = items.reduce((s,x) => s + Number(x.qty) * Number(x.rate), 0);
  const rows = items.map(x => [billNo, data.date, data.farmer, data.mobile || '', x.name, Number(x.qty), Number(x.rate), Number(x.qty)*Number(x.rate), paid, data.note || '']);
  sh.getRange(sh.getLastRow()+1,1,rows.length,10).setValues(rows);
  items.forEach(x => updateStock_(ss, x.name, Number(x.qty), Number(x.rate)));
  return {billNo, total, balance: total-paid, message:'બિલ સાચવાઈ ગયું.'};
}

function updateStock_(ss, item, sold, rate) {
  const sh = ss.getSheetByName('Stock');
  const values = sh.getDataRange().getValues();
  let row = values.findIndex((r,i) => i > 0 && String(r[0]).trim().toLowerCase() === item.trim().toLowerCase());
  if (row < 0) {
    sh.appendRow([item,0,0,sold,-sold,rate]);
  } else {
    const r = row + 1;
    const opening = Number(sh.getRange(r,2).getValue() || 0);
    const purchased = Number(sh.getRange(r,3).getValue() || 0);
    const oldSold = Number(sh.getRange(r,4).getValue() || 0);
    sh.getRange(r,4).setValue(oldSold + sold);
    sh.getRange(r,5).setValue(opening + purchased - oldSold - sold);
    if (rate) sh.getRange(r,6).setValue(rate);
  }
}

function getBills() {
  const sh = setup_().getSheetByName('Bills');
  const v = sh.getDataRange().getValues();
  if (v.length < 2) return [];
  const map = {};
  v.slice(1).forEach(r => {
    const id = String(r[0]);
    if (!map[id]) map[id] = {billNo:id,date:r[1],farmer:r[2],mobile:r[3],items:[],paid:Number(r[8]||0),note:r[9],total:0};
    map[id].items.push({name:r[4],qty:Number(r[5]),rate:Number(r[6]),amount:Number(r[7])});
    map[id].total += Number(r[7]||0);
  });
  return Object.values(map).reverse();
}

function getLedger(farmer) {
  const bills = getBills().filter(b => b.farmer === farmer);
  return bills.map(b => ({billNo:b.billNo,date:b.date,total:b.total,paid:b.paid,balance:b.total-b.paid}));
}

function getFarmers() {
  const v = setup_().getSheetByName('Bills').getDataRange().getValues();
  return [...new Set(v.slice(1).map(r => String(r[2]).trim()).filter(Boolean))].sort();
}

function getStock() {
  const sh = setup_().getSheetByName('Stock');
  return sh.getDataRange().getValues().slice(1).filter(r => r[0]).map(r => ({
    item:r[0], opening:Number(r[1]||0), purchased:Number(r[2]||0),
    sold:Number(r[3]||0), balance:Number(r[4]||0), rate:Number(r[5]||0)
  }));
}

function addStock(data) {
  if (!data || !data.item) throw new Error('વસ્તુનું નામ લખો.');
  const ss = setup_(), sh = ss.getSheetByName('Stock');
  const v = sh.getDataRange().getValues();
  const idx = v.findIndex((r,i) => i>0 && String(r[0]).trim().toLowerCase() === data.item.trim().toLowerCase());
  if (idx < 0) sh.appendRow([data.item,Number(data.qty||0),0,0,Number(data.qty||0),Number(data.rate||0)]);
  else {
    const row = idx+1, opening=Number(sh.getRange(row,2).getValue()||0);
    const purchased=Number(sh.getRange(row,3).getValue()||0)+Number(data.qty||0);
    const sold=Number(sh.getRange(row,4).getValue()||0);
    sh.getRange(row,3).setValue(purchased);
    sh.getRange(row,5).setValue(opening+purchased-sold);
    sh.getRange(row,6).setValue(Number(data.rate||sh.getRange(row,6).getValue()||0));
  }
  return {message:'સ્ટોક અપડેટ થયો.'};
}

function getSpreadsheetUrl() {
  return setup_().getUrl();
}
function doGet() {
  return HtmlService.createHtmlOutput(`
    <!DOCTYPE html>
    <html>
      <head>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
          body {
            font-family: Arial, sans-serif;
            padding: 20px;
            background: #f3f6f4;
          }
          h2 { color: #176b3a; }
          .card {
            background: white;
            padding: 18px;
            border-radius: 12px;
            margin-bottom: 15px;
          }
        </style>
      </head>
      <body>
        <div class="card">
          <h2>શ્રી વિશ્વરથ એગ્રો સેન્ટર</h2>
          <p>ખેડૂત બિલ બુક અને હિસાબી સિસ્ટમ</p>
        </div>
        <div class="card">
          <h3>સિસ્ટમ તૈયાર કરવાની શરૂઆત થઈ ગઈ છે.</h3>
          <p>આગળ બિલ બુક, સ્ટોક અને ખેડૂતવાઇઝ લેજર જોડવામાં આવશે.</p>
        </div>
      </body>
    </html>
  `).setTitle('શ્રી વિશ્વરથ એગ્રો સેન્ટર');
}

function setupSheets() {
  const ss = SpreadsheetApp.openById(
      '1HXTj0ifyJPf-gb0xxG_Qn-LZ7Nkyy0YqSDtc2RS_whk'
        );

          const sheets = {
              Bills: [
                    'Bill No', 'Date', 'Farmer Name',
                          'Total', 'Paid', 'Balance'
                              ],
                                  BillItems: [
                                        'Bill No', 'Item Name', 'Quantity',
                                              'Rate', 'Amount'
                                                  ],
                                                      Farmers: [
                                                            'Farmer ID', 'Farmer Name',
                                                                  'Mobile', 'Address', 'Opening Balance'
                                                                      ],
                                                                          Stock: [
                                                                                'Item Name', 'Opening Stock',
                                                                                      'Purchase', 'Sold', 'Closing Stock'
                                                                                          ],
                                                                                              Ledger: [
                                                                                                    'Date', 'Farmer Name', 'Details',
                                                                                                          'Jama', 'Udhar', 'Balance'
                                                                                                              ]
                                                                                                                };

                                                                                                                  Object.entries(sheets).forEach(([name, headers]) => {
                                                                                                                      let sh = ss.getSheetByName(name);

                                                                                                                          if (!sh) {
                                                                                                                                sh = ss.insertSheet(name);
                                                                                                                                    }

                                                                                                                                        if (sh.getLastRow() === 0) {
                                                                                                                                              sh.getRange(1, 1, 1, headers.length)
                                                                                                                                                      .setValues([headers]);
                                                                                                                                                            sh.setFrozenRows(1);
                                                                                                                                                                }
                                                                                                                                                                  });

                                                                                                                                                                    SpreadsheetApp.getUi();
                                                                                                                                                                    }
