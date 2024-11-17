// store.js
import { createStore } from 'redux';

// Initial state
const initialState = { 
  userRegistered: undefined,
  sessionId: undefined,
  userId: undefined,
  currentPage: "SEARCH"
};

// Reducer function
function countReducer(state = initialState, action) {
  switch (action.type) {

    case "userRegistered":
      return{...state, userRegistered: action.payload}
    
    case 'sessionId':
      return {...state, sessionId: action.payload};

    case 'userId':
      return {...state, userId: action.payload};
    
    case "currentPage":
      return{...state, currentPage:action.payload};

    default:
      return state;
  }
}

// Create Redux store
const state = createStore(countReducer);

export default state;
