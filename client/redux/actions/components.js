import { OPEN_DIALOG, CLOSE_DIALOG} from '../constants'

export const openDialog = () => dispatch => {
    return dispatch({
        type: OPEN_DIALOG,
        show: true
    });
}

export const closeDialog = () => dispatch => {
    return dispatch({
        type: CLOSE_DIALOG,
        show: false
    })
}