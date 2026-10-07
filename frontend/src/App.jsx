import { useState } from 'react';
import { 
  ShieldCheck, 
  ShieldAlert, 
  Shield, 
  AlertCircle,
  Loader2,
  Trash2,
  Send,
  Mail,
  Zap,
  CheckCircle2
} from 'lucide-react';
import { analyzeEmail } from './services/api';

function App() {
  const [subject, setSubject] = useState('');
  const [body, setBody] = useState('');
  const [status, setStatus] = useState('idle'); // idle, loading, success, error
  const [result, setResult] = useState(null);
  const [errorMsg, setErrorMsg] = useState('');

  const handleAnalyze = async () => {
    if (!subject.trim() && !body.trim()) {
      setStatus('error');
      setErrorMsg('Please enter an email subject or body to analyze.');
      return;
    }
    
    setStatus('loading');
    setErrorMsg('');
    try {
      const data = await analyzeEmail(subject, body);
      setResult(data);
      setStatus('success');
    } catch (err) {
      setStatus('error');
      setErrorMsg(err.message || 'An unexpected error occurred.');
    }
  };

  const handleClear = () => {
    setSubject('');
    setBody('');
    setStatus('idle');
    setResult(null);
    setErrorMsg('');
  };

  const loadExampleSpam = () => {
    setSubject('URGENT: Claim your $1000 Amazon Gift Card NOW!');
    setBody('Congratulations! You have been selected to win a free $1000 gift card. Click the link below and enter your credit card details to pay for shipping. Act fast, this offer expires in 10 minutes! http://spam-link.com/claim');
    setStatus('idle');
    setResult(null);
  };

  const loadExampleHam = () => {
    setSubject('Q3 Project Kickoff Meeting');
    setBody('Hi Team,\n\nJust a quick reminder that our Q3 project kickoff meeting is scheduled for tomorrow at 10 AM EST. Please review the attached agenda beforehand.\n\nBest regards,\nSarah');
    setStatus('idle');
    setResult(null);
  };

  const charCount = subject.length + body.length;

  return (
    <div className="min-h-screen flex flex-col font-sans selection:bg-indigo-100 selection:text-indigo-900">
      {/* Header */}
      <header className="bg-white border-b border-slate-200 sticky top-0 z-10">
        <div className="max-w-6xl mx-auto px-4 h-16 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <div className="bg-indigo-600 text-white p-1.5 rounded-lg">
              <ShieldCheck size={24} />
            </div>
            <span className="text-xl font-bold text-slate-800 tracking-tight">SpamGuard</span>
          </div>
          <div className="text-sm font-medium text-slate-500 hidden sm:block">
            AI-powered email spam detection
          </div>
        </div>
      </header>

      <main className="flex-grow max-w-6xl mx-auto w-full px-4 py-8 md:py-12 flex flex-col">
        {/* Hero Section */}
        <div className="text-center mb-10 md:mb-16">
          <h1 className="text-4xl md:text-5xl font-extrabold text-slate-900 mb-4 tracking-tight">
            AI Email Spam Detector
          </h1>
          <p className="text-lg text-slate-600 max-w-2xl mx-auto">
            Analyze any email before you open or interact with it. Our machine learning model accurately identifies malicious spam and phishing attempts.
          </p>
        </div>

        {/* Main Content: Two Panels */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 items-start">
          
          {/* LEFT PANEL: Input */}
          <div className="bg-white rounded-2xl shadow-sm border border-slate-200 overflow-hidden flex flex-col transition-shadow hover:shadow-md">
            <div className="p-5 border-b border-slate-100 bg-slate-50/50 flex justify-between items-center">
              <h2 className="text-lg font-semibold text-slate-800 flex items-center gap-2">
                <Mail size={18} className="text-indigo-500" />
                Email Content
              </h2>
              <div className="flex gap-2">
                <button 
                  onClick={loadExampleHam}
                  className="text-xs font-medium bg-white border border-slate-200 text-slate-600 px-2.5 py-1 rounded hover:bg-slate-50 transition-colors"
                >
                  Example Legitimate
                </button>
                <button 
                  onClick={loadExampleSpam}
                  className="text-xs font-medium bg-white border border-slate-200 text-slate-600 px-2.5 py-1 rounded hover:bg-slate-50 transition-colors"
                >
                  Example Spam
                </button>
              </div>
            </div>
            
            <div className="p-5 flex-grow flex flex-col gap-4">
              <div>
                <label htmlFor="subject" className="block text-sm font-medium text-slate-700 mb-1">Subject</label>
                <input
                  id="subject"
                  type="text"
                  value={subject}
                  onChange={(e) => setSubject(e.target.value)}
                  placeholder="e.g., Claim your prize now!"
                  className="w-full px-4 py-2.5 rounded-xl border border-slate-200 focus:ring-2 focus:ring-indigo-500/20 focus:border-indigo-500 outline-none transition-all text-slate-700 bg-slate-50 focus:bg-white"
                />
              </div>
              
              <div className="flex-grow flex flex-col">
                <label htmlFor="body" className="block text-sm font-medium text-slate-700 mb-1">Body</label>
                <textarea
                  id="body"
                  value={body}
                  onChange={(e) => setBody(e.target.value)}
                  placeholder="Paste the email body here..."
                  className="w-full flex-grow min-h-[200px] px-4 py-3 rounded-xl border border-slate-200 focus:ring-2 focus:ring-indigo-500/20 focus:border-indigo-500 outline-none transition-all text-slate-700 resize-y bg-slate-50 focus:bg-white"
                />
                <div className="text-right mt-1.5 text-xs font-medium text-slate-400">
                  {charCount} characters
                </div>
              </div>
            </div>
            
            <div className="p-5 border-t border-slate-100 bg-slate-50/50 flex gap-3">
              <button
                onClick={handleAnalyze}
                disabled={status === 'loading'}
                className="flex-1 bg-indigo-600 hover:bg-indigo-700 text-white font-semibold py-2.5 px-4 rounded-xl flex items-center justify-center gap-2 transition-all active:scale-[0.98] disabled:opacity-70 disabled:active:scale-100"
              >
                {status === 'loading' ? (
                  <Loader2 size={18} className="animate-spin" />
                ) : (
                  <Zap size={18} />
                )}
                Analyze Email
              </button>
              
              <button
                onClick={handleClear}
                className="px-4 py-2.5 rounded-xl border border-slate-200 text-slate-600 font-semibold hover:bg-slate-100 transition-colors flex items-center gap-2"
              >
                <Trash2 size={18} />
                <span className="hidden sm:inline">Clear</span>
              </button>
            </div>
          </div>

          {/* RIGHT PANEL: Result */}
          <div className="bg-white rounded-2xl shadow-sm border border-slate-200 overflow-hidden flex flex-col min-h-[400px]">
            <div className="p-5 border-b border-slate-100 bg-slate-50/50">
              <h2 className="text-lg font-semibold text-slate-800 flex items-center gap-2">
                <Shield size={18} className="text-slate-500" />
                Analysis Result
              </h2>
            </div>
            
            <div className="p-6 flex-grow flex flex-col justify-center items-center text-center relative">
              
              {/* Empty State */}
              {status === 'idle' && (
                <div className="animate-in fade-in zoom-in duration-300 text-slate-400 flex flex-col items-center">
                  <div className="bg-slate-50 p-6 rounded-full mb-4 ring-1 ring-slate-100">
                    <Shield size={48} strokeWidth={1.5} />
                  </div>
                  <h3 className="text-xl font-semibold text-slate-700 mb-2">Ready to analyze</h3>
                  <p className="max-w-[250px] leading-relaxed">Enter an email and click Analyze to check for spam.</p>
                </div>
              )}

              {/* Loading State */}
              {status === 'loading' && (
                <div className="animate-in fade-in duration-300 text-indigo-500 flex flex-col items-center">
                  <Loader2 size={48} className="animate-spin mb-4" />
                  <p className="font-medium text-slate-600">Analyzing content patterns...</p>
                </div>
              )}

              {/* Error State */}
              {status === 'error' && (
                <div className="animate-in fade-in slide-in-from-bottom-4 duration-300 text-red-500 flex flex-col items-center w-full">
                  <div className="bg-red-50 text-red-500 p-4 rounded-full mb-4 ring-1 ring-red-100">
                    <AlertCircle size={40} />
                  </div>
                  <h3 className="text-xl font-bold text-slate-800 mb-2">Analysis Failed</h3>
                  <p className="text-slate-600 mb-6 bg-red-50 px-4 py-3 rounded-lg border border-red-100 w-full text-sm">
                    {errorMsg}
                  </p>
                  <button onClick={() => setStatus('idle')} className="text-indigo-600 font-medium hover:underline text-sm">
                    Dismiss
                  </button>
                </div>
              )}

              {/* Success State */}
              {status === 'success' && result && (
                <div className="animate-in fade-in slide-in-from-bottom-4 duration-500 w-full flex flex-col items-center">
                  {result.prediction === 'spam' ? (
                    <>
                      <div className="bg-red-100 text-red-600 p-5 rounded-full mb-5 shadow-sm shadow-red-100">
                        <ShieldAlert size={56} />
                      </div>
                      <h3 className="text-2xl font-extrabold text-red-600 mb-2 uppercase tracking-wide">Spam Detected</h3>
                      <p className="text-slate-600 mb-8 font-medium">{result.message}</p>
                      
                      <div className="w-full max-w-sm">
                        <div className="flex justify-between text-sm font-semibold mb-2">
                          <span className="text-slate-700">Confidence Score</span>
                          <span className="text-red-600">{(result.confidence * 100).toFixed(1)}%</span>
                        </div>
                        <div className="h-3 w-full bg-slate-100 rounded-full overflow-hidden">
                          <div 
                            className="h-full bg-red-500 rounded-full transition-all duration-1000 ease-out"
                            style={{ width: `${result.confidence * 100}%` }}
                          />
                        </div>
                      </div>
                    </>
                  ) : (
                    <>
                      <div className="bg-emerald-100 text-emerald-600 p-5 rounded-full mb-5 shadow-sm shadow-emerald-100">
                        <CheckCircle2 size={56} />
                      </div>
                      <h3 className="text-2xl font-extrabold text-emerald-600 mb-2 uppercase tracking-wide">Not Spam</h3>
                      <p className="text-slate-600 mb-8 font-medium">{result.message}</p>
                      
                      <div className="w-full max-w-sm">
                        <div className="flex justify-between text-sm font-semibold mb-2">
                          <span className="text-slate-700">Confidence Score</span>
                          <span className="text-emerald-600">{(result.confidence * 100).toFixed(1)}%</span>
                        </div>
                        <div className="h-3 w-full bg-slate-100 rounded-full overflow-hidden">
                          <div 
                            className="h-full bg-emerald-500 rounded-full transition-all duration-1000 ease-out"
                            style={{ width: `${result.confidence * 100}%` }}
                          />
                        </div>
                      </div>
                    </>
                  )}
                </div>
              )}
            </div>
          </div>
          
        </div>
      </main>
    </div>
  );
}

export default App;
