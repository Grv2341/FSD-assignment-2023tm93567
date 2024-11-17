import './login.css';
import React, { useEffect, useState } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import { useNavigate } from "react-router-dom";
import { ToastContainer, toast } from 'react-toastify';
import { AUTH_USER_URL } from "../../constants/constants";

function Login() {

  const dispatch = useDispatch();
  const navigate = useNavigate();
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const isUserRegistered = useSelector((state) => state.userRegistered);
  useEffect(() => {
    if(isUserRegistered){
      toast.success('Registration Successful', {position: "top-right", autoClose: 5000});
      dispatch({type: "userRegistered", payload: undefined})
    }
  }, [isUserRegistered]);

  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  const passwordRegex = /^(?=.*[A-Z])(?=.*[!@#$%^&*(),.?":{}|<>])[A-Za-z\d!@#$%^&*(),.?":{}|<>]{8,}$/;

  const handleEmailChange = (event) => {
    setEmail(event.target.value)
  }

  const handlePasswordChange = (event) => {
    setPassword(event.target.value)
  }

  const handleSignIn = async () => {
    if (email == '' || password == ''){
      toast.error('Email and Password are required.', {position: "top-right", autoClose: 5000});
    }
    else if(!emailRegex.test(email)){
      toast.error('Invalid Email.', {position: "top-right", autoClose: 5000});
    }
    else if(!passwordRegex.test(password)){
      toast.error('Password must be at least 8 characters long, include one uppercase letter, and one special character.', {position: "top-right", autoClose: 5000});
    }
    else{
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
          toast.success('loggedIn', {position: "top-right", autoClose: 5000});
          dispatch({type: "sessionId", payload: data.sessionId})
          dispatch({type: "userId", payload: data.userId})
          navigate("/home")
        } else {
          toast.error('Invalid Creadentails', {position: "top-right", autoClose: 5000});
          setEmail('')
          setPassword('')
        }
      } catch (error) {
        console.error('Error during login:', error);
        toast.error('Something Went wrong. Please try again.', {position: "top-right", autoClose: 5000});
        setEmail('')
        setPassword('')
      }
    }
  }

  const redirectRegister = () => {
    navigate('/register');
  }

  return (
    <div>
      <div class="login-form">
        <h1>Login</h1>
        <div class="content">
        <div class="input-field">
            <input type="email" placeholder="Email" value = {email} onChange={handleEmailChange}></input>
        </div>
        <div class="input-field">
            <input type="password" placeholder="Password" value = {password} onChange={handlePasswordChange}></input>
        </div>
        <a href="#" class="link">Forgot Your Password?</a>
        </div>
        <div class="action">
        <button onClick={redirectRegister}>Register</button>
        <button onClick={handleSignIn}>Sign in</button>
        </div>
      </div>
      <ToastContainer/>
    </div>
  );
}

export default Login;