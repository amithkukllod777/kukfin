'use client';

import Link from 'next/link';
import { FormEvent, useEffect, useState } from 'react';

import { apiRequest } from '../../lib/api';

type CurrentUser = {
  full_name: string;
  email: string;
  workspace_name: string;
  role: string;
};

type WatchlistItem = {
  id: string;
  symbol: string;
  exchange: string;
  note: string | null;
};

type Holding = {
  id: string;
  symbol: string;
  exchange: string;
  quantity: number;
  average_price: number;
};

type Portfolio = {
  id: string;
  name: string;
  base_currency: string;
  holdings: Holding[];
};

export default function DashboardPage() {
  const [token, setToken] = useState<string | null>(null);
  const [user, setUser] = useState<CurrentUser | null>(null);
  const [watchlist, setWatchlist] = useState<WatchlistItem[]>([]);
  const [portfolios, setPortfolios] = useState<Portfolio[]>([]);
  const [symbol, setSymbol] = useState('');
  const [portfolioName, setPortfolioName] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const storedToken = localStorage.getItem('kukfin_access_token');
    if (!storedToken) {
      window.location.href = '/login';
      return;
    }
    setToken(storedToken);
    void loadWorkspace(storedToken);
  }, []);

  async function loadWorkspace(accessToken: string) {
    setLoading(true);
    setError('');
    try {
      const [currentUser, items, portfolioItems] = await Promise.all([
        apiRequest<CurrentUser>('/v1/auth/me', { token: accessToken }),
        apiRequest<WatchlistItem[]>('/v1/watchlist', { token: accessToken }),
        apiRequest<Portfolio[]>('/v1/portfolios', { token: accessToken })
      ]);
      setUser(currentUser);
      setWatchlist(items);
      setPortfolios(portfolioItems);
    } catch (requestError) {
      localStorage.removeItem('kukfin_access_token');
      setError(requestError instanceof Error ? requestError.message : 'Unable to load workspace');
    } finally {
      setLoading(false);
    }
  }

  async function addWatchlistItem(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (!token || !symbol.trim()) return;
    try {
      const item = await apiRequest<WatchlistItem>('/v1/watchlist', {
        method: 'POST',
        token,
        body: { symbol, exchange: 'NSE' }
      });
      setWatchlist((current) => [item, ...current]);
      setSymbol('');
    } catch (requestError) {
      setError(requestError instanceof Error ? requestError.message : 'Unable to add instrument');
    }
  }

  async function createPortfolio(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (!token || !portfolioName.trim()) return;
    try {
      const portfolio = await apiRequest<Portfolio>('/v1/portfolios', {
        method: 'POST',
        token,
        body: { name: portfolioName, base_currency: 'INR' }
      });
      setPortfolios((current) => [portfolio, ...current]);
      setPortfolioName('');
    } catch (requestError) {
      setError(requestError instanceof Error ? requestError.message : 'Unable to create portfolio');
    }
  }

  function logout() {
    localStorage.removeItem('kukfin_access_token');
    window.location.href = '/login';
  }

  if (loading) {
    return <main className="workspace-loading">Loading secure workspace…</main>;
  }

  return (
    <main className="workspace-shell">
      <aside className="sidebar">
        <Link className="brand" href="/"><span>K</span><strong>KukFin</strong></Link>
        <nav>
          <a className="active">Overview</a>
          <a>AI Research</a>
          <a>Markets</a>
          <a>Strategy Lab</a>
          <a>Portfolio</a>
          <a>Reports</a>
        </nav>
        <button className="secondary-button" onClick={logout}>Sign out</button>
        <p className="disclaimer">Research and educational tools only. Live order execution is disabled.</p>
      </aside>

      <section className="content">
        <header>
          <div>
            <p className="eyebrow">{user?.workspace_name ?? 'KUKFIN WORKSPACE'}</p>
            <h1>Welcome, {user?.full_name ?? 'Investor'}</h1>
            <p className="sub">Authenticated workspace · {user?.role ?? 'member'} · data remains tenant-isolated.</p>
          </div>
          <Link className="button-link" href="/">Public site</Link>
        </header>

        {error ? <p className="form-error workspace-error">{error}</p> : null}

        <section className="metrics">
          <article><p>Watchlist</p><h2>{watchlist.length}</h2><span>Saved instruments</span></article>
          <article><p>Portfolios</p><h2>{portfolios.length}</h2><span>INR base supported</span></article>
          <article><p>Holdings</p><h2>{portfolios.reduce((count, item) => count + item.holdings.length, 0)}</h2><span>Across portfolios</span></article>
          <article><p>Execution</p><h2>Disabled</h2><span>Research mode</span></article>
        </section>

        <section className="workspace-grid">
          <article className="panel">
            <div className="panel-head"><div><p className="eyebrow">WATCHLIST</p><h2>Track research candidates</h2></div><span>Protected API</span></div>
            <form className="inline-form" onSubmit={addWatchlistItem}>
              <input placeholder="RELIANCE" value={symbol} onChange={(event) => setSymbol(event.target.value)} />
              <button type="submit">Add NSE symbol</button>
            </form>
            <div className="data-list">
              {watchlist.length ? watchlist.map((item) => (
                <div key={item.id}><strong>{item.symbol}</strong><span>{item.exchange}</span><small>{item.note ?? 'No research note yet'}</small></div>
              )) : <p className="empty-state">No instruments saved yet.</p>}
            </div>
          </article>

          <article className="panel">
            <div className="panel-head"><div><p className="eyebrow">PORTFOLIOS</p><h2>Organize holdings</h2></div><span>Workspace isolated</span></div>
            <form className="inline-form" onSubmit={createPortfolio}>
              <input placeholder="India Core" value={portfolioName} onChange={(event) => setPortfolioName(event.target.value)} />
              <button type="submit">Create portfolio</button>
            </form>
            <div className="data-list">
              {portfolios.length ? portfolios.map((portfolio) => (
                <div key={portfolio.id}><strong>{portfolio.name}</strong><span>{portfolio.base_currency}</span><small>{portfolio.holdings.length} holdings</small></div>
              )) : <p className="empty-state">No portfolios created yet.</p>}
            </div>
          </article>
        </section>
      </section>
    </main>
  );
}
