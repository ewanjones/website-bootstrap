import React, { Component } from 'react';
import { connect } from 'react-redux'
import {
  Switch,
  Route,
  withRouter
} from "react-router-dom";


import View from './View'
import Navbar from './navbar/Navbar'

import styles from './navigation.scss'


class ViewContainer extends Component {
    render() {
        return (
            <div className={styles.viewContainer}>
                <div className={styles.row}>
                    <Navbar />
                    <div className={styles.content}>
                        <Switch>
                            <Route path='/'>
                                <View />
                            </Route>
                        </Switch>
                    </div>
                </div>
            </div>
        )
    }
}


const mapDispatchToProps = dispatch => ({ });


const mapStateToProps = state => ({ });


export default withRouter(connect(
    mapStateToProps,
    mapDispatchToProps
)(ViewContainer))
