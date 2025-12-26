"use client";

import { motion } from "framer-motion";
import { Card, CardContent } from "@/components/ui/card";

export function QuickStats() {
    const progress = 85;
    const circumference = 2 * Math.PI * 24; // r=24
    const offset = circumference - (progress / 100) * circumference;

    return (
        <motion.div
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ delay: 0.4 }}
        >
            <Card className="bg-gradient-to-br from-indigo-900/20 to-purple-900/20 border-zinc-800">
                <CardContent className="p-4 flex items-center justify-between">
                    <div>
                        <h3 className="text-sm font-medium text-zinc-300">Inbox Zero</h3>
                        <p className="text-xs text-zinc-500">Keep it up, you're close!</p>
                    </div>
                    <div className="relative w-16 h-16 flex items-center justify-center">
                        {/* Background Circle */}
                        <svg className="w-full h-full transform -rotate-90">
                            <circle
                                cx="32"
                                cy="32"
                                r="24"
                                className="stroke-zinc-800"
                                strokeWidth="6"
                                fill="transparent"
                            />
                            {/* Progress Circle */}
                            <circle
                                cx="32"
                                cy="32"
                                r="24"
                                className="stroke-indigo-500"
                                strokeWidth="6"
                                fill="transparent"
                                strokeDasharray={circumference}
                                strokeDashoffset={offset}
                                strokeLinecap="round"
                            />
                        </svg>
                        <span className="absolute text-xs font-bold text-white">{progress}%</span>
                    </div>
                </CardContent>
            </Card>
        </motion.div>
    );
}
