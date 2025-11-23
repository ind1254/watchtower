import { useState } from "react";
import { MainLayout } from "@/components/layout/MainLayout";
import { MetricCard } from "@/components/shared/MetricCard";
import { DataTable } from "@/components/shared/DataTable";
import { UploadBox } from "@/components/shared/UploadBox";
import { Button } from "@/components/ui/button";
import { UserCheck, UserX, Users, AlertCircle } from "lucide-react";
import { Badge } from "@/components/ui/badge";
import { motion } from "framer-motion";

const mockData = [
  { id: "U1001", name: "John Smith", country: "USA", signupDate: "2024-01-15", status: "Verified" },
  { id: "U1002", name: "Maria Garcia", country: "Mexico", signupDate: "2024-01-18", status: "Flagged" },
  { id: "U1003", name: "Wei Chen", country: "China", signupDate: "2024-01-20", status: "Verified" },
  { id: "U1004", name: "Ahmed Hassan", country: "Egypt", signupDate: "2024-01-22", status: "Duplicate" },
  { id: "U1005", name: "Sarah Johnson", country: "UK", signupDate: "2024-01-23", status: "Verified" },
];

export default function KYCVerification() {
  const [isChecked, setIsChecked] = useState(false);

  const getStatusBadge = (status: string) => {
    if (status === "Verified") return <Badge className="bg-success text-success-foreground">Verified</Badge>;
    if (status === "Flagged") return <Badge className="bg-destructive text-destructive-foreground">Flagged</Badge>;
    return <Badge className="bg-warning text-warning-foreground">Duplicate</Badge>;
  };

  const columns = [
    { key: "id", label: "User ID" },
    { key: "name", label: "Name" },
    { key: "country", label: "Country" },
    { key: "signupDate", label: "Signup Date" },
    {
      key: "status",
      label: "Verification Status",
      render: (value: string) => getStatusBadge(value),
    },
  ];

  return (
    <MainLayout title="Identity & KYC Verification">
      <div className="space-y-6">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
        >
          <h3 className="text-2xl font-bold text-foreground mb-2">
            Verify User Identities
          </h3>
          <p className="text-muted-foreground">
            Upload user data to detect fake accounts, duplicates, and compliance issues
          </p>
        </motion.div>

        <UploadBox
          title="Upload User Data"
          description="Drag and drop your CSV file with user information"
          acceptedFormats=".csv"
        />

        <div className="flex justify-center">
          <Button
            size="lg"
            onClick={() => setIsChecked(true)}
            className="px-8"
          >
            <UserCheck className="w-5 h-5 mr-2" />
            Run KYC Check
          </Button>
        </div>

        {isChecked && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="space-y-6"
          >
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
              <MetricCard
                title="Verified Users"
                value="847"
                icon={UserCheck}
                variant="success"
                trend="84.7% pass rate"
              />
              <MetricCard
                title="Flagged IDs"
                value="89"
                icon={UserX}
                variant="destructive"
                trend="8.9% require review"
              />
              <MetricCard
                title="Duplicate Devices"
                value="64"
                icon={AlertCircle}
                variant="warning"
                trend="6.4% potential fraud"
              />
              <MetricCard
                title="Total Users"
                value="1,000"
                icon={Users}
                trend="Processed in 2.3s"
              />
            </div>

            <DataTable
              title="User Verification Results"
              columns={columns}
              data={mockData}
            />

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              <div className="bg-card p-6 rounded-lg shadow-sm border border-border">
                <h4 className="text-lg font-semibold mb-4">Geographic Distribution</h4>
                <div className="space-y-3">
                  {[
                    { country: "United States", users: 342, risk: "Low" },
                    { country: "United Kingdom", users: 156, risk: "Low" },
                    { country: "Nigeria", users: 89, risk: "High" },
                    { country: "India", users: 234, risk: "Medium" },
                  ].map((item, i) => (
                    <div key={i} className="flex justify-between items-center p-3 bg-muted rounded-lg">
                      <div>
                        <span className="font-medium">{item.country}</span>
                        <span className="text-sm text-muted-foreground ml-2">({item.users} users)</span>
                      </div>
                      <Badge
                        className={
                          item.risk === "High"
                            ? "bg-destructive text-destructive-foreground"
                            : item.risk === "Medium"
                            ? "bg-warning text-warning-foreground"
                            : "bg-success text-success-foreground"
                        }
                      >
                        {item.risk}
                      </Badge>
                    </div>
                  ))}
                </div>
              </div>

              <div className="bg-card p-6 rounded-lg shadow-sm border border-border">
                <h4 className="text-lg font-semibold mb-4">Verification Status Breakdown</h4>
                <div className="space-y-4">
                  <div>
                    <div className="flex justify-between text-sm mb-1">
                      <span>Verified</span>
                      <span className="font-semibold">84.7%</span>
                    </div>
                    <div className="w-full h-3 bg-muted rounded-full overflow-hidden">
                      <div className="h-full bg-success" style={{ width: "84.7%" }} />
                    </div>
                  </div>
                  <div>
                    <div className="flex justify-between text-sm mb-1">
                      <span>Flagged</span>
                      <span className="font-semibold">8.9%</span>
                    </div>
                    <div className="w-full h-3 bg-muted rounded-full overflow-hidden">
                      <div className="h-full bg-destructive" style={{ width: "8.9%" }} />
                    </div>
                  </div>
                  <div>
                    <div className="flex justify-between text-sm mb-1">
                      <span>Duplicate</span>
                      <span className="font-semibold">6.4%</span>
                    </div>
                    <div className="w-full h-3 bg-muted rounded-full overflow-hidden">
                      <div className="h-full bg-warning" style={{ width: "6.4%" }} />
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </motion.div>
        )}
      </div>
    </MainLayout>
  );
}
