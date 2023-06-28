import { Outlet, Navigate } from 'react-router-dom'
import { Context } from "../store/Context";
import React, { useContext } from "react";

const PrivateRoutes = () => {
    const { store } = useContext(Context)
    const { token } = store;
    let auth = { 'token': token !== '' };
    return (
       auth.token ? <Outlet/> : <Navigate to="/login" />
    )
}
export default PrivateRoutes;