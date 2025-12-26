"use client";

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import { motion, AnimatePresence } from "framer-motion";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { ArrowRight, ArrowLeft, Shield, Zap, Mail, Calendar } from "lucide-react";
import { useAuthStore } from "@/store/useAuthStore";

interface OnboardingStep {
  title: string;
  description: string;
  icon: React.ReactNode;
}

const steps: OnboardingStep[] = [
  {
    title: "Encrypted And Reliable Email Client Service",
    description: "Our products are open source & they have been independently audited by thousands of experts around the world.",
    icon: <Shield className="w-16 h-16 text-white" />
  },
  {
    title: "AI-Powered Email Management",
    description: "Kyra intelligently prioritizes your emails, suggests replies, and helps you stay on top of what matters most.",
    icon: <Zap className="w-16 h-16 text-white" />
  },
  {
    title: "Integrated Calendar & Tasks",
    description: "Automatically detect deadlines, schedule meetings, and manage your tasks all from your email inbox.",
    icon: <Calendar className="w-16 h-16 text-white" />
  }
];

export default function OnboardingPage() {
  const [currentStep, setCurrentStep] = useState(0);
  const router = useRouter();
  const { user } = useAuthStore();

  useEffect(() => {
    const completed = localStorage.getItem("onboarding_completed");
    if (completed === "true") {
      router.push("/app/dashboard");
    }
  }, [router]);

  const handleNext = () => {
    if (currentStep < steps.length - 1) {
      setCurrentStep(currentStep + 1);
    } else {
      handleComplete();
    }
  };

  const handleSkip = () => {
    handleComplete();
  };

  const handleComplete = () => {
    localStorage.setItem("onboarding_completed", "true");
    router.push("/app/dashboard");
  };

  const handlePrevious = () => {
    if (currentStep > 0) {
      setCurrentStep(currentStep - 1);
    }
  };

  const currentStepData = steps[currentStep];

  return (
    <div className="flex h-screen w-full items-center justify-center bg-white p-4">
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        className="w-full max-w-md space-y-8"
      >
        <div className="flex justify-center mb-8">
          <div className="w-32 h-32 bg-gradient-to-br from-indigo-500 to-purple-600 rounded-full flex items-center justify-center">
            {currentStepData.icon}
          </div>
        </div>

        <AnimatePresence mode="wait">
          <motion.div
            key={currentStep}
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            exit={{ opacity: 0, x: -20 }}
            transition={{ duration: 0.3 }}
            className="space-y-4 text-center"
          >
            <h1 className="text-3xl font-bold text-gray-900">
              {currentStepData.title}
            </h1>
            <p className="text-gray-600 text-lg leading-relaxed">
              {currentStepData.description}
            </p>
          </motion.div>
        </AnimatePresence>

        <div className="flex justify-center gap-2">
          {steps.map((_, index) => (
            <div
              key={index}
              className={`h-2 rounded-full transition-all ${
                index === currentStep
                  ? "bg-red-500 w-8"
                  : "bg-gray-300 w-2"
              }`}
            />
          ))}
        </div>

        <div className="flex gap-4">
          <Button
            variant="outline"
            onClick={handleSkip}
            className="flex-1 border-gray-300 text-gray-700 hover:bg-gray-100"
          >
            Skip
          </Button>
          <Button
            onClick={handleNext}
            className="flex-1 bg-red-500 text-white hover:bg-red-600"
          >
            {currentStep === steps.length - 1 ? "Get Started" : (
              <>
                Next
                <ArrowRight className="ml-2 w-4 h-4" />
              </>
            )}
          </Button>
        </div>

        {currentStep > 0 && (
          <Button
            variant="ghost"
            onClick={handlePrevious}
            className="w-full text-gray-500"
          >
            <ArrowLeft className="mr-2 w-4 h-4" />
            Previous
          </Button>
        )}
      </motion.div>
    </div>
  );
}

