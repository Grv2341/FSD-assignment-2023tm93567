import './nav.css';
import React, { useEffect, useState } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import { useNavigate } from "react-router-dom";

function Nav() {
    const dispatch = useDispatch();
    const navigate = useNavigate();
    const currentPage = useSelector((state) => state.currentPage);

    const handleClick = (option) => {
        dispatch({type: "currentPage", payload: option})
    }

    const handleLogout = () => {
        dispatch({type: "sessionId", payload: undefined})
    }

    return (
        <nav id="main-menu">
            <div class = "nav-bar">
                <div class="nav-button-home nav-option" onClick={() => {handleClick("SEARCH");}}>Search</div>
                <div class="nav-button-services nav-option" onClick={() => {handleClick("ADD_BOOK");}}>Add Book</div>
                <div class="nav-button-products nav-option" onClick={() => {handleClick("MY_BOOK");}}>My Books</div>
                <div class="nav-button-products nav-option" onClick={handleLogout}>Logout</div>
            </div>
        </nav>
    )
}

export default Nav;