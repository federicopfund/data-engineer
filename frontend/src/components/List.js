import React, { useState, useEffect} from "react";
import Axios from "axios";


function List() {
  const [list, setList] = useState([]);
  useEffect(() => {
    Axios({
      url: "http://localhost:8000/productos",
    })
      .then((response) => {
        setList(response.data.dataframe);
      })
      .catch((error) => {
        console.log(error);
      });
  }, [setList]);

  return (
    <div className="table-responsive">
       <table className="table table-sm table-bordered">
         <thead>
            <th>Detalle de Producto</th>
            <th>Subcategoría</th>
            <th>Categoría</th>

         </thead>
            <tbody>
            {Array.from(list).map((item) => (
            <tr>
                    <td>{item.Producto}</td>
                    <td>{item.Cod_Subcategoria}</td>
                    <td>{item.Cod_Categoria}</td>
            </tr>))}
            </tbody>

       </table>

     </div>
     )
}
export default List;