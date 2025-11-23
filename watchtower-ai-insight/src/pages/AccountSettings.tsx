import { useState } from "react";
import { MainLayout } from "@/components/layout/MainLayout";
import { Breadcrumb } from "@/components/shared/Breadcrumb";
import { Card } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Button } from "@/components/ui/button";
import { Switch } from "@/components/ui/switch";
import { Separator } from "@/components/ui/separator";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog";
import { User, Lock, Settings as SettingsIcon, Database, CreditCard } from "lucide-react";
import { motion } from "framer-motion";
import { toast } from "sonner";

export default function AccountSettings() {
  const [darkMode, setDarkMode] = useState(false);
  const [notifications, setNotifications] = useState(true);
  const [explainability, setExplainability] = useState(false);

  const handleSaveChanges = () => {
    toast.success("Settings saved successfully");
  };

  return (
    <MainLayout title="Account Settings">
      <div className="space-y-6">
        <Breadcrumb items={[{ label: "Settings", href: "/settings/account" }, { label: "Account" }]} />

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Profile Information */}
          <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.1 }}>
            <Card className="p-6">
              <div className="flex items-center gap-3 mb-6">
                <div className="w-10 h-10 rounded-full bg-primary/10 flex items-center justify-center">
                  <User className="w-5 h-5 text-primary" />
                </div>
                <h2 className="text-xl font-semibold text-foreground">Profile Information</h2>
              </div>
              
              <div className="space-y-4">
                <div className="space-y-2">
                  <Label htmlFor="name">Full Name</Label>
                  <Input id="name" defaultValue="John Doe" />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="email">Email</Label>
                  <Input id="email" type="email" defaultValue="john@watchtower.ai" />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="organization">Organization</Label>
                  <Input id="organization" defaultValue="Watchtower Inc." />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="role">Role</Label>
                  <Input id="role" defaultValue="Compliance Officer" />
                </div>
              </div>
            </Card>
          </motion.div>

          {/* Password Management */}
          <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.2 }}>
            <Card className="p-6">
              <div className="flex items-center gap-3 mb-6">
                <div className="w-10 h-10 rounded-full bg-primary/10 flex items-center justify-center">
                  <Lock className="w-5 h-5 text-primary" />
                </div>
                <h2 className="text-xl font-semibold text-foreground">Password Management</h2>
              </div>
              
              <p className="text-muted-foreground mb-4">
                Keep your account secure by using a strong password and updating it regularly.
              </p>
              
              <Dialog>
                <DialogTrigger asChild>
                  <Button variant="outline" className="w-full">Change Password</Button>
                </DialogTrigger>
                <DialogContent>
                  <DialogHeader>
                    <DialogTitle>Change Password</DialogTitle>
                    <DialogDescription>
                      Enter your current password and choose a new one.
                    </DialogDescription>
                  </DialogHeader>
                  <div className="space-y-4">
                    <div className="space-y-2">
                      <Label htmlFor="current-password">Current Password</Label>
                      <Input id="current-password" type="password" />
                    </div>
                    <div className="space-y-2">
                      <Label htmlFor="new-password">New Password</Label>
                      <Input id="new-password" type="password" />
                    </div>
                    <div className="space-y-2">
                      <Label htmlFor="confirm-password">Confirm New Password</Label>
                      <Input id="confirm-password" type="password" />
                    </div>
                  </div>
                  <DialogFooter>
                    <Button onClick={() => toast.success("Password updated successfully")}>Update Password</Button>
                  </DialogFooter>
                </DialogContent>
              </Dialog>
            </Card>
          </motion.div>

          {/* Preferences */}
          <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.3 }}>
            <Card className="p-6">
              <div className="flex items-center gap-3 mb-6">
                <div className="w-10 h-10 rounded-full bg-primary/10 flex items-center justify-center">
                  <SettingsIcon className="w-5 h-5 text-primary" />
                </div>
                <h2 className="text-xl font-semibold text-foreground">Preferences</h2>
              </div>
              
              <div className="space-y-6">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="font-medium text-foreground">Dark Mode</p>
                    <p className="text-sm text-muted-foreground">Enable dark theme</p>
                  </div>
                  <Switch checked={darkMode} onCheckedChange={setDarkMode} />
                </div>
                
                <Separator />
                
                <div className="flex items-center justify-between">
                  <div>
                    <p className="font-medium text-foreground">Notifications</p>
                    <p className="text-sm text-muted-foreground">Receive alerts for high-risk transactions</p>
                  </div>
                  <Switch checked={notifications} onCheckedChange={setNotifications} />
                </div>
                
                <Separator />
                
                <div className="flex items-center justify-between">
                  <div>
                    <p className="font-medium text-foreground">Model Explainability</p>
                    <p className="text-sm text-muted-foreground">Advanced mode shows detailed AI reasoning</p>
                  </div>
                  <Switch checked={explainability} onCheckedChange={setExplainability} />
                </div>
              </div>
            </Card>
          </motion.div>

          {/* Data Management */}
          <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.4 }}>
            <Card className="p-6">
              <div className="flex items-center gap-3 mb-6">
                <div className="w-10 h-10 rounded-full bg-primary/10 flex items-center justify-center">
                  <Database className="w-5 h-5 text-primary" />
                </div>
                <h2 className="text-xl font-semibold text-foreground">Data Management</h2>
              </div>
              
              <div className="space-y-4">
                <div>
                  <p className="text-sm text-muted-foreground mb-3">
                    Download all your data or permanently delete your account.
                  </p>
                  <Button variant="outline" className="w-full mb-3" onClick={() => toast.success("Data export initiated")}>
                    Download My Data
                  </Button>
                  <Button variant="destructive" className="w-full" onClick={() => toast.error("Contact support to delete your account")}>
                    Delete Account
                  </Button>
                </div>
              </div>
            </Card>
          </motion.div>

          {/* Billing (Placeholder) */}
          <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.5 }} className="lg:col-span-2">
            <Card className="p-6">
              <div className="flex items-center gap-3 mb-6">
                <div className="w-10 h-10 rounded-full bg-primary/10 flex items-center justify-center">
                  <CreditCard className="w-5 h-5 text-primary" />
                </div>
                <h2 className="text-xl font-semibold text-foreground">Billing & Subscription</h2>
              </div>
              
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <p className="text-sm text-muted-foreground mb-2">Current Plan</p>
                  <p className="text-2xl font-bold text-primary">Professional</p>
                  <p className="text-sm text-muted-foreground mt-1">$99/month</p>
                </div>
                <div>
                  <p className="text-sm text-muted-foreground mb-2">Payment Method</p>
                  <p className="text-lg font-medium text-foreground">•••• •••• •••• 4242</p>
                  <p className="text-sm text-muted-foreground mt-1">Visa expires 12/25</p>
                </div>
              </div>
              
              <Separator className="my-6" />
              
              <div className="flex gap-3">
                <Button variant="outline">Update Payment Method</Button>
                <Button variant="outline">Manage Subscription</Button>
              </div>
            </Card>
          </motion.div>
        </div>

        <div className="flex justify-end">
          <Button size="lg" onClick={handleSaveChanges}>Save Changes</Button>
        </div>
      </div>
    </MainLayout>
  );
}
