"use client";

import { useEffect } from "react";
import { Capacitor } from "@capacitor/core";

export default function ServiceWorkerRegister() {
    useEffect(() => {
        if (
            typeof window !== "undefined" &&
            "serviceWorker" in navigator &&
            Capacitor.getPlatform() === "web"
        ) {
            // Register PWA Service Worker
            navigator.serviceWorker
                .register("/sw.js")
                .then((registration) => {
                    console.log("SW Registered: ", registration);
                })
                .catch((error) => {
                    // Silently fail in dev or if sw.js missing
                    console.log("SW Registration failed: ", error);
                });
        }
    }, []);

    return null;
}
