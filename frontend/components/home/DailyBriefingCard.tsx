"use client";

import { useEffect } from "react";
import { motion } from "framer-motion";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { ArrowRight, AlertCircle, RefreshCw } from "lucide-react";
import { useDigestStore } from "@/store/useDigestStore";
import { useAuthStore } from "@/store/useAuthStore";

export function DailyBriefingCard() {
    const { digest, isLoading, fetchLatestDigest, generateDigest } = useDigestStore();
    const { user } = useAuthStore();

    useEffect(() => {
        if (user?.email) {
            fetchLatestDigest(user.email);
        }
    }, [user?.email, fetchLatestDigest]);

    const handleGenerate = () => {
        if (user?.id && user?.email) {
            generateDigest(user.id, user.email);
        }
    };

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
                <CardHeader className="pb-2 flex flex-row items-center justify-between">
                    <CardTitle className="text-lg font-medium text-zinc-300">Daily Briefing</CardTitle>
                    <button
                        onClick={handleGenerate}
                        disabled={isLoading}
                        className="text-zinc-500 hover:text-white transition-colors disabled:opacity-50"
                    >
                        <RefreshCw size={14} className={isLoading ? "animate-spin" : ""} />
                    </button>
                </CardHeader>
                <CardContent>
                    {digest ? (
                        <div className="prose prose-invert prose-sm max-h-60 overflow-y-auto no-scrollbar">
                            <div className="whitespace-pre-line text-sm text-zinc-300 leading-relaxed">
                                {digest}
                            </div>
                        </div>
                    ) : (
                        <div className="flex flex-col items-center justify-center py-6 text-zinc-500 text-sm">
                            <p>No briefing available yet.</p>
                            <button
                                onClick={handleGenerate}
                                className="mt-2 text-indigo-400 hover:text-indigo-300 underline"
                            >
                                Generate Now
                            </button>
                        </div>
                    )}

                    {digest && (
                        <div className="mt-4 flex justify-end">
                            <button className="text-xs text-zinc-400 hover:text-white flex items-center gap-1 transition-colors">
                                View full report <ArrowRight size={12} />
                            </button>
                        </div>
                    )}
                </CardContent>
            </Card>
        </motion.div>
    );
}
