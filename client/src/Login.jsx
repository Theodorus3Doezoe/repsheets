import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import axios from 'axios'; // Importeer axios
import { Toaster, toast } from 'react-hot-toast'; // Importeer Toaster en toast


export default function Login() {

  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  const [loading, setLoading] = useState(false);

  const navigate = useNavigate();


  const handleSubmit = async (event) => {
    event.preventDefault();
    setLoading(true);

    try {
      const payload = {
      email: email,
      password: password,
    };

    const response = await axios.post('/auth/login', payload);
    const { access_token } = response.data;
      
    localStorage.setItem('authToken', access_token);

    toast.success('Succesvol ingelogd!');

      // Wacht even zodat de gebruiker de toast kan zien voordat we navigeren
    setTimeout(() => {
      navigate('/');
    }, 1000);
    } catch (err) {
      // Toon een fout-toast met de boodschap van de backend
      if (err.response?.data?.detail) {
        toast.error(err.response.data.detail);
      } else {
        toast.error('Login mislukt. Probeer het opnieuw.');
      }
    } finally {
      setLoading(false);
    }
  };

    
  return (
    // Een zachte achtergrondkleur voor de hele pagina laat de kaart eruit springen
    <div className="grid place-items-center min-h-screen bg-gray-50 p-4">
      <Toaster position="top-center" reverseOrder={false} />
      {/* De Login Card zelf */}
      <div className='w-full max-w-md space-y-8 rounded-xl bg-white p-8 shadow-lg'>
        
        {/* Titel en subtitel sectie */}
        <div className="text-center">
          <h1 className="text-3xl font-bold tracking-tight text-gray-900">
            Sign in to your account
          </h1>
          <p className='mt-2 text-sm text-gray-600'>
            Or{' '}
            <Link to="/register" className='font-medium text-indigo-600 hover:text-indigo-500'>
              create an account
            </Link>
          </p>
        </div>

        {/* Formulier sectie */}
        <form onSubmit={handleSubmit} className="mt-8 space-y-6">
          
          {/* Emailadres Veld */}
          <div>
            <label htmlFor="email" className="block text-sm font-medium text-gray-700">
              Email address
            </label>
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
              className="mt-1 block w-full px-3 py-2 bg-white border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
              placeholder="you@example.com"
            />
          </div>

          {/* Wachtwoord Veld */}
          <div>
            <label htmlFor="password" className="block text-sm font-medium text-gray-700">
              Password
            </label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              className="mt-1 block w-full px-3 py-2 bg-white border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
              placeholder="Enter your password"
            />
          </div>
          
          {/* Knop */}
          <button
            type="submit"
            className="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
            disabled={loading}
          >
            {loading ? 'Signing in...' : 'Sign In'}
          </button>
        </form>
      </div>
    </div>
  )
}