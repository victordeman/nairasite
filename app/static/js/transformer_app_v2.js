import React, { useState, Suspense, useRef, useMemo } from 'react';
import { Canvas, useFrame } from '@react-three/fiber';
import { OrbitControls, PerspectiveCamera, Points, Grid, Text } from '@react-three/drei';
import * as THREE from 'three';

const e = React.createElement;

// --- DATA ---
const OLD_TRANSFORMER = {
  id: 'original-2017',
  name: 'Original Transformer (2017)',
  components: [
    { id: 'enc-input-embedding', name: 'Input Embedding', nameIgbo: 'Mtinyere Ihe Ntinye', description: 'Converts input tokens into dense vectors of d_model dimensions.', descriptionIgbo: 'Ọ na-atụgharị mkpụrụokwu ntinye ka ọ bụrụ vectors dị arọ nke akụkụ d_model.', position: [0, 0, 0], color: '#6366f1', shape: 'box', group: 'encoder' },
    { id: 'enc-pos-encoding', name: 'Positional Encoding', nameIgbo: 'Ntinye Ọnọdụ', description: 'Adds information about the relative or absolute position of the tokens.', descriptionIgbo: 'Na-agbakwunye ozi gbasara ọnọdụ ikwu ma ọ bụ zuru oke nke akara ndị ahụ.', position: [0, 1.2, 0], color: '#a855f7', shape: 'box', group: 'encoder' },
    { id: 'enc-mha', name: 'Multi-Head Attention', nameIgbo: 'Nleba anya nwere ọtụtụ isi', description: 'Allows the model to jointly attend to information from different representation subspaces.', descriptionIgbo: 'Na-enye ohere ka ihe nlereanya ahụ lekọta ozi sitere na subspaces nnọchite anya dịiche iche.', position: [0, 2.4, 0], color: '#3b82f6', shape: 'box', group: 'encoder' },
    { id: 'enc-add-norm', name: 'Add & Norm', nameIgbo: 'Tinye & Hazie', description: 'Residual connection followed by layer normalization.', descriptionIgbo: 'Njikọ residual na-esochi ya site na nhazi oyi akwa.', position: [0, 3.6, 0], color: '#10b981', shape: 'box', group: 'encoder' },
    { id: 'enc-ffn', name: 'Feed Forward', nameIgbo: 'Nye n\'ihu', description: 'Point-wise fully connected layers applied to each position identically.', descriptionIgbo: 'Ihe mkpuchi ejikọtara nke ọma na-emetụta ọnọdụ ọ bụla n\'otu aka ahụ.', position: [0, 4.8, 0], color: '#f97316', shape: 'box', group: 'encoder' },
    { id: 'out-linear-softmax', name: 'Linear + Softmax Output', nameIgbo: 'Mmepụta Linear + Softmax', description: 'The final linear layer projects the decoder output to the vocabulary size (e.g., 30,000 dimensions). Softmax converts these logits to probabilities over the vocabulary. The token with the highest probability is selected as the next output token.', descriptionIgbo: 'Ọwa linear ikpeazụ na-atụgharị mmepụta decoder n\'ogo okwu (dịka ọkwa 30,000). Softmax na-atụgharị logits ndị a n\'ike n\'elu okwu. A na-ahọrọ akara nke nwere ike kachasị dị elu dị ka akara mmepụta ọzọ.', position: [5, 3.6, 0], color: '#ec4899', shape: 'box', group: 'output' }
  ]
};

// --- COMPONENTS ---
const Background = ({ variant = "overview", showGrid = true }) => {
  const starsRef = useRef();
  const starCount = 2000;
  const positions = useMemo(() => {
    const pos = new Float32Array(starCount * 3);
    for (let i = 0; i < starCount; i++) {
      pos[i * 3] = (Math.random() - 0.5) * 100;
      pos[i * 3 + 1] = (Math.random() - 0.5) * 100;
      pos[i * 3 + 2] = (Math.random() - 0.5) * 100;
    }
    return pos;
  }, []);

  useFrame((state) => {
    if (starsRef.current) starsRef.current.rotation.y = state.clock.getElapsedTime() * 0.02;
  });

  const gridColor = variant === "overview" ? "#1e293b" : "#334155";

  return e(React.Fragment, null,
    e('color', { attach: "background", args: ['#050a18'] }),
    e(Points, { ref: starsRef, positions: positions, stride: 3 },
      e('pointMaterial', { transparent: true, color: "#ffffff", size: 0.05, sizeAttenuation: true, depthWrite: false, opacity: 0.6 })
    ),
    showGrid && e(Grid, { position: [0, -5, 0], args: [100, 100], cellColor: gridColor, sectionColor: gridColor, cellThickness: 0.5, sectionThickness: 1, fadeDistance: 50, fadeStrength: 1, infiniteGrid: true, transparent: true, opacity: 0.1 }),
    e('ambientLight', { intensity: 0.4, color: "#4488ff" }),
    e('directionalLight', { position: [10, 10, 5], intensity: 1.5, color: "#ffffff" })
  );
};

