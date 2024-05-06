import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Header from './components/Header';
import Footer from './components/Footer';  // <-- Import the Footer component
import Login from './components/Login';
import Register from './components/Register';
import TodoLists from './components/TodoLists';
import axios from 'axios';

axios.defaults.baseURL = 'http://127.0.0.1:5000';

function App() {
    return (
        <Router>
            <div className="App">
                <Header />
                <Routes>
                    <Route path="/login" element={<Login />} />
                    <Route path="/register" element={<Register />} />
                    <Route path="/todolists" element={<TodoLists />} />
                </Routes>
                <Footer />
            </div>
        </Router>
    );
}

export default App;