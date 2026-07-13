'use client';

import Link from 'next/link';
import { FormEvent, useState } from 'react';

import { apiRequest } from '../../lib/api';

export default function RegisterPage() {
  const [fullName, setFullName] = useState('');
  const [workspaceName, setWorkspaceName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [submitting, setSubmitting] = useState(false);

  async function submit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setError('');
    setSubmitting(true);
    try {
      const result = await apiRequest<{ access_token: string }>('/v1/auth/register', {
        method: 'POST',
        body: {
          email,
          full_name: fullName,
          password,
          workspace_name: workspaceName
        }
      });
      localStorage.setItem('kukfin_access_token', result.access_token);
      window.location.href = '/dashboard';
    } catch (requestError) {
      setError(requestError instanceof Error ? requestError.message : 'Unable to create account');
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <main className="auth-shell">
      <section className="auth-card">
        <Link className="auth-brand" href="/"><span>K</span><strong>KukFin</strong></Link>
        <p className="eyebrow">CREATE WORKSPACE</p>
        <h1>Set up your KukFin account</h1>
        <p className="sub">Your first workspace is isolated from every other KukFin customer.</p>
        <form className="auth-form" onSubmit={submit}>
          <label>Full name<input required minLength={2} value={fullName} onChange={(event) => setFullName(event.target.value)} /></label>
          <label>Workspace name<input required minLength={2} value={workspaceName} onChange={(event) => setWorkspaceName(event.target.value)} /></label>
          <label>Email<input required type="email" value={email} onChange={(event) => setEmail(event.target.value)} /></label>
          <label>Password<input required minLength={10} type="password" value={password} onChange={(event) => setPassword(event.target.value)} /></label>
          {error ? <p className="form-error">{error}</p> : null}
          <button disabled={submitting} type="submit">{submitting ? 'Creating account…' : 'Create account'}</button>
        </form>
        <p className="auth-foot">Already registered? <Link href="/login">Sign in</Link></p>
      </section>
    </main>
  );
}
