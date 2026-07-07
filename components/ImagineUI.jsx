import React from 'react';

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