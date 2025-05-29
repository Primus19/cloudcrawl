import React, { useState } from 'react';
import { Select, Input, Textarea, Button } from './UI';

export default function AccountForm({ initialValues = {}, onSubmit }) {
  const [provider, setProvider] = useState(initialValues.provider || 'aws');
  const [authType, setAuthType] = useState(initialValues.authType || (provider === 'aws' ? 'access_key' : provider === 'azure' ? 'service_principal' : 'service_account'));
  const [form, setForm] = useState(initialValues);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setForm(prev => ({ ...prev, [name]: value }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit({ provider, authType, ...form });
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <Input label="Name" name="name" value={form.name || ''} onChange={handleChange} required />

      <Select label="Provider" name="provider" value={provider} onChange={e => { setProvider(e.target.value); setAuthType(provider === 'aws' ? 'access_key' : provider === 'azure' ? 'service_principal' : 'service_account'); }}>
        <option value="aws">AWS</option>
        <option value="azure">Azure</option>
        <option value="gcp">GCP</option>
      </Select>

      {provider === 'aws' && (
        <Select label="Auth Type" name="authType" value={authType} onChange={e => setAuthType(e.target.value)}>
          <option value="access_key">Access Key</option>
          <option value="iam_role">IAM Role</option>
        </Select>
      )}

      {provider === 'azure' && (
        <Select label="Auth Type" name="authType" value={authType} onChange={e => setAuthType(e.target.value)}>
          <option value="service_principal">Service Principal</option>
        </Select>
      )}

      {provider === 'gcp' && (
        <Select label="Auth Type" name="authType" value={authType} onChange={e => setAuthType(e.target.value)}>
          <option value="service_account">Service Account</option>
        </Select>
      )}

      {/* AWS: Access Key */}
      {provider === 'aws' && authType === 'access_key' && (
        <>
          <Input label="Access Key" name="accessKey" value={form.accessKey || ''} onChange={handleChange} required />
          <Input label="Secret Key" name="secretKey" type="password" value={form.secretKey || ''} onChange={handleChange} required />
        </>
      )}

      {/* AWS: IAM Role */}
      {provider === 'aws' && authType === 'iam_role' && (
        <>
          <Input label="Role ARN" name="roleArn" value={form.roleArn || ''} onChange={handleChange} required />
          <Input label="External ID" name="externalId" value={form.externalId || ''} onChange={handleChange} />
        </>
      )}

      {/* Azure */}
      {provider === 'azure' && (
        <>
          <Input label="Subscription ID" name="subscriptionId" value={form.subscriptionId || ''} onChange={handleChange} required />
          <Input label="Tenant ID" name="tenantId" value={form.tenantId || ''} onChange={handleChange} required />
          <Input label="Client ID" name="clientId" value={form.clientId || ''} onChange={(handleChange)} required />
          <Input label="Client Secret" name="clientSecret" type="password" value={form.clientSecret || ''} onChange={handleChange} required />
        </>
      )}

      {/* GCP */}
      {provider === 'gcp' && (
        <Textarea label="Service Account JSON" name="serviceAccountJson" value={form.serviceAccountJson || ''} onChange={handleChange} rows={8} required />
      )}

      <Button type="submit">Save Account</Button>
    </form>
