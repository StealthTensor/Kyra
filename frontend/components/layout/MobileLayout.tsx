"use client";

import React, { useState } from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { motion, AnimatePresence } from 'framer-motion';
import { Home, Mail, MessageSquare, Calendar } from 'lucide-react';
import { Capacitor } from '@capacitor/core';
import { Haptics, ImpactStyle } from '@capacitor/haptics';

export default function MobileLayout({ children }: { children: React.ReactNode }) {
    const pathname = usePathname();

    const handleTabClick = async () => {
        if (Capacitor.isNativePlatform()) {
            await Haptics.impact({ style: ImpactStyle.Light });
        }
    };

    const navItems = [
        { name: 'Home', icon: Home, path: '/app/dashboard' },
        { name: 'Mail', icon: Mail, path: '/app/mail' },
        { name: 'Kyra', icon: MessageSquare, path: '/app/chat' },
        { name: 'Timeline', icon: Calendar, path: '/app/timeline' },
    ];

    return (
        <div className="flex flex-col h-screen bg-zinc-950 text-white overflow-hidden selection:bg-zinc-800">
            <main className="flex-1 overflow-y-auto pb-20 no-scrollbar">
                <AnimatePresence mode="wait">
                    <motion.div
                        key={pathname}
                        initial={{ opacity: 0, x: 20 }}
                        animate={{ opacity: 1, x: 0 }}
                        exit={{ opacity: 0, x: -20 }}
                        transition={{ duration: 0.2, ease: "easeInOut" }}
                        className="h-full"
                    >
                        {children}
                    </motion.div>
                </AnimatePresence>
            </main>

            {/* Sticky Bottom Navigation */}
            <nav className="fixed bottom-0 left-0 right-0 bg-zinc-950/80 backdrop-blur-xl border-t border-zinc-900 pb-[env(safe-area-inset-bottom)] z-50">
                <div className="flex justify-around items-center h-16">
                    {navItems.map((item) => {
                        const isActive = pathname === item.path;
                        return (
                            <Link
                                key={item.path}
                                href={item.path}
                                onClick={handleTabClick}
                                className={`flex flex-col items-center justify-center w-full h-full space-y-1 transition-colors duration-200 ${isActive ? 'text-white' : 'text-zinc-500 hover:text-zinc-400'
                                    }`}
                            >
                                <item.icon size={24} strokeWidth={isActive ? 2.5 : 2} />
                                <span className="text-[10px] font-medium tracking-wide">{item.name}</span>
                                {isActive && (
                                    <motion.div
                                        layoutId="activeTab"
                                        className="absolute bottom-1 w-1 h-1 bg-white rounded-full"
                                    />
                                )}
                            </Link>
                        );
                    })}
                </div>
            </nav>
        </div>
    );
}
