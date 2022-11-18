import React from "react";
import Header from './components/Header';
import { BrowserRouter, Route, Routes } from 'react-router-dom';
import Cliente from './components/Cliente';
import Proveedor from './components/Proveedor';
import Nosotros from './components/Nosotros';
import List from './components/List'
import Home from './components/Home';
import { ThemeProvider } from 'react-jss';

const theme = {
  light: {
    background: "#FFF",
    primary: "#FFF",
    secondary: "#f8f8f8",
    tertiary: "#F64360",
    quaternary: "#B9334A",
    color: "#474747",
    boxShadow: "0 3px 5px ",
    shadow: "#CBCBCB",
    container: {
      fontSize: "1rem",
      margin: "auto",
      marginBottom: "1.5rem",
      padding: "1rem ",
    }
  },
}


function App() {
  return (
    <ThemeProvider theme={{ theme: theme }}>
      <BrowserRouter>
        <Header/>
          <Routes>
            <Route path="/" element={<Home/>}></Route>
            <Route path="/cliente/" element={<Cliente/>}></Route>
            <Route path="/proveedor/" element={<Proveedor/>}></Route>
            <Route path="/nosotros/" element={<Nosotros/>}></Route>
            <Route path="/lista/" element={<List/>}></Route>
          </Routes>
      </BrowserRouter>
      </ThemeProvider>
   
  );
}

export default App;
