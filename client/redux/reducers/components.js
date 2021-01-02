import '../constants'
import { OPEN_DIALOG, CLOSE_DIALOG} from '../constants'

const initialState = {
    show: false
};

export default function(state = initialState, action) {
    switch(action.type) {
        case OPEN_DIALOG: {
            return {
                ...state,
                show: true
            }   
        }
        case CLOSE_DIALOG: {
            return {
                ...state,
                show: false
            }
        }
        default:
            return state;
    }
}