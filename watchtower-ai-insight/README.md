# Watchtower - AML Intelligence Platform

AI-driven AML (Anti-Money Laundering) & Fraud Intelligence platform for transaction risk scoring, identity verification, merchant monitoring, and crypto tracing.

## Tech Stack

- **Vite** - Build tool and dev server
- **TypeScript** - Type-safe JavaScript
- **React** - UI framework
- **shadcn-ui** - UI component library
- **Tailwind CSS** - Styling
- **Supabase** - Authentication and backend services
- **React Router** - Client-side routing
- **Framer Motion** - Animations

## Getting Started

### Prerequisites

- Node.js & npm installed - [install with nvm](https://github.com/nvm-sh/nvm#installing-and-updating)

### Installation

1. Clone the repository:
   ```sh
   git clone <YOUR_GIT_URL>
   cd watchtower-ai-insight
   ```

2. Install dependencies:
   ```sh
   npm install
   ```

3. Start the development server:
   ```sh
   npm run dev
   ```

The application will be available at `http://localhost:8080`

## Project Structure

```
src/
├── components/        # Reusable UI components
│   ├── layout/       # Layout components (Navbar, Sidebar, MainLayout)
│   ├── shared/       # Shared components (DataTable, MetricCard, UploadBox)
│   └── ui/           # shadcn-ui components
├── pages/            # Page components
├── hooks/            # Custom React hooks
├── integrations/     # Third-party integrations (Supabase)
└── lib/              # Utility functions
```

## Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build
- `npm run lint` - Run ESLint

## Features

- **Transaction Risk Scoring** - Upload CSV files to analyze transaction risk
- **KYC Verification** - Identity verification workflows
- **Merchant Monitoring** - Track and monitor merchant activities
- **Crypto Tracing** - Trace cryptocurrency transactions
- **Authentication** - User authentication via Supabase

## Development

This project uses:
- **Vite** for fast HMR (Hot Module Replacement)
- **TypeScript** for type safety
- **ESLint** for code quality

## License

[Add your license here]
