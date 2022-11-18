import React from "react";

function LoginPage () {

    return (
    <div className = "loginPage">
    
    <h3 className = "loginPage-title">Log in como Proveedor</h3>
    
    <form>
    
    <input type = "text" name= "username"></input>
    
    <input type= "password" name= "password"/>
    
    </form>
    
    </div>
    
    );
    
}

export default LoginPage;