// src/components/LoginForm.jsx
import { useState } from 'react';
import axios from 'axios';
import { useAuthContext } from '../contexts/AuthCountext.jsx';

export default function LoginForm(value) {
  const { setisnewuser } = value.value || {};
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const { setAuthUser } = useAuthContext(); // Step 1: Get setAuthUser from context

  const handleLogin = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post(
        'http://localhost:8000/login',
        new URLSearchParams({ username: email, password }),
        { headers: { 'Content-Type': 'application/x-www-form-urlencoded' } }
      );
      localStorage.setItem('access_token', response.data.access_token); // Step 3: Save token
      setAuthUser(localStorage.getItem('access_token'));
      alert('Login successful!');
    } catch (err) {
      alert(err.response?.data?.detail || "Login failed");
    }
  };
  const handleClick = (e) => {
    e.preventDefault();
    setisnewuser(true);
  };

  return (
    <>
      <p>Please Log In to continue.</p>
      <form onSubmit={handleLogin}>
        <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} required placeholder="Email" />
        <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} required placeholder="Password" />
        <button type="submit">Login</button>
      </form>
      <p>
        Don't have an account?&nbsp;
        <a href="" onClick={handleClick}>Sign Up</a>
      </p>
    </>
  );
}
