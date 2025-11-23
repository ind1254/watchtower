import { Toaster } from "@/components/ui/toaster";
import { Toaster as Sonner } from "@/components/ui/sonner";
import { TooltipProvider } from "@/components/ui/tooltip";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import { Chatbot } from "@/components/Chatbot";
import { ProtectedRoute } from "@/components/ProtectedRoute";
import TransactionRisk from "./pages/TransactionRisk";
import KYCVerification from "./pages/KYCVerification";
import MerchantMonitoring from "./pages/MerchantMonitoring";
import CryptoTracing from "./pages/CryptoTracing";
import AccountSettings from "./pages/AccountSettings";
import PrivacyPolicy from "./pages/PrivacyPolicy";
import TermsOfService from "./pages/TermsOfService";
import Changelog from "./pages/Changelog";
import Auth from "./pages/Auth";
import NotFound from "./pages/NotFound";

const queryClient = new QueryClient();

const App = () => (
  <QueryClientProvider client={queryClient}>
    <TooltipProvider>
      <Toaster />
      <Sonner />
      <BrowserRouter>
        <Routes>
          <Route path="/auth" element={<Auth />} />
          <Route path="/" element={<ProtectedRoute><TransactionRisk /></ProtectedRoute>} />
          <Route path="/kyc" element={<ProtectedRoute><KYCVerification /></ProtectedRoute>} />
          <Route path="/merchants" element={<ProtectedRoute><MerchantMonitoring /></ProtectedRoute>} />
          <Route path="/crypto" element={<ProtectedRoute><CryptoTracing /></ProtectedRoute>} />
          <Route path="/settings/account" element={<ProtectedRoute><AccountSettings /></ProtectedRoute>} />
          <Route path="/settings/privacy" element={<ProtectedRoute><PrivacyPolicy /></ProtectedRoute>} />
          <Route path="/settings/terms" element={<ProtectedRoute><TermsOfService /></ProtectedRoute>} />
          <Route path="/settings/changelog" element={<ProtectedRoute><Changelog /></ProtectedRoute>} />
          <Route path="*" element={<NotFound />} />
        </Routes>
        <Chatbot />
      </BrowserRouter>
    </TooltipProvider>
  </QueryClientProvider>
);

export default App;
