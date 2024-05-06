import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import './tempelates/Login.css';

function Login() {
    const navigate = useNavigate();
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [errorMessage, setErrorMessage] = useState('');

    const handleSubmit = (event) => {
        event.preventDefault();
        handleLogin(username, password);
    };

    const handleLogin = (username, password) => {
    
        axios.post('/login', { username, password })
            .then(response => {
                const token = response.data.access_token;
                localStorage.setItem('token', token);
                axios.defaults.headers.common['Authorization'] = 'Bearer ' + token;
                navigate('/todolists');
            })
            .catch(error => {
                setErrorMessage('Invalid credentials or an error occurred. Please try again.');
            });
    };    

    return (
        <div className="login-container">
            <h2>Login</h2>
            <form onSubmit={handleSubmit}>
                <div className="input-wrapper">
                    <label htmlFor="username">Username:</label>
                    <input 
                        type="text" 
                        id="username"
                        placeholder="Enter your username" 
                        value={username}
                        onChange={(e) => setUsername(e.target.value)}
                    />
                </div>
                <div className="input-wrapper">
                    <label htmlFor="password">Password:</label>
                    <input 
                        type="password"
                        id="password" 
                        placeholder="Enter your password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                    />
                </div>
                <button type="submit" className="login-btn">Login</button>
            </form>
            {errorMessage && <p className="error-message">{errorMessage}</p>}
        </div>
    );
}

export default Login;