const TransformerBlock = ({ component, onClick, isSelected }) => {
  const meshRef = useRef();
  useFrame((state) => {
    if (meshRef.current) {
      meshRef.current.position.y = component.position[1] + Math.sin(state.clock.getElapsedTime() + component.position[1]) * 0.1;
      const s = isSelected ? 1 + Math.sin(state.clock.getElapsedTime() * 4) * 0.05 : 1;
      meshRef.current.scale.set(s, s, s);
    }
  });
  return e('group', { position: component.position },
    e('mesh', { ref: meshRef, onClick: (ev) => { ev.stopPropagation(); onClick(); } },
      e('boxGeometry', { args: [3, 0.8, 1] }),
      e('meshPhongMaterial', { color: component.color, emissive: component.color, emissiveIntensity: isSelected ? 1.5 : 0.5, transparent: true, opacity: 0.9 })
    ),
    e(Text, { position: [0, 0.8, 0], fontSize: 0.2, color: "#ffffff" }, component.name)
  );
};

const App = () => {
  const [selectedComp, setSelectedComp] = useState(null);
  const [language, setLanguage] = useState('en');

  return e('div', { className: "relative w-full h-screen bg-slate-950 overflow-hidden text-white font-sans" },
    e(Canvas, { shadows: true },
      e(PerspectiveCamera, { makeDefault: true, position: [0, 5, 15], fov: 50 }),
      e(OrbitControls, { enableDamping: true }),
      e(Suspense, { fallback: null },
        e(Background, null),
        e('group', null,
          OLD_TRANSFORMER.components.map(comp =>
            e(TransformerBlock, {
              key: comp.id,
              component: comp,
              onClick: () => setSelectedComp(comp),
              isSelected: selectedComp?.id === comp.id
            })
          )
        )
      )
    ),
    e('div', { className: "absolute top-6 left-6 pointer-events-none" },
      e('h1', { className: "text-sm font-bold tracking-widest text-indigo-400 uppercase" }, "Transformer 3D Tour"),
      e('h2', { className: "text-2xl font-bold" }, "Original Transformer (2017)")
    ),
    e('div', { className: "absolute top-6 right-6 flex gap-3" },
      e('button', {
        onClick: () => setLanguage(l => l === 'en' ? 'ig' : 'en'),
        className: "px-4 py-2 bg-black/40 backdrop-blur-md border border-white/10 rounded-full text-xs font-bold"
      }, language === 'en' ? 'IGBO' : 'ENGLISH')
    ),
    selectedComp && e('div', { className: "absolute top-24 right-6 w-80 bg-slate-900/80 backdrop-blur-xl rounded-3xl p-6 border border-white/10 shadow-2xl" },
      e('button', { onClick: () => setSelectedComp(null), className: "absolute top-4 right-4 text-slate-400" }, "✕"),
      e('h3', { className: "text-xl font-bold mb-4", style: { color: selectedComp.color } }, selectedComp.name),
      e('div', { className: "space-y-4 text-sm leading-relaxed text-slate-300" },
        e('p', null, e('span', { className: "text-indigo-400 font-bold block mb-1" }, "ENGLISH"), selectedComp.description),
        e('p', { className: "italic" }, e('span', { className: "text-indigo-400 font-bold block mb-1" }, "IGBO"), selectedComp.descriptionIgbo)
      )
    ),
    e('div', { className: "absolute bottom-6 left-6 text-[10px] text-slate-500 uppercase tracking-widest" }, "Click blocks to explore · Drag to rotate · Scroll to zoom")
  );
};

export default App;
