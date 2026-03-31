const { useState, useEffect, useMemo } = React;
const motion = (typeof FramerMotion !== 'undefined' ? FramerMotion.motion : (typeof Motion !== 'undefined' ? Motion.motion : { div: (props) => <div {...props} /> }));

const VillageSquare = ({ onNodeClick, activeNode }) => {
    return (
        <div className="relative w-full max-w-xl mx-auto aspect-square bg-[#2D2424] rounded-full border-8 border-[#5C3D2E] shadow-2xl overflow-hidden flex items-center justify-center p-8 mb-10">
            <svg viewBox="0 0 400 400" className="w-full h-full">
                {/* Decorative Pattern Background */}
                <defs>
                    <pattern id="mudcloth" x="0" y="0" width="40" height="40" patternUnits="userSpaceOnUse">
                        <path d="M0 20 L40 20 M20 0 L20 40" stroke="#3D2B1F" strokeWidth="1" fill="none" />
                        <circle cx="20" cy="20" r="2" fill="#3D2B1F" />
                    </pattern>
                </defs>
                <circle cx="200" cy="200" r="190" fill="url(#mudcloth)" opacity="0.3" pointerEvents="none" />

                {/* Connections */}
                <line x1="200" y1="200" x2="200" y2="80" stroke="#E0AC49" strokeWidth="2" strokeDasharray="5,5" opacity="0.5" pointerEvents="none" />
                <line x1="200" y1="200" x2="320" y2="280" stroke="#E0AC49" strokeWidth="2" strokeDasharray="5,5" opacity="0.5" pointerEvents="none" />
                <line x1="200" y1="200" x2="80" y2="280" stroke="#E0AC49" strokeWidth="2" strokeDasharray="5,5" opacity="0.5" pointerEvents="none" />

                {/* The Fire (Center) */}
                <g
                    onClick={() => onNodeClick('fire')}
                    className="cursor-pointer group"
                >
                    <circle cx="200" cy="200" r="50" fill={activeNode === 'fire' ? '#FF4D00' : '#B85C38'} className="transition-colors duration-500 shadow-lg" />
                    <path d="M185 210 Q200 160 215 210 T200 240 Z" fill="#FF9900">
                        <animate attributeName="d" values="M185 210 Q200 160 215 210 T200 240 Z; M188 210 Q200 150 212 210 T200 250 Z; M185 210 Q200 160 215 210 T200 240 Z" dur="1.5s" repeatCount="indefinite" />
                    </path>
                    <text x="200" y="270" textAnchor="middle" fill="#E0AC49" className="text-[10px] font-bold uppercase tracking-[0.2em] pointer-events-none">The Fire</text>
                </g>

                {/* The Elder (Top) */}
                <g
                    onClick={() => onNodeClick('elder')}
                    className="cursor-pointer group"
                >
                    <circle cx="200" cy="80" r="40" fill={activeNode === 'elder' ? '#B85C38' : '#5C3D2E'} className="transition-colors duration-500" />
                    <path d="M190 70 Q200 50 210 70 L205 95 L195 95 Z" fill="#E0AC49" />
                    <text x="200" y="140" textAnchor="middle" fill="#E0AC49" className="text-[10px] font-bold uppercase tracking-[0.2em] pointer-events-none">The Elder</text>
                </g>

                {/* The Drum (Bottom Right) */}
                <g
                    onClick={() => onNodeClick('drum')}
                    className="cursor-pointer group"
                >
                    <circle cx="320" cy="280" r="40" fill={activeNode === 'drum' ? '#B85C38' : '#5C3D2E'} className="transition-colors duration-500" />
                    <path d="M310 265 L330 265 L325 295 L315 295 Z" fill="#E0AC49" />
                    <circle cx="320" cy="265" r="10" fill="#FDFCF8" stroke="#5C3D2E" strokeWidth="2" />
                    <text x="320" y="340" textAnchor="middle" fill="#E0AC49" className="text-[10px] font-bold uppercase tracking-[0.2em] pointer-events-none">The Drum</text>
                </g>

                {/* The Seeker (Bottom Left) */}
                <g
                    onClick={() => onNodeClick('seeker')}
                    className="cursor-pointer group"
                >
                    <circle cx="80" cy="280" r="40" fill={activeNode === 'seeker' ? '#B85C38' : '#5C3D2E'} className="transition-colors duration-500" />
                    <path d="M70 270 L90 270 L80 300 Z" fill="#E0AC49" />
                    <text x="80" y="340" textAnchor="middle" fill="#E0AC49" className="text-[10px] font-bold uppercase tracking-[0.2em] pointer-events-none">The Seeker</text>
                </g>
            </svg>
        </div>
    );
};

