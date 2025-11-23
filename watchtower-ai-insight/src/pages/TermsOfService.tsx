import { MainLayout } from "@/components/layout/MainLayout";
import { Breadcrumb } from "@/components/shared/Breadcrumb";
import { Card } from "@/components/ui/card";
import { Separator } from "@/components/ui/separator";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Link } from "react-router-dom";
import { motion } from "framer-motion";

export default function TermsOfService() {
  const sections = [
    { id: "service-overview", title: "Service Overview" },
    { id: "eligibility", title: "Eligibility" },
    { id: "account-responsibilities", title: "Account Responsibilities" },
    { id: "acceptable-use", title: "Acceptable Use" },
    { id: "data-ownership", title: "Data Ownership" },
    { id: "intellectual-property", title: "Intellectual Property" },
    { id: "availability", title: "Availability" },
    { id: "limitation", title: "Limitation of Liability" },
    { id: "termination", title: "Termination" },
    { id: "changes", title: "Changes to These Terms" },
    { id: "governing-law", title: "Governing Law" },
    { id: "contact", title: "Contact" },
  ];

  return (
    <MainLayout title="Terms of Service">
      <div className="space-y-6">
        <Breadcrumb items={[{ label: "Settings", href: "/settings/account" }, { label: "Terms of Service" }]} />

        <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
          <motion.div 
            initial={{ opacity: 0, x: -20 }} 
            animate={{ opacity: 1, x: 0 }}
            className="lg:col-span-1"
          >
            <Card className="p-4 sticky top-4">
              <h3 className="font-semibold text-foreground mb-4">Table of Contents</h3>
              <ScrollArea className="h-[calc(100vh-200px)]">
                <nav className="space-y-2">
                  {sections.map((section) => (
                    <a
                      key={section.id}
                      href={`#${section.id}`}
                      className="block text-sm text-muted-foreground hover:text-primary transition-colors"
                    >
                      {section.title}
                    </a>
                  ))}
                </nav>
              </ScrollArea>
            </Card>
          </motion.div>

          <motion.div 
            initial={{ opacity: 0, y: 20 }} 
            animate={{ opacity: 1, y: 0 }}
            className="lg:col-span-3"
          >
            <Card className="p-8">
              <div className="max-w-3xl">
                <div className="mb-8">
                  <h1 className="text-4xl font-bold text-foreground mb-2">Terms of Service</h1>
                  <p className="text-muted-foreground">Effective Date: November 12, 2025</p>
                  <p className="text-foreground mt-4">
                    Welcome to Watchtower.ai ("Watchtower," "we," "us").
                    These Terms explain how you may use our free platform that provides AI-powered fraud detection, AML analytics, and educational insight ("Services").
                  </p>
                  <p className="text-muted-foreground mt-2">
                    By using Watchtower, you agree to these Terms and our Privacy Policy.
                  </p>
                </div>

                <Separator className="my-8" />

                <div className="space-y-8 text-muted-foreground leading-relaxed">
                  <section id="service-overview">
                    <h2 className="text-2xl font-semibold text-foreground mb-4">1. Service Overview</h2>
                    <p>
                      Watchtower is a public demonstration tool that applies machine learning to sample or user-provided transaction data. The results are informational only and do not constitute financial, legal, or compliance advice.
                    </p>
                  </section>

                  <section id="eligibility">
                    <h2 className="text-2xl font-semibold text-foreground mb-4">2. Eligibility</h2>
                    <p>
                      You must be at least 18 years old and legally permitted to use data-analysis tools in your region.
                    </p>
                  </section>

                  <section id="account-responsibilities">
                    <h2 className="text-2xl font-semibold text-foreground mb-4">3. Account Responsibilities</h2>
                    <p>
                      You are responsible for keeping your login credentials secure and for any actions under your account.
                      Report unauthorized activity to <strong>security@watchtower.ai</strong> immediately.
                    </p>
                  </section>

                  <section id="acceptable-use">
                    <h2 className="text-2xl font-semibold text-foreground mb-4">4. Acceptable Use</h2>
                    <p className="mb-4">When using Watchtower, you agree not to:</p>
                    <ul className="list-disc pl-6 space-y-2">
                      <li>Upload sensitive, confidential, or personal banking data;</li>
                      <li>Submit illegal content or simulate real criminal activity;</li>
                      <li>Attempt to exploit, copy, or reverse-engineer Watchtower's models or code;</li>
                      <li>Disrupt or overload system resources.</li>
                    </ul>
                    <p className="mt-4">
                      We may restrict or disable accounts violating these guidelines.
                    </p>
                  </section>

                  <section id="data-ownership">
                    <h2 className="text-2xl font-semibold text-foreground mb-4">5. Data Ownership</h2>
                    <p className="mb-4">
                      You own the files and content you upload.
                      By submitting data, you grant Watchtower a limited license to process it only to run analyses and display results.
                      We do not use or share your raw data beyond these purposes.
                    </p>
                  </section>

                  <section id="intellectual-property">
                    <h2 className="text-2xl font-semibold text-foreground mb-4">6. Intellectual Property</h2>
                    <p>
                      All code, interfaces, and design elements belong to Watchtower Technologies Inc.
                      You may not reproduce or redistribute any portion of the platform without written consent.
                    </p>
                  </section>

                  <section id="availability">
                    <h2 className="text-2xl font-semibold text-foreground mb-4">7. Availability</h2>
                    <p>
                      This is a free educational service offered "as is."
                      We make no guarantees of uptime, continuity, or model accuracy. The platform may change or go offline at any time without notice.
                    </p>
                  </section>

                  <section id="limitation">
                    <h2 className="text-2xl font-semibold text-foreground mb-4">8. Limitation of Liability</h2>
                    <p>
                      Watchtower is not liable for losses, damages, or decisions made based on platform outputs.
                      Our service should supplement—not replace—professional risk assessment or regulatory processes.
                    </p>
                  </section>

                  <section id="termination">
                    <h2 className="text-2xl font-semibold text-foreground mb-4">9. Termination</h2>
                    <p className="mb-4">
                      You may delete your account at any time in Settings. We may suspend accounts that violate our policies or security rules.
                    </p>
                  </section>

                  <section id="changes">
                    <h2 className="text-2xl font-semibold text-foreground mb-4">10. Changes to These Terms</h2>
                    <p>
                      We may update these Terms periodically. New versions will appear on this page with the effective date clearly listed.
                    </p>
                  </section>

                  <section id="governing-law">
                    <h2 className="text-2xl font-semibold text-foreground mb-4">11. Governing Law</h2>
                    <p>
                      These Terms are governed by the laws of Ontario, Canada, and any applicable federal statutes.
                      Disputes shall be resolved in the courts of Toronto, Ontario.
                    </p>
                  </section>

                  <section id="contact">
                    <h2 className="text-2xl font-semibold text-foreground mb-4">12. Contact</h2>
                    <div className="bg-muted p-4 rounded-lg">
                      <p className="font-medium text-foreground">Watchtower Technologies Inc.</p>
                      <p className="text-sm mt-1">Toronto, Ontario, Canada</p>
                      <p className="text-sm mt-2">Email: <strong>team@watchtower.ai</strong></p>
                    </div>
                  </section>
                </div>

                <Separator className="my-8" />

                <div className="flex items-center justify-between text-sm">
                  <div className="flex gap-4">
                    <Link to="/settings/privacy" className="text-primary hover:underline">
                      Privacy Policy
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
      </div>
    </MainLayout>
  );
}
