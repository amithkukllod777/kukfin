'use client';

import Link from 'next/link';
import { FormEvent, useState } from 'react';

import { apiRequest } from '../../lib/api';

export default function LoginPage() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [submitting, setSubmitting] = useState(false);

  async function submit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setError('');
    setSubmitting(true);
    try {
      const result = await apiRequest<{ access_token: string }>('/v1/auth/login', {
        method: 'POST',
        body: { email, password }
      });
      localStorage.setItem('kukfin_access_token', result.access_token);
      window.location.href = '/dashboard';
    } catch (requestError) {
      setError(requestError instanceof Error ? requestError.message : 'Unable to sign in');
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <main className="auth-shell">
      <section className="auth-card">
        <Link className="auth-brand" href="/"><span>K</span><strong>KukFin</strong></Link>
        <p className="eyebrow">SECURE ACCESS</p>
        <h1>Sign in to your workspace</h1>
        <p className="sub">Portfolio intelligence, research and strategy validation in one account.</p>
        <form className="auth-form" onSubmit={submit}>
          <label>Email<input required type="email" value={email} onChange={(event) => setEmail(event.target.value)} /></label>
          <label>Password<input required minLength={10} type="password" value={password} onChange={(event) => setPassword(event.target.value)} /></label>
          {error ? <p className="form-error">{error}</p> : null}
          <button disabled={submitting} type="submit">{submitting ? 'Signing in…' : 'Sign in'}</button>
        </form>
        <p className="auth-foot">New to KukFin? <Link href="/register">Create an account</Link></p>
      </section>
    </main>
  );
}
