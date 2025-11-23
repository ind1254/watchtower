import { MainLayout } from "@/components/layout/MainLayout";
import { Breadcrumb } from "@/components/shared/Breadcrumb";
import { Card } from "@/components/ui/card";
import { Separator } from "@/components/ui/separator";
import { Link } from "react-router-dom";
import { motion } from "framer-motion";
import {
  Accordion,
  AccordionContent,
  AccordionItem,
  AccordionTrigger,
} from "@/components/ui/accordion";

export default function PrivacyPolicy() {
  return (
    <MainLayout title="Privacy Policy">
      <div className="space-y-6">
        <Breadcrumb items={[{ label: "Settings", href: "/settings/account" }, { label: "Privacy Policy" }]} />

        <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }}>
          <Card className="p-8">
            <div className="max-w-4xl mx-auto">
              <div className="mb-8">
                <h1 className="text-4xl font-bold text-foreground mb-2">Privacy Policy</h1>
                <p className="text-muted-foreground">Effective Date: November 12, 2025</p>
                <p className="text-foreground mt-4 font-medium">
                  At Watchtower.ai, your privacy is a responsibility, not an afterthought.
                </p>
                <p className="text-muted-foreground mt-2">
                  This Privacy Policy explains how we handle information when you use our web app and its AI-powered fraud and AML tools ("Services").
                </p>
                <p className="text-muted-foreground mt-2">
                  Using Watchtower means you consent to this Policy. If you disagree, please stop using the Services.
                </p>
              </div>

              <Separator className="my-8" />

              <Accordion type="single" collapsible className="space-y-4">
                <AccordionItem value="purpose">
                  <AccordionTrigger className="text-xl font-semibold">
                    1. Purpose
                  </AccordionTrigger>
                  <AccordionContent className="text-muted-foreground leading-relaxed">
                    <p>
                      Watchtower is a research and educational platform that demonstrates how artificial intelligence can identify financial irregularities. We collect minimal information only to operate the platform, improve functionality, and protect security.
                    </p>
                  </AccordionContent>
                </AccordionItem>

                <AccordionItem value="information-collected">
                  <AccordionTrigger className="text-xl font-semibold">
                    2. Information We Collect
                  </AccordionTrigger>
                  <AccordionContent className="text-muted-foreground leading-relaxed">
                    <ul className="list-disc pl-6 space-y-2">
                      <li><strong>Account Data</strong> – Name, email, and encrypted password when you sign up.</li>
                      <li><strong>Uploaded Data</strong> – Transaction files or sample data you provide for scoring.</li>
                      <li><strong>Usage Data</strong> – Browser type, page activity, and feature interactions, collected anonymously for performance analytics.</li>
                      <li><strong>Chat Interactions</strong> – Questions or prompts sent to the AI Copilot; these are logged for quality control but never sold or shared.</li>
                    </ul>
                    <p className="mt-4">
                      We do not collect or store payment data—Watchtower is entirely free to use.
                    </p>
                  </AccordionContent>
                </AccordionItem>

                <AccordionItem value="how-we-use">
                  <AccordionTrigger className="text-xl font-semibold">
                    3. How We Use Information
                  </AccordionTrigger>
                  <AccordionContent className="text-muted-foreground leading-relaxed">
                    <ul className="list-disc pl-6 space-y-2">
                      <li>To deliver accurate risk scoring and analysis results;</li>
                      <li>To improve algorithms through aggregated, anonymized data;</li>
                      <li>To troubleshoot bugs and ensure site reliability;</li>
                      <li>To communicate important product or security updates.</li>
                    </ul>
                    <p className="mt-4">
                      We do not use data for advertising or resale.
                    </p>
                  </AccordionContent>
                </AccordionItem>

                <AccordionItem value="ai-model">
                  <AccordionTrigger className="text-xl font-semibold">
                    4. AI Model Usage
                  </AccordionTrigger>
                  <AccordionContent className="text-muted-foreground leading-relaxed">
                    <ul className="list-disc pl-6 space-y-2">
                      <li>Uploaded or chat data may pass through third-party AI providers (e.g., OpenAI, Anthropic) to generate results.</li>
                      <li>Data is processed securely, may be briefly cached for inference, and is not used to train external models.</li>
                      <li>You can request deletion of your content at <strong>privacy@watchtower.ai</strong>.</li>
                    </ul>
                  </AccordionContent>
                </AccordionItem>

                <AccordionItem value="storage-security">
                  <AccordionTrigger className="text-xl font-semibold">
                    5. Storage & Security
                  </AccordionTrigger>
                  <AccordionContent className="text-muted-foreground leading-relaxed">
                    <ul className="list-disc pl-6 space-y-2">
                      <li>Encrypted database storage (Supabase).</li>
                      <li>HTTPS/TLS encryption for all connections.</li>
                      <li>Strict internal access control and periodic audits.</li>
                      <li>We maintain backups but automatically purge inactive accounts and files after 60 days.</li>
                    </ul>
                  </AccordionContent>
                </AccordionItem>

                <AccordionItem value="your-choices">
                  <AccordionTrigger className="text-xl font-semibold">
                    6. Your Choices
                  </AccordionTrigger>
                  <AccordionContent className="text-muted-foreground leading-relaxed">
                    <p className="mb-4">You can:</p>
                    <ul className="list-disc pl-6 space-y-2">
                      <li>Update or delete your account;</li>
                      <li>Request a copy of your stored data;</li>
                      <li>Ask for complete deletion of uploaded datasets.</li>
                    </ul>
                    <p className="mt-4">
                      All requests go to <strong>privacy@watchtower.ai</strong>.
                    </p>
                  </AccordionContent>
                </AccordionItem>

                <AccordionItem value="cookies">
                  <AccordionTrigger className="text-xl font-semibold">
                    7. Cookies
                  </AccordionTrigger>
                  <AccordionContent className="text-muted-foreground leading-relaxed">
                    <p>
                      Only essential cookies are used to remember sessions and dark-mode preferences. We do not use tracking or advertising cookies.
                    </p>
                  </AccordionContent>
                </AccordionItem>

                <AccordionItem value="children">
                  <AccordionTrigger className="text-xl font-semibold">
                    8. Children's Privacy
                  </AccordionTrigger>
                  <AccordionContent className="text-muted-foreground leading-relaxed">
                    <p>
                      Watchtower is not designed for users under 18. We do not knowingly collect data from minors.
                    </p>
                  </AccordionContent>
                </AccordionItem>

                <AccordionItem value="updates">
                  <AccordionTrigger className="text-xl font-semibold">
                    9. Updates
                  </AccordionTrigger>
                  <AccordionContent className="text-muted-foreground leading-relaxed">
                    <p>
                      We may revise this Policy as we evolve. Major changes will appear in your dashboard and on this page with a new "Effective Date."
                    </p>
                  </AccordionContent>
                </AccordionItem>

                <AccordionItem value="contact">
                  <AccordionTrigger className="text-xl font-semibold">
                    10. Contact
                  </AccordionTrigger>
                  <AccordionContent className="text-muted-foreground leading-relaxed">
                    <div className="bg-muted p-4 rounded-lg">
                      <p className="font-medium text-foreground">Watchtower Technologies Inc.</p>
                      <p className="text-sm mt-1">Toronto, Ontario, Canada</p>
                      <p className="text-sm mt-2">Email: <strong>privacy@watchtower.ai</strong></p>
                    </div>
                  </AccordionContent>
                </AccordionItem>
              </Accordion>

              <Separator className="my-8" />

              <div className="flex items-center justify-between text-sm">
                <div className="flex gap-4">
                  <Link to="/settings/terms" className="text-primary hover:underline">
                    Terms of Service
                  </Link>
                  <Link to="/settings/changelog" className="text-primary hover:underline">
                    Changelog
                  </Link>
                  <Link to="/" className="text-primary hover:underline">
                    Back to Dashboard
                  </Link>
                </div>
              </div>
            </div>
          </Card>
        </motion.div>
      </div>
    </MainLayout>
  );
}
