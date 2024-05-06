import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import './tempelates/Register.css';

function Register() {
    const navigate = useNavigate();
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [message, setMessage] = useState('');

    const handleSubmit = async (event) => {
        event.preventDefault();

        try {
            const response = await axios.post('/register', { username, password });
            setMessage(response.data.message);

            if (response.status === 201) {
                navigate('/login');
            }
        } catch (error) {
            if (error.response && error.response.data.message) {
                setMessage(error.response.data.message);
            } else {
                setMessage("An error occurred during registration.");
            }
        }
    };

    return (
        <div className="register-container">
            <h2>Register</h2>
            {message && <p className="message">{message}</p>}
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
                <button type="submit" className="register-btn">Register</button>
            </form>
        </div>
    );
}

export default Register;