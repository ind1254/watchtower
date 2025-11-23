import { useState } from "react";
import { MainLayout } from "@/components/layout/MainLayout";
import { MetricCard } from "@/components/shared/MetricCard";
import { DataTable } from "@/components/shared/DataTable";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Network, GitBranch, AlertCircle, ArrowUpRight } from "lucide-react";
import { Badge } from "@/components/ui/badge";
import { motion } from "framer-motion";

const mockData = [
  { wallet: "0x742d...3a4f", category: "Exchange", risk: "Low", connections: 234 },
  { wallet: "0x9f31...8b2c", category: "Mixer", risk: "High", connections: 89 },
  { wallet: "0x1e45...6d9a", category: "Private Wallet", risk: "Medium", connections: 12 },
  { wallet: "0x5c28...4f1b", category: "DeFi Protocol", risk: "Low", connections: 567 },
  { wallet: "0xa893...2e7d", category: "Suspicious", risk: "High", connections: 156 },
];

export default function CryptoTracing() {
  const [isTraced, setIsTraced] = useState(false);
  const [walletAddress, setWalletAddress] = useState("");

  const getRiskBadge = (risk: string) => {
    if (risk === "High") return <Badge className="bg-destructive text-destructive-foreground">High Risk</Badge>;
    if (risk === "Medium") return <Badge className="bg-warning text-warning-foreground">Medium Risk</Badge>;
    return <Badge className="bg-success text-success-foreground">Low Risk</Badge>;
  };

  const columns = [
    { key: "wallet", label: "Wallet Address" },
    { key: "category", label: "Category" },
    { key: "connections", label: "Connections" },
    {
      key: "risk",
      label: "Risk Level",
      render: (value: string) => getRiskBadge(value),
    },
  ];

  return (
    <MainLayout title="Crypto Tracing">
      <div className="space-y-6">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
        >
          <h3 className="text-2xl font-bold text-foreground mb-2">
            Trace Blockchain Wallets
          </h3>
          <p className="text-muted-foreground">
            Analyze cryptocurrency wallets and their transaction networks for risk assessment
          </p>
        </motion.div>

        <div className="bg-card p-6 rounded-lg shadow-sm border border-border">
          <div className="flex gap-3">
            <Input
              placeholder="Enter wallet address (e.g., 0x742d35Cc6634C0532925a3b844Bc9e7595f3a4f)"
              value={walletAddress}
              onChange={(e) => setWalletAddress(e.target.value)}
              className="flex-1"
            />
            <Button
              size="lg"
              onClick={() => setIsTraced(true)}
              disabled={!walletAddress}
            >
              <Network className="w-5 h-5 mr-2" />
              Trace Wallet
            </Button>
          </div>
        </div>

        {isTraced && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="space-y-6"
          >
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
              <MetricCard
                title="Mixers Linked"
                value="3"
                icon={AlertCircle}
                variant="destructive"
                trend="High anonymity risk"
              />
              <MetricCard
                title="Inbound Transfers"
                value="1,247"
                icon={ArrowUpRight}
                trend="From 342 unique wallets"
              />
              <MetricCard
                title="Outbound Transfers"
                value="892"
                icon={GitBranch}
                trend="To 218 unique wallets"
              />
              <MetricCard
                title="Chain Depth"
                value="8 Hops"
                icon={Network}
                variant="warning"
                trend="Complex routing detected"
              />
            </div>

            <div className="bg-card p-6 rounded-lg shadow-sm border border-border">
              <h4 className="text-lg font-semibold mb-4">Network Graph Visualization</h4>
              <div className="h-64 bg-muted rounded-lg flex items-center justify-center border-2 border-dashed border-border">
                <div className="text-center">
                  <Network className="w-12 h-12 text-muted-foreground mx-auto mb-2" />
                  <p className="text-muted-foreground">
                    Interactive network graph would be displayed here
                  </p>
                  <p className="text-sm text-muted-foreground mt-1">
                    Showing wallet-to-wallet transaction flows
                  </p>
                </div>
              </div>
            </div>

            <DataTable
              title="Connected Counterparties"
              columns={columns}
              data={mockData}
            />

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              <div className="bg-card p-6 rounded-lg shadow-sm border border-border">
                <h4 className="text-lg font-semibold mb-4">Risk Indicators</h4>
                <div className="space-y-3">
                  {[
                    { indicator: "Mixer Usage", severity: "High", description: "3 known mixers detected" },
                    { indicator: "Rapid Transfers", severity: "Medium", description: "Unusual velocity pattern" },
                    { indicator: "New Address", severity: "Low", description: "Created 15 days ago" },
                    { indicator: "Exchange Deposits", severity: "Low", description: "Regular CEX activity" },
                  ].map((item, i) => (
                    <div key={i} className="p-3 bg-muted rounded-lg">
                      <div className="flex justify-between items-start mb-1">
                        <span className="font-medium">{item.indicator}</span>
                        <Badge
                          className={
                            item.severity === "High"
                              ? "bg-destructive text-destructive-foreground"
                              : item.severity === "Medium"
                              ? "bg-warning text-warning-foreground"
                              : "bg-success text-success-foreground"
                          }
                        >
                          {item.severity}
                        </Badge>
                      </div>
                      <p className="text-sm text-muted-foreground">{item.description}</p>
                    </div>
                  ))}
                </div>
              </div>

              <div className="bg-card p-6 rounded-lg shadow-sm border border-border">
                <h4 className="text-lg font-semibold mb-4">Transaction Timeline</h4>
                <div className="space-y-3">
                  {[
                    { time: "2 hours ago", type: "Outbound", amount: "2.45 ETH", to: "Mixer" },
                    { time: "5 hours ago", type: "Inbound", amount: "5.00 ETH", to: "Exchange" },
                    { time: "1 day ago", type: "Outbound", amount: "1.23 ETH", to: "Private Wallet" },
                    { time: "2 days ago", type: "Inbound", amount: "3.67 ETH", to: "DeFi Protocol" },
                  ].map((item, i) => (
                    <div key={i} className="flex items-center gap-3 p-3 bg-muted rounded-lg">
                      <div className="flex-1">
                        <div className="flex justify-between items-center mb-1">
                          <span className="font-medium text-sm">{item.type}</span>
                          <span className="text-sm text-muted-foreground">{item.time}</span>
                        </div>
                        <div className="flex justify-between items-center">
                          <span className="text-xs text-muted-foreground">{item.to}</span>
                          <span className="text-sm font-semibold">{item.amount}</span>
                        </div>
                      </div>
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
