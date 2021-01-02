import { applyMiddleware, createStore } from "redux";
import { createLogger } from 'redux-logger'
import thunk from 'redux-thunk';
import * as storage from 'redux-storage'
import createEngine from 'redux-storage-engine-localstorage';

import { SAVE_ACTIONS } from './constants'

import rootReducer from "./reducers";


const logger = createLogger()

// react storage
const engine = createEngine('escalo');
const storageMiddleware = storage.createMiddleware(engine, [], SAVE_ACTIONS);


// Create a factory function which combines store with local storage
// Add middleware to this function here
const createStoreWithMiddleware = applyMiddleware(
    logger,
    thunk,
    storageMiddleware,
)(createStore);

// Create store
export const store = createStoreWithMiddleware(rootReducer, window.__REDUX_DEVTOOLS_EXTENSION__ && window.__REDUX_DEVTOOLS_EXTENSION__())

// save store in the local storage
const load = storage.createLoader(engine);

// Uncomment these lines when saving state

// load(store)
//     .then((newState) => console.log('Loaded state:', newState))
//     .catch(() => console.log('Failed to load previous state'));
