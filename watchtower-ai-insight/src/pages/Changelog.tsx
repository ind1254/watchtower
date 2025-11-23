import { useState } from "react";
import { MainLayout } from "@/components/layout/MainLayout";
import { Breadcrumb } from "@/components/shared/Breadcrumb";
import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Tabs, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { motion } from "framer-motion";
import { Sparkles, TrendingUp, Wrench, AlertCircle } from "lucide-react";

interface ChangelogEntry {
  version: string;
  date: string;
  type: "feature" | "enhancement" | "fix";
  changes: string[];
}

const changelogData: ChangelogEntry[] = [
  {
    version: "1.1.1",
    date: "March 2025",
    type: "feature",
    changes: [
      "Added comprehensive Settings menu with Account Management, Privacy Policy, and Terms of Service",
      "Implemented user authentication with email/password login and signup",
      "Introduced AI Copilot Chat for real-time AML and fraud detection queries",
      "Enhanced user profile management with password change functionality",
      "Added dark mode toggle and notification preferences",
      "Integrated billing & subscription management interface"
    ]
  },
  {
    version: "1.1.0",
    date: "February 2025",
    type: "feature",
    changes: [
      "Launched Identity & KYC Verification module with duplicate detection",
      "Introduced Merchant Monitoring dashboard with chargeback tracking",
      "Added geo-heatmap visualization for merchant risk distribution",
      "Implemented device fingerprinting for fraud prevention",
      "Enhanced transaction risk scoring with machine learning models",
      "Added export functionality for compliance reports"
    ]
  },
  {
    version: "1.0.5",
    date: "January 2025",
    type: "enhancement",
    changes: [
      "Improved Crypto Tracing network graph performance",
      "Optimized transaction risk calculation algorithms",
      "Enhanced UI responsiveness across mobile and tablet devices",
      "Reduced page load times by 40% through code optimization",
      "Added keyboard shortcuts for power users",
      "Improved accessibility with WCAG 2.1 AA compliance"
    ]
  },
  {
    version: "1.0.2",
    date: "December 2024",
    type: "fix",
    changes: [
      "Fixed CSV upload parsing errors for international date formats",
      "Resolved issue with risk score color coding in edge cases",
      "Corrected merchant leaderboard sorting algorithm",
      "Fixed chatbot message history scroll behavior",
      "Addressed memory leak in real-time transaction monitoring",
      "Improved error handling for malformed data uploads"
    ]
  },
  {
    version: "1.0.0",
    date: "January 2025",
    type: "feature",
    changes: [
      "Initial release of Watchtower AML Intelligence Platform",
      "Launched Transaction Risk Scoring with anomaly detection",
      "Introduced Crypto Tracing for blockchain wallet analysis",
      "Built responsive fintech-styled UI with Tailwind CSS",
      "Implemented drag-and-drop file upload for CSV data",
      "Created reusable component library for rapid development",
      "Established secure authentication infrastructure"
    ]
  }
];

export default function Changelog() {
  const [filter, setFilter] = useState<"all" | "feature" | "enhancement" | "fix">("all");

  const filteredChangelog = changelogData.filter(
    (entry) => filter === "all" || entry.type === filter
  );

  const getTypeIcon = (type: string) => {
    switch (type) {
      case "feature":
        return <Sparkles className="w-5 h-5" />;
      case "enhancement":
        return <TrendingUp className="w-5 h-5" />;
      case "fix":
        return <Wrench className="w-5 h-5" />;
      default:
        return <AlertCircle className="w-5 h-5" />;
    }
  };

  const getTypeBadge = (type: string) => {
    const variants: Record<string, string> = {
      feature: "bg-primary text-primary-foreground",
      enhancement: "bg-chart-2 text-white",
      fix: "bg-chart-3 text-white"
    };
    return variants[type] || "bg-muted";
  };

  return (
    <MainLayout title="Changelog">
      <div className="space-y-6">
        <Breadcrumb items={[{ label: "Settings", href: "/settings/account" }, { label: "Changelog" }]} />

        <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }}>
          <Card className="p-6">
            <div className="mb-6">
              <h1 className="text-3xl font-bold text-foreground mb-2">Version History</h1>
              <p className="text-muted-foreground">
                Track all updates, new features, enhancements, and bug fixes to Watchtower.
              </p>
            </div>

            <Tabs value={filter} onValueChange={(value) => setFilter(value as any)} className="mb-6">
              <TabsList>
                <TabsTrigger value="all">All Changes</TabsTrigger>
                <TabsTrigger value="feature">New Features</TabsTrigger>
                <TabsTrigger value="enhancement">Enhancements</TabsTrigger>
                <TabsTrigger value="fix">Bug Fixes</TabsTrigger>
              </TabsList>
            </Tabs>

            <div className="space-y-6">
              {filteredChangelog.map((entry, index) => (
                <motion.div
                  key={entry.version}
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: index * 0.1 }}
                  className="border-l-4 border-primary pl-6 pb-6 relative"
                >
                  <div className="absolute -left-3 top-0 w-6 h-6 bg-primary rounded-full flex items-center justify-center">
                    <div className="w-3 h-3 bg-background rounded-full" />
                  </div>

                  <div className="flex items-start justify-between mb-4">
                    <div>
                      <div className="flex items-center gap-3 mb-2">
                        <h3 className="text-xl font-semibold text-foreground">
                          Version {entry.version}
                        </h3>
                        <Badge className={getTypeBadge(entry.type)}>
                          <span className="flex items-center gap-1">
                            {getTypeIcon(entry.type)}
                            {entry.type.charAt(0).toUpperCase() + entry.type.slice(1)}
                          </span>
                        </Badge>
                      </div>
                      <p className="text-sm text-muted-foreground">{entry.date}</p>
                    </div>
                  </div>

                  <ul className="space-y-2">
                    {entry.changes.map((change, changeIndex) => (
                      <li key={changeIndex} className="flex items-start gap-2 text-muted-foreground">
                        <span className="text-primary mt-1">•</span>
                        <span>{change}</span>
                      </li>
                    ))}
                  </ul>
                </motion.div>
              ))}
            </div>
          </Card>
        </motion.div>
      </div>
    </MainLayout>
  );
}
