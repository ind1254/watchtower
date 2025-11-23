import { NavLink } from "@/components/NavLink";
import { Shield, FileCheck, Store, Network } from "lucide-react";
import { motion } from "framer-motion";

const navItems = [
  {
    title: "Transaction Risk Scoring",
    href: "/",
    icon: Shield,
  },
  {
    title: "Identity & KYC",
    href: "/kyc",
    icon: FileCheck,
  },
  {
    title: "Merchant Monitoring",
    href: "/merchants",
    icon: Store,
  },
  {
    title: "Crypto Tracing",
    href: "/crypto",
    icon: Network,
  },
];

export const Sidebar = () => {
  return (
    <aside className="w-64 bg-sidebar border-r border-sidebar-border flex flex-col">
      <div className="p-6 border-b border-sidebar-border">
        <motion.div
          initial={{ opacity: 0, y: -10 }}
          animate={{ opacity: 1, y: 0 }}
          className="flex items-center gap-3"
        >
          <div className="w-10 h-10 bg-sidebar-primary rounded-lg flex items-center justify-center">
            <Shield className="w-6 h-6 text-sidebar-primary-foreground" />
          </div>
          <div>
            <h1 className="text-xl font-bold text-sidebar-foreground">Watchtower</h1>
            <p className="text-xs text-sidebar-foreground/70">AML Intelligence</p>
          </div>
        </motion.div>
      </div>

      <nav className="flex-1 p-4 space-y-1">
        {navItems.map((item, index) => (
          <motion.div
            key={item.href}
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: index * 0.1 }}
          >
            <NavLink
              to={item.href}
              end
              className="flex items-center gap-3 px-4 py-3 rounded-lg text-sidebar-foreground/80 hover:bg-sidebar-accent hover:text-sidebar-accent-foreground transition-all duration-200"
              activeClassName="bg-sidebar-accent text-sidebar-accent-foreground font-medium"
            >
              <item.icon className="w-5 h-5" />
              <span className="text-sm">{item.title}</span>
            </NavLink>
          </motion.div>
        ))}
      </nav>

      <div className="p-4 border-t border-sidebar-border">
        <div className="px-4 py-2 bg-sidebar-accent/50 rounded-lg">
          <p className="text-xs text-sidebar-foreground/70">Version 1.0</p>
          <p className="text-xs text-sidebar-foreground/50">© 2025 Watchtower</p>
        </div>
      </div>
    </aside>
  );
};
