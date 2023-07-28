import injectContext from "./store/Context";
import React, { useEffect } from "react";
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import Home from "./view/Home";
import Navbar from "./component/_navbar";
import Register from "./view/Register";
import Login from "./view/Login";
import "./App.css";
import Footer from "./component/_footer";
import UpdateTask from "./view/UpdateTask";
import PrivateRoutes from "./utils/PrivateRoutes";
import { Toaster } from "react-hot-toast";
import User from "./view/User";
import { useContext } from "react";
import { Context } from "./store/Context";


function App() {
const { actions } =useContext(Context);

useEffect(()=>{
  actions.getUser();
  console.log("estamos up")
},[])

  return (
    <BrowserRouter>
      <Navbar />
      <Routes>
        <Route element={<PrivateRoutes />}>
          <Route path="/" element={<Home />} />
          <Route path="/update/:id" element={<UpdateTask />} />
          <Route path="/user" element={<User/>}/>
        </Route>
        <Route path="/register" element={<Register />} />
        <Route path="/login" element={<Login />} />
        <Route path="/*" element={< Navigate to="/"/>} />
      </Routes>
      <Footer />
      <Toaster position="bottom-right" reverseOrder={false} />
    </BrowserRouter>
  );
}

export default injectContext(App);
