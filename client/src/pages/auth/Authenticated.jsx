import React from 'react';
import {Navigate, useLocation} from "react-router-dom";
import PATHS from "../../config/PATHS";

function Authenticated({children}) {
    const isAuthenticated = localStorage.getItem('token') != null
    const location = useLocation();

    if (isAuthenticated)
        return children;

    return (<Navigate to={PATHS.LOGIN} state={{from: location}} replace/>);
}

export default Authenticated;