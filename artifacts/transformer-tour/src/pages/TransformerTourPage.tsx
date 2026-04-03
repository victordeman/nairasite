import React, { useState, Suspense } from 'react';
import { Canvas } from '@react-three/fiber';
import { OrbitControls, PerspectiveCamera } from '@react-three/drei';
import { Background } from '../components/Background';
import { OLD_TRANSFORMER, MODERN_TRANSFORMER } from '../data/architectureData';
import { BlockData } from '../types';

export const TransformerTourPage: React.FC = () => {
  const [selectedArch, setSelectedArch] = useState(OLD_TRANSFORMER);
  const [selectedBlock, setSelectedBlock] = useState<BlockData | null>(null);

  const handleBlockClick = (block: BlockData) => {
    setSelectedBlock(block);
  };

  return (
    <div className="w-full h-screen bg-[#050a18] relative overflow-hidden">
      {/* 3D Canvas */}
      <Canvas shadows>
        <Suspense fallback={null}>
          <Background variant={selectedBlock ? "drilldown" : "overview"} />
          
          <PerspectiveCamera makeDefault position={[0, 2, 12]} />
          <OrbitControls enableDamping dampingFactor={0.05} />

          <group>
            {selectedArch.blocks.map((block) => (
              <mesh 
                key={block.id} 
                position={block.position}
                onClick={() => handleBlockClick(block)}
                onPointerOver={() => (document.body.style.cursor = 'pointer')}
                onPointerOut={() => (document.body.style.cursor = 'auto')}
              >
                <boxGeometry args={[3, 0.8, 1]} />
                <meshPhongMaterial 
                  color={block.color} 
                  emissive={block.color}
                  emissiveIntensity={selectedBlock?.id === block.id ? 1.5 : 0.4}
                  transparent
                  opacity={0.9}
                />
              </mesh>
            ))}
          </group>
        </Suspense>
      </Canvas>

      {/* UI Overlay */}
      <div className="absolute top-6 left-6 pointer-events-none z-10">
        <h1 className="text-sm font-bold tracking-widest text-indigo-400 uppercase">Transformer 3D Tour</h1>
        <h2 className="text-2xl font-bold text-white">{selectedArch.name}</h2>
      </div>

      {/* Info Panel */}
      {selectedBlock && (
        <div className="fixed top-20 right-6 w-[420px] bg-[#0a0f1a] border border-slate-800/40 rounded-[32px] shadow-[0_24px_64px_rgba(0,0,0,0.6)] overflow-hidden z-50">
          <div 
            className="px-8 py-6 flex items-center justify-between border-b transition-all duration-700"
            style={{ 
              background: `linear-gradient(to bottom, #${(selectedBlock.color * 0.1).toString(16).split('.')[0].padStart(6, '0')}, #${(selectedBlock.color * 0.18).toString(16).split('.')[0].padStart(6, '0')})`,
              borderBottomColor: `#${selectedBlock.color.toString(16).padStart(6, '0')}22`
            }}
          >
            <div className="flex items-center gap-4">
              <div 
                className="w-2.5 h-2.5 rounded-full transition-all duration-700"
                style={{ 
                  backgroundColor: `#${selectedBlock.color.toString(16).padStart(6, '0')}`,
                  boxShadow: `0 0 20px #${selectedBlock.color.toString(16).padStart(6, '0')}`
                }}
              />
              <div>
                <h2 className="text-white font-bold text-xl tracking-tight leading-none mb-1.5">{selectedBlock.name}</h2>
                <p className="text-slate-400 text-xs font-semibold uppercase tracking-wider opacity-80">{selectedBlock.nameIgbo}</p>
              </div>
            </div>
            <button 
              onClick={() => setSelectedBlock(null)}
              className="text-slate-500 hover:text-white transition-all hover:rotate-90 duration-300 p-2"
            >
              <svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line></svg>
            </button>
          </div>

          <div className="p-8 space-y-10">
            <div className="space-y-4">
              <div className="flex items-center gap-2.5 text-[#38bdf8] text-[11px] font-black tracking-[0.2em] uppercase">
                <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"></path><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"></path></svg>
                ENGLISH
              </div>
              <p className="text-slate-100/95 leading-relaxed text-[16px] font-medium tracking-wide">
                {selectedBlock.description}
              </p>
            </div>
          </div>

          <div className="px-8 pb-8">
            <button 
              className="w-full transition-all text-white font-bold py-5 rounded-[24px] flex items-center justify-center gap-3 shadow-2xl active:scale-[0.97] border tracking-wide"
              style={{
                background: `linear-gradient(to bottom, #${(selectedBlock.color * 0.15).toString(16).split('.')[0].padStart(6, '0')}, #${(selectedBlock.color * 0.1).toString(16).split('.')[0].padStart(6, '0')})`,
                borderColor: `#${selectedBlock.color.toString(16).padStart(6, '0')}44`,
                color: `#${selectedBlock.color.toString(16).padStart(6, '0')}`
              }}
            >
              <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line><line x1="11" y1="8" x2="11" y2="14"></line><line x1="8" y1="11" x2="14" y2="11"></line></svg>
              Drill Down — See Internals
            </button>
          </div>
        </div>
      )}

      <div className="absolute bottom-6 left-6 text-[10px] text-slate-500 uppercase tracking-widest z-10">
        Click blocks to explore · Drag to rotate · Scroll to zoom
      </div>
    </div>
  );
};
