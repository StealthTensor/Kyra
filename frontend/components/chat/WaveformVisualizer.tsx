"use client";

import { motion } from "framer-motion";

export function WaveformVisualizer() {
    // Simulate waveform bars
    const bars = 20;

    return (
        <div className="h-48 w-full flex items-center justify-center gap-1.5 opacity-80 mt-8">
            {Array.from({ length: bars }).map((_, i) => (
                <motion.div
                    key={i}
                    className="w-1.5 bg-indigo-500 rounded-full"
                    animate={{
                        height: [10, Math.random() * 60 + 20, 10],
                        opacity: [0.5, 1, 0.5],
                    }}
                    transition={{
                        duration: 1.5,
                        repeat: Infinity,
                        repeatType: "mirror",
                        delay: i * 0.1,
                        ease: "easeInOut",
                    }}
                />
            ))}
        </div>
    );
}
