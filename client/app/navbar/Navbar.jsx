import React, { Component } from 'react';
import { NavLink } from "react-router-dom";

import styles from './navbar.scss'


class Navbar extends Component {
    render() {
        return (
            <nav className={styles.navBar}>
                <ul>
                    <NavLink exact to="/" activeClassName={styles.activeLink}>
                        <li>Overview</li>
                    </NavLink>
                </ul>
            </nav>
        );
    }
}


export default Navbar;
