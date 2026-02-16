import React, { useState } from 'react';
import axios from 'axios';
import { HiSparkles, HiLightningBolt, HiShieldCheck } from 'react-icons/hi';

function App() {
  const [text, setText] = useState('');
  const [status, setStatus] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleAnalyze = async () => {
    if (!text) return;
    setLoading(true);
    try {
      const response = await axios.post('http://localhost:5000/analyze', { text });
      setStatus({ type: 'success', msg: 'Sent to SQS', id: response.data.message_id });
    } catch (e) {
      setStatus({ type: 'error', msg: 'Connection Failed' });
    }
    setLoading(false);
  };

  return (
    <div className="min-h-screen bg-[#020617] text-slate-300 flex items-center justify-center p-4 font-sans relative overflow-hidden">
      {/* Animated Background Glows */}
      <div className="absolute top-[-10%] left-[-10%] w-[40%] h-[40%] bg-blue-600/10 blur-[120px] rounded-full" />
      <div className="absolute bottom-[-10%] right-[-10%] w-[40%] h-[40%] bg-purple-600/10 blur-[120px] rounded-full" />

      <div className="relative z-10 w-full max-w-xl bg-slate-900/40 backdrop-blur-md border border-slate-800 rounded-3xl p-8 shadow-2xl">
        <header className="flex items-center gap-4 mb-8">
          <div className="bg-gradient-to-br from-blue-500 to-cyan-400 p-3 rounded-2xl shadow-lg shadow-blue-500/20">
            <HiSparkles className="text-white text-2xl" />
          </div>
          <div>
            <h1 className="text-2xl font-bold text-white tracking-tight">Sentiment<span className="text-blue-400">Engine</span></h1>
            <p className="text-slate-500 text-xs font-medium uppercase tracking-widest">DevOps Pipeline v1.0</p>
          </div>
        </header>

        <textarea 
          className="w-full h-40 bg-slate-950/50 border border-slate-800 rounded-2xl p-4 text-slate-200 focus:ring-2 focus:ring-blue-500/50 focus:border-blue-500 outline-none transition-all placeholder:text-slate-700 resize-none mb-6"
          placeholder="Enter text to analyze sentiment..."
          value={text}
          onChange={(e) => setText(e.target.value)}
        />

        <button 
          onClick={handleAnalyze}
          disabled={loading || !text}
          className="w-full bg-blue-600 hover:bg-blue-500 disabled:bg-slate-800 text-white font-bold py-4 rounded-2xl transition-all flex items-center justify-center gap-3 shadow-xl shadow-blue-600/10 active:scale-[0.98]"
        >
          {loading ? (
            <div className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin" />
          ) : (
            <><HiLightningBolt /> Analyze Sentiment</>
          )}
        </button>

        {status && (
          <div className={`mt-6 p-4 rounded-2xl border flex items-center gap-4 animate-in fade-in zoom-in-95 duration-300 ${
            status.type === 'success' ? 'bg-emerald-500/5 border-emerald-500/20 text-emerald-400' : 'bg-red-500/5 border-red-500/20 text-red-400'
          }`}>
            <HiShieldCheck className="text-xl shrink-0" />
            <div className="overflow-hidden">
              <p className="text-sm font-bold">{status.msg}</p>
              {status.id && <p className="text-[10px] opacity-50 truncate font-mono">{status.id}</p>}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;