const RiddleProverb = ({ content, onResponse, isCorrect, showResult }) => {
    const text = content.type === 'proverb' ? content.text : content.question;
    const words = text.split(' ');

    return (
        <div className="flex flex-col h-full">
            <header className="mb-6">
                <span className="text-[#E0AC49] font-bold uppercase tracking-widest text-xs">{content.type}</span>
            </header>

            <div className="flex-1">
                <motion.div
                    className="text-2xl font-display text-white leading-relaxed italic mb-8"
                    initial="hidden"
                    animate="visible"
                >
                    {words.map((word, i) => (
                        <motion.span
                            key={i}
                            className="inline-block mr-2"
                            initial={{ opacity: 0, y: 20 }}
                            animate={{ opacity: 1, y: 0 }}
                            transition={{
                                delay: i * 0.1,
                                duration: 0.5,
                                ease: "easeOut"
                            }}
                        >
                            {word}
                        </motion.span>
                    ))}
                </motion.div>

                {content.type === 'proverb' ? (
                    <div className="grid gap-3">
                        {content.options.map((opt, idx) => (
                            <button
                                key={idx}
                                disabled={showResult}
                                onClick={() => onResponse(opt.value)}
                                className={`p-4 rounded-xl text-left text-sm transition-all border ${
                                    showResult
                                        ? opt.text === content.truth
                                            ? 'bg-emerald-600/30 border-emerald-500 text-white'
                                            : 'bg-black/20 border-white/5 text-slate-500'
                                        : 'bg-white/5 border-white/10 text-slate-300 hover:bg-[#B85C38]/20 hover:border-[#B85C38]'
                                }`}
                            >
                                {opt.text}
                            </button>
                        ))}
                    </div>
                ) : (
                    <div className="space-y-4">
                        {!showResult ? (
                            <div className="flex gap-2">
                                <input
                                    id="riddle-input"
                                    type="text"
                                    placeholder="Your answer..."
                                    className="flex-1 bg-white/5 border border-white/10 rounded-xl px-4 py-3 text-white focus:outline-none focus:border-[#E0AC49]"
                                    onKeyDown={(e) => {
                                        if (e.key === 'Enter') {
                                            const val = e.target.value.toLowerCase();
                                            const isRight = val.includes(content.answer.toLowerCase());
                                            onResponse(isRight ? 1.0 : 0.0);
                                        }
                                    }}
                                />
                                <button
                                    onClick={() => {
                                        const input = document.getElementById('riddle-input');
                                        const val = input.value.toLowerCase();
                                        const isRight = val.includes(content.answer.toLowerCase());
                                        onResponse(isRight ? 1.0 : 0.0);
                                    }}
                                    className="px-6 py-3 bg-[#B85C38] text-white rounded-xl font-bold hover:bg-[#A65232] transition-colors"
                                >
                                    Submit
                                </button>
                            </div>
                        ) : (
                            <div className={`p-6 rounded-2xl border ${isCorrect ? 'bg-emerald-600/20 border-emerald-500/50' : 'bg-red-600/20 border-red-500/50'}`}>
                                <h5 className={`font-bold mb-2 ${isCorrect ? 'text-emerald-400' : 'text-red-400'}`}>
                                    {isCorrect ? 'Wise Choice!' : 'Not Quite...'}
                                </h5>
                                <p className="text-white">The answer was: <span className="font-bold text-[#E0AC49]">{content.answer}</span></p>
                            </div>
                        )}
                    </div>
                )}
            </div>

            {showResult && (
                <button
                    onClick={() => onResponse(null)}
                    className="mt-6 w-full py-4 bg-white/5 border border-white/10 rounded-xl text-white font-bold hover:bg-white/10 transition-colors flex items-center justify-center gap-2"
                >
                    Continue Journey
                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M5 12h14"></path><path d="m12 5 7 7-7 7"></path></svg>
                </button>
            )}
        </div>
    );
};

