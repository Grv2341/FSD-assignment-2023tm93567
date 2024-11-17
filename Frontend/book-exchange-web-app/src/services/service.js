import { GET_BOOK_BULK_URL, GET_BOOK_URL, AUTH_USER_URL, ADD_BOOK_URL } from "../constants/constants";
import { useSelector, useDispatch } from 'react-redux';

export const AuthorizeLogin = async (email, password) => {
    const dispatch = useDispatch();
    try {
        const response = await fetch(AUTH_USER_URL, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            "email": email,
            "password": password,
          }),
        });
  
        const data = await response.json();
  
        if (response.ok) {
          console.log(data);
          dispatch({type: "loginSuccess", payload: true})
          dispatch({type: "sessionId", payload: data.sessionId})
          dispatch({type: "userId", payload: data.userId})
        } else {
          dispatch({type: "loginFailed", payload: true})
        }
      } catch (error) {
        console.error('Error during login:', error);
        dispatch({type: "loginError", payload: true})
      }
}