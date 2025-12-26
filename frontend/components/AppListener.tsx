"use client";

import { useEffect } from 'react';
import { App as CapacitorApp } from '@capacitor/app';
import { Capacitor } from '@capacitor/core';

export default function AppListener() {
    useEffect(() => {
        if (Capacitor.getPlatform() === 'web') return;

        const setupListener = async () => {
            CapacitorApp.addListener('backButton', ({ canGoBack }) => {
                if (canGoBack) {
                    window.history.back();
                } else {
                    CapacitorApp.exitApp();
                }
            });
        };

        setupListener();

        return () => {
            if (Capacitor.getPlatform() !== 'web') {
                CapacitorApp.removeAllListeners();
            }
        };
    }, []);

    return null;
}