const OralityLabApp = () => {
    const [activeNode, setActiveNode] = useState(null);
    const [interactions, setInteractions] = useState(0);
    const [totalTruth, setTotalTruth] = useState(0);
    const [totalDeviation, setTotalDeviation] = useState(0);
    const [visitedNodes, setVisitedNodes] = useState(new Set());
    const [currentContent, setCurrentContent] = useState(null);
    const [showResult, setShowResult] = useState(false);
    const [lastCorrect, setLastCorrect] = useState(false);

    const handleNodeClick = (node) => {
        if (showResult) return;
        setActiveNode(node);
        setVisitedNodes(prev => new Set(prev).add(node));

        // Pick new content
        const pool = Math.random() > 0.5 ? KNOWLEDGE_BANK.proverbs : KNOWLEDGE_BANK.riddles;
        const type = pool === KNOWLEDGE_BANK.proverbs ? 'proverb' : 'riddle';
        const item = pool[Math.floor(Math.random() * pool.length)];
        setCurrentContent({ ...item, type });
        setShowResult(false);
    };

    const handleResponse = (tValue) => {
        if (tValue === null) {
            // Reset for next interaction
            setCurrentContent(null);
            setShowResult(false);
            setActiveNode(null);
            return;
        }

        const T = tValue;
        const D = Math.abs(1.0 - T);

        setTotalTruth(prev => prev + T);
        setTotalDeviation(prev => prev + D);
        setInteractions(prev => prev + 1);
        setLastCorrect(T > 0.7);
        setShowResult(true);
    };

    // LT = f(I, T, D)
    const ltModel = useMemo(() => {
        const I = visitedNodes.size / 4; // Max nodes: Elder, Drum, Fire, Seeker
        const avgT = interactions > 0 ? totalTruth / interactions : 0;
        const avgD = interactions > 0 ? totalDeviation / interactions : 0;

        const lt = (I * 0.3 + avgT * 0.7) * (1 - avgD * 0.4);
        return Math.max(0, Math.min(1, lt));
    }, [visitedNodes.size, totalTruth, totalDeviation, interactions]);

    return (
        <div className={`orality-lab-container p-8 md:p-12 rounded-[3rem] transition-all duration-1000 border border-white/10 shadow-2xl relative overflow-hidden ${ltModel > 0.7 ? 'orality-vibrant' : ltModel < 0.3 && interactions > 0 ? 'orality-distorted' : ''}`} style={{ backgroundColor: '#2D2424' }}>
            {/* Visual Feedback Overlays */}
            {ltModel > 0.7 && <div className="absolute inset-0 pointer-events-none animate-pulse bg-indigo-500/5"></div>}
            {ltModel < 0.3 && interactions > 0 && <div className="absolute inset-0 pointer-events-none bg-slate-900/40 backdrop-grayscale"></div>}

            <div className="grid lg:grid-cols-2 gap-12 items-center relative z-10">
                <div>
                    <header className="mb-8">
                        <span className="text-[#E0AC49] font-bold uppercase tracking-widest text-[10px]">Indigenous Knowledge Systems</span>
                        <h3 className="text-4xl font-display font-bold text-white mt-2">IKS: The Orality Lab</h3>
                        <p className="text-slate-400 mt-4 leading-relaxed">
                            Interact with the nodes of wisdom. Journey through the village square to unlock the secrets of African orality.
                        </p>
                    </header>

                    <VillageSquare onNodeClick={handleNodeClick} activeNode={activeNode} />

                    <div className="grid grid-cols-3 gap-4 mt-10">
                        <div className="bg-black/40 p-4 rounded-2xl border border-white/5 text-center">
                            <span className="block text-[10px] text-[#E0AC49] uppercase font-bold mb-1">Interactions</span>
                            <span className="text-2xl font-display font-bold text-white">{interactions}</span>
                        </div>
                        <div className="bg-black/40 p-4 rounded-2xl border border-white/5 text-center">
                            <span className="block text-[10px] text-[#E0AC49] uppercase font-bold mb-1">Truth (T)</span>
                            <span className="text-2xl font-display font-bold text-white">{(totalTruth / (interactions || 1)).toFixed(2)}</span>
                        </div>
                        <div className="bg-black/40 p-4 rounded-2xl border border-white/5 text-center">
                            <span className="block text-[10px] text-[#E0AC49] uppercase font-bold mb-1">LT Model</span>
                            <span className="text-2xl font-display font-bold text-indigo-400">{(ltModel * 100).toFixed(0)}%</span>
                        </div>
                    </div>
                </div>

                <div className="relative min-h-[450px] flex flex-col">
                    {!currentContent ? (
                        <div className="flex-1 flex items-center justify-center text-center p-10 border-2 border-dashed border-white/10 rounded-[2rem] bg-black/20">
                            <div className="space-y-4">
                                <div className="w-16 h-16 bg-[#B85C38]/20 rounded-full flex items-center justify-center mx-auto text-[#E0AC49]">
                                    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"></path><path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"></path></svg>
                                </div>
                                <h4 className="text-xl font-bold text-white">Begin Your Journey</h4>
                                <p className="text-slate-400 text-sm">Click on a node in the Village Square to receive a riddle or proverb.</p>
                            </div>
                        </div>
                    ) : (
                        <div className="flex-1 bg-black/40 rounded-[2rem] p-8 border border-white/10 shadow-2xl relative overflow-hidden backdrop-blur-md">
                             <RiddleProverb
                                content={currentContent}
                                onResponse={handleResponse}
                                isCorrect={lastCorrect}
                                showResult={showResult}
                             />
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
};

const root = ReactDOM.createRoot(document.getElementById('orality-lab-root'));
root.render(<OralityLabApp />);
