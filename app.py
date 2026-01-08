import streamlit as st
import streamlit.components.v1 as components

# Page configuration
st.set_page_config(page_title="Vaninheaven Card Gen", layout="wide")

# Read the HTML content (Assuming it's in the same directory or pasting directly)
html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Vaninheaven - Advanced Card Generator</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Inter:wght@400;600;800&display=swap');
        body { background-color: #0f172a; color: #f8fafc; font-family: 'Inter', sans-serif; margin: 0; padding: 0; }
        .custom-scrollbar::-webkit-scrollbar { width: 6px; }
        .custom-scrollbar::-webkit-scrollbar-track { background: rgba(255, 255, 255, 0.05); }
        .custom-scrollbar::-webkit-scrollbar-thumb { background: rgba(255, 255, 255, 0.2); border-radius: 10px; }
        .card-row { background: rgba(30, 41, 59, 0.5); border: 1px solid rgba(255, 255, 255, 0.1); transition: all 0.2s ease; }
        .card-row:hover { border-color: #3b82f6; background: rgba(59, 130, 246, 0.1); transform: translateY(-1px); }
        .input-field { background: rgba(0, 0, 0, 0.3); border: 1px solid rgba(255, 255, 255, 0.1); color: #93c5fd; transition: all 0.3s ease; appearance: none; }
        .input-field:focus { border-color: #3b82f6; background: rgba(0, 0, 0, 0.5); box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.2); outline: none; }
        select.input-field option { background-color: #ffffff; color: #000000; font-weight: 600; }
        select.input-field { background-image: url("data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 20 20'%3e%3cpath stroke='%233b82f6' stroke-linecap='round' stroke-linejoin='round' stroke-width='1.5' d='M6 8l4 4 4-4'/%3e%3c/svg%3e"); background-position: right 0.5rem center; background-repeat: no-repeat; background-size: 1.5em 1.5em; padding-right: 2.5rem; }
        .generate-btn { background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%); color: white; transition: all 0.3s ease; }
        .generate-btn:hover { transform: scale(1.02); box-shadow: 0 10px 20px -5px rgba(37, 99, 235, 0.5); }
        .sidebar-card { background: rgba(30, 41, 59, 0.7); border: 1px solid rgba(255, 255, 255, 0.1); box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.3); }
        .brand-logo { text-shadow: 0 0 20px rgba(59, 130, 246, 0.5); }
    </style>
</head>
<body class="p-4 md:p-8">
    <div class="max-w-4xl mx-auto">
        <header class="text-center mb-10">
            <h1 class="text-4xl font-extrabold text-white mb-2 tracking-tight brand-logo">Vanin<span class="text-blue-500">heaven</span></h1>
            <p class="text-slate-400 text-xs font-bold tracking-[0.2em] uppercase">Premium Dark UI • Streamlit Hosted</p>
        </header>
        <div class="grid grid-cols-1 lg:grid-cols-12 gap-8">
            <div class="lg:col-span-4 space-y-6">
                <div class="sidebar-card p-6 rounded-3xl">
                    <h2 class="text-lg font-bold text-white mb-5 flex items-center gap-2">Configuration</h2>
                    <div class="space-y-4">
                        <div>
                            <label class="block text-[11px] font-bold uppercase tracking-wider text-slate-500 mb-1.5 ml-1">BIN / Pattern</label>
                            <input type="text" id="bin" maxlength="16" placeholder="e.g. 412345" oninput="validateInput(this)" class="input-field w-full rounded-xl px-4 py-3 font-mono text-lg tracking-widest font-bold">
                        </div>
                        <div class="grid grid-cols-2 gap-3">
                            <div>
                                <label class="block text-[11px] font-bold uppercase tracking-wider text-slate-500 mb-1.5 ml-1">Month</label>
                                <select id="month" class="input-field w-full rounded-xl px-4 py-3 font-mono font-bold cursor-pointer">
                                    <option value="">Random</option>
                                    <option value="01">01 - Jan</option><option value="02">02 - Feb</option>
                                    <option value="03">03 - Mar</option><option value="04">04 - Apr</option>
                                    <option value="05">05 - May</option><option value="06">06 - Jun</option>
                                    <option value="07">07 - Jul</option><option value="08">08 - Aug</option>
                                    <option value="09">09 - Sep</option><option value="10">10 - Oct</option>
                                    <option value="11">11 - Nov</option><option value="12">12 - Dec</option>
                                </select>
                            </div>
                            <div>
                                <label class="block text-[11px] font-bold uppercase tracking-wider text-slate-500 mb-1.5 ml-1">Year</label>
                                <select id="year" class="input-field w-full rounded-xl px-4 py-3 font-mono font-bold cursor-pointer">
                                    <option value="">Random</option>
                                    <option value="2025">2025</option><option value="2026">2026</option>
                                    <option value="2027">2027</option><option value="2028">2028</option>
                                    <option value="2029">2029</option><option value="2030">2030</option>
                                    <option value="2031">2031</option><option value="2032">2032</option>
                                    <option value="2033">2033</option><option value="2034">2034</option>
                                </select>
                            </div>
                        </div>
                        <div>
                            <label class="block text-[11px] font-bold uppercase tracking-wider text-slate-500 mb-1.5 ml-1">CVV</label>
                            <input type="text" id="cvv" maxlength="4" placeholder="Random" oninput="this.value = this.value.replace(/[^0-9]/g, '')" class="input-field w-full rounded-xl px-4 py-3 font-mono font-bold">
                        </div>
                        <div>
                            <label class="block text-[11px] font-bold uppercase tracking-wider text-slate-500 mb-1.5 ml-1">Quantity</label>
                            <select id="quantity" class="input-field w-full rounded-xl px-4 py-3 font-mono font-bold cursor-pointer">
                                <option value="10">10 Cards</option>
                                <option value="20">20 Cards</option>
                                <option value="50">50 Cards</option>
                                <option value="100">100 Cards</option>
                            </select>
                        </div>
                        <button onclick="generateBulk()" class="generate-btn w-full py-4 rounded-xl font-bold uppercase tracking-widest text-sm mt-2 shadow-lg">Generate Now</button>
                    </div>
                </div>
            </div>
            <div class="lg:col-span-8">
                <div class="bg-slate-900/50 rounded-3xl border border-slate-700 shadow-xl overflow-hidden flex flex-col h-[620px]">
                    <div class="p-6 border-b border-slate-800 flex justify-between items-center bg-slate-900/30">
                        <h2 class="text-lg font-bold text-white flex items-center gap-2">Generated List</h2>
                        <button onclick="copyAll()" id="copy-all-btn" class="text-[10px] text-blue-400 hover:text-white hidden uppercase font-bold tracking-widest border-2 border-blue-400/30 px-4 py-2 rounded-xl">Copy All</button>
                    </div>
                    <div id="results-list" class="flex-1 overflow-y-auto p-5 custom-scrollbar space-y-3">
                        <div id="placeholder" class="h-full flex flex-col items-center justify-center text-slate-600 opacity-50">Ready to generate cards...</div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    <div id="toast" class="fixed bottom-10 left-1/2 -translate-x-1/2 bg-blue-600 text-white px-8 py-3.5 rounded-2xl font-bold opacity-0 transition-all z-50 text-sm">Successfully Copied</div>
    <script>
        function validateInput(input) {
            const myanmarNumbers = {'၀':'0','၁':'1','၂':'2','၃':'3','၄':'4','၅':'5','၆':'6','၇':'7','၈':'8','၉':'9'};
            let value = input.value;
            for (let myan in myanmarNumbers) { value = value.split(myan).join(myanmarNumbers[myan]); }
            input.value = value.replace(/[^0-9xX]/g, '');
        }
        function generateBulk() {
            const binInput = document.getElementById('bin').value.trim();
            const qty = parseInt(document.getElementById('quantity').value) || 10;
            const resultsList = document.getElementById('results-list');
            if (!binInput) { alert("Please enter a BIN!"); return; }
            document.getElementById('placeholder').classList.add('hidden');
            document.getElementById('copy-all-btn').classList.remove('hidden');
            resultsList.innerHTML = '';
            for (let i = 0; i < qty; i++) {
                const card = generateCard(binInput);
                const row = document.createElement('div');
                row.className = 'card-row flex items-center justify-between p-4 rounded-2xl';
                row.innerHTML = `<div class="card-text font-mono text-sm text-slate-300 font-bold">${card.full}</div>
                <button onclick="copyText('${card.full}')" class="p-2 hover:bg-slate-700 rounded-xl">Copy</button>`;
                resultsList.appendChild(row);
            }
        }
        function generateCard(bin) {
            let num = bin.replace(/x/gi, () => Math.floor(Math.random()*10));
            while(num.length < 16) num += Math.floor(Math.random()*10);
            let m = document.getElementById('month').value || '12';
            let y = document.getElementById('year').value || '2028';
            let c = document.getElementById('cvv').value || '123';
            return { full: `${num}|${m}|${y}|${c}` };
        }
        function copyText(text) {
            navigator.clipboard.writeText(text);
            const toast = document.getElementById('toast');
            toast.style.opacity = '1';
            setTimeout(() => toast.style.opacity = '0', 2000);
        }
        function copyAll() {
            const cards = Array.from(document.querySelectorAll('.card-text')).map(el => el.innerText).join('\\n');
            copyText(cards);
        }
    </script>
</body>
</html>
"""

# Render HTML in Streamlit
components.html(html_content, height=800, scrolling=True)
