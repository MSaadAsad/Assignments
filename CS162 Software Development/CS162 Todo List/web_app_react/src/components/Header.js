import React from 'react';
import { useNavigate } from 'react-router-dom';
import './tempelates/Header.css';

function Header() {
    const navigate = useNavigate();

    const handleLogout = () => {
        localStorage.removeItem('jwt_key');
        navigate('/login');
    };

    return (
        <header>
            <h1>Todo List App</h1>
            {window.location.pathname !== '/login' && window.location.pathname !== '/register' && 
            <button onClick={handleLogout} className="logout-btn">Logout</button>}
        </header>
    );    
}

export default Header;