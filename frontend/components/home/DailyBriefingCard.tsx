"use client";

import { motion } from "framer-motion";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { ArrowRight, AlertCircle } from "lucide-react";

export function DailyBriefingCard() {
    // Mock data for now, eventually will fetch from DailyDigest API
    const briefingItems = [
        { id: 1, text: "Project 'Titan' proposal due by 5 PM", type: "deadline" },
        { id: 2, text: "Lab meeting at 2 PM", type: "event" },
        { id: 3, text: "Review SRM budget report", type: "task" },
    ];

    return (
        <motion.div
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.1 }}
        >
            <Card className="bg-white/5 border-zinc-800 backdrop-blur-md text-zinc-100 overflow-hidden relative">
                <div className="absolute top-0 right-0 p-3 opacity-10">
                    <AlertCircle size={80} />
                </div>
                <CardHeader className="pb-2">
                    <CardTitle className="text-lg font-medium text-zinc-300">Daily Briefing</CardTitle>
                </CardHeader>
                <CardContent>
                    <ul className="space-y-3">
                        {briefingItems.map((item, index) => (
                            <motion.li
                                key={item.id}
                                initial={{ opacity: 0, x: -10 }}
                                animate={{ opacity: 1, x: 0 }}
                                transition={{ delay: 0.2 + index * 0.1 }}
                                className="flex items-start gap-3 p-3 rounded-lg bg-zinc-900/50 border border-zinc-800/50"
                            >
                                <div className="h-2 w-2 mt-2 rounded-full bg-orange-500 shrink-0" />
                                <span className="text-sm text-zinc-300 leading-snug">{item.text}</span>
                            </motion.li>
                        ))}
                    </ul>
                    <div className="mt-4 flex justify-end">
                        <button className="text-xs text-zinc-400 hover:text-white flex items-center gap-1 transition-colors">
                            View full report <ArrowRight size={12} />
                        </button>
                    </div>
                </CardContent>
            </Card>
        </motion.div>
    );
}
