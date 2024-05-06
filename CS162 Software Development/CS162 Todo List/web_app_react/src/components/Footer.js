import React from 'react';
import './tempelates/Footer.css';

function Footer() {
    return (
        <footer className="app-footer">
            <div className="footer-content">
                <div>
                    <p>&copy; 2023 Todo List App</p>
                </div>
                <div>
                    <ul className="footer-links">
                        <li><a href="/privacy-policy">Privacy Policy</a></li>
                        <li><a href="/terms-of-service">Terms of Service</a></li>
                        <li><a href="/contact">Contact Us</a></li>
                    </ul>
                </div>
            </div>
        </footer>
    );
}

export default Footer;