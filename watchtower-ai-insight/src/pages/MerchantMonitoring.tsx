import { useState } from "react";
import { MainLayout } from "@/components/layout/MainLayout";
import { MetricCard } from "@/components/shared/MetricCard";
import { DataTable } from "@/components/shared/DataTable";
import { UploadBox } from "@/components/shared/UploadBox";
import { Button } from "@/components/ui/button";
import { Store, DollarSign, AlertTriangle, TrendingDown } from "lucide-react";
import { Badge } from "@/components/ui/badge";
import { motion } from "framer-motion";

const mockData = [
  { id: "M1001", name: "TechStore Plus", volume: "$125,000", chargebacks: 23, disputes: 8, rate: "1.84%" },
  { id: "M1002", name: "Fashion Hub", volume: "$89,000", chargebacks: 3, disputes: 1, rate: "0.34%" },
  { id: "M1003", name: "Digital Goods Co", volume: "$234,000", chargebacks: 45, disputes: 18, rate: "1.92%" },
  { id: "M1004", name: "Home Essentials", volume: "$67,000", chargebacks: 2, disputes: 0, rate: "0.30%" },
  { id: "M1005", name: "Quick Electronics", volume: "$156,000", chargebacks: 34, disputes: 12, rate: "2.18%" },
];

export default function MerchantMonitoring() {
  const [isAnalyzed, setIsAnalyzed] = useState(false);

  const getRiskBadge = (rate: string) => {
    const value = parseFloat(rate);
    if (value >= 1.5) return <Badge className="bg-destructive text-destructive-foreground">High Risk</Badge>;
    if (value >= 0.75) return <Badge className="bg-warning text-warning-foreground">Medium Risk</Badge>;
    return <Badge className="bg-success text-success-foreground">Low Risk</Badge>;
  };

  const columns = [
    { key: "id", label: "Merchant ID" },
    { key: "name", label: "Merchant Name" },
    { key: "volume", label: "Monthly Volume" },
    { key: "chargebacks", label: "Chargebacks" },
    { key: "disputes", label: "Disputes" },
    {
      key: "rate",
      label: "Chargeback Rate",
      render: (value: string) => (
        <div className="flex items-center gap-2">
          <span className="font-semibold">{value}</span>
          {getRiskBadge(value)}
        </div>
      ),
    },
  ];

  return (
    <MainLayout title="Merchant Monitoring">
      <div className="space-y-6">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
        >
          <h3 className="text-2xl font-bold text-foreground mb-2">
            Monitor Merchant Performance
          </h3>
          <p className="text-muted-foreground">
            Track payment processors, chargebacks, and merchant risk profiles
          </p>
        </motion.div>

        <UploadBox
          title="Upload Merchant Data"
          description="Drag and drop your CSV file with merchant transaction data"
          acceptedFormats=".csv"
        />

        <div className="flex justify-center">
          <Button
            size="lg"
            onClick={() => setIsAnalyzed(true)}
            className="px-8"
          >
            <Store className="w-5 h-5 mr-2" />
            Analyze Merchants
          </Button>
        </div>

        {isAnalyzed && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="space-y-6"
          >
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
              <MetricCard
                title="Total Merchants"
                value="342"
                icon={Store}
                trend="Active merchants"
              />
              <MetricCard
                title="Monthly Volume"
                value="$8.7M"
                icon={DollarSign}
                variant="success"
                trend="↑ 12% from last month"
              />
              <MetricCard
                title="Avg Chargeback Rate"
                value="1.24%"
                icon={TrendingDown}
                variant="warning"
                trend="Industry avg: 0.9%"
              />
              <MetricCard
                title="High-Risk Merchants"
                value="28"
                icon={AlertTriangle}
                variant="destructive"
                trend="8.2% of total"
              />
            </div>

            <DataTable
              title="Merchant Risk Leaderboard"
              columns={columns}
              data={mockData}
            />

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              <div className="bg-card p-6 rounded-lg shadow-sm border border-border">
                <h4 className="text-lg font-semibold mb-4">Chargeback Trend (Last 6 Months)</h4>
                <div className="space-y-3">
                  {[
                    { month: "Jan", count: 45 },
                    { month: "Feb", count: 52 },
                    { month: "Mar", count: 38 },
                    { month: "Apr", count: 61 },
                    { month: "May", count: 48 },
                    { month: "Jun", count: 71 },
                  ].map((item, i) => (
                    <div key={i} className="flex items-center gap-3">
                      <span className="text-sm font-medium w-12">{item.month}</span>
                      <div className="flex-1 h-8 bg-muted rounded overflow-hidden">
                        <div
                          className="h-full bg-destructive flex items-center justify-end px-2"
                          style={{ width: `${(item.count / 71) * 100}%` }}
                        >
                          <span className="text-xs text-destructive-foreground font-medium">{item.count}</span>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              <div className="bg-card p-6 rounded-lg shadow-sm border border-border">
                <h4 className="text-lg font-semibold mb-4">Top Risk Categories</h4>
                <div className="space-y-3">
                  {[
                    { category: "Electronics", risk: "High", merchants: 45 },
                    { category: "Digital Services", risk: "High", merchants: 38 },
                    { category: "Fashion", risk: "Medium", merchants: 67 },
                    { category: "Home Goods", risk: "Low", merchants: 122 },
                  ].map((item, i) => (
                    <div key={i} className="flex justify-between items-center p-3 bg-muted rounded-lg">
                      <div>
                        <span className="font-medium">{item.category}</span>
                        <span className="text-sm text-muted-foreground ml-2">({item.merchants} merchants)</span>
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
            </div>
          </motion.div>
        )}
      </div>
    </MainLayout>
  );
}
