import * as storage from 'redux-storage'
import { combineReducers } from "redux";
import { reducer as form } from 'redux-form'

import components from './components'


const reducers = { components }


// Wrap our reducers in a redux-storage listener
export default storage.reducer(combineReducers(reducers));
