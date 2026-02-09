import React, { useState } from 'react';
import axios from 'axios';

function App() {
  const [text, setText] = useState('');
  const [status, setStatus] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleAnalyze = async () => {
    setLoading(true);
    try {
      const response = await axios.post('http://localhost:5000/analyze', { text });
      setStatus({ type: 'success', message: `Queued! ID: ${response.data.message_id}` });
    } catch (error) {
      setStatus({ type: 'error', message: 'Failed to connect to Backend.' });
    }
    setLoading(false);
  };

  return (
    <div className="min-h-screen bg-gray-900 text-white flex flex-col items-center justify-center p-4">
      <div className="max-w-2xl w-full bg-gray-800 rounded-xl shadow-2xl p-8 border border-gray-700">
        <h1 className="text-4xl font-bold mb-2 text-blue-400">Sentiment AI</h1>
        <p className="text-gray-400 mb-8">Real-time NLP analysis via AWS SQS & Kubernetes.</p>
        
        <textarea 
          className="w-full h-40 p-4 bg-gray-900 border border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:outline-none text-lg"
          placeholder="Type how you feel today..."
          value={text}
          onChange={(e) => setText(e.target.value)}
        />

        <button 
          onClick={handleAnalyze}
          disabled={loading}
          className="mt-6 w-full bg-blue-600 hover:bg-blue-500 transition-colors py-3 rounded-lg font-semibold text-xl disabled:opacity-50"
        >
          {loading ? 'Sending to Queue...' : 'Analyze Sentiment'}
        </button>

        {status && (
          <div className={`mt-6 p-4 rounded-lg border ${status.type === 'success' ? 'bg-green-900/30 border-green-500 text-green-400' : 'bg-red-900/30 border-red-500 text-red-400'}`}>
            {status.message}
          </div>
        )}
      </div>
      <footer className="mt-8 text-gray-500 text-sm">DevOps PFE Platform • 2026</footer>
    </div>
  );
}

export default App;