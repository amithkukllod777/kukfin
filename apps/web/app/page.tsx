import { Activity, BarChart3, BrainCircuit, BriefcaseBusiness, ChevronRight, ShieldCheck } from 'lucide-react';
import Link from 'next/link';

const metrics = [
  ['Portfolio value', '₹12,48,620', '+1.84%'],
  ['Paper P&L', '₹38,420', '+4.12%'],
  ['Risk score', 'Moderate', '62/100'],
  ['Active alerts', '7', '2 new']
];

const modules = [
  { icon: BrainCircuit, title: 'AI Research', text: 'Evidence-backed company and market research with saved reports.' },
  { icon: BarChart3, title: 'Strategy Lab', text: 'Build, test and validate strategies with India-specific costs.' },
  { icon: BriefcaseBusiness, title: 'Portfolio Intelligence', text: 'Exposure, concentration, correlation and scenario analysis.' },
  { icon: ShieldCheck, title: 'Investment Committee', text: 'Fundamental, technical, sentiment and risk agents with a final verdict.' }
];

export default function HomePage() {
  return (
    <main>
      <aside className="sidebar">
        <div className="brand"><span>K</span><strong>KukFin</strong></div>
        <nav>{['Overview','AI Research','Markets','Strategy Lab','Portfolio','Paper Trading','Reports'].map((item, i) => <a className={i === 0 ? 'active' : ''} key={item}>{item}</a>)}</nav>
        <p className="disclaimer">Research and educational tools only. No guaranteed returns.</p>
      </aside>
      <section className="content">
        <header>
          <div>
            <p className="eyebrow">KUKLABS FINANCIAL INTELLIGENCE</p>
            <h1>Market decisions, with evidence.</h1>
            <p className="sub">Research, test, compare and monitor—without pretending simulated data is live.</p>
          </div>
          <div className="landing-actions">
            <Link className="text-link" href="/login">Sign in</Link>
            <Link className="button-link" href="/register">Start research <ChevronRight size={16}/></Link>
          </div>
        </header>
        <div className="status"><Activity size={16}/><span>Demo environment</span><b>NSE/BSE · US · Crypto</b></div>
        <section className="metrics">{metrics.map(([label,value,delta]) => <article key={label}><p>{label}</p><h2>{value}</h2><span>{delta}</span></article>)}</section>
        <section className="panel"><div className="panel-head"><div><p className="eyebrow">CORE PLATFORM</p><h2>One workspace for research and validation</h2></div><span>Delayed demo data</span></div><div className="module-grid">{modules.map(({icon: Icon,title,text}) => <article key={title}><Icon size={22}/><h3>{title}</h3><p>{text}</p><Link href="/register">Open module <ChevronRight size={14}/></Link></article>)}</div></section>
      </section>
    </main>
  );
}
