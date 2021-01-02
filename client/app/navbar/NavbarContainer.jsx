import React, { Component } from 'react';
import { connect } from 'react-redux'

import Navbar from './Navbar'


class NavbarContainer extends Component {
    render() {
        return (
            <Navbar/>
        );
    }
}


const mapDispatchToProps = dispatch => ({
});


const mapStateToProps = state => ({
});


export default connect(
    mapStateToProps,
    mapDispatchToProps
)(NavbarContainer )
