import React from 'react';
import React, { useState } from 'react';

export default function CopilotAI() {
  const [prompt, setPrompt] = useState('');
  const [loading, setLoading] = useState(false);
  const [aiConfig, setAiConfig] = useState(null);
  const [concepts, setConcepts] = useState([]);
  const [country, setCountry] = useState("Kenya");

  // Step 1: Send prompt to AI for interpretation
  const handleInterpret = async () => {
    if (!prompt.trim()) return;
    setLoading(true);
    setAiConfig(null);
    try {
      const res = await fetch('http://localhost:8000/api/interpret', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ prompt })
      });
      const data = await res.json();
      setAiConfig(data); // e.g. { domain: "Residential", type: "Luxury Villa", floors: 4, ... }
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  // Step 2: Generate concepts using the AI-confirmed config
  const handleGenerate = async () => {
    if (!aiConfig) return;
    setLoading(true);
    try {
      const payload = { 
        ...aiConfig, 
        country: country, // User selects country separately
        prompt: prompt // Pass original prompt back to help AI Score logic
      };
      const res = await fetch('http://localhost:8000/api/generate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });
      const data = await res.json();
      setConcepts(data.concepts);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ background: '#0f172a', borderRadius: '16px', padding: '24px', border: '1px solid #1e293b', maxWidth: '1200px', margin: '0 auto' }}>
      
      {/* --- Copilot Input --- */}
      <div style={{ display: 'flex', gap: '16px', flexWrap: 'wrap' }}>
        <div style={{ flex: 3, minWidth: '300px' }}>
          <label style={{ color: '#94a3b8', fontSize: '0.9rem', display: 'block', marginBottom: '8px' }}>🤖 RANDOM COPILOT - Describe your dream project</label>
          <textarea 
            value={prompt} 
            onChange={(e) => setPrompt(e.target.value)}
            placeholder="e.g. A 3-story sustainable glass office in Kampala with a rooftop terrace..."
            style={{ 
              width: '100%', height: '80px', background: '#1e293b', border: '1px solid #334155', 
              borderRadius: '8px', color: 'white', padding: '12px', fontFamily: 'inherit', resize: 'none' 
            }}
          />
          <div style={{ marginTop: '10px', display: 'flex', gap: '10px' }}>
            <button onClick={() => setPrompt("A 4-story luxury beach villa with open spaces and natural ventilation")} style={{ background: '#1e293b', border: 'none', color: '#94a3b8', padding: '6px 12px', borderRadius: '4px', fontSize: '12px', cursor: 'pointer' }}>🌱 Beach Villa</button>
            <button onClick={() => setPrompt("A modern corporate hub block with 5 floors and a conference hall")} style={{ background: '#1e293b', border: 'none', color: '#94a3b8', padding: '6px 12px', borderRadius: '4px', fontSize: '12px', cursor: 'pointer' }}>🏛️ Corporate Hub</button>
          </div>
        </div>
        
        <div style={{ flex: 1, display: 'flex', flexDirection: 'column', justifyContent: 'flex-end' }}>
          <button 
            onClick={handleInterpret} 
            disabled={loading}
            style={{ 
              width: '100%', padding: '12px', background: 'linear-gradient(90deg, #8b5cf6, #3b82f6)', 
              border: 'none', borderRadius: '8px', color: 'white', fontWeight: '700', cursor: 'pointer',
              boxShadow: '0 0 20px rgba(59, 130, 246, 0.3)'
            }}
          >
            {loading ? '🧠 AI Thinking...' : '🚀 Interpret & Generate'}
          </button>
        </div>
      </div>

      {/* --- AI Interpreted Configuration (Shows the user the AI got it right) --- */}
      {aiConfig && !concepts.length > 0 && (
        <div style={{ marginTop: '20px', background: '#1e293b', padding: '16px', borderRadius: '8px', borderLeft: '4px solid #22c55e' }}>
          <div style={{ color: '#22c55e', fontWeight: '600', fontSize: '0.9rem' }}>✅ AI Agent confirmed your intentions:</div>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: '16px', marginTop: '10px', color: '#e2e8f0' }}>
            <div><span style={{ color: '#94a3b8' }}>Type:</span> {aiConfig.type}</div>
            <div><span style={{ color: '#94a3b8' }}>Floors:</span> {aiConfig.floors}</div>
            <div><span style={{ color: '#94a3b8' }}>Plot Size:</span> {aiConfig.plot_size}m²</div>
            <div><span style={{ color: '#94a3b8' }}>Bathrooms:</span> {aiConfig.bathrooms}</div>
          </div>
          <div style={{ marginTop: '12px', display: 'flex', alignItems: 'center', gap: '12px' }}>
            <label style={{ color: '#94a3b8', fontSize: '0.85rem' }}>Target Region:</label>
            <select value={country} onChange={(e) => setCountry(e.target.value)} style={{ background: '#0f172a', color: 'white', border: '1px solid #334155', borderRadius: '4px', padding: '6px' }}>
              <option>Kenya</option><option>Uganda</option><option>Tanzania</option><option>South Sudan</option><option>Rwanda</option><option>Ethiopia</option>
            </select>
            <button onClick={handleGenerate} style={{ marginLeft: 'auto', background: '#22c55e', border: 'none', padding: '6px 16px', borderRadius: '4px', fontWeight: '600', color: 'white', cursor: 'pointer' }}>
              🏗️ Generate 5 Concepts
            </button>
          </div>
        </div>
      )}

      {/* --- Render the Evolution Engine Cards (The exact code you already have) --- */}
      {concepts.length > 0 && (
        <div style={{ marginTop: '32px' }}>
          <h3 style={{ color: 'white', marginBottom: '16px' }}>🔥 EVOLUTION ENGINE RESULTS</h3>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(5, 1fr)', gap: '16px' }}>
            {concepts.map((c) => (
              <div key={c.id} style={{ textAlign: 'center', background: '#131a26', padding: '16px', borderRadius: '12px', border: '1px solid #2a3a4e' }}>
                 <div style={{ fontSize: '14px', fontWeight: '600', color: '#e2e8f0', marginBottom: '8px' }}>{c.name}</div>
                 <CircularScore score={c.scores.architectural} label="Overall" />
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

// --- Helper CircularScore component (Copy from my previous message) ---
const CircularScore = ({ score, label }) => {
  const radius = 18;
  const circumference = radius * 2 * Math.PI;
  const strokeDash = (score / 100) * circumference;
  let color = "#3b82f6"; if (score >= 85) color = "#22c55e"; else if (score >= 70) color = "#eab308";
  return (
    <div style={{ textAlign: 'center', padding: '10px' }}>
      <div style={{ position: 'relative', width: '70px', height: '70px', margin: '0 auto' }}>
        <svg width="70" height="70" viewBox="0 0 50 50">
          <circle cx="25" cy="25" r="18" stroke="#1e293b" strokeWidth="4" fill="none" />
          <circle cx="25" cy="25" r="18" stroke={color} strokeWidth="4" fill="none" strokeDasharray={`${strokeDash} ${circumference}`} strokeLinecap="round" transform="rotate(-90 25 25)" />
        </svg>
        <div style={{ position: 'absolute', top: '50%', left: '50%', transform: 'translate(-50%, -50%)', fontWeight: '700', color: 'white' }}>{score}</div>
      </div>
      <div style={{ fontWeight: '600', color: 'white', marginTop: '6px', fontSize: '13px' }}>{label}</div>
    </div>
  );
};


// --- 1. Circular Progress Score Component ---
const CircularScore = ({ score, label }) => {
  const radius = 18;
  const circumference = radius * 2 * Math.PI;
  const strokeDash = (score / 100) * circumference;

  // Determine color based on score
  let color = "#3b82f6"; // Blue default
  if (score >= 85) color = "#22c55e"; // Green
  else if (score >= 70) color = "#eab308"; // Yellow

  return (
    <div style={{ textAlign: 'center', padding: '15px', background: '#0f172a', borderRadius: '12px', border: '1px solid #1e293b' }}>
      <div style={{ position: 'relative', width: '70px', height: '70px', margin: '0 auto' }}>
        <svg width="70" height="70" viewBox="0 0 50 50">
          <circle cx="25" cy="25" r="18" stroke="#1e293b" strokeWidth="4" fill="none" />
          <circle 
            cx="25" cy="25" r="18" stroke={color} strokeWidth="4" fill="none" 
            strokeDasharray={`${strokeDash} ${circumference}`} strokeLinecap="round" 
            transform="rotate(-90 25 25)" 
          />
        </svg>
        <div style={{ position: 'absolute', top: '50%', left: '50%', transform: 'translate(-50%, -50%)', fontFamily: 'sans-serif', fontSize: '18px', fontWeight: '700', color: 'white' }}>
          {score}
        </div>
      </div>
      <div style={{ fontWeight: '600', color: 'white', marginTop: '6px', fontSize: '14px' }}>{label}</div>
    </div>
  );
};

// --- 2. AI Agent Evaluation Bar Component ---
const AIAgentCard = ({ title, subtitle, score, color, icon }) => {
  return (
    <div style={{ 
      background: '#0f172a', borderRadius: '12px', padding: '16px', 
      borderLeft: `4px solid ${color}`, marginBottom: '12px' 
    }}>
      <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
        <span style={{ fontSize: '20px' }}>{icon}</span>
        <div>
          <div style={{ color: color, fontWeight: '600', fontSize: '14px' }}>{title}</div>
          <div style={{ color: '#94a3b8', fontSize: '12px' }}>{subtitle}</div>
        </div>
      </div>
      
      <div style={{ fontSize: '20px', fontWeight: '700', color: 'white', marginTop: '8px' }}>
        {score}%
      </div>
      
      {/* Progress Bar */}
      <div style={{ width: '100%', height: '6px', background: '#1e293b', borderRadius: '4px', marginTop: '8px', overflow: 'hidden' }}>
        <div style={{ width: `${score}%`, height: '100%', background: color, borderRadius: '4px', transition: 'width 1s ease-in-out' }}></div>
      </div>
    </div>
  );
};

// --- 3. Example usage in your main App Component ---
export default function ImagineDashboard() {
  // In your real app, this comes from your fetch() response!
  const apiData = {
    concepts: [
      { id: "A1B2", name: "Alpha", scores: { architectural: 92, structural: 88, sustainability: 90, cost: 85 } },
      { id: "C3D4", name: "Beta", scores: { architectural: 85, structural: 70, sustainability: 78, cost: 65 } },
    ]
  };

  return (
    <div style={{ background: '#030712', minHeight: '100vh', padding: '40px', color: 'white' }}>
      <h1 style={{ fontSize: '2rem', fontFamily: 'sans-serif' }}>AI Generation Results</h1>
      
      {/* Render the 5 Concept Cards */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(5, 1fr)', gap: '16px', marginBottom: '30px' }}>
        {apiData.concepts.map((concept, idx) => (
          <CircularScore 
            key={concept.id} 
            score={concept.scores.architectural} // Using Arch score as the main ring
            label={`Concept ${concept.name}`} 
          />
        ))}
      </div>

      {/* Render the AI Agent Evaluations for Concept Alpha */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: '16px' }}>
        <AIAgentCard title="Architect AI" subtitle="Function & Aesthetics" score={92} color="#4ade80" icon="🏛️" />
        <AIAgentCard title="Structural AI" subtitle="Safety & Stability" score={88} color="#00d2ff" icon="⚙️" />
        <AIAgentCard title="Sustainability AI" subtitle="Green & Efficiency" score={90} color="#38bdf8" icon="🌱" />
        <AIAgentCard title="Cost AI" subtitle="Budget & Value" score={85} color="#facc15" icon="💰" />
      </div>
    </div>
  );
}