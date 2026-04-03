import React, { useRef, useMemo } from 'react';
import { useFrame } from '@react-three/fiber';
import { Points, PointMaterial, Grid } from '@react-three/drei';
import * as THREE from 'three';

interface BackgroundProps {
  variant?: "overview" | "drilldown";
  showGrid?: boolean;
  starCount?: number;
}

export const Background: React.FC<BackgroundProps> = ({ 
  variant = "overview", 
  showGrid = true, 
  starCount = 3000 
}) => {
  const starsRef = useRef<THREE.Points>(null);

  // Generate random star positions
  const positions = useMemo(() => {
    const pos = new Float32Array(starCount * 3);
    for (let i = 0; i < starCount; i++) {
      pos[i * 3] = (Math.random() - 0.5) * 100;
      pos[i * 3 + 1] = (Math.random() - 0.5) * 100;
      pos[i * 3 + 2] = (Math.random() - 0.5) * 100;
    }
    return pos;
  }, [starCount]);

  useFrame((state) => {
    if (starsRef.current) {
      starsRef.current.rotation.y += 0.0001;
      starsRef.current.rotation.x += 0.00005;
    }
  });

  return (
    <>
      <color attach="background" args={['#050a18']} />
      
      {/* Star Field */}
      <Points ref={starsRef} positions={positions} stride={3} frustumCulled={false}>
        <PointMaterial
          transparent
          color="#ffffff"
          size={0.05}
          sizeAttenuation={true}
          depthWrite={false}
          opacity={variant === "drilldown" ? 0.4 : 0.8}
        />
      </Points>

      {/* Subtle Grid */}
      {showGrid && (
        <Grid
          position={[0, -6, 0]}
          args={[100, 100]}
          cellSize={1}
          cellThickness={0.5}
          cellColor="#1e293b"
          sectionSize={5}
          sectionThickness={1}
          sectionColor="#334155"
          fadeDistance={30}
          fadeStrength={1}
          infiniteGrid
        />
      )}

      {/* Fog for depth */}
      <fog attach="fog" args={['#050a18', 10, 50]} />

      {/* Ambient and Directional Lights */}
      <ambientLight intensity={0.4} color="#4488ff" />
      <directionalLight position={[10, 10, 5]} intensity={1.5} color="#ffffff" />
      <pointLight position={[-10, -10, -10]} intensity={0.5} color="#4338ca" />
    </>
  );
};
