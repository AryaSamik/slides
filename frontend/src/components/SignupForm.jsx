// src/components/SignupForm.jsx
import { useState } from 'react';
import axios from 'axios';

function SignupForm(value) {
  const { setisnewuser } = value.value || {};
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  const handleSignup = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post('http://localhost:8000/signup', {
        email,
        password
      });
      alert(response.data.message);
      setisnewuser(false);
    } catch (err) {
      alert(err.response?.data?.detail || "Signup failed");
    }
  };

  const handleClick = (e) => {
    e.preventDefault();
    setisnewuser(false);
  }

  return (
    <>
      <p>Please Sign Up to continue.</p>
      <form onSubmit={handleSignup}>
        <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} required placeholder="Email" />
        <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} required placeholder="Password" />
        <button type="submit">Sign Up</button>
      </form>
      <p>
        Already have an account?&nbsp;
        <a href="" onClick={handleClick}>Log In</a>
      </p>
    </>
  );
}

export default SignupForm;