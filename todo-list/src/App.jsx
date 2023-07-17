import injectContext from "./store/Context";
import React from "react";
import { BrowserRouter, Routes, Route } from "react-router-dom";
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

function App() {
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
      </Routes>
      <Footer />
      <Toaster position="bottom-right" reverseOrder={false} />
    </BrowserRouter>
  );
}

export default injectContext(App);
