import './register.css';
import React, { useEffect, useState } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import { useNavigate } from "react-router-dom";
import { REGISTER_USER_URL } from '../../constants/constants';
import { ToastContainer, toast } from 'react-toastify';

function Register() {

  const dispatch = useDispatch();
  const navigate = useNavigate();

  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [firstName, setFirstName] = useState('')
  const [lastname, setLastName] = useState('')

  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  const passwordRegex = /^(?=.*[A-Z])(?=.*[!@#$%^&*(),.?":{}|<>])[A-Za-z\d!@#$%^&*(),.?":{}|<>]{8,}$/;
  const nameRegex = /^[A-Za-z]+([\-\'\s]?[A-Za-z]+)*$/;

  const handleEmailChange = (event) => {
    setEmail(event.target.value)
  }

  const handlePasswordChange = (event) => {
    setPassword(event.target.value)
  }

  const handleFirstNameChange = (event) => {
    setFirstName(event.target.value)
  }

  const handleLastNameChange = (event) => {
    setLastName(event.target.value)
  }

  const increment = () => {
    dispatch({ type: 'INCREMENT' });
  };

  const redirectLogin = () => {
    navigate('/login');
  }

  const handleRegister = async () => {
    if (email == '' || password == '' || firstName == '' || lastname == ''){
      toast.error('Email, Password, First Name and Last Name are required.', {position: "top-right", autoClose: 5000});
    }
    else if(!emailRegex.test(email)){
      toast.error('Invalid Email.', {position: "top-right", autoClose: 5000});
    }
    else if(!passwordRegex.test(password)){
      toast.error('Password must be at least 8 characters long, include one uppercase letter, and one special character.', {position: "top-right", autoClose: 5000});
    }
    else if(!nameRegex.test(firstName) || !nameRegex.test(lastname)){
      toast.error('Invalid First Name or Last Name.', {position: "top-right", autoClose: 5000});
    }
    else{
      try {
        const response = await fetch(REGISTER_USER_URL, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            "email": email,
            "password": password,
            "firstName": firstName,
            "lastName": lastname
          }),
        });
  
        const data = await response.json();
  
        if (response.ok) {
          console.log(data);
          toast.success('loggedIn', {position: "top-right", autoClose: 5000});
          dispatch({type: "userRegistered", payload: true})
          navigate("/login")
        } else if (response.status === 500){
          toast.error("Something Went wrong. Please try again.", {position: "top-right", autoClose: 5000});
          setEmail('')
          setPassword('')
          setFirstName('')
          setLastName('')
        }
      } catch (error) {
        console.error('Error during login:', error);
        toast.error('Something Went wrong. Please try again.', {position: "top-right", autoClose: 5000});
        setEmail('')
        setPassword('')
        setFirstName('')
        setLastName('')
      }
    }
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
              <input type="password" placeholder="Password" value={password} onChange={handlePasswordChange}></input>
          </div>
          <div class="input-field">
              <input type="text" placeholder="Fist Name" value={firstName} onChange={handleFirstNameChange}></input>
          </div>
          <div class="input-field">
              <input type="text" placeholder="Last Name" value={lastname} onChange={handleLastNameChange}></input>
          </div>
          </div>
          <div class="register-action">
          <button onClick={handleRegister}>Register</button>
          <button onClick={redirectLogin}>Sign in</button>
          </div>
      </div>
      <ToastContainer/>
    </div>
  );
}

export default Register;