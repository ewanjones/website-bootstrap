import React, { Component } from 'react';
import Backend from 'services/backend.js'
import { HashRouter } from "react-router-dom";

import ViewContainer from './ViewContainer'


class App extends Component {
    render() {
        return (
            <HashRouter>
                <ViewContainer />
            </HashRouter>
        );
    }
}


export default App
