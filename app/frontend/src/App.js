import React, { useState } from 'react'; // Removed useEffect
import axios from 'axios';
import { HiSparkles, HiLightningBolt, HiCheckCircle, HiExclamationCircle } from 'react-icons/hi';

function App() {
  const [text, setText] = useState('');
  const [loading, setLoading] = useState(false);
  const [messageId, setMessageId] = useState(null); // Now used in the UI below
  const [analysis, setAnalysis] = useState(null);

  const pollForResult = (id) => {
    const interval = setInterval(async () => {
      try {
        const response = await axios.get(`http://localhost:5000/results/${id}`);
        if (response.status === 200) {
          setAnalysis(response.data);
          clearInterval(interval);
          setLoading(false);
        }
      } catch (error) {
        // 404 or 202 is expected while the worker is still processing
        console.log("Waiting for worker to update DynamoDB...");
      }
    }, 2000);
  };

  const handleAnalyze = async () => {
    if (!text.trim()) return;
    setLoading(true);
    setAnalysis(null);
    setMessageId(null);

    try {
      const res = await axios.post('http://localhost:5000/analyze', { text });
      const id = res.data.message_id;
      setMessageId(id); // Set the ID to show the user
      pollForResult(id);
    } catch (e) {
      setLoading(false);
      alert("Backend connection failed!");
    }
  };

  return (
    <div className="min-h-screen bg-[#020617] text-slate-300 flex items-center justify-center p-4">
      <div className="w-full max-w-xl bg-slate-900/50 border border-slate-800 rounded-3xl p-8 shadow-2xl">
        
        {/* Header */}
        <div className="flex justify-between items-center mb-6">
          <h1 className="text-2xl font-bold text-white flex items-center gap-2">
            <HiSparkles className="text-blue-400" /> SentimentEngine
          </h1>
          {messageId && (
            <span className="text-[10px] bg-slate-800 px-2 py-1 rounded text-slate-500 font-mono">
              ID: {messageId.substring(0, 8)}...
            </span>
          )}
        </div>

        {/* Input */}
        <textarea 
          className="w-full h-32 bg-slate-950 border border-slate-800 rounded-xl p-4 mb-4 focus:ring-2 focus:ring-blue-500 outline-none transition-all text-white"
          value={text}
          onChange={(e) => setText(e.target.value)}
          placeholder="Enter text to analyze sentiment..."
        />

        {/* Action Button */}
        <button 
          onClick={handleAnalyze}
          disabled={loading}
          className={`w-full py-4 rounded-xl font-bold flex items-center justify-center gap-2 transition-all ${
            loading 
              ? 'bg-slate-800 cursor-not-allowed text-slate-500' 
              : 'bg-blue-600 hover:bg-blue-500 text-white shadow-lg shadow-blue-500/20'
          }`}
        >
          {loading ? (
            <span className="flex items-center gap-2 animate-pulse">
              <div className="w-4 h-4 border-2 border-t-transparent border-white rounded-full animate-spin"></div>
              Processing...
            </span>
          ) : (
            <><HiLightningBolt /> Analyze Sentiment</>
          )}
        </button>

        {/* Result Card */}
        {analysis && (
          <div className={`mt-8 p-6 rounded-2xl border-2 animate-in fade-in zoom-in duration-500 ${
            analysis.sentiment === 'POSITIVE' 
              ? 'bg-emerald-500/10 border-emerald-500/50 text-emerald-400 shadow-lg shadow-emerald-500/10' 
              : 'bg-rose-500/10 border-rose-500/50 text-rose-400 shadow-lg shadow-rose-500/10'
          }`}>
            <div className="flex items-center justify-between mb-2">
              <span className="text-xs font-black tracking-widest uppercase opacity-70">Analysis Complete</span>
              {analysis.sentiment === 'POSITIVE' ? <HiCheckCircle size={24}/> : <HiExclamationCircle size={24}/>}
            </div>
            <div className="text-3xl font-black mb-1 tracking-tight">{analysis.sentiment}</div>
            <p className="text-sm opacity-80 italic">"{analysis.text}"</p>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;