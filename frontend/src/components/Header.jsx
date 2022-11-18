import * as React from "react";
import { Link } from 'react-router-dom';
import styles from "../styles/header.module.css"




const Header = () => {

    return (
      <div className={styles.header}>
        <Link className={styles.button}  to='/'>Inicio</Link>
        <Link className={styles.button} to='/cliente'>Cliente</Link>
        <Link className={styles.button} to='/proveedor'>Proveedor</Link>
        <Link className={styles.button} to='/lista'>Lista de Productos</Link>
        <Link className={styles.button} to='/nosotros'>Quienes somos</Link>
        
      </div>
    )
  }

  export default Header;