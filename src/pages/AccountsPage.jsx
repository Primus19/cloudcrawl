import React, { useEffect, useState } from 'react';
import AccountForm from '../components/AccountForm';

export default function AccountsPage() {
  const [accounts, setAccounts] = useState([]);

  const fetchAccounts = () => {
    fetch('/api/v1/accounts')
      .then(res => res.json())
      .then(data => setAccounts(data))
      .catch(err => console.error(err));
  };

  useEffect(() => {
    fetchAccounts();
  }, []);

  const handleSubmit = (form) => {
    fetch('/api/v1/accounts', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(form),
    }).then(() => fetchAccounts());
  };

  const handleDelete = (id) => {
    fetch(\`/api/v1/accounts/\${id}\`, { method: 'DELETE' })
      .then(() => fetchAccounts());
  };

  return (
    <div className="p-4">
      <h1 className="text-2xl font-bold mb-4">Cloud Accounts</h1>
      <AccountForm onSubmit={handleSubmit} />
      <ul className="mt-4 space-y-2">
        {accounts.map(acc => (
          <li key={acc.id} className="flex justify-between items-center">
            <span>{acc.name} ({acc.provider})</span>
            <button onClick={() => handleDelete(acc.id)} className="text-red-500">Delete</button>
          </li>
        ))}
      </ul>
    </div>
  );
}
